# Deaf Connect: Real-Time ASL-to-English Communication System

Deaf Connect is a production-level communication bridge between Deaf/Hard-of-Hearing individuals and hearing people. Built with a futuristic, high-performance interface, it leverages computer vision and neural translation to enable fluid conversation.

## 🚀 Core Features
- **Real-Time ASL Recognition**: Powered by MediaPipe Hands and custom heuristic/neural inference logic.
- **Neural Translation**: Uses Gemini 2.0 Flash to convert ASL gloss sequences into natural English sentences.
- **Vocal Synthesis (TTS)**: Automatically speaks translated English sentences for the hearing person.
- **Voice Recognition (STT)**: Converts spoken English from hearing people into real-time text for the Deaf user.
- **Modular Architecture**: Clean, scalable directory structure (Core, Pages, Components, Utils).

## 🛠 Tech Stack
- **Frontend**: React 18, Vite, Tailwind CSS 4, Framer Motion
- **AI/CV**: MediaPipe Hands, TensorFlow.js, Gemini 2.0
- **Storage**: LocalStorage for session persistence
- **APIs**: Web Speech API (Synthesis & Recognition)

## 📂 Project Structure
- `backend/`: FastAPI application, SQLAlchemy models, and Supabase integration.
- `frontend/`: Streamlit dashboard and user interface.
- `core/`: Recognition engine and landmark extraction.
- `utils/`: Shared utilities and configuration.

## 🗄️ Database Setup (Supabase PostgreSQL)
This project has migrated from SQLite to Supabase PostgreSQL for production-ready scalability.

### 1. Environment Configuration
Create a `.env` file in the root directory (use `.env.example` as a template):
```env
DATABASE_URL=postgresql://postgres:PASSWORD@db.PROJECT.supabase.co:5432/postgres
SUPABASE_URL=https://PROJECT.supabase.co
SUPABASE_KEY=YOUR_SUPABASE_KEY
```

### 2. Initialize Database
Run the following command to create the necessary tables in your Supabase project:
```bash
python -m backend.database.init_db
```

### 3. Run the Backend
Start the FastAPI server:
```bash
uvicorn backend.main:app --reload
```

### 4. Run the Frontend
Start the Streamlit interface:
```bash
streamlit run frontend/app.py
```

---
*Created by Deaf Connect Engineering Team - 2026*
