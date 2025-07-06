"""
Configuration settings for API quota management and application behavior
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for API quota management"""
    
    # API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Rate Limiting Configuration
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "2"))  # seconds
    RATE_LIMIT_DELAY: float = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))  # seconds between calls
    
    # Cache Configuration
    CACHE_EXPIRE_TIME: int = int(os.getenv("CACHE_EXPIRE_TIME", "3600"))  # 1 hour
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    
    # Fallback Configuration
    ENABLE_FALLBACK: bool = os.getenv("ENABLE_FALLBACK", "true").lower() == "true"
    
    # OpenAI Model Configuration
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Document Configuration
    DOCS_DIRECTORY: str = os.getenv("DOCS_DIRECTORY", "docs")
    
    # Translation Configuration
    ENABLE_TRANSLATION: bool = os.getenv("ENABLE_TRANSLATION", "true").lower() == "true"
    
    @classmethod
    def get_openai_config(cls) -> Dict[str, Any]:
        """Get OpenAI configuration dictionary"""
        return {
            "model": cls.OPENAI_MODEL,
            "max_tokens": cls.OPENAI_MAX_TOKENS,
            "temperature": cls.OPENAI_TEMPERATURE,
        }
    
    @classmethod
    def get_rate_limit_config(cls) -> Dict[str, Any]:
        """Get rate limiting configuration dictionary"""
        return {
            "max_retries": cls.MAX_RETRIES,
            "retry_delay": cls.RETRY_DELAY,
            "rate_limit_delay": cls.RATE_LIMIT_DELAY,
        }
    
    @classmethod
    def get_cache_config(cls) -> Dict[str, Any]:
        """Get cache configuration dictionary"""
        return {
            "cache_expire_time": cls.CACHE_EXPIRE_TIME,
            "enable_cache": cls.ENABLE_CACHE,
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        if not cls.OPENAI_API_KEY:
            print("⚠️  Warning: OPENAI_API_KEY not set. API calls will fail.")
            return False
        
        if cls.MAX_RETRIES < 1:
            print("⚠️  Warning: MAX_RETRIES should be at least 1.")
            return False
        
        if cls.RETRY_DELAY < 0:
            print("⚠️  Warning: RETRY_DELAY should be non-negative.")
            return False
        
        if cls.RATE_LIMIT_DELAY < 0:
            print("⚠️  Warning: RATE_LIMIT_DELAY should be non-negative.")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration for debugging"""
        print("📋 Current Configuration:")
        print(f"   OpenAI Model: {cls.OPENAI_MODEL}")
        print(f"   Max Retries: {cls.MAX_RETRIES}")
        print(f"   Retry Delay: {cls.RETRY_DELAY}s")
        print(f"   Rate Limit Delay: {cls.RATE_LIMIT_DELAY}s")
        print(f"   Cache Enabled: {cls.ENABLE_CACHE}")
        print(f"   Cache Expire Time: {cls.CACHE_EXPIRE_TIME}s")
        print(f"   Fallback Enabled: {cls.ENABLE_FALLBACK}")
        print(f"   Translation Enabled: {cls.ENABLE_TRANSLATION}")
        print(f"   Docs Directory: {cls.DOCS_DIRECTORY}")
        print(f"   Log Level: {cls.LOG_LEVEL}")

# Example .env file content
ENV_EXAMPLE = """
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
"""