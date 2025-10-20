# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routers.chat_router import router as chat_router
# from app.routers.upload_router import router as upload_router  # ✅ make sure this line exists

# app = FastAPI(
#     title="PDF Chatbot",
#     description="Chatbot that answers questions from uploaded PDFs",
#     version="1.0"
# )

# # --- CORS setup ---
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "Welcome to PDF Chatbot API!"}

# # ✅ Register routers
# app.include_router(chat_router)
# app.include_router(upload_router)  # ✅ this line is essential

# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat_router import router as chat_router
from app.routers.upload_router import router as upload_router

app = FastAPI(title="PDF Chatbot", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    print("\n" + "="*60)
    print("🚀 PDF CHATBOT STARTED")
    print("="*60)
    print("📡 http://localhost:8000")
    print("📚 http://localhost:8000/docs")
    print("="*60 + "\n")


@app.get("/")
def home():
    return {
        "status": "running",
        "endpoints": {
            "upload": "/upload/",
            "chat": "/chat/",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(upload_router)
app.include_router(chat_router)