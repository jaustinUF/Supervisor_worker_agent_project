# Supervisor agent/worker agent project #
(in progress 3/3/2025)

<i>Directories are discussed in chronological order of work; detailed notes are in README.md files in each directroy.</i>

### react_agents_chris_hay ###
- discusses and illustrates the thought, action, observation processing of the ReAct agent design
- use a simple get time tool
- shows what's going on 'under the hood'
- compares 
  - agent/worker structure built using the langchain.agents package (hello-agent-3.py) with
  - agent/worker process created in simple langchain (hello-langchain-6.py)

### build_react_agent_pavan_belagatti ###
- structured_chat_agent.py
  - simple agent using the langchain_community Tavily web search tool
  - uses ReAct prompt from the langchain hub
- reAct_AI_agent.py
  - more complicated agent, using two tools ('wikipedia', 'calculate')
  - Agent (instantiated from class 'Charbot') decides which tool to use
  - Agent uses Action step to pass tool name/tool input to script
  - Observation step allows agent to get tool results back

### agent_tests ###
- simple agent/tool tests in LangChain
- tavily_test.py: uses langchain_community tool to search the web
- wikipedia_test.py: uses custom tool to search Wikipedia
- pdf_query_test directory
  - pdf_query_agent_save_db.py: code for agent to quey PDF
  - pdf_query_agent_main.py: simple test for pdf_query_agent_save_db.py
  - Employee Handbook (Sears).pdf: PDF for testing; must be in 'data' subdirectory

### supervisor_worker_design_URLs ###
- examples_design_sources.md
  - sites that discuss the supervisor agent/worker agent design.
  - notes on specific implementations
- Supervisor-worker agent design.docx
- ChatGPT Deep Research paper
  
### LangGraph ###
- initial work in LangGraph
- seven scripts, from very simple to conditional edge and simplified state management
- more complex scripts deviated from tutorial: different tool (weather), discontinued prebuilts 



### pdf_deepseek_Rishab ###
- notes and comments on LangChain document load (PDF) tutorial
