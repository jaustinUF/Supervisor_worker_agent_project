import httpx
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings('ignore')

# Initialize the language model
llm = ChatOpenAI(temperature=0, model="gpt-4o")

def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

wikipedia_tool = Tool(
    name='Wikipedia Search',
    func=wikipedia,
    description="Search Wikipedia and return the snippet from the first search result."
)
# Initialize the agent with the wikipedia tool
agent = initialize_agent(
    tools=[wikipedia_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # verbose=False,
    verbose=True,
    handle_parsing_errors=True  # Enable handling of parsing errors
)
# Define the prompt to test the agent
prompt = "What languages are spoken in Spain that are also spoken in France?"
input_data = {"input": prompt} # Prepare the input for the agent

# Run the agent with the provided input data
print(f"\nTesting Wikipedia Search with prompt: '{prompt}'\n")
try:
    response = agent.invoke(input_data)
    print(f"Response:\n{response['output']}\n")
except Exception as e:
    print(f"An error occurred: {e}")
