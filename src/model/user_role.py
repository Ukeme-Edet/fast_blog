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


class UserRoleCreate(BaseModel):
    """
    User role create model

    This class contains the attributes of the user role create model.

    Attributes:
        name (str): The name of the user role
    """

    name: str


class UserRoleUpdate(BaseModel):
    """
    User role update model

    This class contains the attributes of the user role update model.

    Attributes:
        name (str): The name of the user role
    """

    name: str


class UserRoleInDB(UserRole):
    """
    User role in database model

    This class contains the attributes of the user role in database model.

    Attributes:
        id (str): The unique identifier for the user role
        name (str): The name of the user role
    """

    pass
