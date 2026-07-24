from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.complaint_schema import ComplaintExtraction
from app.services import auth_service, complaint_service

router = APIRouter(prefix="/complaints", tags=["complaints"])
security = HTTPBearer()


@router.post("")
def create_complaint(
    complaint_data: ComplaintExtraction,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        user_data = auth_service.get_current_user(credentials.credentials)
        user_id = user_data["id"]
        source_type = complaint_data.source or "Unknown"

        new_complaint = complaint_service.create_complaint(
            user_id=user_id,
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
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("")
def get_complaints(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        user_data = auth_service.get_current_user(credentials.credentials)
        user_id = user_data["id"]
        complaints = complaint_service.get_all_complaints(user_id=user_id)
        return {"status": "success", "data": complaints}
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{complaint_id}")
def update_existing_complaint(
    complaint_id: int,
    complaint_data: ComplaintExtraction,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        user_data = auth_service.get_current_user(credentials.credentials)
        user_id = user_data["id"]
        success, message, complaint = complaint_service.update_complaint(
            complaint_id=complaint_id,
            user_id=user_id,
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

