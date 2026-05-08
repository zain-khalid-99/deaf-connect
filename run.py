"""
Module: run.py
Purpose: Launch script — starts FastAPI backend then Streamlit frontend.
"""
import subprocess
import time
import sys
import os

def run_app():
    print("🚀 Starting Deaf Connect Platform...")

    # Ensure we run from the project root regardless of where script is called from
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # 1. Start Backend (FastAPI via uvicorn)
    print("📡 Launching FastAPI Backend on http://localhost:8000")
    backend_process = subprocess.Popen(
        # FIX: Use sys.executable so the correct venv Python is used on Windows
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"],
        cwd=project_root,
    )

    time.sleep(2)  # Give backend time to start

    # 2. Start Frontend (Streamlit)
    print("🎨 Launching Streamlit Frontend on http://localhost:8501")
    print("   Run URL: http://localhost:8501")
    try:
        subprocess.run(
            # FIX: Use sys.executable -m streamlit instead of bare 'streamlit'
            # so Windows finds it in the active venv without PATH issues.
            [sys.executable, "-m", "streamlit", "run", "frontend/app.py",
             "--server.port", "8501",
             "--server.headless", "false"],
            cwd=project_root,
        )
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        backend_process.terminate()
        print("✅ All processes stopped.")

if __name__ == "__main__":
    run_app()
