from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from src.models import llm
from enum import Enum

class PriorityEnum(str, Enum):
    high = "High"
    medium = "Medium"
    low = "Low"

class RaiseQuery(BaseModel):
   reply : str = Field(description="The reply to the user query in the same language as that of user.")
   priority : PriorityEnum = Field(description="The priority of the user query based on tone, urgency, issue duration, and sentiment of conversation.")

raise_query_prompt_template = """
You are an expert who knows multiple languages and understands the user's sentiment easily. 
Your task is to identify the sentiment of the user query based on a conversation with Customer Support Team {conversation} and based on the tone, urgency, issue duration, and sentiment you have to set the priority of the user query
as High, Medium or Low.
For Example: 
If the user is very angry or frustated or the query seems to persist since many days the priority may be set as High.

You also have to identify the language of the conversation and translate "I have raised your query for further investigation. Our Customer Support Team will reach you soon." in the same language.
**IMPORTANT**
Translate the statement "I have raised your query for further investigation. Our Customer Support Team will reach you soon." in the **same language** as that of user (which may be English, Hindi, or any Indian regional language or maybe any Indian Language written in English For E.g. 'Merko paise nikalne hain' so this is Hindi words written in English so you also have to answer ask question in Hindi written in English).
{format_instructions}
"""

raise_query_json_parser = JsonOutputParser(pydantic_object=RaiseQuery)

raise_query_prompt = PromptTemplate(
    template=raise_query_prompt_template,
    input_variables=["conversation"],
    partial_variables={"format_instructions": raise_query_json_parser.get_format_instructions()},
)

raise_query_chain = raise_query_prompt | llm | raise_query_json_parser

def raise_user_query(state):
    print("raise_user_query")
    try:
        print('-'*120)
        query_description = state["query_description"]
        conversation = state["additional_info"]
        result = raise_query_chain.invoke({"conversation" : conversation})
        state["final_answer"] = result["reply"]
        print(result["priority"])
        print(query_description)
        print('-'*120)
        return state
    except Exception as e:
        print(f"Error in raise_user_query: {str(e)}")
        state["final_answer"] = "I have raised your query for further investigation. Our Customer Support Team will reach you soon."
        return state