from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import get_db
from app.models.user import UserSchemaInput, DependentSchemaInput, UserSchemaOutput
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserSchemaInput])
def get_all_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_users = user_service.get_users()
    return db_users


@router.post("/", response_model=UserSchemaOutput)
def create_user(user: UserSchemaInput, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.create_user(user)
    return db_user


@router.get("/{user_id}", response_model=UserSchemaOutput)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/dependents", response_model=UserSchemaOutput)
def create_relation_between_user_dependents(user_id, dependent: DependentSchemaInput, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.add_related_user(user_id, dependent)


@router.delete('/{user_id}/dependents/{dependent_id}', status_code=204)
def delete_dependent(user_id: int, dependent_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_id(user_id)
    dependent = user_service.get_user_by_id(user_id)

    if not db_user or not dependent:
        raise HTTPException(status_code=404, detail="User or dependent not found")

    for dependent in db_user.dependents:
        if dependent.id == dependent_id:
            db_user.dependents.remove(dependent)

    db.delete(dependent)
    db.commit()

    return None
