from configuration.db import Base
from sqlalchemy import Column, Integer, ForeignKey

class Profile(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('users'))
