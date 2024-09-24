from config import Config
from sqlmodel import SQLModel, create_engine

DB_URI = Config().get_db_uri()

engine = create_engine(DB_URI)

from .user import User
from .blog import Blog

SQLModel.metadata.create_all(engine)
