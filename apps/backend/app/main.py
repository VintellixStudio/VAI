from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

app.include_router(
    api_router,
    prefix=settings.API_V1_STR
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Vintellix AI Agent"
    }