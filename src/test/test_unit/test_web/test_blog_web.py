"""
Unit tests for blog web

This module contains the unit tests for the blog web module.
"""

from pytest import fixture, mark
from faker import Faker
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from httpx import Response
import os

os.environ["ENV"] = "prod"
from model.user import UserCreate, UserOut
from model.blog import BlogCreate, BlogOut, BlogUpdate
from service import blog as blog_service
from service import user as user_service
from web import create_app

faker = Faker()


@fixture
def app() -> FastAPI:
    """
    Create a new FastAPI app

    Returns:
        FastAPI: A FastAPI app
    """
    return create_app()


@fixture
def new_user_in_db() -> UserOut:
    """
    Create a new user in db

    Returns:
        UserInDB: A new user in db
    """
    return user_service.create_user(
        UserCreate(
            username=faker.user_name(),
            password=faker.password(),
        )
    )


@fixture
def new_blog(new_user_in_db: UserOut) -> BlogCreate:
    """
    Create a new blog

    Args:
        new_user_in_db (UserOut): A new user in db

    Returns:
        BlogCreate: A new blog
    """
    return BlogCreate(
        title=faker.sentence(),
        content=faker.text(),
        user_id=new_user_in_db.id,
    )


@fixture
def new_blog_in_db(new_user_in_db: UserOut) -> BlogOut:
    """
    Create a new blog in db

    Args:
        new_user_in_db (UserOut): A new user in db

    Returns:
        BlogOut: A new blog in db
    """
    return blog_service.create_blog(
        BlogCreate(
            title=faker.sentence(),
            content=faker.text(),
            user_id=new_user_in_db.id,
        )
    )


@fixture
def new_blog_update() -> BlogUpdate:
    """
    Create a new blog update

    Args:
        new_user_in_db (UserOut): A new user in db

    Returns:
        BlogUpdate: A new blog update
    """
    return BlogUpdate(
        id=str(faker.uuid4()),
        title=faker.sentence(),
        content=faker.text(),
    )


@mark.anyio
async def test_create_blog(
    app: FastAPI, new_user_in_db: UserOut, new_blog: BlogCreate
):
    """
    Test create blog

    Args:
        app (FastAPI): A FastAPI app
        new_user_in_db (UserOut): A new user in db
        new_blog (BlogCreate): A new blog
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.post(
            f"/api/blog/", json=new_blog.model_dump()
        )
        assert response.status_code == 201
        blog = BlogOut(**response.json())
        assert blog.title == new_blog.title
        assert blog.content == new_blog.content
        assert blog.user_id == new_user_in_db.id


@mark.anyio
async def test_create_blog_invalid(app: FastAPI, new_user_in_db: UserOut):
    """
    Test create blog invalid

    Args:
        app (FastAPI): A FastAPI app
        new_user_in_db (UserOut): A new user in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.post(
            f"/api/blog/",
            json={"title": "a", "content": "b", "user_id": new_user_in_db.id},
        )
        assert response.status_code == 422


@mark.anyio
async def test_read_blog(app: FastAPI, new_blog_in_db: BlogOut):
    """
    Test read blog

    Args:
        app (FastAPI): A FastAPI app
        new_blog_in_db (BlogOut): A new blog in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get(f"/api/blog/{new_blog_in_db.id}")
        assert response.status_code == 200
        blog = BlogOut(**response.json())
        assert blog == new_blog_in_db


@mark.anyio
async def test_read_blog_missing(app: FastAPI):
    """
    Test read blog missing

    Args:
        app (FastAPI): A FastAPI app
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get(f"/api/blog/{faker.uuid4()}")
        assert response.status_code == 404


@mark.anyio
async def test_read_blog_by_user(app: FastAPI, new_blog_in_db: BlogOut):
    """
    Test read blog by user

    Args:
        app (FastAPI): A FastAPI app
        new_blog_in_db (BlogOut): A new blog in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get(
            f"/api/blog/user/{new_blog_in_db.user_id}"
        )
        assert response.status_code == 200
        blogs = [BlogOut(**b) for b in response.json()]
        assert len(blogs) >= 1
        assert new_blog_in_db in blogs


@mark.anyio
async def test_read_blog_by_user_missing(app: FastAPI):
    """
    Test read blog by user missing

    Args:
        app (FastAPI): A FastAPI app
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get(f"/api/blog/user/{faker.uuid4()}")
        assert response.status_code == 404


@mark.anyio
async def test_read_all_blogs(
    app: FastAPI, new_blog_in_db: BlogOut, new_blog: BlogCreate
):
    """
    Test read all blogs

    Args:
        app (FastAPI): A FastAPI app
        new_blog_in_db (BlogOut): A new blog in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get("/api/blog/all")
        print(response.json())
        assert response.status_code == 200
        blogs = [BlogOut(**b) for b in response.json()]
        assert len(blogs) >= 1
        assert new_blog_in_db in blogs


@mark.anyio
async def test_update_blog(
    app: FastAPI, new_blog_in_db: BlogOut, new_blog_update: BlogUpdate
):
    """
    Test update blog

    Args:
        app (FastAPI): A FastAPI app
        new_blog_in_db (BlogOut): A new blog in db
        new_blog_update (BlogUpdate): A new blog update
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.patch(
            f"/api/blog/{new_blog_in_db.id}", json=new_blog_update.model_dump()
        )
        assert response.status_code == 200
        blog = BlogOut(**response.json())
        assert blog.title == new_blog_update.title
        assert blog.content == new_blog_update.content
        assert blog.user_id == new_blog_in_db.user_id


@mark.anyio
async def test_update_blog_missing(app: FastAPI, new_blog_update: BlogUpdate):
    """
    Test update blog missing

    Args:
        app (FastAPI): A FastAPI app
        new_blog_update (BlogUpdate): A new blog update
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.patch(
            f"/api/blog/{faker.uuid4()}", json=new_blog_update.model_dump()
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Blog not found"


@mark.anyio
async def test_update_blog_invalid(app: FastAPI, new_blog_in_db: BlogOut):
    """
    Test update blog invalid

    Args:
        app (FastAPI): A FastAPI app
        new_blog_in_db (BlogOut): A new blog in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.patch(
            f"/api/blog/{new_blog_in_db.id}",
            json={
                "title": "a",
                "content": "b",
                "user_id": new_blog_in_db.user_id,
            },
        )
        assert response.status_code == 422
