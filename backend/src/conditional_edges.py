from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from src.models import llm

class Enough(BaseModel):
    is_enough: bool = Field(description="Whether the information provided by user is enough to answer the user's query")


is_enough_content_prompt_template = """
You are Dream11's official customer support assistant.
You assist users by answering queries related to Dream11's fantasy sports platform such as deposits, account verification, contest rules, point system, withdrawals, and other gameplay-related questions.
You receive the information about the user's query {query} in the form of conversation with helper which maybe in English, Hindi or any other Indian Language.
Your Task :
You have to check whether the information provided by user is enough to answer the query. If the number of (User, Customer Support Team) conversation pairs is more than 5, then return "enough" even if it is not enough.
{format_instructions}
"""

is_enough_json_parser = JsonOutputParser(pydantic_object=Enough)


# Create the prompt object for the LLM
is_enough_content_prompt = PromptTemplate(
    template=is_enough_content_prompt_template,
    input_variables=["query"],
    partial_variables={"format_instructions": is_enough_json_parser.get_format_instructions()},
)

# Combine prompt, LLM, and parser into a chain
is_enough_content_chain = is_enough_content_prompt | llm | is_enough_json_parser


def is_info_enough(state):
    print("is_info_enough")
    """
    Determines if the information is enough to answer the query.

    Args:
        state (dict): A dictionary containing:
            - "query": The query question.

    Returns:
        str: "enough" if the context is enough, "not enough" otherwise.
    """
    try:
        question = state["question"]
        additional_info = state.get("additional_info", "")

        # Prepare the input data for the LLM chain
        input_data = {"query": question + " " + additional_info}

        # Invoke the LLM chain to determine if the info is enough
        output = is_enough_content_chain.invoke(input_data)
        if output["is_enough"]:
            return "enough"
        else:
            return "not_enough"
    except Exception as e:
        print(f"Error in is_info_enough: {str(e)}")
        return "not_enough"
    
def is_relevant_content_present(state):
    try:
        if state["is_relevant_content_present"]:
            return "relevant_content_present"
        else:
            return "no_relevant_content"
    except Exception as e:
        print(f"Error in is_relevant_content_present: {str(e)}")
        return "no_relevant_content"
