from . import BaseModel, datetime


class User(BaseModel):
    id: str
    username: str
    password_hash: str
    time_created: datetime
    time_updated: datetime


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str
    password: str
    time_updated: datetime


class UserInDB(User):
    pass
