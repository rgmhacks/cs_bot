from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing_extensions import List, TypedDict
from pydantic import  BaseModel, Field
from langchain_core.documents import Document
from langmem.short_term import RunningSummary
from src.side_nodes import *
from src.answer_query import answer_query
from src.describe_query import describe_query
from src.followup_question import ask_for_more_info_chain
from src.refine_query import refine_query
from src.relevant_content import keep_only_relevant_content
from src.conditional_edges import is_info_enough, is_relevant_content_present


class Query(BaseModel):
    """Refined English search query for vector DB retrieval."""
    query: str = Field(description="Refined English version of the user's question for retrieval purposes.")

class State(TypedDict):
    question: str
    additional_info: str | None
    query: Query
    followup_question: str | None
    context: List[Document]
    final_answer: str
    query_description: str
    is_relevant_content_present: bool
    prev: dict[str, RunningSummary]

class RAGAgent:
    def __init__(self, memory):
        self.memory = memory
        self.graph = self.workflow()

    def workflow(self):
        graph = StateGraph(State,pre_model_hook=summarization_node())
        graph.add_node("answer_query", answer_query)
        graph.add_node("followup_question", ask_for_more_info_chain)
        graph.add_node("get_human_reply", get_human_reply)
        graph.add_node("refine_query", refine_query)
        graph.add_node("retrieve", retrieve)
        graph.add_node("retrieve_relevant_content", keep_only_relevant_content)
        graph.add_node("describe_query", describe_query)
        graph.add_node("raise_query", raise_user_query)

        graph.add_conditional_edges(START,is_info_enough,{"enough":"describe_query","not_enough":"followup_question"})
        graph.add_edge("followup_question","get_human_reply")
        graph.add_conditional_edges("get_human_reply",is_info_enough,{"enough":"describe_query","not_enough":"followup_question"})
        graph.add_edge("describe_query","refine_query")
        graph.add_edge("refine_query","retrieve")
        graph.add_edge("retrieve","retrieve_relevant_content")
        graph.add_conditional_edges("retrieve_relevant_content", is_relevant_content_present, {"relevant_content_present":"answer_query","no_relevant_content":"raise_query"})
        graph.add_edge("raise_query",END)
        graph.add_edge("answer_query",END)

        return graph.compile(checkpointer=self.memory)
    
    def get_response(self, user_query: str, user_id: str):
        """Get RAG-based response"""
        config = {"configurable": {"thread_id": user_id}}
        result = self.graph.invoke({"question": f"User : {user_query}"}, config=config)
        if "final_answer" in result:
            return {"reply" : result["final_answer"], "isCompleted" : True}
        else:
            return {"reply" : result["followup_question"], "isCompleted" : False}
    
    def resume_chat(self, human_response: str, user_id: str):
        config = {"configurable": {"thread_id": user_id}}
        result = self.graph.invoke(Command(resume=human_response),config)
        if "final_answer" in result:
            return {"reply" : result["final_answer"], "isCompleted" : True}
        else:
            return {"reply" : result["followup_question"], "isCompleted" : False}
