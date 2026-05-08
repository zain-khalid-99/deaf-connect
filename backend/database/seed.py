from .connection import SessionLocal
from . import models, crud, schemas

def seed_db():
    db = SessionLocal()
    # Check if a test user exists
    test_user_id = "test-user-001"
    db_user = crud.get_user(db, test_user_id)
    if not db_user:
        print("Seeding test data...")
        user_in = schemas.UserCreate(
            id=test_user_id,
            email="test@example.com",
            full_name="Test User",
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=test"
        )
        crud.create_user(db, user_in)
        print("Test user created.")
    else:
        print("Test user already exists.")
    db.close()

if __name__ == "__main__":
    seed_db()
