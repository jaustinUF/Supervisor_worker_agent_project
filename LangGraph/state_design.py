# Use 'AgentState' to pass info along graph (12:30)
#   see AgentState_design.JPG
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph
import python_weather
import asyncio
from dotenv import load_dotenv
load_dotenv()       # load environmental variables

model = ChatOpenAI(temperature = 0.7)
# AgentState = {'messages': []} # shows the state structure; not used by the script

def func1(state):
    messages = state['messages']
    user_input = messages[-1]
    get_city_prompt = "Your task is to provide only the city name based on the user query. \
            Nothing more, just the city name mentioned. Following is the user query: " + user_input
    response = model.invoke(get_city_prompt)
    state['messages'].append(response.content) # add this response
    return state

def func2(state):
    messages = state['messages']
    agent_response = messages[-1]       # last message should be city

    async def fetch_weather(agent_resp):
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get(agent_resp)
            return weather # string: <Forecast location='Miami' datetime=datetime.datetime(2025, 3, 14, 11, 4) temperature=75>
    state['messages'].append(str(asyncio.run(fetch_weather(agent_response)))) # original return is of type 'forcast'
    return state

def func3(state):
    messages = state['messages']
    user_input = messages[0]            # first message is original user input
    available_info = messages[-1]       # last message should weather
    # pass both messages in prompt to LLM
    weather_prompt = "Your task is to provide info concisely based on the user query and the available information from the internet. Output a short sentence with only the city and temperature. Following is the user query: " + user_input + " Available information: " + available_info
    response = model.invoke(weather_prompt) # final response; could append to messages for consistency.
    return response.content

workflow = Graph()                      # instantiate Langchain graph
workflow.add_node('agent1', func1)       # create nodes
workflow.add_node('tool', func2)
workflow.add_node('responder', func3)
# -    -    -    -
workflow.add_edge('agent1', 'tool') # create edges
workflow.add_edge('tool', 'responder')
# -    -    -    -
workflow.set_entry_point('agent1')
workflow.set_finish_point('responder')
# -    -    -    -
app = workflow.compile()

inputs = {'messages': ['What is the temperature in Tampa?']}
# print(app.invoke(inputs))
input = {"messages": ["what is the temperature in las vegas"]}
for output in app.stream(input):
    # stream() yields dictionaries with output keyed by node name
    for key, value in output.items():
        print(f"Output from node '{key}': {value}")
        # print("---")
        # print(value)
    print("---")