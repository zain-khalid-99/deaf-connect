import sys
import os
import platform
import subprocess

def check_environment():
    print("==========================================")
    print("      DEAF CONNECT ENVIRONMENT CHECK      ")
    print("==========================================")
    
    # 1. Python Version
    python_version = platform.python_version()
    print(f"[SYSTEM] Python Version: {python_version}")
    if python_version.startswith("3.11"):
        print("   ✅ COMPATIBLE")
    else:
        print("   ⚠️  WARNING: Recommended version is 3.11.9")

    # 2. Critical Packages
    packages = [
        "tensorflow", "mediapipe", "cv2", "streamlit", "fastapi", "sqlalchemy", "psycopg2", "supabase"
    ]
    
    for pkg in packages:
        try:
            if pkg == "cv2":
                import cv2
                print(f"[PACKAGE] OpenCV: {cv2.__version__} ✅")
            elif pkg == "tensorflow":
                import tensorflow as tf
                print(f"[PACKAGE] TensorFlow: {tf.__version__} ✅")
            elif pkg == "mediapipe":
                import mediapipe as mp
                print(f"[PACKAGE] MediaPipe: {mp.__version__} ✅")
            else:
                __import__(pkg)
                print(f"[PACKAGE] {pkg}: Installed ✅")
        except ImportError:
            print(f"[PACKAGE] {pkg}: MISSING ❌")

    # 3. Database URL Check
    from dotenv import load_dotenv
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if db_url and "YOUR_PASSWORD" not in db_url:
        print("[DATABASE] Connection URL: Configured ✅")
    else:
        print("[DATABASE] Connection URL: NOT CONFIGURED ❌")

    print("==========================================")

if __name__ == "__main__":
    check_environment()
