from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings('ignore')

# Initialize the language model
llm = ChatOpenAI(temperature=0, model="gpt-4o")

# Initialize the Tavily Search tool
tavily_tool = TavilySearchResults(max_results=2)

# Initialize the agent with the Tavily Search tool
agent = initialize_agent(
    tools=[tavily_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True  # Enable handling of parsing errors
)
# Define the prompt to test the agent
prompt = "Search for the latest advancements in AI research."

# Prepare the input for the agent
input_data = {"input": prompt}

# Run the agent with the provided input data
print(f"\nTesting SearchAgent with prompt: '{prompt}'\n")
try:
    response = agent.invoke(input_data)
    print(f"Response:\n{response['output']}\n")
except Exception as e:
    print(f"An error occurred: {e}")
