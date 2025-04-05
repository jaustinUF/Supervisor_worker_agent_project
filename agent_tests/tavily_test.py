from print_messages import prnt_msg
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain.schema import OutputParserException
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')
load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4o")
# Refactored tavily_agent.py
tavily_tool = TavilySearchResults(max_results=2)
tavi_agent = create_react_agent(
    model=llm,
    tools=[tavily_tool],
    name="tavi_agent",
    prompt="You are a web search expert. Use the Tavily tool to answer current or recent questions."
)

# Define the prompt to test the agent
prompt = "Search for the latest advancements in AI research."
input_data = {
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

# Run the agent with the provided input data
print(f"\nTesting Wikipedia Search with prompt: '{prompt}'\n")
try:
    response = tavi_agent.invoke(input_data)
    # print(response)
    # prnt_msg(response['messages'])
    # print(f"Response:\n{response['output']}\n")
    print(response["messages"][-1].content)
except OutputParserException as e:
    print(f"Parsing error encountered: {e}")
    # Define fallback behavior here
except Exception as e:
    print(f"An unexpected error occurred: {e}")