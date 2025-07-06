# Mac Setup Guide: LLM Agent Alternatives

## Prerequisites for Mac

First, ensure you have the basic tools installed:

### 1. Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Docker Desktop for Mac
```bash
brew install --cask docker
```
Or download from: https://www.docker.com/products/docker-desktop

### 3. Install Python and pip (if not already installed)
```bash
brew install python
```

## Option 1: LocalAI (RECOMMENDED for Mac)

### Quick Start with Docker
```bash
# Start LocalAI with CPU support (works on all Macs)
docker run -p 8080:8080 --name local-ai -ti localai/localai:latest-aio-cpu

# For Mac with Apple Silicon (M1/M2/M3) - GPU acceleration
docker run -p 8080:8080 --name local-ai -ti localai/localai:latest-aio-gpu-nvidia-cuda-11
```

### Alternative: Direct Installation on Mac
```bash
# Install LocalAI directly
brew install localai/tap/localai

# Or using Go (if you have Go installed)
go install github.com/go-skynet/LocalAI@latest
```

### Test LocalAI is working
```bash
# In a new terminal, test the API
curl http://localhost:8080/v1/models
```

## Option 2: Ollama (Great for Mac)

### Install Ollama
```bash
# Method 1: Using Homebrew (recommended)
brew install ollama

# Method 2: Direct download
curl -fsSL https://ollama.com/install.sh | sh
```

### Start Ollama and Download Models
```bash
# Start Ollama service
ollama serve

# In a new terminal, pull models
ollama pull llama3.1:8b          # Good general model
ollama pull codellama:7b         # Great for coding
ollama pull mistral:7b           # Fast and efficient
ollama pull deepseek-coder:6.7b  # Excellent for coding

# List available models
ollama list
```

### Test Ollama
```bash
# Test directly
ollama run llama3.1:8b

# Or test via API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Hello, world!",
  "stream": false
}'
```

## Option 3: OpenRouter (Cloud-based)

### Setup OpenRouter
```bash
# Install required packages
pip install openai

# Get API key from https://openrouter.ai/
# Set environment variable
export OPENROUTER_API_KEY="your-api-key-here"
```

## Mac-Specific Setup for Your Existing Code

### 1. Update your Python environment
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install your requirements
pip install streamlit llama-index openai deep-translator langdetect python-dotenv
```

### 2. Create/Update your .env file
```bash
# Create .env file in your project directory
cat > .env << EOF
# For LocalAI
OPENAI_API_BASE=http://localhost:8080/v1
OPENAI_API_KEY=fake-key

# For Ollama (if using OpenAI-compatible endpoint)
# OPENAI_API_BASE=http://localhost:11434/v1
# OPENAI_API_KEY=fake-key

# For OpenRouter
# OPENAI_API_BASE=https://openrouter.ai/api/v1
# OPENAI_API_KEY=your-openrouter-key
EOF
```

### 3. Update your LLM-agent.py for Mac
```python
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

# Configure for local LLM (LocalAI or Ollama)
openai.api_base = os.getenv("OPENAI_API_BASE", "http://localhost:8080/v1")
openai.api_key = os.getenv("OPENAI_API_KEY", "fake-key")

# Your existing code continues here...
# The rest remains the same!
```

## Running Your Applications on Mac

### 1. Start your chosen LLM service

**For LocalAI:**
```bash
# Terminal 1: Start LocalAI
docker run -p 8080:8080 --name local-ai -ti localai/localai:latest-aio-cpu
```

**For Ollama:**
```bash
# Terminal 1: Start Ollama
ollama serve
```

### 2. Run your Streamlit app
```bash
# Terminal 2: Navigate to your project
cd /path/to/your/project
source venv/bin/activate

# Run your Streamlit app
streamlit run LLM-agent.py
```

### 3. Test your MCP Llama script
```bash
# Run your document search script
python MCP_llama.py
```

## Mac Performance Optimization

### For Apple Silicon Macs (M1/M2/M3)
```bash
# Use ARM-optimized images for better performance
docker run -p 8080:8080 --platform linux/arm64 --name local-ai -ti localai/localai:latest-aio-cpu

# For Ollama, it's automatically optimized for Apple Silicon
```

### Resource Management
```bash
# Monitor resource usage
# Activity Monitor (GUI) or:
top -o cpu
htop  # install with: brew install htop

# Check Docker resource usage
docker stats
```

## Troubleshooting Common Mac Issues

### 1. Docker Permission Issues
```bash
# Add your user to docker group (if needed)
sudo dkms run test

# Or run docker with sudo (not recommended)
sudo docker run -p 8080:8080 --name local-ai -ti localai/localai:latest-aio-cpu
```

### 2. Port Already in Use
```bash
# Check what's using port 8080
lsof -i :8080

# Kill process if needed
sudo kill -9 <PID>

# Or use different port
docker run -p 8081:8080 --name local-ai -ti localai/localai:latest-aio-cpu
```

### 3. Python/Package Issues
```bash
# Upgrade pip
pip install --upgrade pip

# Install specific versions if needed
pip install openai==1.3.0
pip install llama-index==0.9.0
```

## Complete Mac Setup Script

Create this script to automate the setup:

```bash
#!/bin/bash
# mac_setup.sh - Complete setup script for Mac

echo "🍎 Setting up LLM alternatives on Mac..."

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    brew install --cask docker
    echo "⚠️  Please start Docker Desktop manually before continuing"
    read -p "Press Enter once Docker Desktop is running..."
fi

# Install Python requirements
echo "Setting up Python environment..."
python -m venv venv
source venv/bin/activate
pip install streamlit llama-index openai deep-translator langdetect python-dotenv

# Create .env file
echo "Creating .env file..."
cat > .env << EOF
OPENAI_API_BASE=http://localhost:8080/v1
OPENAI_API_KEY=fake-key
EOF

# Option 1: Start LocalAI
echo "Starting LocalAI..."
docker run -d -p 8080:8080 --name local-ai localai/localai:latest-aio-cpu

# Wait for LocalAI to start
echo "Waiting for LocalAI to start..."
sleep 30

# Test the setup
echo "Testing setup..."
python test_localai_setup.py

echo "✅ Setup complete! You can now run your applications."
echo "To start your Streamlit app: streamlit run LLM-agent.py"
```

## Running the Setup

1. **Save the script:**
```bash
chmod +x mac_setup.sh
./mac_setup.sh
```

2. **Or run manually step by step:**
```bash
# Start LocalAI
docker run -p 8080:8080 --name local-ai -ti localai/localai:latest-aio-cpu

# In new terminal, test
python test_localai_setup.py

# Run your app
streamlit run LLM-agent.py
```

## Daily Usage Commands

```bash
# Start LocalAI (if stopped)
docker start local-ai

# Stop LocalAI
docker stop local-ai

# Remove LocalAI container (to start fresh)
docker rm local-ai

# Run your Streamlit app
streamlit run LLM-agent.py

# Check logs
docker logs local-ai
```

This setup will eliminate your API quota issues completely while running everything locally on your Mac!