import logging.config

from starlette.middleware.cors import CORSMiddleware

from backend.api.routers import calc
from backend.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from fastapi import FastAPI

app = FastAPI(
    title="KRDom",
    version="0.1.0",
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
