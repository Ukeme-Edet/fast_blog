from typing import Optional
from pydantic import Field
from . import BaseModel, datetime


class User(BaseModel):
    id: str = Field(..., description="The unique identifier for the user")
    username: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="The username of the user",
    )
    password_hash: str = Field(
        ..., min_length=2, description="The password hash of the user"
    )
    time_created: datetime = Field(
        ..., description="The time the user was created"
    )
    time_updated: datetime = Field(
        ..., description="The time the user was last updated"
    )


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="The username of the user",
    )
    password: str = Field(
        ..., min_length=8, description="The password of the user"
    )


class UserUpdate(BaseModel):
    id: str = Field(..., description="The unique identifier for the user")
    username: Optional[str] = Field(
        ...,
        min_length=2,
        max_length=100,
        description="The username of the user",
    )
    password: Optional[str] = Field(
        ..., min_length=8, description="The password of the user"
    )
    time_updated: datetime = Field(
        ..., description="The time the user was last updated"
    )


class UserInDB(User):
    pass
