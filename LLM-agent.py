import streamlit as st
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool
from deep_translator import GoogleTranslator
from langdetect import detect
from dotenv import load_dotenv
import os
import openai

# Load API keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# Create an agent with tools
agent = OpenAIAgent.from_tools([exchange_tool], verbose=True)

# Streamlit UI
st.set_page_config(page_title="Jeeves LLM Agent", layout="centered")
st.title("Jeeves LLM Assistant")

st.write("Type your question in English, Spanish, or Portuguese about a fintech product, and get an intelligent response.")

user_input = st.text_area("Your Question:", height=150)

if st.button("Submit") and user_input:
    try:
        original_lang = detect(user_input)
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

        prompt = f"You are a fintech assistant specialized in Latin American financial systems. Answer the following question clearly and concisely:\n\n{translated_input}"

        # Call OpenAI
        response = agent.chat(translated_input)

        final_output = GoogleTranslator(source='auto', target=original_lang).translate(str(response))

        st.markdown("### Response:")
        st.success(final_output)

    except Exception as e:
        st.error(f"Error: {e}")