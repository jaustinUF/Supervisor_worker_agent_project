What agent is doing:
    An agent repeats a looping process (as prompted ... in this tutorial by the react prompt)
    - agent calls the first piece,
    - when agent sees 'Observation' (if ReAct prompt) it stops,
    - executes the next action,
    - concatenates the result of the action to the prompt ('message' - history),
    - put (enhanced longer history) prompt back through the llm,
    - continues loop until final answer.

Overall tutorial plan:
    - develops simple agentic script; in parallel develops non-agentic script to show how agent works with the llm
    - the 'hello-agent-x.py' thread develops an agent with a tool that gets the current time
    - the hello-langchain-x.py' thread illustrates what is happening 'under the hood'
hello-langchain-6.py: is for teaching, doesn't get the current time:
    prompt_template is modified as if the tool had run and injected the real time.
hello-langchain-5.py; add tool to 'hello-langchain-4.py'
    - this version does not actually run the tools, so values is bogus or hallucinated
hello-langchain-4.py: get time using standard model, no agent and no tool
hello-agent-3.py (13:00): mod of 'hello-agent-2'
    - gets 'prompt_template' locally from react_template.py, downloaded from hub

system_time_tool.py: script with time tool function 'check_system_time
    - needs '@tool' decorator from 'langchain.agents import tool'        
        "Make tools out of functions, can be used with or without arguments." (from hoover doco)
        (21:52) 'pass out in a nice formatted form ... '
hello-agent-2.py (13:00) :
    - copy of hello-agent-1.py but discussed in detail (18:00))
    - build tool: 'check_system_time' function in system_time_tool.py file 
        simple python formatted 'datetime'

hello-langchain-2.py (9:17): mod hello-langchain-1.py into prompt template format
hello-langchain-1.py (3:40): simple query in langchain

hello-agent-1.py (0:08): simple get-time agent in langchain
    - Reason and action loop: see output
    - thought, action, observation ... then think about observation and continuer looping until final answer.
    - discussed in detail in hello-agent-2.py (0:08):

(See overall tutorial plan at top)
"Getting Started with ReAct AI agents work using langchain"
https://www.youtube.com/watch?v=W7TZwB-KErw