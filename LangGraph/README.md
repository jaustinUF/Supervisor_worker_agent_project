Note:   simplest script at bottom (two_nodes_one_edge.py)
        progressively more complex from bottom up (to AgentState_design.py)

AgentState_design.py:
        - worked with ChatGPT to replace the prebuilts
                https://chatgpt.com/c/67d634c9-bfd8-800c-a4dd-1904b0dcebd6
        - handles user inputs with no city name.
        - can bind tools to model, but method in tutorial is being depreciated.
        - note: new binding syntax (model.bind_tools(tools)) requires the code to run the tool
                https://chatgpt.com/c/67d634c9-bfd8-800c-a4dd-1904b0dcebd6
(see diagram: C:\Users\jaust\Desktop\langchain_work\LangGraph\diagrams_images\conditional_edge_design.JPG)
AgentState_design_tutorial.py(18:34):
        - conditional edge to handle no city name in user input
        - shortcut (17:13): 'typing' and other pakages facilitate appending to 'messages' 
        - uses two langgraph prebuilts that have been replaced

state_design.py (12:30): see diagram state_design.JPG
        - AgentState dictionary illustrate the state structure; not used in script
        - state structure is set by the structure of the 'input' variable from 'entry_point'
        - see end of 'LangGraph Workflow Explanation' https://chatgpt.com/c/67d0afbe-1bb4-800c-b053-144163a536aa
        - node cycle (14:16): get last message in 'messages' list, pass it to agent/tool, append reposnse to 'messages'
Note: code above uses state, much more widely useful (11:35)

Note: below deals with city/temp issue in one way, possible because 
        the weather string contains both city name and temp
1st_agent_tool_weather.py:
        - 'agent1' calls LLM to parse city from user input
        - 'tool' returns weather string.
        - 'agent2' calls LLM to use city and temp from weather string to respond.

1st_agent_tool_temp.py (7:40):
        - 'agent' calls LLM to parse city from user input
        - 'tool' returns only the temp for this city.
        _ 'return' builds response from city and temp
Note: Weather tool in above scripts different from tutorial
Weather tool dev: https://chatgpt.com/c/67d335e7-bd8c-800c-8a09-9a7320e669de

add_LLM_call.py (4:27): first node (agent > func1) makes LLM call
        - other changes minor: node names, strings, etc.

two_nodes_one_edge.py (two_nodes_one_edge.JPG) (1:10):
(see diagrams in 'diagrams_images')
'Learn LangGraph - The Easy Way' https://www.youtube.com/watch?v=R8KB-Zcynxc
Colab = https://colab.research.google.com/drive/1E98lHu3QhyBZcmRL40nxtKN0SmT1QA2U#scrollTo=8tDqN1y7dLhl
Medium  https://anilktalla.medium.com/understanding-langgraph-note-1-83554ff5d50a
        https://anilktalla.medium.com/understanding-langgraph-note-2-e2efd24b40f3
Note: Tutorial is not perfect, but discussion of complex process in conditional edge section (AgentState_design) (starting 19:00) is useful

