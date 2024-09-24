from pytest import fixture
import os
from faker import Faker

os.environ["ENV"] = "test"
from data.blog import *
from data.user import *

faker = Faker()


@fixture
def user():
    user = User(username=faker.name(), password_hash=faker.name())
    return user


@fixture
def blog():
    blog = Blog(title="testtitle", content="testcontent")
    return blog


def test_get_all_blogs(blog: Blog, user: User):
    user = create_user(user)
    blog.user_id = user.id
    blog = create_blog(blog)
    assert blog in get_all_blogs()


def test_create_blog(blog: Blog, user: User):
    user = create_user(user)
    blog.user_id = user.id
    blog = create_blog(blog)
    assert get_blog_by_id(blog.id) == blog


def test_update_blog(blog: Blog, user: User):
    user = create_user(user)
    blog.user_id = user.id
    blog = create_blog(blog)
    blog.title = "newtitle"
    blog = update_blog(blog)
    assert get_blog_by_id(blog.id).title == "newtitle"


def test_delete_blog(blog: Blog, user: User):
    user = create_user(user)
    blog.user_id = user.id
    blog = create_blog(blog)
    blog = delete_blog(blog)
    assert get_blog_by_id(blog.id) is None


def test_get_blog_by_id(blog: Blog, user: User):
    user = create_user(user)
    blog.user_id = user.id
    blog = create_blog(blog)
    assert get_blog_by_id(blog.id) == blog


def test_get_blogs_by_user_id(blog: Blog, user: User):
    user = create_user(user)
    blog.user_id = user.id
    blog = create_blog(blog)
    assert get_blogs_by_user_id(user.id) == [blog]


def test_get_blog_by_id_none():
    assert get_blog_by_id("123") is None


def test_get_blogs_by_user_id_none():
    assert get_blogs_by_user_id("123") == []
