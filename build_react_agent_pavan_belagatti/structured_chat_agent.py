from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()       # load environmental variables
# Create Agent arguments: tools, prompt, llm
tools = [TavilySearchResults(max_results =1)]
# 'pull' popular ReAct process prompt from 'LangChain Hub' @ 'https://smith.langchain.com/hub'
prompt =  hub.pull("hwchase17/structured-chat-agent")
# select model
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")
llm = ChatOpenAI(temperature=0, model="gpt-4o")
# Create Agent
agent = create_structured_chat_agent(llm, tools, prompt)    # Create an agent aimed at supporting tools with multiple inputs.
# Create executor to run the agent
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    # verbose=True,
    verbose=False,
    handle_parsing_errors= True
)
# execute the agent
result = agent_executor.invoke({"input": "what is LlamaIndex and what is the difference between LangChain and LlamaIndex?"})
# print(f'*     *     *     *     *\n') # if agent_executor 'verbose' true
print(result)