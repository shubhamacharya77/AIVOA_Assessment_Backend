import os
import shutil
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from app.agent.complaint_agent import build_complaint_graph
from app.services import auth_service
from app.services.document_service import process_uploaded_file

router = APIRouter(prefix="/chat", tags=["chat"])
security = HTTPBearer()

# Initialize graph globally
app_graph = build_complaint_graph()


class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    agent_response: str
    extracted_data: dict
    is_complete: bool
    missing_fields: list


@router.post("/message", response_model=ChatResponse)
async def process_chat_message(
    request: ChatRequest,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        user_data = auth_service.get_current_user(credentials.credentials)
        scoped_thread_id = f"user_{user_data['id']}_{request.thread_id}"

        config = {"configurable": {"thread_id": scoped_thread_id}}

        # Append the new human message to the state.
        # The MemorySaver will automatically fetch the existing state for this thread_id
        # and merge this new message into chat_history using operator.add
        state = {"chat_history": [HumanMessage(content=request.message)]}

        result = app_graph.invoke(state, config=config)

        return ChatResponse(
            agent_response=result.get("agent_response", ""),
            extracted_data=result.get("extracted_data", {}),
            is_complete=result.get("is_complete", False),
            missing_fields=result.get("missing_fields", []),
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=ChatResponse)
async def upload_document(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    thread_id: str = Form(...),
    file: UploadFile = File(...),
):
    user_data = auth_service.get_current_user(credentials.credentials)
    scoped_thread_id = f"user_{user_data['id']}_{thread_id}"

    temp_path = f"/tmp/{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        text = process_uploaded_file(temp_path)

        config = {"configurable": {"thread_id": scoped_thread_id}}
        state = {
            "chat_history": [
                HumanMessage(
                    content=f"I have uploaded a document with the following content:\n\n{text}"
                )
            ]
        }
        result = app_graph.invoke(state, config=config)

        return ChatResponse(
            agent_response=result.get("agent_response", ""),
            extracted_data=result.get("extracted_data", {}),
            is_complete=result.get("is_complete", False),
            missing_fields=result.get("missing_fields", []),
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

