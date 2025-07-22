from langgraph.types import interrupt
from langmem.short_term import SummarizationNode
from langchain_core.messages.utils import count_tokens_approximately
from src.models import vector_store, llm

def get_human_reply(state):
    # Interrupt and get human response
    print("get_human_reply")
    human_response = interrupt(state["followup_question"])
    # Append the user's response to additional_info
    if state.get("additional_info") is None:
        state["additional_info"] = ""
    state["additional_info"] += f' User : {human_response} \n'
    print(state["additional_info"])
    return state

def retrieve(state):
    print("retrieve")
    try:
        query = state["query"]
        retrieved_docs = vector_store.similarity_search(
            query, k = 3
        )
        print(retrieved_docs)
        state["context"] = retrieved_docs
        return state
    except Exception as e:
        print(f"Error in retrieve: {str(e)}")
        state["context"] = []
        return state

def summarization_node():
    print("summarization_node")
    try:
        return SummarizationNode(
                token_counter=count_tokens_approximately,
                model=llm,
                max_tokens=2048,
                max_summary_tokens=256,
                output_messages_key="llm_input_messages",
            )
    except Exception as e:
        print(f"Error in summarization_node: {str(e)}")
        # Return a basic summarization node with default settings
        return SummarizationNode(
                token_counter=count_tokens_approximately,
                model=llm,
                max_tokens=2048,
                max_summary_tokens=256,
                output_messages_key="llm_input_messages",
            )