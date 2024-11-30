from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import translator_router, llm_router, admin_ai_router
from src.startup import StartupManager
from src.config import Settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings().allowed_origins,  # Allow specific origins
    allow_credentials=True,  # Allow cookies and other credentials
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allow all headers
)
app.include_router(translator_router.router, prefix="/api/translator")
app.include_router(llm_router.router, prefix="/api/llm-chat")
app.include_router(admin_ai_router.router, prefix="/api/admin-ai")

StartupManager.load()