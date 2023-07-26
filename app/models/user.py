from typing import Optional, List

from pydantic import BaseModel, Field, conlist
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship, backref

from app import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    email = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    user_type = Column(Integer, default=0, index=True)
    has_access = Column(Boolean, default=True)

    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())

    # Define the one-to-one relationship between User and Profile
    # Set 'nullable=True' to make Profile optional
    profile = relationship("Profile", uselist=False, back_populates="user", cascade="all, delete-orphan")

    # Define the one-to-many relationship between User and Dependents
    parent_id = Column(Integer, ForeignKey('users.id'))
    dependents = relationship("User", backref=backref("parent", remote_side=[id]))


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Float)
    weight = Column(Float)
    bio = Column(String)

    # Define the foreign key for the user
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    # Create a back reference to the User model
    user = relationship("User", back_populates="profile", lazy="joined", cascade="all, delete-orphan",
                        single_parent=True)


class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: str


class UserSchemaInput(UserBase):
    password: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DependentSchemaInput(UserBase):
    id: Optional[int]
    username: str
    email: Optional[str]
    password: Optional[str]
    full_name: str
    user_type: int
    has_access: bool
    age: int
    gender: str
    height: int
    weight: float
    bio: str
    imageUrl: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProfileOutput(BaseModel):
    id: int = None
    full_name: str = None
    age: int = None
    gender: str = None
    height: float = None
    weight: float = None
    bio: str = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserOutputBase(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool = None
    user_type: int = None
    has_access: bool = None
    profile: Optional[ProfileOutput] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserSchemaOutput(UserOutputBase):
    dependents: Optional[List[UserOutputBase]] = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
