# app/routers/upload_router.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.database import supabase
import pdfplumber
import io
import uuid
from datetime import datetime
from sentence_transformers import SentenceTransformer
import numpy as np

router = APIRouter(prefix="/upload", tags=["Upload"])

# Initialize model
print("🔄 Loading AI model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ AI model loaded")


def chunk_text(text: str, chunk_size: int = 500):
    """Split text into chunks with overlap"""
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())
    
    return chunks


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload PDF and store in Supabase"""
    try:
        print(f"\n{'='*60}")
        print(f"📤 UPLOAD: {file.filename}")
        print(f"{'='*60}")
        
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

        contents = await file.read()
        pdf_text = ""
        
        print("📖 Extracting text...")
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    pdf_text += text + "\n"
                print(f"   Page {page_num}/{len(pdf.pages)}")

        if not pdf_text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")

        # Clean the text
        pdf_text = ' '.join(pdf_text.split())
        
        print(f"✅ Extracted {len(pdf_text)} characters")

        document_id = str(uuid.uuid4())

        # Create smaller chunks with overlap
        chunks = chunk_text(pdf_text, chunk_size=500)
        if not chunks:
            raise HTTPException(status_code=400, detail="Failed to create chunks")

        print(f"✂️  Created {len(chunks)} chunks")

        # Insert metadata
        print("💾 Storing metadata...")
        meta_result = supabase.table("pdf_files").insert({
            "document_id": document_id,
            "filename": file.filename,
            "uploaded_at": datetime.utcnow().isoformat()
        }).execute()

        if not meta_result.data:
            raise HTTPException(status_code=500, detail="Failed to store metadata")

        # Process and store chunks
        print(f"🔄 Processing {len(chunks)} chunks...")
        success_count = 0
        
        for idx, chunk in enumerate(chunks):
            try:
                # Generate embedding
                emb = model.encode(chunk, normalize_embeddings=True)
                emb_list = emb.tolist()

                # Verify embedding dimension
                if len(emb_list) != 384:
                    print(f"⚠️ Wrong dimension: {len(emb_list)}")
                    continue

                # Store in database
                result = supabase.table("pdf_chunks").insert({
                    "document_id": document_id,
                    "chunk_index": idx,
                    "content": chunk,
                    "embedding": emb_list,
                    "created_at": datetime.utcnow().isoformat()
                }).execute()

                if result.data:
                    success_count += 1
                    if (idx + 1) % 3 == 0 or (idx + 1) == len(chunks):
                        print(f"   ✅ Stored {idx + 1}/{len(chunks)}")
                else:
                    print(f"   ⚠️ Failed chunk {idx}")

            except Exception as chunk_error:
                print(f"   ❌ Error on chunk {idx}: {chunk_error}")
                continue

        if success_count == 0:
            raise HTTPException(status_code=500, detail="No chunks were stored")

        print(f"\n{'='*60}")
        print(f"✅ SUCCESS: {success_count}/{len(chunks)} chunks stored")
        print(f"{'='*60}\n")

        return {
            "success": True,
            "message": f"✅ Uploaded {success_count} chunks for '{file.filename}'",
            "document_id": document_id,
            "filename": file.filename,
            "chunks": success_count
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))