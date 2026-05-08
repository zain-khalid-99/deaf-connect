from backend.database.connection import engine, Base
from backend.database import models

def init_db():
    print("Initializing PostgreSQL tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully.")
    except Exception as e:
        print(f"❌ DATABASE ERROR: Could not connect to Supabase. {str(e)}")
        print("The application will run in offline mode with limited functionality.")

if __name__ == "__main__":
    init_db()
