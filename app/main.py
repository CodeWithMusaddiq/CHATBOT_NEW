# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat_router import router as chat_router  # ✅ Add this line

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

# --- Routes ---
@app.get("/")
def home():
    return {"message": "Welcome to PDF Chatbot API!"}

# ✅ Include the chat router
app.include_router(chat_router)
