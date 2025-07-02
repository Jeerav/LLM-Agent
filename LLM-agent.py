import streamlit as st
import openai
from deep_translator import GoogleTranslator
from langdetect import detect
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response['choices'][0]['message']['content']

        # Translate back to original language
        final_output = GoogleTranslator(source='auto', target=original_lang).translate(answer)

        st.markdown("### Response:")
        st.success(final_output)

    except Exception as e:
        st.error(f"Error: {e}")
