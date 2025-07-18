from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from src.models import llm


class Query(BaseModel):
    """Refined English search query for vector DB retrieval."""
    query: str = Field(description="Refined English version of the user's question for retrieval purposes.")

refine_query_prompt_template = """
You are an assistant helping to improve search accuracy in a vector-based knowledge system.
You will receive the complete description of the user's query.
The user may have asked the question in a regional language or informal tone.
Use the relevant parts from the Description and Rephrase and translate their question into a clear, concise English search query that best represents their intent.
Description : {question}

Refined English Search Query:
{format_instructions}
"""

refine_query_json_parser = JsonOutputParser(pydantic_object=Query)

refine_query_prompt = PromptTemplate(
    template=refine_query_prompt_template,
    input_variables=["question"],
    partial_variables={"format_instructions": refine_query_json_parser.get_format_instructions()},
)

refine_query_chain = refine_query_prompt | llm | refine_query_json_parser

def refine_query(state):
    query = refine_query_chain.invoke({"question": state["query_description"]})
    state["query"] = query["query"]
    return state