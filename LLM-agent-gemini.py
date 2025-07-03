import streamlit as st
from llama_index.core.tools import FunctionTool
from llama_index.llms.gemini import Gemini
from llama_index.core.agent import ReActAgent
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

# Use Google Gemini (free tier)
# Get API key from: https://makersuite.google.com/app/apikey
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        llm = Gemini(api_key=api_key)
        agent = ReActAgent.from_tools([exchange_tool], llm=llm, verbose=True)
        llm_provider = "Google Gemini (Free Tier)"
    else:
        raise ValueError("No API key found")
except Exception as e:
    # Fallback to simple response system
    llm_provider = f"Simple Response System (Error: {str(e)})"
    agent = None

# Streamlit UI
st.set_page_config(page_title="Jeeves LLM Agent (Gemini)", layout="centered")
st.title("Jeeves LLM Assistant (Google Gemini)")
st.write(f"🤖 Using: {llm_provider}")

if not os.getenv("GOOGLE_API_KEY"):
    st.warning("⚠️ No GOOGLE_API_KEY found in environment variables. Add it to your .env file.")

st.write("Type your question in English, Spanish, or Portuguese about a fintech product, and get an intelligent response.")

user_input = st.text_area("Your Question:", height=150)

if st.button("Submit") and user_input:
    try:
        original_lang = detect(user_input)
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

        if agent and os.getenv("GOOGLE_API_KEY"):
            # Use Gemini agent
            response = agent.chat(f"You are a fintech assistant specialized in Latin American financial systems. Answer this question clearly and concisely: {translated_input}")
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

# Setup instructions
with st.expander("🔧 Setup Instructions for Google Gemini"):
    st.markdown("""
    ### Google Gemini Free Tier Setup:
    
    1. **Get API Key**: Go to https://makersuite.google.com/app/apikey
    2. **Create .env file** with:
       ```
       GOOGLE_API_KEY=your_gemini_api_key_here
       ```
    3. **Install package**:
       ```bash
       pip install llama-index-llms-gemini
       ```
    4. **Free Tier Limits**: 
       - 60 requests per minute
       - 1,500 requests per day
       - Much more generous than OpenAI free tier!
    
    ### Benefits:
    - ✅ No billing required
    - ✅ High-quality responses
    - ✅ Good free tier limits
    - ✅ No credit card needed
    """)