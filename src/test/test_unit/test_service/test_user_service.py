from pytest import fixture, raises
from faker import Faker
import os

os.environ["ENV"] = "test"
from service import user
from errors.errors import Duplicate, Missing
from model.user import UserCreate, UserUpdate

faker = Faker()


@fixture
def new_user() -> UserCreate:
    return UserCreate(username=faker.user_name(), password=faker.password())


@fixture
def updated_user() -> UserUpdate:
    return UserUpdate(
        id=str(faker.uuid4()),
        username=faker.user_name(),
        password=faker.password(),
    )


def test_create_user(new_user: UserCreate):
    created_user = user.create_user(new_user)
    assert created_user.username == new_user.username


def test_create_user_duplicate(new_user: UserCreate):
    user.create_user(new_user)
    with raises(Duplicate) as exc_info:
        user.create_user(new_user)
    assert (
        exc_info.value.msg
        == f"User with username {new_user.username!r} already exists"
    )


def test_get_user_by_id(new_user: UserCreate):
    created_user = user.create_user(new_user)
    user_by_id = user.get_user_by_id(created_user.id)
    assert user_by_id.username == new_user.username


def test_get_user_by_username(new_user: UserCreate):
    created_user = user.create_user(new_user)
    user_by_username = user.get_user_by_username(created_user.username)
    assert user_by_username.username == new_user.username


def test_get_all_users(new_user: UserCreate):
    user.create_user(new_user)
    all_users = user.get_all_users()
    assert len(all_users) > 0
    assert any(user.username == new_user.username for user in all_users)


def test_get_user_by_id_missing():
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        user.get_user_by_id(id)
    assert exc_info.value.msg == f"User with id {id!r} not found"


def test_get_user_by_username_missing():
    with raises(Missing) as exc_info:
        username = faker.user_name()
        user.get_user_by_username(username)
    assert exc_info.value.msg == f"User with username {username!r} not found"


def test_update_user(new_user: UserCreate, updated_user: UserUpdate):
    created_user = user.create_user(new_user)
    updated_user.id = created_user.id
    updated_user.username = faker.user_name()
    updated_user.password = faker.password()
    user.update_user(updated_user)
    user_by_id = user.get_user_by_id(created_user.id)
    assert user_by_id.username == updated_user.username


def test_update_user_missing(new_user: UserCreate, updated_user: UserUpdate):
    with raises(Missing) as exc_info:
        updated_user.id = str(faker.uuid4())
        user.update_user(updated_user)
    assert exc_info.value.msg == f"User with id {updated_user.id!r} not found"


def test_update_user_duplicate(new_user: UserCreate, updated_user: UserUpdate):
    user.create_user(new_user)
    created_user = user.create_user(
        UserCreate(username=faker.user_name(), password=faker.password())
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
    created_user = user.create_user(new_user)
    user.delete_user(created_user.id)
    with raises(Missing) as exc_info:
        user.get_user_by_id(created_user.id)
    assert exc_info.value.msg == f"User with id {created_user.id!r} not found"


def test_delete_user_missing():
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        user.delete_user(id)
    assert exc_info.value.msg == f"User with id {id!r} not found"
