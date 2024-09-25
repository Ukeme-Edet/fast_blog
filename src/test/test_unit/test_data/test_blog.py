from pytest import fixture, raises
import os
from faker import Faker

from errors.errors import Duplicate, Missing

os.environ["ENV"] = "test"
from data import blog, user
from model.blog import BlogInDB, BlogCreate, BlogUpdate
from model.user import UserInDB, UserCreate

faker = Faker()


@fixture
def this_user() -> UserInDB:
    return user.create_user(
        UserCreate(username=faker.first_name(), password=faker.password())
    )


@fixture
def new_blog(this_user: UserInDB) -> BlogCreate:
    return BlogCreate(
        user_id=this_user.id,
        title=faker.sentence(),
        content=faker.text(),
    )


@fixture
def updated_blog() -> BlogUpdate:
    return BlogUpdate(
        id=faker.uuid4(),
        title=faker.sentence(),
        content=faker.text(),
        time_updated=faker.date_time(),
    )


def test_create_blog(new_blog: BlogCreate):
    created_blog = blog.create_blog(new_blog)
    assert created_blog.title == new_blog.title
    assert created_blog.content == new_blog.content
    assert created_blog.user_id == new_blog.user_id


def test_update_blog(new_blog: BlogCreate, updated_blog: BlogUpdate):
    created_blog = blog.create_blog(new_blog)
    updated_blog.id = created_blog.id
    blog.update_blog(updated_blog)
    blog_by_id = blog.get_blog_by_id(created_blog.id)
    assert blog_by_id.title == updated_blog.title
    assert blog_by_id.content == updated_blog.content
    assert blog_by_id.time_updated != updated_blog.time_updated


def test_update_blog_missing(updated_blog: BlogUpdate):
    with raises(Missing) as exc_info:
        blog.update_blog(updated_blog)
    assert exc_info.value.msg == f"Blog with id {updated_blog.id!r} not found"


def test_delete_blog(new_blog: BlogCreate):
    created_blog = blog.create_blog(new_blog)
    blog.delete_blog(created_blog)
    with raises(Missing) as exc_info:
        blog.get_blog_by_id(created_blog.id)
    assert exc_info.value.msg == f"Blog with id {created_blog.id!r} not found"
