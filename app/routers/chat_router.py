# app/routers/chat_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

# Request model
class ChatRequest(BaseModel):
    question: str

@router.post("/")
async def chat(request: ChatRequest):
    try:
        # Mock response (no real API call)
        answer = f"This is a mock response to your question: '{request.question}'."
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
