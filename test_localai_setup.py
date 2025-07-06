#!/usr/bin/env python3
"""
Quick test script to verify LocalAI setup and compatibility
Run this after setting up LocalAI to ensure everything works
"""

import openai
import os
from typing import Optional

def test_localai_connection(base_url: str = "http://localhost:8080/v1", api_key: str = "fake-key") -> bool:
    """Test basic connection to LocalAI"""
    print("🔍 Testing LocalAI connection...")
    
    # Configure OpenAI client for LocalAI
    openai.api_base = base_url
    openai.api_key = api_key
    
    try:
        # Test basic chat completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # LocalAI will use its default model
            messages=[{"role": "user", "content": "Hello! Can you respond with 'LocalAI is working'?"}],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ LocalAI Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ LocalAI Connection Failed: {e}")
        return False

def test_llamaindex_compatibility():
    """Test LlamaIndex compatibility with LocalAI"""
    print("\n🔍 Testing LlamaIndex compatibility...")
    
    try:
        from llama_index.agent.openai import OpenAIAgent
        from llama_index.core.tools import FunctionTool
        
        # Create a simple test tool
        def test_tool(query: str) -> str:
            """A simple test function"""
            return f"Test tool received: {query}"
        
        function_tool = FunctionTool.from_defaults(
            fn=test_tool,
            name="TestTool",
            description="A simple test tool"
        )
        
        # Create agent with LocalAI
        agent = OpenAIAgent.from_tools([function_tool], verbose=True)
        
        # Test the agent
        response = agent.chat("Use the test tool with 'hello world'")
        print(f"✅ LlamaIndex Agent Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ LlamaIndex Test Failed: {e}")
        return False

def test_fintech_compatibility():
    """Test compatibility with your fintech use case"""
    print("\n🔍 Testing fintech assistant compatibility...")
    
    try:
        # Simulate your exchange rate tool
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
        
        # Test basic fintech query
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fintech assistant for Latin American markets."},
                {"role": "user", "content": "What's the exchange rate for Brazil?"}
            ],
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        print(f"✅ Fintech Query Response: {result}")
        
        # Test the exchange rate tool
        test_rate = get_exchange_rate("Brazil")
        print(f"✅ Exchange Rate Tool: {test_rate}")
        return True
        
    except Exception as e:
        print(f"❌ Fintech Test Failed: {e}")
        return False

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        "openai",
        "llama-index",
        "streamlit",
        "deep-translator",
        "langdetect",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 LocalAI Setup Testing Script")
    print("=" * 50)
    
    # Check if LocalAI is likely running
    print("\n💡 Make sure LocalAI is running first:")
    print("   docker run -p 8080:8080 --name local-ai -ti localai/localai:latest-aio-cpu")
    print("   Or visit: https://localai.io for installation instructions")
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install missing packages first")
        return
    
    # Test LocalAI connection
    if not test_localai_connection():
        print("\n❌ LocalAI connection failed. Is LocalAI running on port 8080?")
        return
    
    # Test LlamaIndex compatibility
    test_llamaindex_compatibility()
    
    # Test fintech functionality
    test_fintech_compatibility()
    
    print("\n" + "=" * 50)
    print("🎉 Testing complete!")
    print("\n📝 Next steps:")
    print("1. Update your .env file:")
    print("   OPENAI_API_BASE=http://localhost:8080/v1")
    print("   OPENAI_API_KEY=fake-key")
    print("2. Run your existing applications")
    print("3. Monitor performance and adjust models as needed")

if __name__ == "__main__":
    main()