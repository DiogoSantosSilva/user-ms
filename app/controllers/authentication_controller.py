from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.token import Token, Login
from app.config import settings
from app.services.autentication_service import AuthenticationService

router = APIRouter(prefix="/token", tags=["token"])

@router.post("/", response_model=Token)
async def login_for_access_token(
    data: Login = Depends()
):
    authentication_service = AuthenticationService()
    user = authentication_service.authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}