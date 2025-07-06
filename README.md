# Jeeves LLM Assistant - API Quota Resistant

This project provides a robust LLM assistant with comprehensive API quota management to prevent build failures and ensure reliable operation.

## 🚀 Features

### API Quota Management
- **Rate Limiting**: Automatic delays between API calls to prevent quota exhaustion
- **Retry Logic**: Exponential backoff for temporary failures
- **Caching**: Responses cached for 1 hour to reduce API usage
- **Fallback Responses**: Graceful degradation when API is unavailable
- **Error Handling**: Comprehensive error handling for quota exceeded scenarios

### Multi-Language Support
- **Translation**: Automatic translation between English, Spanish, and Portuguese
- **Language Detection**: Automatic detection of input language
- **Localized Fallbacks**: Fallback responses in multiple languages

### Streamlit Web Interface
- **User-Friendly UI**: Clean, modern interface with status indicators
- **Real-time Feedback**: Loading spinners and progress indicators
- **Usage Statistics**: Cache status and API usage information
- **Configuration Display**: Current settings and quota status

## 📋 Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# Rate Limiting Configuration
MAX_RETRIES=3
RETRY_DELAY=2
RATE_LIMIT_DELAY=1.0

# Cache Configuration
CACHE_EXPIRE_TIME=3600
ENABLE_CACHE=true

# Feature Configuration
ENABLE_FALLBACK=true
ENABLE_TRANSLATION=true

# Logging Configuration
LOG_LEVEL=INFO

# Document Configuration
DOCS_DIRECTORY=docs
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | OpenAI model to use |
| `MAX_RETRIES` | `3` | Maximum retries for failed API calls |
| `RETRY_DELAY` | `2` | Initial retry delay in seconds |
| `RATE_LIMIT_DELAY` | `1.0` | Delay between API calls in seconds |
| `CACHE_EXPIRE_TIME` | `3600` | Cache expiration time in seconds |
| `ENABLE_CACHE` | `true` | Enable response caching |
| `ENABLE_FALLBACK` | `true` | Enable fallback responses |
| `ENABLE_TRANSLATION` | `true` | Enable translation features |

## 🏃 Usage

### Running the Streamlit App

```bash
streamlit run LLM-agent.py
```

### Running the MCP Demo

```bash
python MCP_llama.py
```

## 🛡️ Quota Protection Features

### 1. Rate Limiting
- Automatic delays between API calls
- Configurable rate limits via environment variables
- Prevents overwhelming API endpoints

### 2. Retry Logic
- Exponential backoff for transient failures
- Distinguishes between quota errors and other failures
- Configurable retry attempts

### 3. Caching System
- MD5-based cache keys for efficient storage
- Automatic cache expiration
- Significant reduction in API calls for repeated queries

### 4. Fallback Responses
- Graceful degradation when API is unavailable
- Contextual fallback messages
- Multi-language fallback support

### 5. Error Handling
- Comprehensive error categorization
- User-friendly error messages
- Logging for debugging and monitoring

## 🔍 Monitoring and Debugging

### Logging
The application provides detailed logging:
- API call attempts and successes
- Cache hits and misses
- Rate limiting activities
- Error occurrences

### Status Indicators
- **✅ AI Assistant ready**: OpenAI service is available
- **⚠️ OpenAI service unavailable**: Fallback mode active
- **📱 X responses cached**: Number of cached responses
- **🔄 Fallback Response**: When using fallback mode

### Configuration Validation
The application validates configuration on startup:
```python
from config import Config
Config.validate_config()
Config.print_config()
```

## 🚨 Troubleshooting

### Common Issues

1. **API Quota Exceeded**
   - **Solution**: The application automatically handles this with fallback responses
   - **Prevention**: Adjust `RATE_LIMIT_DELAY` to slow down requests

2. **Build Failures**
   - **Solution**: All API calls are wrapped in try-catch blocks
   - **Prevention**: Enable fallback mode with `ENABLE_FALLBACK=true`

3. **Slow Response Times**
   - **Solution**: Responses are cached for faster subsequent requests
   - **Optimization**: Increase `CACHE_EXPIRE_TIME` for longer caching

4. **Translation Errors**
   - **Solution**: Translation can be disabled with `ENABLE_TRANSLATION=false`
   - **Fallback**: App works in English-only mode

### Debug Mode
Enable debug logging:
```bash
LOG_LEVEL=DEBUG streamlit run LLM-agent.py
```

## 📊 Performance Optimization

### Cache Strategy
- **Hit Rate**: Typically 30-50% for repeated queries
- **Memory Usage**: Minimal with automatic cleanup
- **Expiration**: Configurable based on use case

### API Efficiency
- **Rate Limiting**: Prevents throttling
- **Batch Processing**: Future enhancement for multiple queries
- **Model Selection**: Use cheaper models when possible

## 🔄 Fallback Strategies

### API Unavailable
1. **Cached Response**: Use previously cached identical queries
2. **Fallback Message**: Context-aware fallback responses
3. **Offline Mode**: Basic functionality without AI

### Quota Exceeded
1. **Exponential Backoff**: Automatic retry with increasing delays
2. **Graceful Degradation**: Fallback to cached or static responses
3. **User Notification**: Clear messaging about current status

## 🌍 Multi-Language Support

### Supported Languages
- **English**: Primary language
- **Spanish**: Full translation support
- **Portuguese**: Full translation support

### Translation Features
- **Auto-detection**: Automatic input language detection
- **Bidirectional**: Input and output translation
- **Fallback**: Language-specific fallback messages

## 📈 Usage Examples

### Basic Query
```python
# English
"What are the current exchange rates for Brazil?"

# Spanish
"¿Cuáles son los tipos de cambio actuales para Brasil?"

# Portuguese
"Quais são as taxas de câmbio atuais para o Brasil?"
```

### Error Handling
```python
try:
    response = get_ai_response(query)
    print(f"✅ AI Response: {response}")
except QuotaExceededError:
    print("⚠️ Using fallback response")
    response = get_fallback_response(query)
```

## 🔧 Advanced Configuration

### Custom Rate Limits
```python
# For high-volume usage
RATE_LIMIT_DELAY=0.5
MAX_RETRIES=5

# For low-quota scenarios
RATE_LIMIT_DELAY=3.0
MAX_RETRIES=2
```

### Cache Optimization
```python
# Long-term caching
CACHE_EXPIRE_TIME=7200  # 2 hours

# Short-term caching
CACHE_EXPIRE_TIME=1800  # 30 minutes
```

## 🛠️ Development

### Adding New Features
1. Update `config.py` for new configuration options
2. Add rate limiting decorators to new API calls
3. Implement fallback mechanisms for new features
4. Update documentation and examples

### Testing
```bash
# Test quota handling
python -c "from config import Config; Config.validate_config()"

# Test with limited quota
RATE_LIMIT_DELAY=10.0 python MCP_llama.py
```

## 📝 License

This project is designed to be robust and production-ready with comprehensive API quota management to prevent build failures and ensure reliable operation in production environments.

## 🤝 Contributing

When contributing, please ensure:
1. All API calls include rate limiting
2. Fallback mechanisms are implemented
3. Error handling is comprehensive
4. Configuration options are documented
5. Tests cover quota scenarios