"""
Test user data

This module contains the unit tests for the user data module.
"""

from pytest import fixture, raises
from faker import Faker
from model.user import UserCreate, UserCreate, UserInDB, UserUpdate
import os
from errors.errors import Duplicate, Missing

os.environ["ENV"] = "test"
from data import user

faker = Faker()


@fixture
def new_user() -> UserCreate:
    """
    Create a new user

    Returns:
        UserCreate: A new user
    """
    return UserCreate(
        username=faker.user_name(), password=faker.password()
    )


@fixture
def updated_user() -> UserUpdate:
    """
    Create an updated user

    Returns:
        UserUpdate: An updated user
    """
    return UserUpdate(
        id=str(faker.uuid4()),
        username=faker.user_name(),
        password=faker.password(),
    )


def test_create_user(new_user: UserCreate):
    """
    Test create user

    Args:
        new_user (UserCreate): A new user
    """
    created_user = user.create_user(new_user)
    assert created_user.username == new_user.username
    assert created_user.password_hash != new_user.password


def test_create_user_duplicate(new_user: UserCreate):
    """
    Test create user duplicate

    Args:
        new_user (UserCreate): A new user
    """
    user.create_user(new_user)
    with raises(Duplicate) as exc_info:
        user.create_user(new_user)
    assert (
        exc_info.value.msg
        == f"User with username {new_user.username!r} already exists"
    )


def test_update_user(new_user: UserCreate, updated_user: UserUpdate):
    """
    Test update user

    Args:
        new_user (UserCreate): A new user
        updated_user (UserUpdate): An updated user
    """
    created_user = user.create_user(new_user)
    updated_user.id = created_user.id
    user.update_user(updated_user)
    user_by_id = user.get_user_by_id(created_user.id)
    assert user_by_id.username == updated_user.username
    assert user_by_id.password_hash != updated_user.password


def test_update_user_missing(updated_user: UserUpdate):
    """
    Test update user missing

    Args:
        updated_user (UserUpdate): An updated user
    """
    with raises(Missing) as exc_info:
        user.update_user(updated_user)
    assert exc_info.value.msg == f"User with id {updated_user.id!r} not found"


def test_update_user_duplicate(new_user: UserCreate):
    """
    Test update user duplicate

    Args:
        new_user (UserCreate): A new user
    """
    created_user = user.create_user(new_user)
    new_user.username = faker.user_name()
    user.create_user(new_user)
    with raises(Duplicate) as exc_info:
        user.update_user(
            UserUpdate(
                id=created_user.id,
                username=new_user.username,
                password=None,
            )
        )
    assert (
        exc_info.value.msg
        == f"User with username {new_user.username!r} already exists"
    )


def test_delete_user(new_user: UserCreate):
    """
    Test delete user

    Args:
        new_user (UserCreate): A new user
    """
    created_user = user.create_user(new_user)
    user.delete_user(created_user)
    with raises(Missing) as exc_info:
        user.get_user_by_id(created_user.id)
    assert exc_info.value.msg == f"User with id {created_user.id!r} not found"


def test_delete_user_missing():
    """
    Test delete user missing
    """
    id = str(faker.uuid4())
    with raises(Missing) as exc_info:
        user.delete_user(
            UserInDB(
                id=id,
                username=faker.user_name(),
                password_hash=faker.password(),
                time_created=faker.date_time(),
                time_updated=faker.date_time(),
            )
        )
    assert exc_info.value.msg == f"User with id {id!r} not found"


def test_get_user_by_id(new_user: UserCreate):
    """
    Test get user by id

    Args:
        new_user (UserCreate): A new user
    """
    created_user = user.create_user(new_user)
    user_id = created_user.id
    user_by_id = user.get_user_by_id(user_id)
    assert user_by_id.id == user_id


def test_get_user_by_username(new_user: UserCreate):
    """
    Test get user by username

    Args:
        new_user (UserCreate): A new user
    """
    created_user = user.create_user(new_user)
    username = created_user.username
    user_by_username = user.get_user_by_username(username)
    assert user_by_username.username == username
