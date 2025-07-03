# LLM Setup Guide

Your original script exceeded OpenAI quota. Here are the alternatives I've created:

## 🚀 Option 1: Google Gemini (Recommended)

**File:** `LLM-agent-gemini.py`

### Setup:
1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to your `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   streamlit run LLM-agent-gemini.py
   ```

**Pros:** 
- Free tier with generous limits
- High quality responses
- Easy setup

---

## 🏠 Option 2: Ollama (Completely Free)

**Files:** `LLM-agent-ollama.py`, `MCP_llama_ollama.py`

### Setup:
1. Install Ollama:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Start Ollama service:
   ```bash
   ollama serve
   ```
3. Pull a model (in another terminal):
   ```bash
   ollama pull llama2
   # or other models: mistral, codellama, neural-chat
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run Streamlit app:
   ```bash
   streamlit run LLM-agent-ollama.py
   ```
6. Or run LlamaIndex agent:
   ```bash
   python MCP_llama_ollama.py
   ```

**Pros:**
- Completely free
- Runs locally (privacy)
- No API quotas
- Multiple model choices

**Cons:**
- Requires local installation
- Uses more system resources

---

## 🔄 Migration Summary

| Original | Alternative |
|----------|-------------|
| `LLM-agent.py` (OpenAI) | `LLM-agent-gemini.py` or `LLM-agent-ollama.py` |
| `MCP_llama.py` (OpenAI) | `MCP_llama_ollama.py` |

## 🎯 Quick Start

**For immediate use (Gemini):**
1. Get Gemini API key
2. Update `.env` file
3. `streamlit run LLM-agent-gemini.py`

**For free forever (Ollama):**
1. `curl -fsSL https://ollama.com/install.sh | sh`
2. `ollama serve` (in background)
3. `ollama pull llama2`
4. `streamlit run LLM-agent-ollama.py`