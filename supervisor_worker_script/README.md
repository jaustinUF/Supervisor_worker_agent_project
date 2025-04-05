## Supervisor/worker agent pattern script ##
supervisor_worker_3.py: supervisor selects agents (all working)  
- test with appropriate 'content' in 'input_data'
- use 'prnt_msg(response['messages'])' to see steps in 'messages'
  - shows which agent was selected by supervisor (usually Step 3.)

Simple test scripts for each agent in agent_test directory  
    - wikipedia_test.py: working  
    - tavily_test.py: working  
    - pdf_query_test.py: working

Based on Quickstart example from https://github.com/langchain-ai/langgraph-supervisor-py



