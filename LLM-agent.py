import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from dotenv import load_dotenv
import os
import google.generativeai as genai
import PyPDF2
import docx
import io
from PIL import Image

# Load API keys
load_dotenv()

# Configure Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Create exchange rate data
LATAM_EXCHANGE_RATES = {
    "Brazil": "5.2 BRL",
    "Mexico": "17.1 MXN",
    "Argentina": "900 ARS",
    "Colombia": "3950 COP",
    "Chile": "925 CLP",
    "Peru": "3.7 PEN"
}

def get_exchange_rate(country: str) -> str:
    """Get USD exchange rate for a Latin American country"""
    rate = LATAM_EXCHANGE_RATES.get(country.title())
    if rate:
        return f"The current exchange rate in {country} is 1 USD = {rate}."
    else:
        return f"Sorry, I don't have exchange rate data for {country}."

def process_query(query: str, image=None) -> str:
    """Process user query and handle exchange rate requests"""
    # Check if query is asking about exchange rates (only for text queries)
    if not image:
        countries = ["Brazil", "Mexico", "Argentina", "Colombia", "Chile", "Peru"]
        query_lower = query.lower()
        
        for country in countries:
            if country.lower() in query_lower and ("exchange" in query_lower or "rate" in query_lower or "currency" in query_lower):
                return get_exchange_rate(country)
    
    # For queries with images or other general queries
    if image:
        if query.strip():
            # User provided both image and question
            enhanced_query = f"""You are a fintech assistant specialized in Latin American financial systems. 
            
Available exchange rates:
- Brazil: 1 USD = 5.2 BRL
- Mexico: 1 USD = 17.1 MXN  
- Argentina: 1 USD = 900 ARS
- Colombia: 1 USD = 3950 COP
- Chile: 1 USD = 925 CLP
- Peru: 1 USD = 3.7 PEN

Please analyze this image and answer the user's question: {query}

Focus on any financial, fintech, or business-related content in the image."""
        else:
            # Only image provided
            enhanced_query = """You are a fintech assistant specialized in Latin American financial systems. 
            
Please analyze this image and provide insights about any financial, fintech, business, or economic content you can identify. 
Look for:
- Financial documents, charts, or graphs
- Business reports or presentations
- Banking interfaces or apps
- Economic data or statistics
- Any relevant financial information

If the image contains text, please also extract and summarize the key points."""
    else:
        # Text-only query
        enhanced_query = f"""You are a fintech assistant specialized in Latin American financial systems. 
        
Available exchange rates:
- Brazil: 1 USD = 5.2 BRL
- Mexico: 1 USD = 17.1 MXN  
- Argentina: 1 USD = 900 ARS
- Colombia: 1 USD = 3950 COP
- Chile: 1 USD = 925 CLP
- Peru: 1 USD = 3.7 PEN

User question: {query}

Please provide a helpful response about fintech or financial services in Latin America."""
    
    try:
        if image:
            response = model.generate_content([enhanced_query, image])
        else:
            response = model.generate_content(enhanced_query)
        return response.text
    except Exception as e:
        return f"I apologize, but I encountered an error processing your request: {str(e)}"

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

def process_image(uploaded_image):
    """Process uploaded image"""
    try:
        image = Image.open(uploaded_image)
        return image
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(page_title="Jeeves LLM Agent", layout="centered")
st.title("Jeeves LLM Assistant")

st.write("Type your question in English, Spanish, or Portuguese about a fintech product, and get an intelligent response.")

# Create two columns for file uploads
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📎 Attach Document")
    uploaded_file = st.file_uploader(
        "Upload a document for analysis",
        type=['txt', 'pdf', 'docx'],
        help="Upload a text, PDF, or Word document. The content will be analyzed automatically."
    )

with col2:
    st.markdown("### 🖼️ Upload Image")
    uploaded_image = st.file_uploader(
        "Upload an image for analysis",
        type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
        help="Upload an image containing financial data, charts, documents, or any visual content to analyze."
    )

# Display uploaded image
if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", width=400)

# Text input section
user_input = st.text_area("Your Question:", height=150, placeholder="Ask a question, or leave blank to analyze uploaded files...")

if st.button("Submit") and (user_input or uploaded_file or uploaded_image):
    try:
        # Handle file upload
        file_content = ""
        if uploaded_file:
            with st.spinner("Reading document..."):
                file_content = extract_text_from_file(uploaded_file)
                st.success(f"✅ File '{uploaded_file.name}' loaded successfully!")
        
        # Handle image upload
        image = None
        if uploaded_image:
            with st.spinner("Processing image..."):
                image = process_image(uploaded_image)
                if image:
                    st.success(f"✅ Image '{uploaded_image.name}' loaded successfully!")
        
        # Prepare the query
        if user_input and file_content and image:
            # All three: question, file, and image
            query = f"User question: {user_input}\n\nDocument content: {file_content}\n\nPlease also analyze the uploaded image in context."
        elif user_input and file_content:
            # Question and file
            query = f"User question: {user_input}\n\nDocument content: {file_content}"
        elif user_input and image:
            # Question and image
            query = user_input
        elif file_content and image:
            # File and image
            query = f"Please analyze both the document content and the image:\n\nDocument content: {file_content}"
        elif file_content:
            # Only file
            query = f"Please analyze this document and provide key insights about its fintech/financial content: {file_content}"
        elif image:
            # Only image
            query = ""  # Will be handled by process_query
        else:
            # Only question
            query = user_input
        
        # Language detection and translation
        original_lang = detect(query) if query.strip() else 'en'
        translated_input = GoogleTranslator(source='auto', target='en').translate(query) if query.strip() else ""

        # Process with Gemini
        response = process_query(translated_input, image)

        final_output = GoogleTranslator(source='auto', target=original_lang).translate(str(response))

        st.markdown("### Response:")
        st.success(final_output)

    except Exception as e:
        st.error(f"Error: {e}")
        if "api_key" in str(e).lower():
            st.info("💡 Make sure your Google API key is set in the .env file as GOOGLE_API_KEY=your-key-here")
        elif "quota" in str(e).lower():
            st.info("💡 You may have exceeded your API quota. Please check your Google Cloud Console.")
else:
    if not user_input and not uploaded_file and not uploaded_image:
        st.info("💡 Please enter a question, upload a document, or upload an image to get started!")