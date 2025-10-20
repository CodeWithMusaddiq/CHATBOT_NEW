# app/routers/chat_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
from app.core.database import supabase
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import numpy as np

load_dotenv()

router = APIRouter(prefix="/chat", tags=["Chat"])

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

client = Groq(api_key=GROQ_API_KEY)

print("🔄 Loading AI model for chat...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Chat model ready")


class ChatRequest(BaseModel):
    question: str


@router.post("/")
async def chat(request: ChatRequest):
    """Answer questions from all PDFs"""
    try:
        print(f"\n{'='*60}")
        print(f"💬 QUESTION: {request.question}")
        print(f"{'='*60}")
        
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question is empty")

        # Generate embedding with normalization
        print("🔍 Generating query embedding...")
        q_emb = model.encode(request.question, normalize_embeddings=True)
        q_emb_list = q_emb.tolist()
        
        print(f"   Embedding dimension: {len(q_emb_list)}")

        # Search database with lower threshold
        print("🔎 Searching database...")
        matches = supabase.rpc("match_pdf_chunks", {
            "query_embedding": q_emb_list,
            "match_threshold": 0.1,  # Much lower threshold
            "match_count": 15
        }).execute()

        print(f"📊 Raw matches: {len(matches.data) if matches.data else 0}")

        if not matches.data or len(matches.data) == 0:
            # Try to check if any documents exist
            check = supabase.table("pdf_chunks").select("id").limit(1).execute()
            if not check.data:
                return {
                    "answer": "❌ No documents found in database. Please upload a PDF first.",
                    "matches": 0
                }
            else:
                return {
                    "answer": "⚠️ I found documents but couldn't match your question. Try rephrasing or asking about the general topic of the document.",
                    "matches": 0
                }

        # Sort by similarity
        sorted_matches = sorted(matches.data, key=lambda x: x.get('similarity', 0), reverse=True)
        top_matches = sorted_matches[:5]

        print(f"✅ Using top {len(top_matches)} matches")
        for i, m in enumerate(top_matches, 1):
            print(f"   Match {i}: similarity={m.get('similarity', 0):.3f}, file={m.get('filename', 'Unknown')}")

        # Build context
        context_parts = []
        for i, m in enumerate(top_matches, 1):
            context_parts.append(
                f"[Chunk {i} from {m.get('filename', 'Unknown')} - Relevance: {m.get('similarity', 0):.2%}]\n{m.get('content', '')}"
            )
        
        context = "\n\n---\n\n".join(context_parts)

        # Generate answer
        print("🤖 Generating answer with AI...")
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer the question based on the provided context from PDF documents. If the context doesn't clearly answer the question, say so and provide what information is available."
                },
                {
                    "role": "user",
                    "content": f"Context from PDF documents:\n\n{context}\n\n---\n\nQuestion: {request.question}\n\nProvide a clear, detailed answer based on the context above:"
                }
            ],
            temperature=0.4,
            max_tokens=1000
        )

        answer = completion.choices[0].message.content.strip()
        
        print(f"✅ Answer generated: {answer[:150]}...")
        print(f"{'='*60}\n")

        # Get unique filenames
        sources = list(set([m.get('filename', 'Unknown') for m in top_matches]))

        return {
            "answer": answer,
            "matches": len(matches.data),
            "sources": sources,
            "top_similarity": top_matches[0].get('similarity', 0) if top_matches else 0
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents")
async def list_documents():
    """List all uploaded PDFs"""
    try:
        result = supabase.table("pdf_files").select("*").order("uploaded_at", desc=True).execute()
        
        # Also get chunk counts
        docs_with_counts = []
        if result.data:
            for doc in result.data:
                chunks = supabase.table("pdf_chunks").select("id", count="exact").eq("document_id", doc["document_id"]).execute()
                doc["chunk_count"] = len(chunks.data) if chunks.data else 0
                docs_with_counts.append(doc)
        
        return {
            "count": len(docs_with_counts),
            "documents": docs_with_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))