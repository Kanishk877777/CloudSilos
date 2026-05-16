from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_hash = Column(String, unique=True)
    gcs_path = Column(String)
    size = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
