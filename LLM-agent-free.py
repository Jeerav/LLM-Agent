import streamlit as st
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.agent.openai import OpenAIAgent
from deep_translator import GoogleTranslator
from langdetect import detect
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

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

# Option 1: Use Ollama (free local LLM)
# Requires: pip install llama-index-llms-ollama
try:
    llm = Ollama(model="llama3.2", request_timeout=60.0)
    agent = OpenAIAgent.from_tools([exchange_tool], llm=llm, verbose=True)
    llm_provider = "Ollama (Local)"
except:
    # Fallback to a simple response system
    llm_provider = "Simple Response System (No LLM)"
    agent = None

# Streamlit UI
st.set_page_config(page_title="Jeeves LLM Agent (Free Version)", layout="centered")
st.title("Jeeves LLM Assistant (Free Version)")
st.write(f"🤖 Using: {llm_provider}")

st.write("Type your question in English, Spanish, or Portuguese about a fintech product, and get an intelligent response.")

user_input = st.text_area("Your Question:", height=150)

if st.button("Submit") and user_input:
    try:
        original_lang = detect(user_input)
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

        if agent:
            # Use LLM agent
            response = agent.chat(translated_input)
            answer = str(response)
        else:
            # Simple fallback response
            if any(word in translated_input.lower() for word in ["exchange", "rate", "currency"]):
                # Check if any country is mentioned
                for country in LATAM_EXCHANGE_RATES.keys():
                    if country.lower() in translated_input.lower():
                        answer = get_exchange_rate(country)
                        break
                else:
                    answer = "I can provide exchange rates for Brazil, Mexico, Argentina, Colombia, Chile, and Peru. Please specify a country."
            else:
                answer = f"I'm a fintech assistant specializing in Latin American financial systems. You asked: '{translated_input}'. I can help with exchange rates and basic financial information. Please ask about exchange rates or specify how I can help with Latin American fintech topics."

        # Translate back to original language
        final_output = GoogleTranslator(source='auto', target=original_lang).translate(answer)

        st.markdown("### Response:")
        st.success(final_output)

    except Exception as e:
        st.error(f"Error: {e}")

# Instructions for setup
with st.expander("🔧 Setup Instructions"):
    st.markdown("""
    ### Free LLM Options:
    
    **Option 1: Ollama (Recommended)**
    1. Install Ollama: https://ollama.ai/
    2. Run: `ollama pull llama3.2`
    3. Install: `pip install llama-index-llms-ollama`
    
    **Option 2: Hugging Face Transformers**
    1. Install: `pip install llama-index-llms-huggingface`
    2. Use free models like: microsoft/DialoGPT-medium
    
    **Option 3: Google Gemini (Free tier)**
    1. Get free API key: https://makersuite.google.com/app/apikey
    2. Install: `pip install llama-index-llms-gemini`
    
    **Current Status**: This version falls back to simple responses if no LLM is available.
    """)