# In langgraph.prebuilt, ToolInvocation, ToolExecutor replaced by ToolNode, ValidationNode respectively
#   'func2'extensively rewritten, as ia the response output syntax
#           https://chatgpt.com/c/67d634c9-bfd8-800c-a4dd-1904b0dcebd6
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, FunctionMessage, AIMessage, HumanMessage
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
    """Retrieve weather information for a given location."""
    async def fetch_weather():
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get('Miami')
            return weather.temperature
    return asyncio.run(fetch_weather())

tools = [getweather]

model = ChatOpenAI(temperature=0, streaming=True)
functions = [convert_to_openai_function(t) for t in tools]
model = model.bind_functions(functions) # bind tools directly to model but being depreciated.
# model = model.bind_tools(tools) # bind tools directly to model, but requires more code to execute tool.

def func1(state):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

# tool_executor = ToolExecutor(tools) # ValidationNode
tool_executor = ValidationNode(tools)
tool_node = ToolNode(tools)

def func2(state):
    messages = state['messages']
    last_message = messages[-1]

    # Check if the last message contains a function (tool) call
    if "function_call" in last_message.additional_kwargs:
        function_call = last_message.additional_kwargs["function_call"]
        tool_name = function_call["name"]
        tool_args = json.loads(function_call["arguments"])

        # Create a tool call structure
        tool_call = {
            "name": tool_name,
            "args": tool_args,
            "id": "tool_call_id",
            "type": "tool_call",
        }

        # Create an AIMessage with the tool call
        ai_message = AIMessage(content="", tool_calls=[tool_call])

        # Invoke the tool using ToolNode
        tool_response = tool_node.invoke({"messages": [ai_message]})

        # Extract the tool's response message
        tool_message = tool_response["messages"][-1]

        # Create a FunctionMessage with the tool's response
        function_message = FunctionMessage(content=tool_message.content, name=tool_name)

        # Return the updated state with the new message
        return {"messages": messages + [function_message]}

    # If no function_call is present, return the state unchanged
    return {"messages": messages}

def where_to_go(state):
    messages = state['messages']
    last_message = messages[-1]
    if "function_call" in last_message.additional_kwargs:
        return "continue"
    else:
        return "end"
# -    -  instantiate graph  -    -
workflow = StateGraph(AgentState)       # allows us to define the state structure
# -    -  create nodes  -    -
workflow.add_node('agent', func1)       # create nodes
workflow.add_node('tool', func2)
# -    -  create edges  -    -
workflow.add_conditional_edges('agent', where_to_go, { # to tool or end (back to user)
    # Based on the return from where_to_go
    # If return is "continue" then we call the tool node.
    "continue": "tool",
    # Otherwise we finish. END is a special node marking that the graph should finish.
    "end": END
})
workflow.add_edge('tool', 'agent')      # allow tool response to get back to agent (see diagram)
# -    -    -    -
workflow.set_entry_point('agent')
# -    -  compile and run  -    -
app = workflow.compile()

inputs = {"messages": [HumanMessage(content="what is the temperature in Tampa")]}
# inputs = {"messages": [HumanMessage(content="what is your name")]}
result = app.invoke(inputs)
# print(result)
last_ai_message = next((m.content for m in reversed(result["messages"]) if isinstance(m, AIMessage)), "No AI response found")
print(last_ai_message)

''' # more detailed method of getting the final LLM output from the complex state 'messages'
messages = result['messages']
# Find the assistant's final response
assistant_response = None
for message in reversed(messages):
    if isinstance(message, AIMessage):
        assistant_response = message.content
        break

# Display the assistant's response
if assistant_response:
    print(f"Assistant: {assistant_response}")
else:
    print("No assistant response found.")
'''

