from fastapi import FastAPI
from .routers import item
from .core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.include_router(item.route, prefix=settings.API_V1_STR)
