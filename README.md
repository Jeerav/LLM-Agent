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