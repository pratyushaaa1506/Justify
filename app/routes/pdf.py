from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.pdf_generator import generate_pdf

router = APIRouter()

class SummaryData(BaseModel):
    issue: str
    category: str
    applicable_laws: list[str] = Field(default_factory=list)
    guidance: str

class PDFRequest(BaseModel):
    summary: SummaryData

@router.post("/pdf")
async def pdf_endpoint(request: PDFRequest):
    summary = request.summary
    if not summary.issue.strip():
        raise HTTPException(status_code=400, detail="Issue field cannot be empty.")
    file_path = generate_pdf(summary.dict())
    return {
        "message": "PDF generated successfully",
        "file_path": file_path
    }
