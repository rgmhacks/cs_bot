from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from src.models import llm

class Question(BaseModel):
  question : str = Field(description="The question which will be asked to user to get more information about the user query.")

ask_question_prompt_template = """
You are Cricbuzz11's official customer support assistant.
You assist users by answering queries related to Cricbuzz11's fantasy sports platform such as deposits, account verification, contest rules, point system, withdrawals, and other gameplay-related questions.
You receive the information about the user's query {query} in the form of conversation with Customer Support Agent which is not enough to answer the query.
Your task is to act as a professional Customer Support Assistant and ask a relevant question to the user to get more information about the user query.
**IMPORTANT**
Ask the question in the **same language** as that of user (which may be English, Hindi, or any Indian regional language or maybe any Indian Language written in English For E.g. 'Merko paise nikalne hain' so this is Hindi words written in English so you also have to answer ask question in Hindi written in English).
{format_instructions}
"""

ask_question_json_parser = JsonOutputParser(pydantic_object=Question)


# Create the prompt object for the LLM
ask_question_content_prompt = PromptTemplate(
    template=ask_question_prompt_template,
    input_variables=["query"],
    partial_variables={"format_instructions": ask_question_json_parser.get_format_instructions()},
)

# Combine prompt, LLM, and parser into a chain
ask_question_content_chain = ask_question_content_prompt | llm | ask_question_json_parser

def ask_for_more_info_chain(state):
    print("ask_for_more_info_chain")
    try:
        question = state["question"]
        if state.get("additional_info") is None:
            state["additional_info"] = ""
        if question not in state["additional_info"]:
            state["additional_info"] += question
        additional_info = state.get("additional_info", "")
        input_data = {"query": additional_info}
        followup_question = ask_question_content_chain.invoke(input_data)
        state["followup_question"] = followup_question["question"]
        # Append the helper's question to additional_info for context
        state["additional_info"] += f' Customer Support Team : {state["followup_question"]} \n'
        return state
    except Exception as e:
        print(f"Error in ask_for_more_info_chain: {str(e)}")
        state["followup_question"] = "I'm sorry, I encountered an error. Could you please provide more details about your query?"
        if state.get("additional_info") is None:
            state["additional_info"] = ""
        state["additional_info"] += f' Customer Support Team : {state["followup_question"]} \n'
        return state