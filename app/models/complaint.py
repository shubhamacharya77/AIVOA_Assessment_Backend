from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Complaint(SQLModel, table=True):
    __tablename__ = "complaint_table"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_table.id")
    status: str = Field(default="Pending Triage")
    source_type: str = Field(default="Text")  # Text, Email, Document

    # Store the exact 13 structured fields here as JSON
    structured_data: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSONB)
    )

    # Store the AI Risk Assessment output here
    risk_assessment: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSONB)
    )

    # Store the raw conversation or parsed text here
    original_context: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
