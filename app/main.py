# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Later we will import our routers here:
# from app.routers.upload_router import router as upload_router
# from app.routers.chat_router import router as chat_router

app = FastAPI(
    title="PDF Chatbot",
    description="Chatbot that answers questions from uploaded PDFs",
    version="1.0"
)

# --- CORS setup (lets frontend talk to backend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now (we can restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes placeholder ---
@app.get("/")
def home():
    return {"message": "Welcome to PDF Chatbot API!"}

# When routers are ready, we’ll include them like this:
# app.include_router(upload_router)
# app.include_router(chat_router)
