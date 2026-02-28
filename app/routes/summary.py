from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.classifier import LegalIssueClassifier
from app.services.rag_engine import RAGEngine
from app.services.summarizer import generate_summary

router = APIRouter()
classifier = LegalIssueClassifier()
rag_engine = RAGEngine()

class SummaryRequest(BaseModel):
    query: str

@router.post("/summary")
async def summary_endpoint(request: SummaryRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query field cannot be empty.")
    # Classify the legal issue
    category_result = classifier.classify(query)
    category = category_result["category"]
    # Retrieve relevant laws
    rag_results = rag_engine.search_legal_knowledge(query)
    # Generate summary
    summary = generate_summary(query, category, rag_results)
    return summary
