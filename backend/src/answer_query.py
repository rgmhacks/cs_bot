from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from src.models import llm

class Answer(BaseModel):
  answer : str = Field(description="The answer to the user query.")

final_answer_prompt_template = """
You are Dream11’s official customer support assistant.
You assist users by answering queries related to Dream11's fantasy sports platform such as deposits, account verification, contest rules, point system, withdrawals, and other gameplay-related questions.
You will receive conversation between user and customer support team and you will also receive some relevant content related to query.
Your task is to answer the query. Use only the provided context to answer the user's question. If the context does not contain enough information, respond with:
"I'm not sure about that. Let me connect you to a human support agent for further assistance."

Be clear, concise, friendly, and professional in your tone. Avoid making up any information that is not in the context.

**IMPORTANT**
Ask the question in the **same language** as that of user (which may be English, Hindi, or any Indian regional language or maybe any Indian Language written in English For E.g. 'Merko paise nikalne hain' so this is Hindi words written in English so you also have to answer ask question in Hindi written in English).

Context : {context}

Conversation : {question}

Helpful Answer: ** Remember to answer in structured format using bullet points
{format_instructions}
"""

final_answer_json_parser = JsonOutputParser(pydantic_object=Answer)

final_answer_prompt  = PromptTemplate(
    template=final_answer_prompt_template,
    input_variables=["context", "question"],
    partial_variables={"format_instructions": final_answer_json_parser.get_format_instructions()},
)

final_answer_chain = final_answer_prompt | llm | final_answer_json_parser

def answer_query(state):
    print("answer_query")
    try:
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        final_answer = final_answer_chain.invoke({"question" : state["additional_info"], "context" : docs_content})
        state["final_answer"] = final_answer["answer"]
        state["additional_info"] += f' Customer Support Team : {state["final_answer"]} \n'
        return state
    except Exception as e:
        print(f"Error in answer_query: {str(e)}")
        state["final_answer"] = "I'm sorry, I encountered an error while processing your request. Please try again or contact support."
        return state