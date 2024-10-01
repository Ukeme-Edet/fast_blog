"""
Unit tests for blog data

This file contains the unit tests for the blog data.
"""

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
    """
    Create a user

    Returns:
        UserInDB: UserInDB object
    """
    return user.create_user(
        UserCreate(
            username=faker.user_name(),
            password=faker.password(),
        )
    )


@fixture
def new_blog(this_user: UserInDB) -> BlogCreate:
    """
    Create a blog

    Args:
        this_user (UserInDB): UserInDB object

    Returns:
        BlogCreate: BlogCreate object
    """
    return BlogCreate(
        user_id=this_user.id,
        title=faker.sentence(),
        content=faker.text(),
    )


@fixture
def updated_blog() -> BlogUpdate:
    """
    Create an updated blog

    Returns:
        BlogUpdate: BlogUpdate object
    """
    return BlogUpdate(
        id=str(faker.uuid4()), title=faker.sentence(), content=faker.text()
    )


def test_create_blog(new_blog: BlogCreate):
    """
    Test create blog

    Args:
        new_blog (BlogCreate): BlogCreate object
    """
    created_blog = blog.create_blog(new_blog)
    assert created_blog.title == new_blog.title
    assert created_blog.content == new_blog.content
    assert created_blog.user_id == new_blog.user_id


def test_get_blog_by_id(new_blog: BlogCreate):
    """
    Test get blog by id

    Args:
        new_blog (BlogCreate): BlogCreate object
    """
    created_blog = blog.create_blog(new_blog)
    blog_by_id = blog.get_blog_by_id(created_blog.id)
    assert blog_by_id.title == new_blog.title
    assert blog_by_id.content == new_blog.content
    assert blog_by_id.user_id == new_blog.user_id


def test_get_blog_by_id_missing():
    """
    Test get blog by id missing
    """
    with raises(Missing) as exc_info:
        id = str(faker.uuid4())
        blog.get_blog_by_id(id)
    assert exc_info.value.msg == f"Blog with id {id!r} not found"


def test_get_blogs_by_user_id(new_blog: BlogCreate):
    """
    Test get blogs by user id

    Args:
        new_blog (BlogCreate): BlogCreate object
    """
    created_blog = blog.create_blog(new_blog)
    blogs_by_user_id = blog.get_blogs_by_user_id(created_blog.user_id)
    assert len(blogs_by_user_id) == 1
    assert blogs_by_user_id[0].title == new_blog.title
    assert blogs_by_user_id[0].content == new_blog.content
    assert blogs_by_user_id[0].user_id == new_blog.user_id


def test_get_blog_by_user_id_missing():
    """
    Test get blog by user id missing
    """
    with raises(Missing) as exc_info:
        user_id = str(faker.uuid4())
        blog.get_blogs_by_user_id(user_id)
    assert exc_info.value.msg == f"Blogs with user id {user_id!r} not found"


def test_get_all_blogs(new_blog: BlogCreate):
    """
    Test get all blogs

    Args:
        new_blog (BlogCreate): BlogCreate object
    """
    created_blog = blog.create_blog(new_blog)
    all_blogs = blog.get_all_blogs()
    assert len(all_blogs) >= 1
    assert any([b.title == new_blog.title for b in all_blogs])


def test_update_blog(new_blog: BlogCreate, updated_blog: BlogUpdate):
    """
    Test update blog

    Args:
        new_blog (BlogCreate): BlogCreate object
        updated_blog (BlogUpdate): BlogUpdate object
    """
    created_blog = blog.create_blog(new_blog)
    updated_blog.id = created_blog.id
    blog.update_blog(updated_blog)
    blog_by_id = blog.get_blog_by_id(created_blog.id)
    assert blog_by_id.title == updated_blog.title
    assert blog_by_id.content == updated_blog.content
    assert blog_by_id.time_updated != created_blog.time_updated


def test_update_blog_missing(updated_blog: BlogUpdate):
    """
    Test update blog missing

    Args:
        updated_blog (BlogUpdate): BlogUpdate object
    """
    with raises(Missing) as exc_info:
        blog.update_blog(updated_blog)
    assert exc_info.value.msg == f"Blog with id {updated_blog.id!r} not found"


def test_delete_blog(new_blog: BlogCreate):
    """
    Test delete blog

    Args:
        new_blog (BlogCreate): BlogCreate object
    """
    created_blog = blog.create_blog(new_blog)
    blog.delete_blog(created_blog)
    with raises(Missing) as exc_info:
        blog.get_blog_by_id(created_blog.id)
    assert exc_info.value.msg == f"Blog with id {created_blog.id!r} not found"
