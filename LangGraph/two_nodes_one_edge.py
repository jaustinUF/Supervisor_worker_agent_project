# graph with two nodes connected by one edge.
# Nodes act like functions that can be called as needed.
#   Node 1 is starting point,Node 2 is finish point.
from langgraph.graph import Graph

def func1(in1):
    return in1 + 'Hi'
def func2(in2):
    return in2 + 'there'

workflow = Graph()                      # instantiate Langchain graph
workflow.add_node('node1', func1)       # create nodes
workflow.add_node('node2', func2)

workflow.add_edge('node1', 'node2') # create edge
workflow.set_entry_point('node1')
workflow.set_finish_point('node2')

app = workflow.compile()
print(app.invoke('Hello'))
print("---")
inpt = 'Hello'
for output in app.stream(inpt):
    print(output.items())
