"""
User service

This module contains functions to interact with the user data
"""

from model.user import UserInDB, UserCreate, UserUpdate, UserOut
from data import user


def create_user(new_user: UserCreate) -> UserOut:
    """
    Create a new user

    Args:
        new_user (UserCreate): UserCreate object

    Returns:
        UserInDB: UserInDB object
    """
    try:
        return UserOut(**user.create_user(new_user).model_dump())
    except Exception as e:
        raise e


def get_user_by_id(id: str) -> UserOut:
    """
    Get a user by id

    Args:
        id (str): id of the user

    Returns:
        UserInDB: UserInDB object
    """
    try:
        return UserOut(**user.get_user_by_id(id).model_dump())
    except Exception as e:
        raise e


def get_user_by_username(username: str) -> UserOut:
    """
    Get a user by username

    Args:
        username (str): username of the user

    Returns:
        UserInDB: UserInDB object
    """
    try:
        return UserOut(**user.get_user_by_username(username).model_dump())
    except Exception as e:
        raise e


def get_all_users() -> list[UserOut]:
    """
    Get all users

    Returns:
        List[UserInDB]: List of UserInDB objects
    """
    try:
        return [UserOut(**u.model_dump()) for u in user.get_all_users()]
    except Exception as e:
        raise e


def update_user(updated_user: UserUpdate) -> UserOut:
    """
    Update a user

    Args:
        user (UserUpdate): UserUpdate object

    Returns:
        UserInDB: UserInDB object
    """
    try:
        return UserOut(**user.update_user(updated_user).model_dump())
    except Exception as e:
        raise e


def delete_user(deleted_user_id: str):
    """
    Delete a user

    Args:
        deleted_user (UserInDB): UserInDB object
    """
    try:
        deleted_user = user.get_user_by_id(deleted_user_id)
        user.delete_user(UserInDB(**deleted_user.model_dump()))
    except Exception as e:
        raise e
