from fastapi import FastAPI
from src.routers import translator_router
# Example of using .env values
# print(Config().app.SOME_TOKEN)

app = FastAPI()

app.include_router(translator_router.router, prefix="/api/translator")




