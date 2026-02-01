import logging.config

from starlette.middleware.cors import CORSMiddleware

from backend.api.routers import admin, auth, calc, health, materials
from backend.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from fastapi import FastAPI

app = FastAPI(
    title="KRDom",
    version="0.1.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calc.router, prefix="/calc", tags=["calc"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(materials.router, prefix="/api/v1/materials", tags=["materials"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
