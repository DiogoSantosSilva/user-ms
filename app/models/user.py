from app import Base
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel

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

class UserCreateSchema(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True