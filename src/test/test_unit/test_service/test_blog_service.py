"""
Unit tests for blog service

This module contains unit tests for the blog service
"""

from pytest import fixture, raises
from faker import Faker
import os

os.environ["ENV"] = "test"
from model.user import UserCreate, UserInDB, UserOut
from service import blog, user
from errors.errors import Missing
from model.blog import BlogCreate, BlogUpdate

faker = Faker()


@fixture
def new_user() -> UserOut:
    """
    Create a new user

    Returns:
        UserOut: A new user
    """
    return user.create_user(
        UserCreate(
            username=faker.user_name(),
            password=faker.password(),
        )
    )


@fixture
def new_blog(new_user: UserInDB) -> BlogCreate:
    """
    Create a new blog

    Args:
        new_user (UserInDB): A new user

    Returns:
        BlogCreate: A new blog
    """
    return BlogCreate(
        title=faker.sentence(), content=faker.text(), user_id=new_user.id
    )


@fixture
def updated_blog() -> BlogUpdate:
    """
    Create an updated blog

    Returns:
        BlogUpdate: An updated blog
    """
    return BlogUpdate(
        id=str(faker.uuid4()), title=faker.sentence(), content=faker.text()
    )


def test_create_blog(new_blog: BlogCreate):
    """
    Test create blog

    Args:
        new_blog (BlogCreate): A new blog
    """
    created_blog = blog.create_blog(new_blog)
    assert created_blog.title == new_blog.title
    assert created_blog.content == new_blog.content


def test_get_blog_by_id(new_blog: BlogCreate):
    """
    Test get blog by id

    Args:
        new_blog (BlogCreate): A new blog
    """
    created_blog = blog.create_blog(new_blog)
    blog_by_id = blog.get_blog_by_id(created_blog.id)
    assert blog_by_id.title == new_blog.title
    assert blog_by_id.content == new_blog.content


def test_get_all_blogs(new_blog: BlogCreate):
    """
    Test get all blogs

    Args:
        new_blog (BlogCreate): A new blog
    """
    blog.create_blog(new_blog)
    all_blogs = blog.get_all_blogs()
    assert len(all_blogs) > 0


def test_update_blog(new_blog: BlogCreate, updated_blog: BlogUpdate):
    """
    Test update blog

    Args:
        new_blog (BlogCreate): A new blog
        updated_blog (BlogUpdate): An updated blog
    """
    created_blog = blog.create_blog(new_blog)
    updated_blog.id = created_blog.id
    blog_updated = blog.update_blog(updated_blog)
    assert blog_updated.title == updated_blog.title
    assert blog_updated.content == updated_blog.content
    assert blog_updated.time_created == created_blog.time_created
    assert blog_updated.time_updated != created_blog.time_updated


def test_update_blog_missing():
    """
    Test update blog missing
    """
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        blog.update_blog(
            BlogUpdate(id=id, title=faker.sentence(), content=faker.text())
        )
    assert exc_info.value.msg == f"Blog with id {id!r} not found"


def test_delete_blog(new_blog: BlogCreate):
    """
    Test delete blog

    Args:
        new_blog (BlogCreate): A new blog
    """
    created_blog = blog.create_blog(new_blog)
    blog.delete_blog(created_blog.id)
    with raises(Missing) as exc_info:
        blog.get_blog_by_id(created_blog.id)
    assert exc_info.value.msg == f"Blog with id {created_blog.id!r} not found"


def test_delete_blog_missing():
    """
    Test delete blog missing
    """
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        blog.delete_blog(id)
    assert exc_info.value.msg == f"Blog with id {id!r} not found"
