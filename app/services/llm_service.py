import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.prompts.pharma_prompts import extraction_prompt
from app.schemas.complaint_schema import ComplaintExtraction

# Load env variables if running outside of main FastAPI app context
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env")))


def get_llm():
    """
    Returns the configured Groq LLM instance.
    We are using llama-3.3-70b-versatile as it fully supports structured JSON output.
    """
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def get_extraction_chain():
    """
    Returns the LangChain chain that strictly outputs the structured ComplaintExtraction Pydantic model.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(ComplaintExtraction)
    return extraction_prompt | structured_llm
