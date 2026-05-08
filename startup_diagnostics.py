import os
import sys
import platform
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DeafConnect")

def run_diagnostics():
    logger.info("Starting System Diagnostics...")
    logger.info(f"Python Version: {platform.python_version()}")
    logger.info(f"OS: {platform.system()} {platform.release()}")
    
    # Check TensorFlow
    try:
        import tensorflow as tf
        logger.info(f"TensorFlow Status: OK (Version: {tf.__version__})")
    except Exception as e:
        logger.error(f"TensorFlow Status: FAILED - {str(e)}")

    # Check MediaPipe
    try:
        import mediapipe as mp
        logger.info(f"MediaPipe Status: OK (Version: {mp.__version__})")
    except Exception as e:
        logger.error(f"MediaPipe Status: FAILED - {str(e)}")

    # Check OpenCV
    try:
        import cv2
        logger.info(f"OpenCV Status: OK (Version: {cv2.__version__})")
    except Exception as e:
        logger.error(f"OpenCV Status: FAILED - {str(e)}")

    # Check Database
    try:
        from backend.database.connection import engine
        with engine.connect() as conn:
            logger.info("Database Connection: OK")
    except Exception as e:
        logger.error(f"Database Connection: FAILED - {str(e)}")

if __name__ == "__main__":
    run_diagnostics()
