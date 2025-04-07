## Supervisor/worker agent pattern script ##
The 'supervisor_worker_3.py' script uses the supervisor/worker agent pattern (see link below). It accepts a question or request for information, then selects the appropriate worker agent to respond. The supervisor agent has three agents to choose from:  
- a query agent that searches for information in an employee handbook in a PDF; the PDF is in the data directory.
- an agent to search Wikipedia.
- an agent that can search the web.

Test with appropriate 'content' in 'input_data'; use 'prnt_msg(response['messages'])' to see steps in 'messages.'  

Simple test scripts for each agent are in the agent_test directory  
  - wikipedia_test.py: working  
  - tavily_test.py: working  
  - pdf_query_test.py: working

Development code in PyCharm project 'langchain_work':  supervisor_worker_dev directory  
Based on Quickstart example from https://github.com/langchain-ai/langgraph-supervisor-py



