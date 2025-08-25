


The Supervisor Pattern for Gen AI Agent Systems - Vipin Nair  
https://medium.com/aitech/the-supervisor-pattern-for-gen-ai-agent-systems-d1920c0bdbbb  
Code: https://github.com/vipinn123/Supervisor_Agentic_Pattern
- this paper uses LangGraph with nodes and edges to represent the workflow
  - "The add_conditional_edges method is used to define transitions from the
  "Supervisor" node based on the output of the router function. The router
  function analyzes the most recent message from the Supervisor and decides
  which agent should be activated next."
- the agents write and check code to solve the (mathematical) problem

Hierarchical AI Agents: Create a Supervisor AI Agent Using LangChain - Vijaykumar Kartha
https://www.linkedin.com/pulse/hierarchical-ai-agents-create-supervisor-agent-vijaykumar-kartha-ikibc/
(see 'Previous Articles' at end of article)
- uses LangGraph: from langgraph.graph import StateGraph, END

CopilotKit / open-multi-agent-canvas (Georgios 2/22/2025)
https://github.com/CopilotKit/open-multi-agent-canvas
- "... built with Next.js, LangGraph, and CopilotKit"

Supervisor Worker in LangChain
https://chatgpt.com/c/67be15c4-3e6c-800c-a274-4bfa0293cb66
- dummy 'choose_worker' function
- has some thoughts on model returning worker choice with a stuctured (JSON) string.
