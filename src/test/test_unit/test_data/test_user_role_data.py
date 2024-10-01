"""
Test user role data

This module contains the unit tests for the user role data.
"""

from pytest import fixture, raises
from faker import Faker
from model.user_role import UserRoleCreate, UserRoleUpdate, UserRoleInDB
import os
from errors.errors import Duplicate, Missing

os.environ["ENV"] = "test"
from data import user_role

faker = Faker()


@fixture
def new_user_role1() -> UserRoleCreate:
    """
    Create a new user role

    Returns:
        UserRoleCreate: User role create object
    """
    return UserRoleCreate(
        name=faker.word().zfill(2),
    )


@fixture
def new_user_role2() -> UserRoleCreate:
    """
    Create a new user role

    Returns:
        UserRoleCreate: User role create object
    """
    return UserRoleCreate(
        name=faker.word(),
    )


@fixture
def new_user_role3() -> UserRoleCreate:
    """
    Create a new user role

    Returns:
        UserRoleCreate: User role create object
    """
    return UserRoleCreate(
        name=faker.word().zfill(2),
    )


@fixture
def updated_user_role() -> UserRoleUpdate:
    """
    Create an updated user role

    Returns:
        UserRoleUpdate: User role update object
    """
    return UserRoleUpdate(
        name=faker.word(),
    )


def test_create_user_role(new_user_role1: UserRoleCreate):
    """
    Test create user role

    Args:
        new_user_role (UserRoleCreate): User role create object
    """
    user_role_in_db = user_role.create_user_role(new_user_role1)
    assert user_role_in_db.name == new_user_role1.name


def test_create_user_role_duplicate(new_user_role2: UserRoleCreate):
    """
    Test create user role duplicate

    Args:
        new_user_role (UserRoleCreate): User role create object
    """
    user_role.create_user_role(new_user_role2)
    with raises(Duplicate):
        user_role.create_user_role(new_user_role2)


def test_get_user_role_by_id(new_user_role3: UserRoleCreate):
    """
    Test get user role by id

    Args:
        new_user_role (UserRoleCreate): User role create object
    """
    user_role_in_db = user_role.create_user_role(new_user_role3)
    user_role_by_id = user_role.get_user_role_by_id(user_role_in_db.id)
    assert user_role_in_db.id == user_role_by_id.id
    assert user_role_in_db.name == user_role_by_id.name


def test_get_user_role_by_name(new_user_role3: UserRoleCreate):
    """
    Test get user role by name

    Args:
        new_user_role (UserRoleCreate): User role create object
    """
    user_role_in_db = user_role.create_user_role(new_user_role3)
    user_role_by_name = user_role.get_user_role_by_name(user_role_in_db.name)
    assert user_role_in_db.id == user_role_by_name.id
    assert user_role_in_db.name == user_role_by_name.name


def test_get_all_user_roles(
    new_user_role1: UserRoleCreate, new_user_role2: UserRoleCreate
):
    """
    Test get all user roles

    Args:
        new_user_role1 (UserRoleCreate): User role create object
        new_user_role2 (UserRoleCreate): User role create object
    """
    user_role_in_db1 = user_role.create_user_role(new_user_role1)
    user_role_in_db2 = user_role.create_user_role(new_user_role2)
    user_roles = user_role.get_all_user_roles()
    assert user_role_in_db1 in user_roles
    assert user_role_in_db2 in user_roles


def test_update_user_role(
    new_user_role1: UserRoleCreate, updated_user_role: UserRoleUpdate
):
    """
    Test update user role

    Args:
        new_user_role (UserRoleCreate): User role create object
        updated_user_role (UserRoleUpdate): User role update object
    """
    user_role_in_db = user_role.create_user_role(new_user_role1)
    user_role.update_user_role(user_role_in_db.id, updated_user_role)
    user_role_in_db = user_role.get_user_role_by_id(user_role_in_db.id)
    assert user_role_in_db.name == updated_user_role.name


def test_update_user_role_duplicate(
    new_user_role1: UserRoleCreate, new_user_role2: UserRoleCreate
):
    """
    Test update user role duplicate

    Args:
        new_user_role1 (UserRoleCreate): User role create object
        new_user_role2 (UserRoleCreate): User role create object
    """
    user_role_in_db1 = user_role.create_user_role(new_user_role1)
    user_role_in_db2 = user_role.create_user_role(new_user_role2)
    with raises(Duplicate):
        user_role.update_user_role(
            user_role_in_db1.id, UserRoleUpdate(name=user_role_in_db2.name)
        )


def test_update_user_role_missing(updated_user_role: UserRoleUpdate):
    """
    Test update user role missing

    Args:
        updated_user_role (UserRoleUpdate): User role update object
    """
    with raises(Missing):
        user_role.update_user_role(str(faker.uuid4()), updated_user_role)


def test_delete_user_role(new_user_role1: UserRoleCreate):
    """
    Test delete user role

    Args:
        new_user_role (UserRoleCreate): User role create object
    """
    user_role_in_db = user_role.create_user_role(new_user_role1)
    user_role.delete_user_role(user_role_in_db.id)
    with raises(Missing):
        user_role.get_user_role_by_id(user_role_in_db.id)


def test_delete_user_role_missing():
    """
    Test delete user role missing
    """
    with raises(Missing):
        user_role.delete_user_role(str(faker.uuid4()))
