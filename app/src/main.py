from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import translator_router
# Example of using .env values
# print(Config().app.SOME_TOKEN)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,  # Allow cookies and other credentials
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allow all headers
)
app.include_router(translator_router.router, prefix="/api/translator")


