import logging
import logging.config

from starlette.middleware.cors import CORSMiddleware

from backend.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from fastapi import FastAPI

app = FastAPI(
    title="KRDom",
    version="0.1.0",
)
