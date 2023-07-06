from app import Base
from sqlalchemy import Column, Integer, ForeignKey


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("User"))
