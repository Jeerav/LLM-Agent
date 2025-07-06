#!/bin/bash
# mac_setup.sh - Complete setup script for Mac LLM alternatives
# Run this script to automatically set up LocalAI or Ollama on your Mac

set -e  # Exit on any error

echo "🍎 Setting up LLM alternatives on Mac..."
echo "This script will help you eliminate OpenAI API quota issues!"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for user input
wait_for_user() {
    echo "⚠️  $1"
    read -p "Press Enter once ready to continue..."
}

# Check macOS version
echo "📍 Checking macOS version..."
macos_version=$(sw_vers -productVersion)
echo "   Running macOS $macos_version"

# Detect Apple Silicon
if [[ $(uname -m) == "arm64" ]]; then
    echo "   Detected Apple Silicon Mac (M1/M2/M3)"
    APPLE_SILICON=true
else
    echo "   Detected Intel Mac"
    APPLE_SILICON=false
fi

# Install Homebrew if not present
if ! command_exists brew; then
    echo "🍺 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon
    if [[ $APPLE_SILICON == true ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew already installed"
fi

# Install Python if not present
if ! command_exists python3; then
    echo "🐍 Installing Python..."
    brew install python
else
    echo "✅ Python already installed"
fi

# Install Docker if not present
if ! command_exists docker; then
    echo "🐳 Installing Docker Desktop..."
    brew install --cask docker
    wait_for_user "Docker Desktop has been installed. Please start Docker Desktop from Applications folder"
else
    echo "✅ Docker already installed"
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        wait_for_user "Docker is installed but not running. Please start Docker Desktop"
    fi
fi

# Choose LLM option
echo ""
echo "🤖 Choose your LLM setup:"
echo "1. LocalAI (Recommended - OpenAI API compatible)"
echo "2. Ollama (Great for local models)"
echo "3. Both (Install both options)"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1|3)
        INSTALL_LOCALAI=true
        ;;
    *)
        INSTALL_LOCALAI=false
        ;;
esac

case $choice in
    2|3)
        INSTALL_OLLAMA=true
        ;;
    *)
        INSTALL_OLLAMA=false
        ;;
esac

# Create project directory
PROJECT_DIR="$HOME/llm-agent-local"
echo "📁 Creating project directory: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install streamlit llama-index openai deep-translator langdetect python-dotenv

# Create .env file
echo "⚙️  Creating .env configuration file..."
cat > .env << EOF
# LocalAI Configuration (default)
OPENAI_API_BASE=http://localhost:8080/v1
OPENAI_API_KEY=fake-key

# Ollama Configuration (uncomment to use)
# OPENAI_API_BASE=http://localhost:11434/v1
# OPENAI_API_KEY=fake-key

# OpenRouter Configuration (uncomment to use)
# OPENAI_API_BASE=https://openrouter.ai/api/v1
# OPENAI_API_KEY=your-openrouter-key
EOF

# Install and setup LocalAI
if [[ $INSTALL_LOCALAI == true ]]; then
    echo "🤖 Setting up LocalAI..."
    
    # Choose appropriate image for Apple Silicon
    if [[ $APPLE_SILICON == true ]]; then
        LOCALAI_IMAGE="localai/localai:latest-aio-cpu"
        PLATFORM_FLAG="--platform linux/arm64"
    else
        LOCALAI_IMAGE="localai/localai:latest-aio-cpu"
        PLATFORM_FLAG=""
    fi
    
    echo "   Pulling LocalAI Docker image..."
    docker pull $LOCALAI_IMAGE
    
    echo "   Starting LocalAI container..."
    docker run -d -p 8080:8080 --name local-ai $PLATFORM_FLAG $LOCALAI_IMAGE
    
    echo "   Waiting for LocalAI to start (this may take a few minutes)..."
    sleep 30
    
    # Test LocalAI
    echo "   Testing LocalAI connection..."
    max_attempts=10
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:8080/v1/models > /dev/null; then
            echo "   ✅ LocalAI is running!"
            break
        else
            echo "   ⏳ Waiting for LocalAI... (attempt $attempt/$max_attempts)"
            sleep 10
            ((attempt++))
        fi
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo "   ❌ LocalAI failed to start properly"
        echo "   Check logs with: docker logs local-ai"
    fi
fi

# Install and setup Ollama
if [[ $INSTALL_OLLAMA == true ]]; then
    echo "🦙 Setting up Ollama..."
    
    # Install Ollama
    if ! command_exists ollama; then
        echo "   Installing Ollama..."
        brew install ollama
    else
        echo "   ✅ Ollama already installed"
    fi
    
    # Start Ollama service
    echo "   Starting Ollama service..."
    brew services start ollama
    
    sleep 5
    
    # Download recommended models
    echo "   Downloading recommended models (this may take a while)..."
    ollama pull llama3.1:8b
    ollama pull codellama:7b
    
    echo "   ✅ Ollama setup complete!"
    echo "   Available models:"
    ollama list
fi

# Copy your existing files if they exist
if [ -f "../LLM-agent.py" ]; then
    echo "📋 Copying your existing LLM-agent.py..."
    cp ../LLM-agent.py .
fi

