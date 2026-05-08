import subprocess
import time
import sys
import os

def run_app():
    print("🚀 Starting Deaf Connect Platform...")
    
    # 0. Validate Environment
    print("🔍 Validating Python 3.11 Environment...")
    try:
        subprocess.run([sys.executable, "dependency_validator.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Critical dependencies missing or incompatible. Please run 'pip install -r requirements.txt'")
        return

    # 1. Start Backend
    print("📡 Launching FastAPI Backend on http://localhost:8000")
    backend_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"])
    
    time.sleep(2) # Give backend time to start
    
    # 2. Start Frontend
    print("🎨 Launching Streamlit Frontend on http://localhost:8501")
    try:
        frontend_process = subprocess.run(["streamlit", "run", "frontend/app.py"])
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend_process.terminate()

if __name__ == "__main__":
    run_app()
