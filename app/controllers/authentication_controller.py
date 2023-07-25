from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app import get_db
from app.models.token import TokenSchema
from app.models.user import UserSchemaInput, UserSchemaOutput, UserAuth
from app.services import autentication_service
from app.services.user_service import UserService
from app.deps import get_current_user

router = APIRouter(tags=["authentication"])


@router.get('/me', response_model=UserSchemaOutput)
async def get_me(user: UserSchemaInput = Depends(get_current_user)):
    return user


@router.post('/signup', response_model=UserSchemaOutput)
def create_user(response: Response, data: UserSchemaInput, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_email(data.email)
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = UserSchemaInput(
        email=data.email,
        username=data.username,
        password=autentication_service.get_hashed_password(data.password)
    )
    return user_service.create_user(user)


@router.post('/login', response_model=TokenSchema)
def login(login_data: UserAuth, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.get_user_by_email(login_data.email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_password = db_user.password
    if not autentication_service.verify_password(login_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "id": db_user.id,
        "access_token": autentication_service.create_access_token(db_user.email),
        "refresh_token": autentication_service.create_refresh_token(db_user.email)
    }
