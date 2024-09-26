"""
User API

This module contains the user API
"""

from fastapi import APIRouter, HTTPException, status
from errors.errors import Duplicate, Missing
from model.user import UserCreate, UserOut, UserUpdate
from service import user as user_service

user = APIRouter(prefix="/user", tags=["user"])


@user.get("/")
async def user_root():
    """
    Root endpoint
    """
    return {"Hello": "User"}


@user.get("/all")
async def read_all_users() -> list[UserOut]:
    """
    Get all users

    Returns:
        List[UserOut]: List of UserOut objects
    """
    return user_service.get_all_users()


@user.get("/{user_id}")
async def read_user(user_id: str) -> UserOut:
    """
    Get a user by id

    Args:
        user_id (str): id of the user

    Returns:
        UserOut: UserOut object
    """
    try:
        return user_service.get_user_by_id(user_id)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@user.get("/username/{username}")
async def read_user_by_username(username: str) -> UserOut:
    """
    Get a user by username

    Args:
        username (str): username of the user

    Returns:
        UserOut: UserOut object
    """
    try:
        return user_service.get_user_by_username(username)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@user.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate) -> UserOut:
    """
    Create a new user

    Args:
        user_create (UserCreate): UserCreate object

    Returns:
        UserOut: UserOut object
    """
    try:
        return user_service.create_user(user_create)
    except Duplicate as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )


@user.patch(
    "/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK
)
async def update_user(user_id: str, user_update: UserUpdate) -> UserOut:
    """
    Update a user

    Args:
        user_id (str): id of the user
        user_update (UserUpdate): UserUpdate object

    Returns:
        UserOut: UserOut object
    """
    user_update.id = user_id
    try:
        return user_service.update_user(user_update)
    except (Missing, Duplicate) as e:
        if isinstance(e, Missing):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        elif isinstance(e, Duplicate):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )


@user.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Delete a user

    Args:
        user_id (str): id of the user
    """
    try:
        return user_service.delete_user(user_id)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
