from model.user import UserInDB, UserCreate, UserUpdate
from data import user


def create_user(new_user: UserCreate) -> UserInDB:
    """
    Create a new user

    Args:
        new_user (UserCreate): UserCreate object

    Returns:
        UserInDB: UserInDB object
    """
    try:
        return user.create_user(new_user)
    except Exception as e:
        raise e


def get_user_by_id(id: str) -> UserInDB:
    """
    Get a user by id

    Args:
        id (str): id of the user

    Returns:
        UserInDB: UserInDB object
    """
    try:
        return user.get_user_by_id(id)
    except Exception as e:
        raise e


def get_user_by_username(username: str) -> UserInDB:
    """
    Get a user by username

    Args:
        username (str): username of the user

    Returns:
        UserInDB: UserInDB object
    """
    try:
        return user.get_user_by_username(username)
    except Exception as e:
        raise e


def get_all_users() -> list[UserInDB]:
    """
    Get all users

    Returns:
        List[UserInDB]: List of UserInDB objects
    """
    try:
        return user.get_all_users()
    except Exception as e:
        raise e


def update_user(updated_user: UserUpdate) -> UserInDB:
    """
    Update a user

    Args:
        user (UserUpdate): UserUpdate object

    Returns:
        UserInDB: UserInDB object
    """
    try:
        return user.update_user(updated_user)
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
        user.delete_user(deleted_user)
    except Exception as e:
        raise e
