# mcp_llamaindex_demo.py

from llama_index.agent.openai import OpenAIAgent
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import FunctionTool, QueryEngineTool

documents = SimpleDirectoryReader("docs").load_data()
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

agent = OpenAIAgent.from_tools([doc_tool, weather_tool], verbose=True)

response = agent.chat("What's the weather in Paris and what do the documents say about revenue?")
print(response)
