# mcp_llamaindex_ollama_demo.py

from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.agent import ReActAgent
import os

# Configure Ollama LLM
llm = Ollama(model="llama2", request_timeout=120.0)
Settings.llm = llm

# Check if docs directory exists, if not create a simple document
docs_dir = "docs"
if not os.path.exists(docs_dir):
    os.makedirs(docs_dir)
    # Create a sample document if none exists
    with open(f"{docs_dir}/sample.txt", "w") as f:
        f.write("Our company revenue for Q1 was $500,000. We expect 20% growth in Q2.")

documents = SimpleDirectoryReader(docs_dir).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

doc_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="DocSearch",
    description="Searches business documents for information."
)

def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny with 25°C."

weather_tool = FunctionTool.from_defaults(
    fn=get_weather,
    name="WeatherTool",
    description="Provides weather info for a given city"
)

# Create agent with Ollama LLM
agent = ReActAgent.from_tools([doc_tool, weather_tool], llm=llm, verbose=True)

response = agent.chat("What's the weather in Paris and what do the documents say about revenue?")
print(response)