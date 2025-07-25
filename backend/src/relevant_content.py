from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from src.models import llm


# Output schema for the filtered relevant content
class KeepRelevantContent(BaseModel):
    relevant_content: str = Field(
        description="The relevant content from the retrieved documents that is relevant to the user query."
    )
    is_relevant_content_present: bool = Field(
        description="Whether the relevant content is present or not."
    )

keep_only_relevant_content_prompt_template = """
You receive a user query which maybe in English, Hindi or any other Indian Language : {query} and retrieved documents: {retrieved_documents} from a vector store.
You need to filter out all the non relevant information that doesn't supply important information regarding the query: {query}.
The retrieved documents are in the following format : Title\nContent\n\nTitle\nContent\n\n .....
Your goal is just to filter out the non relevant (Title, Content) pair.
You can remove (Title, Content) pair that are not relevant to the query.
DO NOT ADD ANY NEW INFORMATION THAT IS NOT IN THE RETRIEVED DOCUMENTS OR DO NOT ADD ANY SENTENCE, JUST GIVE THE RELEVANT (Title,Content) pairs in the same format. {format_instructions}
"""

keep_only_relevant_content_prompt_parser = JsonOutputParser(pydantic_object=KeepRelevantContent)

# Create the prompt for the LLM
keep_only_relevant_content_prompt = PromptTemplate(
    template=keep_only_relevant_content_prompt_template,
    input_variables=["query", "retrieved_documents"],
    partial_variables={"format_instructions": keep_only_relevant_content_prompt_parser.get_format_instructions()},
)


# Create the LLM chain for filtering relevant content
keep_only_relevant_content_chain = keep_only_relevant_content_prompt | llm | keep_only_relevant_content_prompt_parser


def keep_only_relevant_content(state):
    print("keep_only_relevant_content")
    try:
        retrieved_docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        input_data = {"query": state["query_description"], "retrieved_documents": retrieved_docs_content}
        output = keep_only_relevant_content_chain.invoke(input_data)
        state["is_relevant_content_present"] = output["is_relevant_content_present"]
        print(output["is_relevant_content_present"])
        if output["is_relevant_content_present"]:
            state["context"] = [Document(page_content=content) for content in output["relevant_content"].split("\n\n")]
        return state
    except Exception as e:
        print(f"Error in keep_only_relevant_content: {str(e)}")
        state["is_relevant_content_present"] = False
        return state