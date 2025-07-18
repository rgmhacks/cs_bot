import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv(override=True)

llm = ChatOpenAI(
            model="gpt-4o",
            api_key=SecretStr(os.getenv("OPENAI_API_KEY") or "")
        )
        
embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=SecretStr(os.getenv("GOOGLE_API_KEY") or "")
        )
        
vector_store = PineconeVectorStore(
            index_name=os.getenv("PINECONE_INDEX_NAME"),
            embedding=embeddings,
            pinecone_api_key=os.getenv("PINECONE_API_KEY")
        )