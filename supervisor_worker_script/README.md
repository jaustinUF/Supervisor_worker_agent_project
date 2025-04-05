## Supervisor/worker agent pattern script ##
supervisor_worker_3.py: supervisor selects agents (all working)
    - test with appropriate 'content' in 'input_data'
    - use 'prnt_msg(response['messages'])' to see steps in 'messages'
        - shows which agent was selected by supervisor (usually Step 3.)

Simple test scripts for each agent in test directory 
    - wikipedia_test.py: working
    - tavily_test.py: working
    - pdf_query_test.py: working

supervisor_worker_2.py: uses 'refactored agents'
    - runs, but returns errors or can't find agent
    - suspect output of 'create_react_agent' needs to be cleaned up

supervisor_worker_1.py: superseded by langgraph-supervisor example syntax
    - uses 'create_react_agent' to create agents for 'create_supervisor'
agents
- agents refactored to langgraph-supervisor pattern
- current agents from chatGPT 'create agents ... list subfolders/files'
  - (https://chatgpt.com/c/67ec0dd9-f528-800c-985a-532c0f8e3283)
- original source
    - document_load > pdf_query_agent.py
        - loads pdf from 'data/'
        - saves 'vectorstores' directory in 'data/' in 
    - agent_tests > wikipedia > wikipedia_agent.py
    - agent_tests > tavily > tavily_agent.py

Quickstart_example.py
Examples: https://github.com/langchain-ai/langgraph-supervisor-py
    - same Quickstart script used in Hierarchical multi-agent > Example_from_Coding_Crash_Courses.py



