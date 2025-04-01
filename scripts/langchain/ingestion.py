import os 
import sys
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

OPENAI_API_KEY = sys.argv[1]
PINECONE_API_KEY = sys.argv[2]
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY

if __name__ == "__main__":
    print("Reading doc")
    loader = TextLoader("myblog.txt")
    documents = loader.load()
    print("Splitting")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    texts = text_splitter.split_documents(documents)
    print(f"Created {len(texts)} chunks")
    print("Creating embeddings")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    print("Ingesting into Pinecone")
    PineconeVectorStore.from_documents(texts, embeddings, index_name="index-1")