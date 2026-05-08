"""
Module: main.py
Purpose: FastAPI application entry point for Deaf Connect backend.
"""
import os
import sys
import logging
import platform
from contextlib import asynccontextmanager

# CRITICAL: Resolve project root and add to sys.path BEFORE any local imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import conversations, analytics, settings, auth
from backend.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FIX: @app.on_event("startup") is deprecated in FastAPI >= 0.93.
# Use the lifespan context manager instead.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info("Deaf Connect Terminal Starting...")
    logger.info(f"System: {platform.system()} {platform.release()}")
    logger.info(f"Python: {platform.python_version()}")
    try:
        import tensorflow as tf
        logger.info(f"TensorFlow: {tf.__version__}")
    except ImportError:
        logger.warning("TensorFlow not installed — model inference will be unavailable.")
    init_db.init_db()
    yield
    # --- Shutdown ---
    logger.info("Deaf Connect Terminal shutting down.")


app = FastAPI(title="Deaf Connect API", version="1.0.0", lifespan=lifespan)

# CORS — allow Streamlit frontend (localhost:8501) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["Conversations"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])


@app.get("/")
async def root():
    return {"message": "Deaf Connect API is running", "version": "1.0.0"}


@app.get("/api/health")
async def health_check():
    health = {
        "status": "healthy",
        "python_version": platform.python_version(),
        "database": "unknown",
    }
    try:
        from backend.database.connection import engine
        with engine.connect():
            health["database"] = "connected"
    except Exception as e:
        health["status"] = "degraded"
        health["database"] = f"disconnected: {e}"
    return health
