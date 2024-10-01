"""
This file is used to create the database engine and to import the models.
"""

from config import Config
from sqlmodel import SQLModel, create_engine

DB_URI = Config().get_db_uri()

engine = create_engine(DB_URI, echo=True)

from .user import User
from .blog import Blog

SQLModel.metadata.create_all(engine)
