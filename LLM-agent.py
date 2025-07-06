import streamlit as st
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool
from deep_translator import GoogleTranslator
from langdetect import detect
from dotenv import load_dotenv
import os
import openai
import time
import json
import hashlib
from functools import wraps
from typing import Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
CACHE_EXPIRE_TIME = 3600  # 1 hour
RATE_LIMIT_DELAY = 1  # seconds between calls

# Simple in-memory cache
cache = {}

def rate_limit(func):
    """Decorator to add rate limiting"""
    last_call = [0]
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_time = time.time()
        time_since_last = current_time - last_call[0]
        
        if time_since_last < RATE_LIMIT_DELAY:
            sleep_time = RATE_LIMIT_DELAY - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        last_call[0] = time.time()
        return func(*args, **kwargs)
    
    return wrapper

def get_cache_key(text: str) -> str:
    """Generate cache key from text"""
    return hashlib.md5(text.encode()).hexdigest()

def get_from_cache(key: str) -> Optional[str]:
    """Get cached response if available and not expired"""
    if key in cache:
        timestamp, response = cache[key]
        if time.time() - timestamp < CACHE_EXPIRE_TIME:
            logger.info("Using cached response")
            return response
        else:
            del cache[key]  # Remove expired cache
    return None

def save_to_cache(key: str, response: str):
    """Save response to cache"""
    cache[key] = (time.time(), response)

def retry_on_quota_error(func):
    """Decorator to retry on quota errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        last_exception = None
        
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                error_msg = str(e).lower()
                
                # Check for quota/rate limit related errors
                if any(term in error_msg for term in ['quota', 'rate limit', 'too many requests', 'insufficient quota']):
                    logger.warning(f"API quota/rate limit hit on attempt {attempt + 1}: {e}")
                    
                    if attempt < MAX_RETRIES - 1:
                        delay = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logger.error("Max retries exceeded for quota error")
                        raise QuotaExceededError("API quota exceeded after multiple retries")
                else:
                    # For non-quota errors, raise immediately
                    raise e
        
        raise last_exception
    
    return wrapper

class QuotaExceededError(Exception):
    pass

# Create tools
LATAM_EXCHANGE_RATES = {
    "Brazil": "5.2 BRL",
    "Mexico": "17.1 MXN",
    "Argentina": "900 ARS",
    "Colombia": "3950 COP",
    "Chile": "925 CLP",
    "Peru": "3.7 PEN"
}

def get_exchange_rate(country: str) -> str:
    rate = LATAM_EXCHANGE_RATES.get(country.title())
    if rate:
        return f"The current exchange rate in {country} is 1 USD = {rate}."
    else:
        return f"Sorry, I don't have exchange rate data for {country}."

exchange_tool = FunctionTool.from_defaults(
    fn=get_exchange_rate,
    name="LatAmExchangeTool",
    description="Returns USD exchange rates for Latin American countries"
)

# Create an agent with tools (with error handling)
try:
    agent = OpenAIAgent.from_tools([exchange_tool], verbose=True)
except Exception as e:
    logger.error(f"Failed to create OpenAI agent: {e}")
    agent = None

@rate_limit
@retry_on_quota_error
def get_ai_response(query: str) -> str:
    """Get AI response with rate limiting and retry logic"""
    if agent is None:
        raise Exception("OpenAI agent not available")
    
    cache_key = get_cache_key(query)
    cached_response = get_from_cache(cache_key)
    
    if cached_response:
        return cached_response
    
    response = agent.chat(query)
    response_str = str(response)
    
    save_to_cache(cache_key, response_str)
    return response_str

def get_fallback_response(query: str, original_lang: str) -> str:
    """Provide fallback response when API is unavailable"""
    fallback_responses = {
        'en': "I apologize, but I'm currently experiencing high demand. Here are some general fintech insights for Latin America: Exchange rates fluctuate daily, and it's important to use official banking channels for international transfers. Please try again in a few minutes.",
        'es': "Disculpe, pero actualmente estoy experimentando alta demanda. Aquí hay algunas ideas generales de fintech para América Latina: Los tipos de cambio fluctúan diariamente, y es importante usar canales bancarios oficiales para transferencias internacionales. Intente nuevamente en unos minutos.",
        'pt': "Desculpe, mas atualmente estou enfrentando alta demanda. Aqui estão algumas ideias gerais de fintech para a América Latina: As taxas de câmbio flutuam diariamente, e é importante usar canais bancários oficiais para transferências internacionais. Tente novamente em alguns minutos."
    }
    
    return fallback_responses.get(original_lang, fallback_responses['en'])

# Streamlit UI
st.set_page_config(page_title="Jeeves LLM Agent", layout="centered")
st.title("Jeeves LLM Assistant")

# Add status indicator
if agent is None:
    st.error("⚠️ OpenAI service unavailable. Fallback mode active.")
else:
    st.success("✅ AI Assistant ready")

st.write("Type your question in English, Spanish, or Portuguese about a fintech product, and get an intelligent response.")

# Display cache status
if cache:
    st.info(f"📱 {len(cache)} responses cached for faster access")

user_input = st.text_area("Your Question:", height=150)

if st.button("Submit") and user_input:
    try:
        with st.spinner("Processing your question..."):
            original_lang = detect(user_input)
            translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

            prompt = f"You are a fintech assistant specialized in Latin American financial systems. Answer the following question clearly and concisely:\n\n{translated_input}"

            # Try to get AI response
            try:
                response = get_ai_response(translated_input)
                
                final_output = GoogleTranslator(source='auto', target=original_lang).translate(str(response))
                
                st.markdown("### Response:")
                st.success(final_output)
                
            except QuotaExceededError:
                st.warning("⚠️ API quota exceeded. Using fallback response.")
                fallback_response = get_fallback_response(translated_input, original_lang)
                st.markdown("### Fallback Response:")
                st.info(fallback_response)
                
            except Exception as e:
                logger.error(f"Error getting AI response: {e}")
                st.warning("⚠️ AI service temporarily unavailable. Using fallback response.")
                fallback_response = get_fallback_response(translated_input, original_lang)
                st.markdown("### Fallback Response:")
                st.info(fallback_response)

    except Exception as e:
        st.error(f"Error: {e}")
        logger.error(f"General error: {e}")

# Add usage tips
with st.expander("💡 Usage Tips"):
    st.write("""
    - **Cached responses**: Identical questions are cached for 1 hour to reduce API usage
    - **Rate limiting**: Automatic delays between API calls to prevent quota issues
    - **Fallback mode**: If API quotas are exceeded, you'll get helpful fallback responses
    - **Retry logic**: Automatic retries with exponential backoff for temporary failures
    - **Multi-language**: Supports English, Spanish, and Portuguese
    """)