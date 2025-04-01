import streamlit as st
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_models import ChatOpenAI
from langchain import hub
import sys

OPENAI_API_KEY = sys.argv[1]

# Upload PDF files
st.header("My first Chatbot")

with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader("Upload a PDf file and start asking questions", type="pdf")

# Extract the text
if file is not None:
    pdf_reader = PdfReader(file)
    loader = PyPDFLoader(file.name) # ***
    documents = loader.load() # ***
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10, separator="\n") # ***
    docs = text_splitter.split_documents(documents) # ***


    print(file.name)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        #st.write(text)

# Break it into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    #st.write(chunks)

    # Generating embedding
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Creating vector store - FAISS
    vector_store = FAISS.from_texts(chunks, embeddings)
    vector_Store_new = FAISS.from_documents(docs, embeddings) # ***
    vector_Store_new.save_local("faiss_index_new") # ***
    new_vector_store = FAISS.load_local("faiss_index_new", embeddings, allow_dangerous_deserialization=True) # ***
    role_prompt = hub.pull("langchain-ai/retrieval-qa-chat") # ***
    combine_docs_chain = create_stuff_documents_chain(OpenAI(api_key=OPENAI_API_KEY), prompt=role_prompt) # ***
    retrieval_chain = create_retrieval_chain(retriever=new_vector_store.as_retriever(), combine_docs_chain=combine_docs_chain) # ***
    result = retrieval_chain.invoke(input={"input": "What is phone number of Santosh Pawar?"}) # ***
    print(result['answer']) # ***

    # Get user question
    user_question = st.text_input("Type Your question here")

    # Do similarity search
    if user_question:
        match = vector_store.similarity_search(user_question)
        #st.write(match)

        # Define the LLM
        llm = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY,
            temperature = 0,
            max_tokens = 1000,
            model_name = "gpt-3.5-turbo"
        )

        #output results
        #chain -> take the question, get relevant document, pass it to the LLM, generate the output
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents = match, question = user_question)
        st.write(response)