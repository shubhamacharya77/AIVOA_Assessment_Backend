from fastapi import APIRouter, HTTPException

from app.schemas.complaint_schema import ComplaintExtraction
from app.services import complaint_service

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.post("")
def create_complaint(complaint_data: ComplaintExtraction):
    try:
        # Use the existing complaint service to save it to PostgreSQL
        # We pass a mock user_id=1 for now, and extract source_type from the data
        source_type = complaint_data.source or "Unknown"

        new_complaint = complaint_service.create_complaint(
            user_id=1,
            source_type=source_type,
            structured_data=complaint_data.model_dump(exclude_none=True),
        )
        return {
            "status": "success",
            "data": {
                "id": new_complaint.id,
                "risk_assessment": new_complaint.risk_assessment,
            },
        }
    except ValueError as e:
        # Catch our custom validation errors (like "Complaint already exists")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("")
def get_complaints():
    try:
        # Using mock user_id=1 for now
        complaints = complaint_service.get_all_complaints(user_id=1)
        return {"status": "success", "data": complaints}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{complaint_id}")
def update_existing_complaint(complaint_id: int, complaint_data: ComplaintExtraction):
    try:
        # Pass mock user_id=1
        success, message, complaint = complaint_service.update_complaint(
            complaint_id=complaint_id,
            user_id=1,
            updated_data=complaint_data.model_dump(exclude_none=True),
        )
        if not success:
            raise HTTPException(status_code=404, detail=message)

        return {
            "status": "success",
            "data": {"id": complaint.id, "risk_assessment": complaint.risk_assessment},
        }
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
