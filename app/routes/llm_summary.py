from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_engine import RAGEngine
from app.services.gemini_client import generate_llm_response

router = APIRouter()
rag_engine = RAGEngine()

class LLMRequest(BaseModel):
    query: str

@router.post("/llm-summary")
async def llm_summary_endpoint(request: LLMRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query field cannot be empty.")
    sources = rag_engine.search_legal_knowledge(query)
    llm_response = generate_llm_response(query, sources)
    return {
        "response": llm_response,
        "sources": sources
    }
