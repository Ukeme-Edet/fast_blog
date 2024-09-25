"""
This module contains the user model.
"""

from typing import Optional
from pydantic import Field
from . import BaseModel, datetime


class User(BaseModel):
    """
    User model

    This class contains the attributes of the user model.

    Attributes:
        id (str): The unique identifier for the user
        username (str): The username of the user
        password_hash (str): The password hash of the user
        time_created (datetime): The time the user was created
        time_updated (datetime): The time the user was last updated
    """

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
    """
    User create model

    This class contains the attributes of the user create model.

    Attributes:
        username (str): The username of the user
        password (str): The password of the user
    """

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
    """
    User update model

    This class contains the attributes of the user update model.

    Attributes:
        username (str): The username of the user
        password (str): The password of the user
    """

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


class UserInDB(User):
    """
    User in database model

    This class contains the attributes of the user in database model.

    Attributes:
        password_hash (str): The password hash of the user
    """

    pass


class UserOut(BaseModel):
    """
    User out model

    This class contains the attributes of the user out model.

    Attributes:
        username (str): The username of the user
    """

    id: str = Field(..., description="The unique identifier for the user")
    username: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="The username of the user",
    )
    time_created: datetime = Field(
        ..., description="The time the user was created"
    )
    time_updated: datetime = Field(
        ..., description="The time the user was last updated"
    )
