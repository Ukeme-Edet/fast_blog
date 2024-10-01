"""
This module contains the pydantic models for the user role.
"""

from . import BaseModel


class UserRole(BaseModel):
    """
    User role model

    This class contains the attributes of the user role model.

    Attributes:
        id (str): The unique identifier for the user role
        name (str): The name of the user role
    """

    id: str
    name: str
