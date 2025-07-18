from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from src.models import llm

class QueryDescription(BaseModel):
    query_description: str = Field(description="The description of the query based on the user's answer over the entire conversation.")

describe_query_prompt_template = """
You are an expert Customer Support Assistant who understands the user query very easily.
You will receive the Conversation between the user and Customer Support Team which maybe in English, Hindi or any other Indian Language.
Your task is to extract all the details about the user query from the Conversation : {conversation} and describe it in a structured way which is easy to understand the overall query.
Remember to extract all the details from the Conversation only. Do not add any information on your own.
**IMPORTANT**
Describe the query in the **same language** as that of user (which may be English, Hindi, or any Indian regional language or maybe any Indian Language written in English For E.g. 'Merko paise nikalne hain' so this is Hindi words written in English so you also have to answer ask question in Hindi written in English).
{format_instructions}
"""

describe_query_json_parser = JsonOutputParser(pydantic_object=QueryDescription)

describe_query_prompt = PromptTemplate(
    template=describe_query_prompt_template,
    input_variables=["conversation"],
    partial_variables={"format_instructions": describe_query_json_parser.get_format_instructions()},
)

describe_query_chain = describe_query_prompt | llm | describe_query_json_parser

def describe_query(state):
    question = state["question"]
    additional_info = state.get("additional_info", "")
    input_data = {"conversation": question + " " + additional_info}
    query_description = describe_query_chain.invoke(input_data)
    state["query_description"] = query_description["query_description"]
    return state