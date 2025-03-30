# tutorial code out of date:
#   In langgraph.prebuilt, ToolInvocation, ToolExecutor replaced by ToolNode, ValidationNode respectively
# 'func2'extensively rewritten... see AgentState_design.py
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, FunctionMessage
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, ValidationNode
import json
import python_weather
import asyncio
from typing import TypedDict, Annotated, Sequence
import operator

from dotenv import load_dotenv
load_dotenv()       # load environmental variables

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

@tool
def getweather():
    async def fetch_weather():
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get('Miami')
            return weather.temperature
    return asyncio.run(fetch_weather())
tools = [getweather]

model = ChatOpenAI(temperature=0, streaming=True)
functions = [convert_to_openai_function(t) for t in tools]
model = model.bind_functions(functions)

def func1(state):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

# tool_executor = ToolExecutor(tools) # ValidationNode
tool_executor = ValidationNode(tools)

def func2(state):
    messages = state['messages']
    last_message = messages[-1]  # this has the query we need to send to the tool provided by the agent

    parsed_tool_input = json.loads(last_message.additional_kwargs["function_call"]["arguments"])

    # We construct an ToolInvocation from the function_call and pass in the tool name and the expected str input for OpenWeatherMap tool
    # action = ToolInvocation( # ToolNode
    action = ToolNode(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=parsed_tool_input['__arg1'],
    )

    # We call the tool_executor and get back a response
    response = tool_executor.invoke(action)

    # We use the response to create a FunctionMessage
    function_message = FunctionMessage(content=str(response), name=action.tool)

    # We return a list, because this will get added to the existing list
    return {"messages": [function_message]}

def where_to_go(state):
    messages = state['messages']
    last_message = messages[-1]
    if "function_call" in last_message.additional_kwargs:
        return "continue"
    else:
        return "end"
# -    -  instantiate graph  -    -
workflow = StateGraph(AgentState)
# -    -  create nodes  -    -
workflow.add_node('agent', func1)       # create nodes
workflow.add_node('tool', func2)
# -    -  create edges  -    -
workflow.add_conditional_edges('agent', where_to_go, {
    # Based on the return from where_to_go
    # If return is "continue" then we call the tool node.
    "continue": "tool",
    # Otherwise we finish. END is a special node marking that the graph should finish.
    "end": END
})
workflow.add_edge('tool', 'agent')
# -    -    -    -
workflow.set_entry_point('agent')
# -    -  compile and run  -    -
app = workflow.compile()
from langchain_core.messages import HumanMessage

inputs = {"messages": [HumanMessage(content="what is the temperature in las vegas")]}
print(app.invoke(inputs))
input = {"messages": ["what is the temperature in las vegas"]}
# for output in app.stream(input):
#     # stream() yields dictionaries with output keyed by node name
#     for key, value in output.items():
#         print(f"Output from node '{key}': {value}")
#         # print("---")
#         # print(value)
#     print("---")
