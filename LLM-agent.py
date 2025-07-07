import streamlit as st
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool
from deep_translator import GoogleTranslator
from langdetect import detect
from dotenv import load_dotenv
import os
import openai
import PyPDF2
import docx
import io

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

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
    try:
        file_type = uploaded_file.type
        
        if file_type == "text/plain":
            return str(uploaded_file.read(), "utf-8")
        
        elif file_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        else:
            return f"Unsupported file type: {file_type}. Please upload a .txt, .pdf, or .docx file."
    
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Jeeves LLM Agent", layout="centered")
st.title("Jeeves LLM Assistant")

st.write("Type your question in English, Spanish, or Portuguese about a fintech product, and get an intelligent response.")

# File upload section
st.markdown("### 📎 Attach File")
uploaded_file = st.file_uploader(
    "Upload a document for analysis",
    type=['txt', 'pdf', 'docx'],
    help="Upload a text, PDF, or Word document. The content will be analyzed automatically."
)

# Text input section
user_input = st.text_area("Your Question:", height=150, placeholder="Ask a question or leave blank to analyze the uploaded file...")

if st.button("Submit") and (user_input or uploaded_file):
    try:
        # Handle file upload
        file_content = ""
        if uploaded_file:
            with st.spinner("Reading file..."):
                file_content = extract_text_from_file(uploaded_file)
                st.success(f"✅ File '{uploaded_file.name}' loaded successfully!")
        
        # Prepare the query
        if user_input and file_content:
            # Both question and file provided
            query = f"User question: {user_input}\n\nDocument content: {file_content}"
        elif file_content:
            # Only file provided
            query = f"Please analyze this document and provide key insights about its fintech/financial content: {file_content}"
        else:
            # Only question provided
            query = user_input
        
        # Language detection and translation
        original_lang = detect(query)
        translated_input = GoogleTranslator(source='auto', target='en').translate(query)

        prompt = f"You are a fintech assistant specialized in Latin American financial systems. Answer the following question clearly and concisely:\n\n{translated_input}"

        # Call OpenAI
        response = agent.chat(translated_input)

        final_output = GoogleTranslator(source='auto', target=original_lang).translate(str(response))

        st.markdown("### Response:")
        st.success(final_output)

    except Exception as e:
        st.error(f"Error: {e}")
        if "api_key" in str(e).lower():
            st.info("💡 Make sure your OpenAI API key is set in the .env file as OPENAI_API_KEY=your-key-here")