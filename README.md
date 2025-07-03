# LLM-Agent

# LLM Agent Setup Guide

## Required Modules Installation

Based on your latest commit, here are all the modules you need to install:

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv llm_agent_env

# Activate virtual environment
source llm_agent_env/bin/activate  # On Windows: llm_agent_env\Scripts\activate

# Install all required packages
pip install openai>=1.3.0 llama-index streamlit deep-translator langdetect python-dotenv
```

### Package List
- **openai** (>=1.3.0) - OpenAI API client
- **llama-index** - AI agent framework  
- **streamlit** - Web interface
- **deep-translator** - Google Translate functionality
- **langdetect** - Language detection
- **python-dotenv** - Environment variables

## Environment Setup

1. Create a `.env` file in your project directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

2. Get your OpenAI API key from: https://platform.openai.com/api-keys

## Common Issues & Solutions

### 1. ModuleNotFoundError: No module named 'openai.types'
**Solution**: Install OpenAI package version 1.3.0 or higher
```bash
pip install --upgrade openai>=1.3.0
```

### 2. Error 429 - insufficient_quota
**Cause**: OpenAI API quota exceeded
**Solutions**:
- Check your OpenAI billing at: https://platform.openai.com/account/billing
- Add payment method if you're on free tier
- Upgrade to paid plan if needed
- Wait for quota reset (if on free tier)

### 3. Running the Application
```bash
# Activate virtual environment
source llm_agent_env/bin/activate

# Run the Streamlit app
streamlit run LLM-agent.py
```

## API Usage Notes
- Free tier has limited monthly credits
- Pay-as-you-go requires adding a payment method
- Monitor usage at: https://platform.openai.com/account/usage

## 🚀 Free Alternatives to Avoid OpenAI Quotas

### Option 1: Ollama (Local LLMs) - COMPLETELY FREE ⭐
```bash
# Install Ollama from: https://ollama.ai/
# Pull a model
ollama pull llama3.2

# Install integration
pip install llama-index-llms-ollama

# Run free version
streamlit run LLM-agent-free.py
```
**Benefits**: No API costs, works offline, unlimited usage

### Option 2: Google Gemini (Free Tier) - RECOMMENDED ⭐
```bash
# Get free API key: https://makersuite.google.com/app/apikey  
pip install llama-index-llms-gemini

# Add to .env file:
GOOGLE_API_KEY=your_gemini_key

# Run Gemini version
streamlit run LLM-agent-gemini.py
```
**Benefits**: 1,500 free requests/day, no billing required, high quality

### Option 3: Hugging Face (Local Models)
```bash
pip install llama-index-llms-huggingface transformers torch
```
**Benefits**: Completely free, runs locally

### Option 4: Together AI (Free Credits)
- Get $25 free credits: https://together.ai/
- Supports many open-source models

### Option 5: Anthropic Claude (Free Tier)
- Get API key: https://console.anthropic.com/
- Has generous free tier

## File Overview
- `LLM-agent.py` - Original with OpenAI (requires quota)
- `LLM-agent-free.py` - Ollama version (completely free)
- `LLM-agent-gemini.py` - Google Gemini version (free tier)
- `requirements.txt` - For OpenAI version
- `requirements-free.txt` - For free alternatives