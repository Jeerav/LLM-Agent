import streamlit as st
import google.generativeai as genai
from deep_translator import GoogleTranslator
from langdetect import detect
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Streamlit UI
st.set_page_config(page_title="Jeeves LLM Agent (Gemini)", layout="centered")
st.title("Jeeves LLM Assistant (Powered by Gemini)")

st.write("Type your question in English, Spanish, or Portuguese about a fintech product, and get an intelligent response.")

user_input = st.text_area("Your Question:", height=150)

if st.button("Submit") and user_input:
    try:
        original_lang = detect(user_input)
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

        prompt = f"You are a fintech assistant specialized in Latin American financial systems. Answer the following question clearly and concisely:\n\n{translated_input}"

        # Call Gemini
        response = model.generate_content(prompt)
        answer = response.text

        # Translate back to original language
        final_output = GoogleTranslator(source='auto', target=original_lang).translate(answer)

        st.markdown("### Response:")
        st.success(final_output)

    except Exception as e:
        st.error(f"Error: {e}")