import operator
from typing import Annotated, Any, Dict, List, TypedDict
from app.prompts.finalize_prompt import FINALIZE_PROMPT_TEMPLATE
from langchain_core.messages import AIMessage, BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from app.schemas.complaint_schema import ComplaintExtraction
from app.services.llm_service import get_extraction_chain, get_llm


# 1. Define the State
class ComplaintAgentState(TypedDict):
    chat_history: Annotated[List[BaseMessage], operator.add]
    extracted_data: Dict[str, Any]
    missing_fields: List[str]
    agent_response: str
    is_complete: bool


# The 13 required fields defined in our schema
REQUIRED_FIELDS = [
    "source",
    "customerName",
    "productName",
    "productStrength",
    "batchNumber",
    "manufacturingDate",
    "expiryDate",
    "quantityAffected",
    "complaintType",
    "complaintDate",
    "complaintDescription",
    "initialSeverity",
    "priority",
]


# 2. Define Nodes
def extract_node(state: ComplaintAgentState):
    """Uses LLM to extract fields based on the entire conversation context."""
    chain = get_extraction_chain()

    # Combine the chat history into a single text block for the extractor
    # (In a production system, you might format this more gracefully)
    conversation_text = "\n".join(
        [f"{msg.type}: {msg.content}" for msg in state["chat_history"]]
    )

    # Run the extraction chain
    result: ComplaintExtraction = chain.invoke({"text": conversation_text})

    # Merge new extractions with existing data
    current_data = state.get("extracted_data", {})
    new_data = result.model_dump()

    # Only update fields that the LLM found (not null)
    for key, value in new_data.items():
        if value is not None:
            current_data[key] = value

    return {"extracted_data": current_data}


def validate_node(state: ComplaintAgentState):
    """Checks if any required fields are missing."""
    current_data = state.get("extracted_data", {})

    missing = []
    for field in REQUIRED_FIELDS:
        # If the field is missing, empty string, or None
        if not current_data.get(field):
            missing.append(field)

    is_complete = len(missing) == 0
    return {"missing_fields": missing, "is_complete": is_complete}


def ask_user_node(state: ComplaintAgentState):
    """Uses LLM to politely ask the user for the missing fields."""
    llm = get_llm()
    missing = state["missing_fields"]
    from app.prompts.ask_user_prompt import ASK_USER_PROMPT_TEMPLATE

    prompt = ASK_USER_PROMPT_TEMPLATE.format(missing_fields=", ".join(missing))

    response = llm.invoke(prompt)

    # We append the AI's question to the chat history
    return {
        "agent_response": response.content,
        "chat_history": [AIMessage(content=response.content)],
    }


def finalize_node(state: ComplaintAgentState):
    """Uses LLM to generate a dynamic final confirmation or update acknowledgment."""
    llm = get_llm()

    # Get the last user message reliably from chat history
    last_user_msg = ""
    if state.get("chat_history"):
        for msg in reversed(state["chat_history"]):
            msg_type = getattr(msg, "type", "")
            if msg_type == "human" or msg.__class__.__name__ == "HumanMessage":
                last_user_msg = msg.content if hasattr(msg, "content") else str(msg)
                break

    prompt = FINALIZE_PROMPT_TEMPLATE.format(last_user_msg=last_user_msg)

    response = llm.invoke(prompt)

    return {
        "agent_response": response.content,
        "chat_history": [AIMessage(content=response.content)],
    }


# 3. Define Edges (Routing)
def should_continue(state: ComplaintAgentState):
    if state["is_complete"]:
        return "finalize"
    else:
        return "ask_user"


# 4. Build the Graph
def build_complaint_graph():
    workflow = StateGraph(ComplaintAgentState)

    # Add nodes
    workflow.add_node("extract", extract_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("ask_user", ask_user_node)
    workflow.add_node("finalize", finalize_node)

    # Add edges
    workflow.set_entry_point("extract")
    workflow.add_edge("extract", "validate")

    workflow.add_conditional_edges(
        "validate", should_continue, {"ask_user": "ask_user", "finalize": "finalize"}
    )
    workflow.add_edge("ask_user", END)
    workflow.add_edge("finalize", END)

    # Compile with memory checkpointer to persist state across API calls
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
