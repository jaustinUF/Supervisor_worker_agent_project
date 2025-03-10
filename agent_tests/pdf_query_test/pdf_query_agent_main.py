# pdf_query_agent_save_db.py: saves vectorstores so don't need to reprocess
# pdf_query_agent.py: does not save vectorstores directory
#   see https://chatgpt.com/c/67cc9148-af3c-800c-a81e-64f7227ae221
# same ChatGPT session discusses various ways of importing agent.

from pdf_query_agent_save_db import pdf_query_agent

pdfs_directory = 'data/'
file_name = 'Employee Handbook (Sears).pdf'

response = pdf_query_agent(pdfs_directory + file_name, 'What is the employee pay rate on weekends?')
# response = pdf_query_agent(pdfs_directory + file_name, 'What is the employee pay rate on holidays?')
print(response)
