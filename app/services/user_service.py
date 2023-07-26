from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, Profile, UserSchemaInput


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

    def create_user_profile(self, user_id, profile):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        profile = Profile(
            full_name=profile.full_name, age=profile.age, gender=profile.gender,
            height=profile.height, weight=profile.weight, bio=profile.bio
        )
        user.profile = profile
        self.db.commit()
        self.db.refresh(user)

    def add_related_user(self, user_id, dependent):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        user_dependent = User(
            username=dependent.username,
            password=dependent.password,
            email=dependent.email,
            user_type=dependent.user_type,
            has_access=dependent.has_access,
            parent_id=user.id
        )
        user_profile = Profile(
            full_name=dependent.full_name,
            age=dependent.age,
            gender=dependent.gender,
            height=dependent.height,
            weight=dependent.weight,
            bio=dependent.bio
        )
        user_dependent.profile = user_profile
        self.db.add(user_dependent)
        self.db.commit()
        self.db.refresh(user_dependent)
        return user_dependent

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, user_email: str):
        return self.db.query(User).filter(User.email == user_email).first()
