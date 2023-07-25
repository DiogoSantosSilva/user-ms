from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import get_db
from app.models.user import UserSchemaInput
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserSchemaInput])
def get_all_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_users = user_service.get_users()
    return db_users


@router.post("/", response_model=UserSchemaInput)
def create_user(user: UserSchemaInput, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.create_user(user)
    return db_user


@router.get("/{user_id}", response_model=UserSchemaInput)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/dependents")
def create_relation_between_user_dependents(user_id: int, data):
    pass
