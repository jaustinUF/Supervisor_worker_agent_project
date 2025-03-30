# 'agent' prompts LLM to parse user request for city name.
#   tool gets city name and returns temperature
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
            return weather.temperature
    temperature = asyncio.run(fetch_weather())
    return f'Assistant says the temperature in {in2} is {temperature}\u00b0 F'

workflow = Graph()                      # instantiate Langchain graph
workflow.add_node('agent', func1)       # create nodes
workflow.add_node('tool', func2)

workflow.add_edge('agent', 'tool') # create edge
workflow.set_entry_point('agent')
workflow.set_finish_point('tool')

app = workflow.compile()
print(app.invoke('What is the temperature in Miami?'))
