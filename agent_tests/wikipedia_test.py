import httpx
from print_messages import prnt_msg
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool
from langchain.schema import OutputParserException
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')
load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4o")

def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

wikipedia_tool = Tool(
    name="wikipedia_search",
    func=wikipedia,
    description="Search Wikipedia and return the snippet from the first search result."
)

wiki_agent = create_react_agent(
    model=llm,
    tools=[wikipedia_tool],
    name="wiki_agent",
    prompt="You are a Wikipedia expert. Use the Wikipedia Search tool to find reliable background information."
)
# Define the prompt to test the agent
prompt = "What languages are spoken in Spain that are also spoken in France?"
input_data = {
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

# Run the agent with the provided input data
print(f"\nTesting Wikipedia Search with prompt: '{prompt}'\n")
try:
    response = wiki_agent.invoke(input_data)
    # print(response)
    prnt_msg(response['messages'])
    # print(f"Response:\n{response['output']}\n")
    print(response["messages"][-1].content)
except OutputParserException as e:
    print(f"Parsing error encountered: {e}")
    # Define fallback behavior here
except Exception as e:
    print(f"An unexpected error occurred: {e}")