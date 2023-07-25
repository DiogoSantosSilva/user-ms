from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship

from app import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    user_type = Column(Integer, default=0, index=True)
    has_access = Column(Boolean, default=True)

    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())

    # Define the one-to-one relationship between User and Profile
    # Set 'nullable=True' to make Profile optional
    profile = relationship("Profile", uselist=False, back_populates="user", lazy="joined", cascade="all, delete-orphan",
                           single_parent=True)

    # Define the one-to-many relationship between User and ResponsibleFor
    responsible_for = relationship("ResponsibleFor", back_populates="responsible_user")


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


class ResponsibleFor(Base):
    __tablename__ = "responsible_for"

    id = Column(Integer, primary_key=True, index=True)
    entity_name = Column(String)

    # Define the foreign key for the user
    user_id = Column(Integer, ForeignKey('users.id'))

    # Create a back reference to the User model
    responsible_user = relationship("User", back_populates="responsible_for")


class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: str


class UserSchemaInput(UserBase):
    password: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserSchemaOutput(BaseModel):
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
