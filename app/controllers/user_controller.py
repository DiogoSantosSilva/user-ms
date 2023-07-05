from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app import get_db
from app.models.user import User, UserCreateSchema, UserSchema


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserSchema)
def create_user(request: Request, user: UserCreateSchema, db: Session = Depends(get_db)):
    user_service = UserService(db)
    _user = user_service.create_user(user)
    return _user

@router.get("/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    return user