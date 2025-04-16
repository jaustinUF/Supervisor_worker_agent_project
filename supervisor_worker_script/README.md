## Supervisor/worker agent pattern scripts ##
The 'supervisor_worker_3.py' script uses the supervisor/worker agent pattern (see link below). It accepts a question or request for information, then selects the appropriate worker agent to respond. The supervisor agent has three agents to choose from:  
- a query agent that searches for information in an employee handbook in a PDF; the PDF is in the data directory.
- an agent to search Wikipedia.
- an agent that can search the web.

The 'supervisor_worker_4.py' script is similar, but with a predictive agent replacing the web search agent. The predictive agent uses a pretrained ML model (iris_model.pkl) to predict Iris flower species from four measurements.

Test with appropriate 'content' in 'input_data'; use 'prnt_msg(response['messages'])' to see steps in 'messages.'  

Notes
- for simplicity the PDF query agent keeps the FAISS vector store in memory.
- pdf_query_agent_test.py is a simple example of saving vector store to disk to save reprocessing time.
- simple test scripts for each agent are in the agent_test directory: wikipedia_test.py, tavily_test.py, pdf_query_test.py.
- developed in PyCharm project 'langchain_work':  supervisor_worker_dev directory.
- based on Quickstart example from https://github.com/langchain-ai/langgraph-supervisor-py



