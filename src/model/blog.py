"""
This module contains the pydantic models for the blog.
"""

from . import BaseModel, datetime
from pydantic import Field
from typing import Optional


class Blog(BaseModel):
    """
    Blog model

    This class contains the attributes of the blog model.

    Attributes:
        id (str): The unique identifier for the blog
        user_id (str): The unique identifier for the user
        title (str): The title of the blog
        content (str): The content of the blog
        time_created (datetime): The time the blog was created
        time_updated (datetime): The time the blog was last updated
    """

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
    """
    Blog create model

    This class contains the attributes of the blog create model.

    Attributes:
        user_id (str): The unique identifier for the user
        title (str): The title of the blog
        content (str): The content of the blog
    """

    user_id: str = Field(..., description="The unique identifier for the user")
    title: str = Field(
        ..., max_length=100, description="The title of the blog", min_length=2
    )
    content: str = Field(
        ..., description="The content of the blog", min_length=2
    )


class BlogUpdate(BaseModel):
    """
    Blog update model

    This class contains the attributes of the blog update model.

    Attributes:
        title (str): The title of the blog
        content (str): The content of the blog
    """

    id: str = Field(..., description="The unique identifier for the blog")
    title: Optional[str] = Field(
        None, max_length=100, description="The title of the blog", min_length=2
    )
    content: Optional[str] = Field(
        None, description="The content of the blog", min_length=2
    )


class BlogInDB(Blog):
    """
    Blog in database model

    This class contains the attributes of the blog in database model.

    Attributes:
        id (str): The unique identifier for the blog
        user_id (str): The unique identifier for the user
        title (str): The title of the blog
        content (str): The content of the blog
        time_created (datetime): The time the blog was created
        time_updated (datetime): The time the blog was last updated
    """

    pass


class BlogOut(Blog):
    """
    Blog out model

    This class contains the attributes of the blog out model.

    Attributes:
        user (User): The user of the blog
    """

    pass
