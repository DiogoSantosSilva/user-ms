from configuration.db import SessionLocal
from models.user import User

def create_user(username: str, email: str):
    db = SessionLocal()
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)