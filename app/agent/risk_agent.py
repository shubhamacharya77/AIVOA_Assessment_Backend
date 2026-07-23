from typing import Any, Dict, List

from pydantic import BaseModel, Field

from app.prompts.risk_prompt import RISK_ASSESSMENT_PROMPT_TEMPLATE
from app.services.llm_service import get_llm


class RiskAssessmentOutput(BaseModel):
    predicted_severity: str = Field(
        description="The predicted severity of the complaint. Must be one of: Low, Medium, High, Critical"
    )
    root_cause_recommendation: str = Field(
        description="A brief hypothesis of the potential root cause based on the complaint details."
    )
    next_suggested_actions: List[str] = Field(
        description="A list of 2-4 actionable next steps for the QA team."
    )
    risk_summary: str = Field(
        description="A 2-3 sentence paragraph summarizing the risk analysis."
    )


def analyze_risk(structured_data: Dict[str, Any]) -> dict:
    """Uses LLM to perform a risk assessment on a complaint."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(RiskAssessmentOutput)

    prompt = RISK_ASSESSMENT_PROMPT_TEMPLATE.format(structured_data=structured_data)

    try:
        response = structured_llm.invoke(prompt)
        return response.model_dump()
    except Exception as e:
        print(f"Error in analyze_risk: {e}")
        return {
            "predicted_severity": "Unknown",
            "root_cause_recommendation": "Unable to determine root cause due to AI error.",
            "next_suggested_actions": ["Review complaint manually"],
            "risk_summary": "Failed to generate risk assessment due to AI error.",
        }
