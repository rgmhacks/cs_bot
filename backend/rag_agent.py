# backend/rag_agent.py

import os
from dotenv import load_dotenv
from langgraph.graph import START, StateGraph
from langchain_core.prompts import PromptTemplate
from typing_extensions import List, TypedDict
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import SecretStr, BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langgraph.checkpoint.mongodb import MongoDBSaver
from langmem.short_term import SummarizationNode, RunningSummary
from langchain_core.messages.utils import count_tokens_approximately

load_dotenv(override=True)

# Define schema for search
class Search(BaseModel):
    """Refined English search query for vector DB retrieval."""
    query: str = Field(..., description="Refined English version of the user's question for retrieval purposes.")

# Define state for application
class State(TypedDict):
    question: str
    query: Search
    context: List[Document]
    answer: str
    prev: dict[str, RunningSummary]

class RAGAgent:
    def __init__(self, memory):
        # Initialize OpenAI components
        self.llm = ChatOpenAI(
            model="gpt-4o",
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
        self.GENERATOR_PROMPT_TEMPLATE = """You are Dream11’s official customer support assistant.

            You assist users by answering queries related to Dream11's fantasy sports platform such as deposits, account verification, contest rules, point system, withdrawals, and other gameplay-related questions.

            Use only the provided context to answer the user's question. If the context does not contain enough information, respond with:
            "I'm not sure about that. Let me connect you to a human support agent for further assistance."

            Be clear, concise, friendly, and professional in your tone. Avoid making up any information that is not in the context.

            **IMPORTANT**
            Answer the question in the **same language** as the user's question (which may be English, Hindi, or any Indian regional language).

            {context}

            Question: {question}

            Helpful Answer: ** Remember to answer in structured format using bullet points"""
        
        self.GENERATOR_PROMPT = PromptTemplate.from_template(self.GENERATOR_PROMPT_TEMPLATE)

        self.summarization_node = SummarizationNode(
            token_counter=count_tokens_approximately,
            model=self.llm,
            max_tokens=384,
            max_summary_tokens=128,
            output_messages_key="llm_input_messages",
        )
        self.graph_builder = StateGraph(State,pre_model_hook=self.summarization_node).add_sequence([self.refine_query, self.retrieve, self.generate])
        self.graph_builder.add_edge(START, "refine_query")
        self.graph = self.graph_builder.compile(checkpointer=memory)

    def refine_query(self, state: State):
        """Refines the user question into a precise English search query for vector retrieval."""
        structured_llm = PromptTemplate.from_template(
        """You are an assistant helping to improve search accuracy in a vector-based knowledge system.

        The user may have asked the question in a regional language or informal tone.

        Rephrase and translate their question into a clear, concise English search query that best represents their intent.

        Original Question:
        {question}

        Refined English Search Query:"""
        ) | self.llm.with_structured_output(Search)

        query = structured_llm.invoke({"question": state["question"]})
        return {"query": query}
    
    def retrieve(self, state: State):
        query = state["query"]
        retrieved_docs = self.vector_store.similarity_search(
            query.query
        )
        return {"context": retrieved_docs}
    
    def generate(self, state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = self.GENERATOR_PROMPT.invoke({"question": state["question"], "context": docs_content})
        response = self.llm.invoke(messages)
        return {"answer": response.content}

    
    def get_response(self, user_query: str, user_id: str) -> str:
        """Get RAG-based response"""
        # with MongoDBSaver.from_conn_string(os.getenv("DB_URI")) as checkpointer:
        config = {"configurable": {"thread_id": user_id}}
        result = self.graph.invoke({"question": user_query}, config=config)
        return str(result["answer"]) 