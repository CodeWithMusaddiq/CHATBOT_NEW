# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat_router import router as chat_router
from app.routers.upload_router import router as upload_router

app = FastAPI(
    title="PDF Chatbot",
    description="Chatbot that answers questions from uploaded PDFs",
    version="1.0"
)

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to PDF Chatbot API!"}

# Routers
app.include_router(chat_router)
app.include_router(upload_router)
