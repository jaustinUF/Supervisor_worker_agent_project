# does not save vectorstores directory
# calls the pdf query agent function in 'pdf_query_agent' in df_query_agent_save_db.py
#   (see https://chatgpt.com/c/67cc9148-af3c-800c-a81e-64f7227ae221)

from pdf_query_agent_save_db import pdf_query_agent

pdfs_directory = 'data/'
file_name = 'Employee Handbook (Sears).pdf'

response = pdf_query_agent(pdfs_directory + file_name, 'What is the employee pay rate on weekends?')
# response = pdf_query_agent(pdfs_directory + file_name, 'What is the employee pay rate on holidays?')
print(response)
