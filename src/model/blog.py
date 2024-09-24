from . import BaseModel, datetime


class Blog(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    time_created: datetime
    time_updated: datetime


class BlogCreate(BaseModel):
    user_id: str
    title: str
    content: str


class BlogUpdate(BaseModel):
    title: str
    content: str
    time_updated: datetime


class BlogInDB(Blog):
    pass
