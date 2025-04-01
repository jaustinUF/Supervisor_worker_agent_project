## agent_tests ##
pdf_query_test (directory)  
    - agent: pdf_query_agent function in pdf_query_agent_save_db.py  
    - pdf_query_agent_save_db.py: contains agent function and saves vectorstore  
    - pdf_query_agent_main.py: calls pdf_query_agent function from pdf_query_agent_save_db.py; does not save vectorstore  
    - PDF must be in ‘data’ subdirectory  
    
wikipedia_test.py : custom tool to search wikipedia

tavily_test.py: search the web 
    - probably needs some work on the prompt.
    (last script in 'Supervisor Worker AI System')

agent_test_template.py: " ... supervisor agent, powered by a Large Language Model (LLM), dynamically analyzes user inputs and delegates tasks to the most appropriate worker agents."

Major basis: ChatGPT 'Supervisor Worker AI System'
https://chatgpt.com/c/67aa66a6-bad4-800c-958d-355e3be646d4

