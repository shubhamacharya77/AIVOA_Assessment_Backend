from datetime import datetime
from typing import Any, Dict, Optional, Tuple

from sqlmodel import select

from app.agent.risk_agent import analyze_risk
from app.models.complaint import Complaint
from app.services.database_service import get_session


def create_complaint(
    user_id: int,
    source_type: str,
    structured_data: Dict[str, Any],
    original_context: str = "",
) -> Complaint:
    """Creates a new complaint and triggers an AI risk assessment."""
    # Generate risk assessment
    risk_assessment = analyze_risk(structured_data)

    with get_session() as session:
        complaint = Complaint(
            user_id=user_id,
            source_type=source_type,
            structured_data=structured_data,
            risk_assessment=risk_assessment,
            original_context=original_context,
        )
        session.add(complaint)
        session.commit()
        session.refresh(complaint)
        return complaint


def get_complaint(complaint_id: int) -> Optional[Complaint]:
    """Retrieves a single complaint by its ID."""
    with get_session() as session:
        return session.get(Complaint, complaint_id)


def get_all_complaints(user_id: int) -> list[Complaint]:
    """Retrieves all complaints belonging to a specific user, sorted by creation date."""
    with get_session() as session:
        statement = (
            select(Complaint)
            .where(Complaint.user_id == user_id)
            .order_by(Complaint.created_at.desc())
        )
        return session.exec(statement).all()


def update_complaint(
    complaint_id: int, user_id: int, updated_data: Dict[str, Any]
) -> Tuple[bool, str, Optional[Complaint]]:
    """
    Attempts to update a complaint.
    Returns: (Success Boolean, Message String, Complaint Object)
    As per requirements, if forced to update but it doesn't exist, we return a polite response.
    """
    with get_session() as session:
        complaint = session.get(Complaint, complaint_id)

        if not complaint:
            # Microservice Validation: Complaint does not exist.
            msg = f"I'm sorry, but I couldn't find an existing complaint with ID {complaint_id}. I would be happy to create a new complaint for you instead."
            return False, msg, None

        # If it exists, update the JSON fields
        current_data = complaint.structured_data.copy()
        current_data.update(updated_data)

        complaint.structured_data = current_data

        # Re-run risk assessment with updated data
        complaint.risk_assessment = analyze_risk(current_data)

        complaint.updated_at = datetime.utcnow()

        session.add(complaint)
        session.commit()
        session.refresh(complaint)

        return True, "Complaint updated successfully.", complaint
