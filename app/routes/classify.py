from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.classifier import LegalIssueClassifier

router = APIRouter()

class ClassifyRequest(BaseModel):
    text: str

@router.post("/classify")
async def classify_legal_issue(request: ClassifyRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    result = LegalIssueClassifier.classify(request.text)
    return result
