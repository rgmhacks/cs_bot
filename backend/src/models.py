import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv(override=True)

try:
    llm = ChatOpenAI(
                model="o4-mini",
                api_key=SecretStr(os.getenv("OPENAI_API_KEY") or "")
            )
except Exception as e:
    print(f"Error initializing OpenAI LLM: {str(e)}")
    llm = None
        
try:
    embeddings = GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004",
                google_api_key=SecretStr(os.getenv("GOOGLE_API_KEY") or "")
            )
except Exception as e:
    print(f"Error initializing Google embeddings: {str(e)}")
    embeddings = None
        
try:
    vector_store = PineconeVectorStore(
                index_name=os.getenv("PINECONE_INDEX_NAME"),
                embedding=embeddings,
                pinecone_api_key=os.getenv("PINECONE_API_KEY")
            )
except Exception as e:
    print(f"Error initializing Pinecone vector store: {str(e)}")
    vector_store = None