import streamlit as st
import main_jja as main

st.title("Chat with PDFs with Deepseek")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf",
    accept_multiple_files=False
)

if uploaded_file:
    main.upload_pdf(uploaded_file)
    db = main.create_vector_store(main.pdfs_directory + uploaded_file.name)
    question = st.chat_input('How can I help you?')

    if question:
        st.chat_message("user").write(question)
        related_documents = main.retrieve_docs(db, question)
        answer = main.question_pdf(question, related_documents)
        st.chat_message("assistant").write(answer)
        # Test retrieval of docs
        # st.text(main.retrieve_docs(db=db, query="NVIDIA STOCK"))

# in C:\Users\jaust\Desktop\langchain_work\document_load\pdf_deepseek_tutorial>,
#   cd document_load\pdf_deepseek_tutorial
#   streamlit run streamlit_UI.py
# opens on localhost 8501