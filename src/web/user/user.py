from fastapi import APIRouter, Depends, HTTPException, status
from errors.errors import Duplicate, Missing
from model.user import UserCreate, UserOut, UserUpdate
from service import user as user_service

user = APIRouter(prefix="/user", tags=["user"])


@user.get("/")
async def user_root():
    return {"Hello": "User"}


@user.get("/all")
async def read_all_users() -> list[UserOut]:
    return user_service.get_all_users()


@user.get("/{user_id}")
async def read_user(user_id: str) -> UserOut:
    try:
        return user_service.get_user_by_id(user_id)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@user.get("/username/{username}")
async def read_user_by_username(username: str) -> UserOut:
    try:
        return user_service.get_user_by_username(username)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@user.post("/")
async def create_user(user_create: UserCreate) -> UserOut:
    try:
        return user_service.create_user(user_create)
    except Duplicate as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )


@user.patch("/{user_id}")
async def update_user(user_id: str, user_update: UserUpdate) -> UserOut:
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


@user.delete("/{user_id}")
async def delete_user(user_id: str):
    try:
        return user_service.delete_user(user_id)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
