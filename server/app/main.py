from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.generate import router as generate_router
from app.api.health import router as health_router
from app.api.providers import router as providers_router
from app.api.tasks import router as tasks_router
from app.config import get_settings


settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory=settings.output_dir), name="outputs")

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(providers_router, prefix=settings.api_prefix)
app.include_router(generate_router, prefix=settings.api_prefix)
app.include_router(tasks_router, prefix=settings.api_prefix)
