from pytest import fixture
from faker import Faker
import os

os.environ["ENV"] = "test"
from data.user import *

faker = Faker()


@fixture
def user():
    user = User(username=faker.name(), password_hash=faker.name())
    return user


def test_get_all_users(user):
    user = create_user(user)
    assert user in get_all_users()


def test_create_user(user):
    user = create_user(user)
    assert get_user_by_id(user.id) == user


def update_user(user):
    user = create_user(user)
    user.username = "newusername"
    user = update_user(user)
    assert get_user_by_id(user.id).username == "newusername"


def test_delete_user(user):
    user = create_user(user)
    user = delete_user(user)
    assert get_user_by_id(user.id) is None


def test_get_user_by_username(user):
    user = create_user(user)
    assert get_user_by_username(user.username) == user


def test_get_user_by_id(user):
    user = create_user(user)
    assert get_user_by_id(user.id) == user


def test_get_user_by_id_none():
    assert get_user_by_id("123") is None


def test_get_user_by_username_none():
    assert get_user_by_username("123") is None
