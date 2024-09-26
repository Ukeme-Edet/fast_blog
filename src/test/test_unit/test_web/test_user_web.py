"""
Unit tests for user web

This module contains the unit tests for the user web module.
"""

from pytest import fixture, raises, mark
from faker import Faker
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from httpx import Response
from model.user import UserCreate, UserInDB, UserOut, UserUpdate
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
def new_user_update() -> UserUpdate:
    """
    Create a new user update

    Returns:
        UserUpdate: A new user update
    """
    return UserUpdate(
        id=str(Faker().uuid4()),
        username="".join(Faker().random_letters(20)),
        password=Faker().password(),
    )


@mark.anyio
async def test_create_user(app: FastAPI, new_user: UserCreate):
    """
    Test create user

    Args:
        new_user (UserCreate): A new user
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.post(
            "/user/", json=new_user.model_dump()
        )
        assert response.status_code == 200
        user = UserOut(**response.json())
        assert user.username == new_user.username


@mark.anyio
async def test_create_user_duplicate(app: FastAPI, new_user: UserCreate):
    """
    Test create user duplicate

    Args:
        new_user (UserCreate): A new user
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post("/user/", json=new_user.model_dump())
        response: Response = await ac.post(
            "/user/", json=new_user.model_dump()
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already exists"
