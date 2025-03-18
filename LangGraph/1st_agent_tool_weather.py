# 'agent1' prompts LLM to parse user request for city name.
#   tool returns weather
#   'agent2' parses city and temperature from weather string.
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph
import python_weather
import asyncio
from dotenv import load_dotenv
load_dotenv()       # load environmental variables

model = ChatOpenAI(temperature = 0.7)
# print(model.invoke('Hi Assistant').content) # quick check of connection

def func1(in1):
    get_city_prompt = "Your task is to provide only the city name based on the user query. \
            Nothing more, just the city name mentioned. Following is the user query: " + in1
    response = model.invoke(get_city_prompt)
    return response.content

def func2(in2):
    async def fetch_weather():
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get(in2)
            return weather # string: <Forecast location='Miami' datetime=datetime.datetime(2025, 3, 14, 11, 4) temperature=75>
    return asyncio.run(fetch_weather())

def func3(in3):
    weather_prompt = 'You job is to parse the following string for city and temperature. Respond by giving only the temperature in the indicated city.' + str(in3)
    response = model.invoke(weather_prompt)
    return response.content

workflow = Graph()                      # instantiate Langchain graph
workflow.add_node('agent1', func1)       # create nodes
workflow.add_node('tool', func2)
workflow.add_node('agent2', func3)

workflow.add_edge('agent1', 'tool') # create edges
workflow.add_edge('tool', 'agent2')

workflow.set_entry_point('agent1')
workflow.set_finish_point('agent2')

app = workflow.compile()
print(app.invoke('What is the temperature in Tampa?'))