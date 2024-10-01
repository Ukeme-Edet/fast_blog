"""
Unit tests for user service

This module contains the unit tests for the user service module.
"""

from pytest import fixture, raises
from faker import Faker
import os

os.environ["ENV"] = "test"
from model.user_role import UserRoleCreate, UserRoleUpdate
from service import user
from errors.errors import Duplicate, Missing
from model.user import UserCreate, UserUpdate

faker = Faker()


@fixture
def new_user() -> UserCreate:
    """
    Create a new user

    Returns:
        UserCreate: A new user
    """
    return UserCreate(
        username=faker.user_name(),
        password=faker.password(),
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


@fixture
def new_role() -> UserRoleCreate:
    """
    Create a new role

    Returns:
        UserRoleCreate: A new role
    """
    return UserRoleCreate(name=faker.word().zfill(2))


@fixture
def updated_role() -> UserRoleUpdate:
    """
    Create an updated role

    Returns:
        UserRoleCreate: An updated role
    """
    return UserRoleUpdate(name=faker.word().zfill(2))


def test_create_user(new_user: UserCreate):
    """
    Test create user

    Args:
        new_user (UserCreate): A new user
    """
    created_user = user.create_user(new_user)
    assert created_user.username == new_user.username


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


def test_get_user_by_id(new_user: UserCreate):
    """
    Test get user by id

    Args:
        new_user (UserCreate): A new user
    """
    created_user = user.create_user(new_user)
    user_by_id = user.get_user_by_id(created_user.id)
    assert user_by_id.username == new_user.username


def test_get_user_by_username(new_user: UserCreate):
    """
    Test get user by username

    Args:
        new_user (UserCreate): A new user
    """
    created_user = user.create_user(new_user)
    user_by_username = user.get_user_by_username(created_user.username)
    assert user_by_username.username == new_user.username


def test_get_all_users(new_user: UserCreate):
    """
    Test get all users

    Args:
        new_user (UserCreate): A new user
    """
    user.create_user(new_user)
    all_users = user.get_all_users()
    assert len(all_users) > 0
    assert any(user.username == new_user.username for user in all_users)


def test_get_user_by_id_missing():
    """
    Test get user by id missing
    """
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        user.get_user_by_id(id)
    assert exc_info.value.msg == f"User with id {id!r} not found"


def test_get_user_by_username_missing():
    """
    Test get user by username missing
    """
    with raises(Missing) as exc_info:
        username = faker.user_name()
        user.get_user_by_username(username)
    assert exc_info.value.msg == f"User with username {username!r} not found"


def test_update_user(new_user: UserCreate, updated_user: UserUpdate):
    """
    Test update user

    Args:
        new_user (UserCreate): A new user
        updated_user (UserUpdate): An updated user
    """
    created_user = user.create_user(new_user)
    updated_user.id = created_user.id
    updated_user.username = faker.user_name()
    updated_user.password = faker.password()
    user.update_user(updated_user)
    user_by_id = user.get_user_by_id(created_user.id)
    assert user_by_id.username == updated_user.username


def test_update_user_missing(updated_user: UserUpdate):
    """
    Test update user missing

    Args:
        new_user (UserCreate): A new user
        updated_user (UserUpdate): An updated user
    """
    with raises(Missing) as exc_info:
        updated_user.id = str(faker.uuid4())
        user.update_user(updated_user)
    assert exc_info.value.msg == f"User with id {updated_user.id!r} not found"


def test_update_user_duplicate(new_user: UserCreate, updated_user: UserUpdate):
    """
    Test update user duplicate

    Args:
        new_user (UserCreate): A new user
        updated_user (UserUpdate): An updated user
    """
    user.create_user(new_user)
    created_user = user.create_user(
        UserCreate(
            username=faker.user_name(),
            password=faker.password(),
        )
    )
    updated_user.id = created_user.id
    updated_user.username = new_user.username
    with raises(Duplicate) as exc_info:
        user.update_user(updated_user)
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
    user.delete_user(created_user.id)
    with raises(Missing) as exc_info:
        user.get_user_by_id(created_user.id)
    assert exc_info.value.msg == f"User with id {created_user.id!r} not found"


def test_delete_user_missing():
    """
    Test delete user missing
    """
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        user.delete_user(id)
    assert exc_info.value.msg == f"User with id {id!r} not found"


def test_user_role_update(new_user: UserCreate, new_role: UserRoleCreate):
    """
    Test user role update

    Args:
        new_user (UserCreate): A new user
    """
    created_user = user.create_user(new_user)
    user.create_user_role(new_role)
    user_role_update = user.user_role_update(created_user.id, new_role.name)
    assert user_role_update == True


def test_user_role_update_missing(new_user: UserCreate):
    """
    Test user role update missing
    """
    n_user = user.create_user(new_user)
    with raises(Missing) as exc_info:
        name = faker.word().zfill(2)
        user.user_role_update(n_user.id, name)
    assert exc_info.value.msg == f"User role with name {name!r} not found"


def test_role_create(new_role: UserRoleCreate):
    """
    Test role create

    Args:
        new_role (UserRoleCreate): A new role
    """
    created_role = user.create_user_role(new_role)
    assert created_role.name == new_role.name


def test_role_create_duplicate(new_role: UserRoleCreate):
    """
    Test role create duplicate

    Args:
        new_role (UserRoleCreate): A new role
    """
    user.create_user_role(new_role)
    with raises(Duplicate) as exc_info:
        user.create_user_role(new_role)
    assert (
        exc_info.value.msg
        == f"User role with name {new_role.name!r} already exists"
    )


def test_get_role_by_id(new_role: UserRoleCreate):
    """
    Test get role by id

    Args:
        new_role (UserRoleCreate): A new role
    """
    created_role = user.create_user_role(new_role)
    role_by_id = user.get_user_role_by_id(created_role.id)
    assert role_by_id.name == new_role.name


def test_get_role_by_name(new_role: UserRoleCreate):
    """
    Test get role by name

    Args:
        new_role (UserRoleCreate): A new role
    """
    created_role = user.create_user_role(new_role)
    role_by_name = user.get_user_role_by_name(created_role.name)
    assert role_by_name.name == new_role.name


def test_get_role_by_id_missing():
    """
    Test get role by id missing
    """
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        user.get_user_role_by_id(id)
    assert exc_info.value.msg == f"User role with id {id!r} not found"


def test_get_role_by_name_missing():
    """
    Test get role by name missing
    """
    with raises(Missing) as exc_info:
        name = faker.user_name()
        user.get_user_role_by_name(name)
    assert exc_info.value.msg == f"User role with name {name!r} not found"


def test_update_role(new_role: UserRoleCreate, updated_role: UserRoleUpdate):
    """
    Test update role

    Args:
        new_role (UserRoleCreate): A new role
        updated_role (UserRoleUpdate): An updated role
    """
    created_role = user.create_user_role(new_role)
    user.update_user_role(created_role.id, updated_role)
    role_by_id = user.get_user_role_by_id(created_role.id)
    assert role_by_id.name == updated_role.name


def test_update_role_missing(updated_role: UserRoleUpdate):
    """
    Test update role missing

    Args:
        new_role (UserRoleCreate): A new role
        updated_role (UserRoleUpdate): An updated role
    """
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        user.update_user_role(id, updated_role)
    assert exc_info.value.msg == f"User role with id {id!r} not found"


def test_update_role_duplicate(
    new_role: UserRoleCreate, updated_role: UserRoleUpdate
):
    """
    Test update role duplicate

    Args:
        new_role (UserRoleCreate): A new role
        updated_role (UserRoleUpdate): An updated role
    """
    user.create_user_role(new_role)
    created_role = user.create_user_role(UserRoleCreate(name=faker.word().zfill(2)))
    updated_role.name = created_role.name
    with raises(Duplicate) as exc_info:
        user.update_user_role(created_role.id, updated_role)
    assert (
        exc_info.value.msg
        == f"User role with name {updated_role.name!r} already exists"
    )


def test_delete_role(new_role: UserRoleCreate):
    """
    Test delete role

    Args:
        new_role (UserRoleCreate): A new role
    """
    created_role = user.create_user_role(new_role)
    user.delete_user_role(created_role.id)
    with raises(Missing) as exc_info:
        user.get_user_role_by_id(created_role.id)
    assert (
        exc_info.value.msg
        == f"User role with id {created_role.id!r} not found"
    )


def test_delete_role_missing():
    """
    Test delete role missing
    """
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        user.delete_user_role(id)
    assert exc_info.value.msg == f"User role with id {id!r} not found"
