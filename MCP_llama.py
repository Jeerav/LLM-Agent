# mcp_llamaindex_demo.py

from llama_index.agent.openai import OpenAIAgent
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import FunctionTool, QueryEngineTool
import time
import logging
import os
from functools import wraps
from typing import Optional
import hashlib

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
CACHE_EXPIRE_TIME = 3600  # 1 hour
RATE_LIMIT_DELAY = 1  # seconds between calls

# Simple in-memory cache
cache = {}

def rate_limit(func):
    """Decorator to add rate limiting"""
    last_call = [0]
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_time = time.time()
        time_since_last = current_time - last_call[0]
        
        if time_since_last < RATE_LIMIT_DELAY:
            sleep_time = RATE_LIMIT_DELAY - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        last_call[0] = time.time()
        return func(*args, **kwargs)
    
    return wrapper

def get_cache_key(text: str) -> str:
    """Generate cache key from text"""
    return hashlib.md5(text.encode()).hexdigest()

def get_from_cache(key: str) -> Optional[str]:
    """Get cached response if available and not expired"""
    if key in cache:
        timestamp, response = cache[key]
        if time.time() - timestamp < CACHE_EXPIRE_TIME:
            logger.info("Using cached response")
            return response
        else:
            del cache[key]  # Remove expired cache
    return None

def save_to_cache(key: str, response: str):
    """Save response to cache"""
    cache[key] = (time.time(), response)

def retry_on_quota_error(func):
    """Decorator to retry on quota errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        last_exception = None
        
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                error_msg = str(e).lower()
                
                # Check for quota/rate limit related errors
                if any(term in error_msg for term in ['quota', 'rate limit', 'too many requests', 'insufficient quota']):
                    logger.warning(f"API quota/rate limit hit on attempt {attempt + 1}: {e}")
                    
                    if attempt < MAX_RETRIES - 1:
                        delay = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logger.error("Max retries exceeded for quota error")
                        raise QuotaExceededError("API quota exceeded after multiple retries")
                else:
                    # For non-quota errors, raise immediately
                    raise e
        
        raise last_exception
    
    return wrapper

class QuotaExceededError(Exception):
    pass

# Safe document loading with fallback
def safe_load_documents():
    """Load documents safely with fallback"""
    try:
        if os.path.exists("docs") and os.listdir("docs"):
            documents = SimpleDirectoryReader("docs").load_data()
            index = VectorStoreIndex.from_documents(documents)
            query_engine = index.as_query_engine()
            
            doc_tool = QueryEngineTool.from_defaults(
                query_engine=query_engine,
                name="DocSearch",
                description="Searches business documents for information."
            )
            return doc_tool
        else:
            logger.warning("No documents found in 'docs' directory")
            return None
    except Exception as e:
        logger.error(f"Failed to load documents: {e}")
        return None

# Load documents with error handling
doc_tool = safe_load_documents()

def get_weather(city: str) -> str:
    """Get weather information (mock implementation)"""
    return f"The weather in {city} is sunny with 25°C."

weather_tool = FunctionTool.from_defaults(
    fn=get_weather,
    name="WeatherTool",
    description="Provides weather info for a given city"
)

# Create tools list based on availability
tools = [weather_tool]
if doc_tool:
    tools.append(doc_tool)
    logger.info("Document search tool loaded successfully")
else:
    logger.warning("Document search tool not available")

# Create agent with error handling
try:
    agent = OpenAIAgent.from_tools(tools, verbose=True)
    logger.info("OpenAI agent created successfully")
except Exception as e:
    logger.error(f"Failed to create OpenAI agent: {e}")
    agent = None

@rate_limit
@retry_on_quota_error
def get_ai_response(query: str) -> str:
    """Get AI response with rate limiting and retry logic"""
    if agent is None:
        raise Exception("OpenAI agent not available")
    
    cache_key = get_cache_key(query)
    cached_response = get_from_cache(cache_key)
    
    if cached_response:
        return cached_response
    
    response = agent.chat(query)
    response_str = str(response)
    
    save_to_cache(cache_key, response_str)
    return response_str

def get_fallback_response(query: str) -> str:
    """Provide fallback response when API is unavailable"""
    return f"I apologize, but I'm currently experiencing high demand. For weather information, I can tell you that most cities are experiencing typical seasonal weather. For document searches, please try again in a few minutes when the service is available."

def main():
    """Main function with comprehensive error handling"""
    query = "What's the weather in Paris and what do the documents say about revenue?"
    
    print(f"🔍 Processing query: {query}")
    print(f"📊 Cache status: {len(cache)} items cached")
    print(f"🔧 Tools available: {len(tools)}")
    
    try:
        response = get_ai_response(query)
        print(f"✅ AI Response: {response}")
        
    except QuotaExceededError:
        print("⚠️ API quota exceeded. Using fallback response.")
        fallback_response = get_fallback_response(query)
        print(f"🔄 Fallback Response: {fallback_response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔄 Using fallback response.")
        fallback_response = get_fallback_response(query)
        print(f"🔄 Fallback Response: {fallback_response}")
    
    # Display usage statistics
    print(f"\n📈 Usage Statistics:")
    print(f"   - Cache entries: {len(cache)}")
    print(f"   - Tools loaded: {len(tools)}")
    print(f"   - Agent status: {'✅ Ready' if agent else '❌ Unavailable'}")

if __name__ == "__main__":
    main()
