from . import BaseModel, datetime
from pydantic import Field
from typing import Optional


class Blog(BaseModel):
    id: str = Field(..., description="The unique identifier for the blog")
    user_id: str = Field(..., description="The unique identifier for the user")
    title: str = Field(
        ..., max_length=100, description="The title of the blog", min_length=2
    )
    content: str = Field(
        ..., description="The content of the blog", min_length=2
    )
    time_created: datetime = Field(
        ..., description="The time the blog was created"
    )
    time_updated: datetime = Field(
        ..., description="The time the blog was last updated"
    )


class BlogCreate(BaseModel):
    user_id: str = Field(..., description="The unique identifier for the user")
    title: str = Field(
        ..., max_length=100, description="The title of the blog", min_length=2
    )
    content: str = Field(
        ..., description="The content of the blog", min_length=2
    )


class BlogUpdate(BaseModel):
    id: str = Field(..., description="The unique identifier for the blog")
    title: Optional[str] = Field(
        None, max_length=100, description="The title of the blog", min_length=2
    )
    content: Optional[str] = Field(
        None, description="The content of the blog", min_length=2
    )
    time_updated: datetime = Field(
        ..., description="The time the blog was last updated"
    )


class BlogInDB(Blog):
    pass
