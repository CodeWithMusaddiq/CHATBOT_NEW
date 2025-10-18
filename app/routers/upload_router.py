# app/routers/upload_router.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.database import supabase
import pdfplumber
import io
import uuid
from datetime import datetime

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        print("📂 Uploading file:", file.filename)

        # Validate file type
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Please upload a PDF file")

        # Read and extract text
        contents = await file.read()
        pdf_text = ""
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                pdf_text += text
        print("📝 Extracted text length:", len(pdf_text))

        if not pdf_text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in PDF")

        # Generate unique document ID
        document_id = str(uuid.uuid4())

        # Insert into Supabase
        print("🛠️ Inserting into Supabase...")
        response = supabase.table("documents").insert({
            "document_id": document_id,
            "filename": file.filename,
            "chunk_index": 0,  # ✅ Added default chunk index
            "content": pdf_text,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        print("✅ Inserted successfully:", response)

        return {
            "message": "✅ PDF uploaded successfully",
            "document_id": document_id
        }

    except Exception as e:
        print("❌ Error during upload:", e)
        raise HTTPException(status_code=500, detail=str(e))


