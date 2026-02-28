
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.agents.legal_agent import LegalAgent
from app.agents.vision_agent import VisionAgent
import tempfile
import os
import shutil

router = APIRouter()
agent = LegalAgent()
vision_agent = VisionAgent()

class AgentRequest(BaseModel):
    query: str
    session_id: str


@router.post("/agent/chat")
async def agent_chat(request: AgentRequest):
    query = request.query.strip()
    session_id = request.session_id.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query field cannot be empty.")
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID cannot be empty.")
    result = agent.decide_and_act(query, session_id)
    return result


# New multimodal endpoint
@router.post("/agent/vision-chat")
async def agent_vision_chat(query: str, session_id: str, file: UploadFile = File(...)):
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name
    try:
        # Analyze with VisionAgent
        vision_context = vision_agent.analyze_document(temp_path)
        # Pass vision_context to LegalAgent
        result = agent.decide_and_act(query, session_id, vision_context=vision_context)
        return result
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
