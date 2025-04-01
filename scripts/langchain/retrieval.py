from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
import sys
import os
import json

OPENAI_API_KEY = sys.argv[1]
PINECONE_API_KEY = sys.argv[2]
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY

if __name__ == "__main__":
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

    query = "What is the difference between a vector database and a traditional database?"
    chain = PromptTemplate.from_template(template=query) | llm
    result = chain.invoke(input={})
    vectorstore = PineconeVectorStore(index_name="index-1", embedding=embeddings)
    role_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=role_prompt)
    retrieval_chain = create_retrieval_chain(retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain)
    result = retrieval_chain.invoke(input={"input": query})
    print(result['answer'])