"""
User service

This module contains functions to interact with the user data
"""

from model.user import UserInDB, UserCreate, UserUpdate, UserOut
from data import user
from data import user_role


def create_user(new_user: UserCreate) -> UserOut:
    """
    Create a new user

    Args:
        new_user (UserCreate): UserCreate object

    Returns:
        UserInDB: UserInDB object
    """
    try:
        n_user = user.create_user(new_user)
        return UserOut(
            **n_user.model_dump(), role=user.get_role_by_user_id(n_user.id)
        )
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
        n_user = user.get_user_by_id(id)
        return UserOut(
            **n_user.model_dump(), role=user.get_role_by_user_id(n_user.id)
        )
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
        n_user = user.get_user_by_username(username)
        return UserOut(
            **n_user.model_dump(), role=user.get_role_by_user_id(n_user.id)
        )
    except Exception as e:
        raise e


def get_all_users() -> list[UserOut]:
    """
    Get all users

    Returns:
        List[UserInDB]: List of UserInDB objects
    """
    try:
        return [
            UserOut(**u.model_dump(), role=user.get_role_by_user_id(u.id))
            for u in user.get_all_users()
        ]
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
        u_user = user.update_user(updated_user)
        return UserOut(
            **u_user.model_dump(), role=user.get_role_by_user_id(u_user.id)
        )
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
        user.delete_user(
            UserInDB(
                **deleted_user.model_dump(exclude={"role_id"}),
                role_id=deleted_user.role_id
            )
        )
    except Exception as e:
        raise e


def update_user_role(user_id: str, role_name: str):
    """
    Update user role

    Args:
        user_id (str): User id
        role_id (str): Role id
    """
    try:
        role_id = user_role.get_user_role_by_name(role_name).id
        user.update_user_role(user_id, role_id)
        return True
    except Exception as e:
        raise e
