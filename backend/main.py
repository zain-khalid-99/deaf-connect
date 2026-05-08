from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.api import conversations, analytics, settings, auth
from backend.database import init_db
import logging
import platform

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Deaf Connect API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Deaf Connect Terminal Starting...")
    logger.info(f"System: {platform.system()} {platform.release()}")
    logger.info(f"Python: {platform.python_version()}")
    try:
        import tensorflow as tf
        logger.info(f"TensorFlow Version: {tf.__version__}")
    except:
        logger.error("TensorFlow not found")
    init_db.init_db()

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["Conversations"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])

@app.get("/")
async def root():
    return {"message": "Deaf Connect API is running"}

@app.get("/api/health")
async def health_check():
    health = {
        "status": "healthy",
        "python_version": platform.python_version(),
        "database": "connected"
    }
    try:
        from backend.database.connection import engine
        with engine.connect() as conn:
            pass
    except:
        health["status"] = "unhealthy"
        health["database"] = "disconnected"
    return health
