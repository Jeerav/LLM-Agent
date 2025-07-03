import streamlit as st
import requests
import json
from deep_translator import GoogleTranslator
from langdetect import detect

# Ollama API endpoint (default local installation)
OLLAMA_URL = "http://localhost:11434/api/generate"

# Streamlit UI
st.set_page_config(page_title="Jeeves LLM Agent (Ollama)", layout="centered")
st.title("Jeeves LLM Assistant (Powered by Ollama)")

st.write("Type your question in English, Spanish, or Portuguese about a fintech product, and get an intelligent response.")

# Model selection
available_models = ["llama2", "codellama", "mistral", "neural-chat", "starling-lm"]
selected_model = st.selectbox("Select Model:", available_models, index=0)

user_input = st.text_area("Your Question:", height=150)

def call_ollama(model, prompt):
    """Call Ollama API with the given model and prompt"""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to Ollama. Make sure Ollama is running on localhost:11434")
    except Exception as e:
        raise Exception(f"Ollama API error: {e}")

if st.button("Submit") and user_input:
    try:
        original_lang = detect(user_input)
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

        prompt = f"You are a fintech assistant specialized in Latin American financial systems. Answer the following question clearly and concisely:\n\n{translated_input}"

        # Call Ollama
        with st.spinner("Generating response..."):
            answer = call_ollama(selected_model, prompt)

        # Translate back to original language
        final_output = GoogleTranslator(source='auto', target=original_lang).translate(answer)

        st.markdown("### Response:")
        st.success(final_output)

    except Exception as e:
        st.error(f"Error: {e}")
        if "Could not connect to Ollama" in str(e):
            st.info("To use Ollama:\n1. Install: `curl -fsSL https://ollama.com/install.sh | sh`\n2. Run: `ollama serve`\n3. Pull a model: `ollama pull llama2`")