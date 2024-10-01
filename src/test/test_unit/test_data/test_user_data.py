"""
Test user data

This module contains the unit tests for the user data module.
"""

from pytest import fixture, raises
from faker import Faker
from model.user import UserCreate, UserCreate, UserInDB, UserUpdate
from model.user_role import UserRoleCreate, UserRoleInDB, UserRoleUpdate
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
    return UserCreate(username=faker.user_name(), password=faker.password())


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


@fixture
def new_user_role() -> UserRoleCreate:
    """
    Create a new user role

    Returns:
        UserRoleCreate: A new user role
    """
    return UserRoleCreate(name=faker.word().zfill(2))


@fixture
def updated_user_role() -> UserRoleUpdate:
    """
    Create an updated user role

    Returns:
        UserRoleUpdate: An updated user role
    """
    return UserRoleUpdate(
        name=faker.word(),
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
                role_id=str(faker.uuid4()),
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


def test_user_role_create(new_user_role: UserRoleCreate):
    """
    Test create user role

    Args:
        new_user_role (UserRoleCreate): A new user role
    """
    created_user_role = user.create_user_role(new_user_role)
    assert created_user_role.name == new_user_role.name


def test_user_role_create_duplicate(new_user_role: UserRoleCreate):
    """
    Test create user role duplicate

    Args:
        new_user_role (UserRoleCreate): A new user role
    """
    user.create_user_role(new_user_role)
    with raises(Duplicate) as exc_info:
        user.create_user_role(new_user_role)
    assert (
        exc_info.value.msg
        == f"User role with name {new_user_role.name!r} already exists"
    )


def test_user_role_update(
    new_user_role: UserRoleCreate, updated_user_role: UserRoleUpdate
):
    """
    Test update user role

    Args:
        new_user_role (UserRoleCreate): A new user role
        updated_user_role (UserRoleUpdate): An updated user role
    """
    created_user_role = user.create_user_role(new_user_role)
    user.update_user_role(created_user_role.id, updated_user_role)
    user_role_by_id = user.get_user_role_by_id(created_user_role.id)
    assert user_role_by_id.name == updated_user_role.name


def test_user_role_update_missing(updated_user_role: UserRoleUpdate):
    """
    Test update user role missing

    Args:
        updated_user_role (UserRoleUpdate): An updated user role
    """
    id = str(faker.uuid4())
    with raises(Missing) as exc_info:
        user.update_user_role(id, updated_user_role)
    assert exc_info.value.msg == f"User role with id {id!r} not found"


def test_user_role_update_duplicate(new_user_role: UserRoleCreate):
    """
    Test update user role duplicate

    Args:
        new_user_role (UserRoleCreate): A new user role
    """
    created_user_role = user.create_user_role(new_user_role)
    new_user_role.name = faker.word().zfill(2)
    user.create_user_role(new_user_role)
    with raises(Duplicate) as exc_info:
        user.update_user_role(
            created_user_role.id, UserRoleUpdate(name=new_user_role.name)
        )
    assert (
        exc_info.value.msg
        == f"User role with name {new_user_role.name!r} already exists"
    )


def test_user_role_delete(new_user_role: UserRoleCreate):
    """
    Test delete user role

    Args:
        new_user_role (UserRoleCreate): A new user role
    """
    created_user_role = user.create_user_role(new_user_role)
    user.delete_user_role(created_user_role.id)
    with raises(Missing) as exc_info:
        user.get_user_role_by_id(created_user_role.id)
    assert (
        exc_info.value.msg
        == f"User role with id {created_user_role.id!r} not found"
    )


def test_user_role_delete_missing():
    """
    Test delete user role missing
    """
    id = str(faker.uuid4())
    with raises(Missing) as exc_info:
        user.delete_user_role(id)
    assert exc_info.value.msg == f"User role with id {id!r} not found"


def test_update_user_role(new_user: UserCreate, new_user_role: UserRoleCreate):
    """
    Test update user role

    Args:
        new_user (UserCreate): A new user
        new_user_role (UserRoleCreate): A new user role
    """
    created_user = user.create_user(new_user)
    created_user_role = user.create_user_role(new_user_role)
    user.user_role_update(created_user.id, created_user_role.name)
    user_by_id = UserInDB(**user.get_user_by_id(created_user.id).model_dump())
    assert user_by_id.role_id == created_user_role.id


def test_update_user_role_missing():
    """
    Test update user role missing
    """
    user_id = str(faker.uuid4())
    role_name = faker.word().zfill(2)
    with raises(Missing) as exc_info:
        user.user_role_update(user_id, role_name)
    assert exc_info.value.msg == f"User with id {user_id!r} not found"
