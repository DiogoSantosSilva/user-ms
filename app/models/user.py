from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean
from typing import Optional

from app import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)


class UserBase(BaseModel):
    username: str
    email: str
    password: Optional[str]


class UserSchema(UserBase):
    id: Optional[int]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserSchemaOut(BaseModel):
    id: Optional[int]
    username: str
    email: str
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")