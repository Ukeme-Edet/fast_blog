"""
This module contains the pydantic models for the user role.
"""

from . import BaseModel


class UserRole(BaseModel):
    id: str
    name: str
