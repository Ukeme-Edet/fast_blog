"""
Unit tests for user web

This module contains the unit tests for the user web module.
"""

from pytest import fixture, mark
from faker import Faker
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from httpx import Response
from model.user import UserCreate, UserOut, UserUpdate
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
        username=faker.user_name(),
        password=Faker().password(),
    )


@mark.anyio
async def test_user_root(app: FastAPI):
    """
    Test user root
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get("/api/user/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "User"}


@mark.anyio
async def test_get_all_users(app: FastAPI, new_user_in_db: UserOut):
    """
    Test get all users

    Args:
        new_user_in_db (UserOut): A new user in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get("/api/user/all")
        assert response.status_code == 200
        users = [UserOut(**u) for u in response.json()]
        assert len(users) >= 1
        assert new_user_in_db in users


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
            "/api/user/", json=new_user.model_dump()
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
        await ac.post("/api/user/", json=new_user.model_dump())
        response: Response = await ac.post(
            "/api/user/", json=new_user.model_dump()
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already exists"


@mark.anyio
async def test_get_user_by_id(app: FastAPI, new_user_in_db: UserOut):
    """
    Test get user by id

    Args:
        new_user_in_db (UserOut): A new user in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get(f"/api/user/{new_user_in_db.id}")
        assert response.status_code == 200
        user = UserOut(**response.json())
        assert user.username == new_user_in_db.username


@mark.anyio
async def test_get_user_by_id_missing(app: FastAPI):
    """
    Test get user by id missing
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get("/api/user/123")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


@mark.anyio
async def test_get_user_by_username(app: FastAPI, new_user_in_db: UserOut):
    """
    Test get user by username

    Args:
        new_user_in_db (UserOut): A new user in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get(
            f"/api/user/username/{new_user_in_db.username}"
        )
        assert response.status_code == 200
        user = UserOut(**response.json())
        assert user.username == new_user_in_db.username


@mark.anyio
async def test_get_user_by_username_missing(app: FastAPI):
    """
    Test get user by username missing
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get("/api/user/username/123")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


@mark.anyio
async def test_update_user(
    app: FastAPI, new_user_in_db: UserOut, new_user_update: UserUpdate
):
    """
    Test update user

    Args:
        new_user_in_db (UserOut): A new user in db
        new_user_update (UserUpdate): A new user update
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        new_user_update.id = new_user_in_db.id
        response: Response = await ac.patch(
            f"/api/user/{new_user_in_db.id}", json=new_user_update.model_dump()
        )
        assert response.status_code == 200
        user = UserOut(**response.json())
        assert user.username == new_user_update.username


@mark.anyio
async def test_update_user_missing(app: FastAPI, new_user_update: UserUpdate):
    """
    Test update user missing

    Args:
        new_user_update (UserUpdate): A new user update
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.patch(
            f"/api/user/{new_user_update.id}",
            json=new_user_update.model_dump(),
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


@mark.anyio
async def test_update_user_duplicate(
    app: FastAPI,
    new_user: UserCreate,
    new_user_in_db: UserOut,
    new_user_update: UserUpdate,
):
    """
    Test update user duplicate

    Args:
        new_user_in_db (UserOut): A new user in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        this_user = await ac.post("/api/user/", json=new_user.model_dump())
        new_user_update.id = this_user.json()["id"]
        print(new_user_update.model_dump())
        new_user_update.username = new_user_in_db.username
        response: Response = await ac.patch(
            f"/api/user/{new_user_update.id}",
            json=new_user_update.model_dump(),
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already exists"


@mark.anyio
async def test_delete_user(app: FastAPI, new_user_in_db: UserOut):
    """
    Test delete user

    Args:
        new_user_in_db (UserOut): A new user in db
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        id = new_user_in_db.id
        response: Response = await ac.delete(f"/api/user/{id}")
        assert response.status_code == 200
        response: Response = await ac.get(f"/api/user/{id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


@mark.anyio
async def test_delete_user_missing(app: FastAPI):
    """
    Test delete user missing
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.delete("/api/user/123")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
