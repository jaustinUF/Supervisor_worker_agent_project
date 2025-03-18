# make LLM call in agent
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph
from dotenv import load_dotenv
load_dotenv()       # load environmental variables

model = ChatOpenAI(temperature = 0.7)
# print(model.invoke('Hi Assistant').content) # quick check of connection

def func1(in1):
    response = model.invoke(in1).content
    return response
def func2(in2):
    return 'Assistant says: ' + in2

workflow = Graph()                      # instantiate Langchain graph
workflow.add_node('agent', func1)       # create nodes
workflow.add_node('node2', func2)

workflow.add_edge('agent', 'node2') # create edge
workflow.set_entry_point('agent')
workflow.set_finish_point('node2')

app = workflow.compile()
print(app.invoke('Hi Assistant'))