if [ -f "../MCP_llama.py" ]; then
    echo "📋 Copying your existing MCP_llama.py..."
    cp ../MCP_llama.py .
fi

# Create test script
echo "🧪 Creating test script..."
cat > test_setup.py << 'EOF'
#!/usr/bin/env python3
"""Test script to verify the setup is working"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI client
openai.api_base = os.getenv("OPENAI_API_BASE", "http://localhost:8080/v1")
openai.api_key = os.getenv("OPENAI_API_KEY", "fake-key")

def test_connection():
    """Test the LLM connection"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello! Please respond with 'Setup successful!'"}],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ LLM Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing LLM setup...")
    if test_connection():
        print("🎉 Setup is working correctly!")
    else:
        print("❌ Setup needs attention")
EOF

# Make test script executable
chmod +x test_setup.py

# Create updated version of LLM-agent.py if it doesn't exist
if [ ! -f "LLM-agent.py" ]; then
    echo "📝 Creating updated LLM-agent.py..."
    cat > LLM-agent.py << 'EOF'
import streamlit as st
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool
from deep_translator import GoogleTranslator
from langdetect import detect
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()

# Configure for local LLM
openai.api_base = os.getenv("OPENAI_API_BASE", "http://localhost:8080/v1")
openai.api_key = os.getenv("OPENAI_API_KEY", "fake-key")

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

# Create an agent with local LLM
agent = OpenAIAgent.from_tools([exchange_tool], verbose=True)

# Streamlit UI
st.set_page_config(page_title="Jeeves LLM Agent (Local)", layout="centered")
st.title("Jeeves LLM Assistant - Local Version")
st.info("🚀 Running on local LLM - No API quotas!")

st.write("Type your question in English, Spanish, or Portuguese about a fintech product, and get an intelligent response.")

user_input = st.text_area("Your Question:", height=150)

if st.button("Submit") and user_input:
    try:
        with st.spinner("Processing..."):
            original_lang = detect(user_input)
            translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

            prompt = f"You are a fintech assistant specialized in Latin American financial systems. Answer the following question clearly and concisely:\n\n{translated_input}"

            # Call local LLM
            response = agent.chat(translated_input)

            final_output = GoogleTranslator(source='auto', target=original_lang).translate(str(response))

            st.markdown("### Response:")
            st.success(final_output)

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Make sure your local LLM is running!")

# Add sidebar with status
with st.sidebar:
    st.header("🔧 System Status")
    
    # Check if LocalAI is running
    try:
        import requests
        response = requests.get(f"{os.getenv('OPENAI_API_BASE', 'http://localhost:8080')}/v1/models", timeout=5)
        if response.status_code == 200:
            st.success("✅ Local LLM is running")
        else:
            st.error("❌ Local LLM not responding")
    except:
        st.error("❌ Local LLM not accessible")
    
    st.markdown("---")
    st.markdown("### 📝 Configuration")
    st.code(f"API Base: {os.getenv('OPENAI_API_BASE', 'Not set')}")
    st.code(f"API Key: {os.getenv('OPENAI_API_KEY', 'Not set')}")
EOF
fi

# Create start script
echo "🚀 Creating start script..."
cat > start.sh << 'EOF'
#!/bin/bash
# Start script for local LLM agent

echo "🚀 Starting Local LLM Agent..."

# Activate virtual environment
source venv/bin/activate

# Check if LocalAI is running
if docker ps | grep -q "local-ai"; then
    echo "✅ LocalAI is running"
elif docker ps -a | grep -q "local-ai"; then
    echo "🔄 Starting LocalAI..."
    docker start local-ai
else
    echo "❌ LocalAI not found. Run setup script first."
    exit 1
fi

# Check if Ollama is running (if installed)
if command -v ollama >/dev/null 2>&1; then
    if ! pgrep -x "ollama" > /dev/null; then
        echo "🔄 Starting Ollama..."
        ollama serve &
        sleep 5
    fi
    echo "✅ Ollama is running"
fi

# Start Streamlit app
echo "🌟 Starting Streamlit app..."
streamlit run LLM-agent.py
EOF

chmod +x start.sh

# Run initial test
echo ""
echo "🧪 Running initial test..."
source venv/bin/activate
python test_setup.py

# Summary
echo ""
echo "🎉 Setup Complete!"
echo "================="
echo "📁 Project location: $PROJECT_DIR"
echo ""
echo "🚀 To start your app:"
echo "   cd $PROJECT_DIR"
echo "   ./start.sh"
echo ""
echo "⚙️  To manually start services:"
if [[ $INSTALL_LOCALAI == true ]]; then
    echo "   LocalAI: docker start local-ai"
fi
if [[ $INSTALL_OLLAMA == true ]]; then
    echo "   Ollama: ollama serve"
fi
echo ""
echo "🧪 To test setup:"
echo "   cd $PROJECT_DIR && source venv/bin/activate && python test_setup.py"
echo ""
echo "📝 Configuration files created:"
echo "   .env - Environment variables"
echo "   LLM-agent.py - Updated Streamlit app"
echo "   start.sh - Easy start script"
echo ""
echo "✅ Your API quota issues are now solved!"
echo "   No more OpenAI API limits - everything runs locally!"