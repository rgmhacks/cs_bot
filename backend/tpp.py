from langchain.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate([
    ("system", """You are Dream11’s official customer support assistant.

You assist users by answering queries related to Dream11's fantasy sports platform such as deposits, account verification, contest rules, point system, withdrawals, and other gameplay-related questions.

Use only the provided context to answer the user's question. If the context does not contain enough information, respond with:
"I'm not sure about that. Let me connect you to a human support agent for further assistance."

Be clear, concise, friendly, and professional in your tone. Avoid making up any information that is not in the context."""),
    ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
])

prompt_value = template.invoke(
    {
        "context": "Bob",
        "question": "What is your name?"
    }
)

print(prompt_value)


# backend/rag_agent.py

import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv(override=True)

class RAGAgent:
    def __init__(self):
        # Initialize OpenAI components
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.4,
            api_key=SecretStr(os.getenv("OPENAI_API_KEY") or "")
        )
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=SecretStr(os.getenv("GOOGLE_API_KEY") or "")
        )
        
        # Initialize Pinecone vector store
        self.vector_store = PineconeVectorStore(
            index_name=os.getenv("PINECONE_INDEX_NAME"),
            embedding=self.embeddings,
            pinecone_api_key=os.getenv("PINECONE_API_KEY")
        )
        
        # Create RAG prompt template
        self.prompt_template = ChatPromptTemplate([
    ("system", """You are Dream11’s official customer support assistant.

You assist users by answering queries related to Dream11's fantasy sports platform such as deposits, account verification, contest rules, point system, withdrawals, and other gameplay-related questions.

Use only the provided context to answer the user's question. If the context does not contain enough information, respond with:
"I'm not sure about that. Let me connect you to a human support agent for further assistance."

Be clear, concise, friendly, and professional in your tone. Avoid making up any information that is not in the context."""),
    ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
])

    
    def retrieve_relevant_docs(self, query: str, k: int = 4) -> List[Document]:
        """Retrieve relevant documents from Pinecone"""
        return self.vector_store.similarity_search(query, k=k)
    
    def format_context(self, documents: List[Document]) -> str:
        """Format retrieved documents into context string"""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"Document {i}:\n{doc.page_content}")
        return "\n\n".join(context_parts)
    
    def get_response(self, user_query: str) -> str:
        """Get RAG-based response"""
        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_docs(user_query)
        
        # Format context
        context = self.format_context(relevant_docs)
        # Generate response using LLM
        prompt = self.prompt_template.invoke({
            "context": context,
            "question": user_query
        })
        print(prompt)
        response = self.llm.invoke(prompt)
        return str(response.content) 