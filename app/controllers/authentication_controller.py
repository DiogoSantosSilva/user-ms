from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import get_db
from app.models.token import TokenSchema
from app.models.user import UserSchema, UserSchemaOut
from app.services import autentication_service
from app.services.user_service import UserService
from app.deps import get_current_user

router = APIRouter(tags=["authentication"])


@router.get('/me', response_model=UserSchemaOut)
async def get_me(user: UserSchema = Depends(get_current_user)):
    return user


@router.post('/signup', response_model=UserSchemaOut)
def create_user(data: UserSchema, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_email(data.email)
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = UserSchema(
        email=data.email,
        username=data.username,
        password=autentication_service.get_hashed_password(data.password)
    )
    return user_service.create_user(user)


@router.post('/login', response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_email(form_data.username)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_password = db_user.password
    if not autentication_service.verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": autentication_service.create_access_token(db_user.email),
        "refresh_token": autentication_service.create_refresh_token(db_user.email)
    }
