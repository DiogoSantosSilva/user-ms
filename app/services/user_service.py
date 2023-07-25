from sqlalchemy.orm import Session

from app.models.user import User, UserSchemaInput


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_users(self):
        return self.db.query(User).all()

    def create_user(self, user: UserSchemaInput) -> User:
        _user = User(username=user.username, email=user.email, password=user.password)
        self.db.add(_user)
        self.db.commit()
        self.db.refresh(_user)
        return _user

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, user_email: str) -> User | None:
        return self.db.query(User).filter(User.email == user_email).first()
