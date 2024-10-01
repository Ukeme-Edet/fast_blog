"""
User data access module.

This module contains the data access functions for the User model.
"""

from datetime import UTC, datetime
import uuid
from sqlmodel import Field, SQLModel, Session, select, Relationship
from model.user import UserCreate, UserInDB, UserUpdate
from bcrypt import hashpw, checkpw, gensalt

from errors.errors import Duplicate, Missing
from data import engine


class User(SQLModel, table=True):
    """
    User Table

    Attributes:
        id: str - primary key
        username: str - unique, index
        password_hash: str
        time_created: datetime
        time_updated: datetime
        blogs: list[Blog] - relationship
    """

    id: str = Field(
        primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    username: str = Field(
        primary_key=True, unique=True, index=True, min_length=2, max_length=100
    )
    password_hash: str = Field(min_length=2)
    time_created: datetime = Field(default=datetime.now())
    time_updated: datetime = Field(default=datetime.now())
    blogs: list["Blog"] = Relationship(back_populates="user")


def get_user_by_username(username: str) -> UserInDB:
    """
    Get a user by username

    Args:
        username (str): username of the user

    Returns:
        UserInDB: UserInDB object
    """
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == username)
        ).first()
        if user:
            return UserInDB(**user.model_dump())
        raise Missing(msg=f"User with username {username!r} not found")


def get_user_by_id(id: str):
    """
    Get a user by id

    Args:
        id (str): id of the user

    Returns:
        UserInDB: UserInDB object
    """
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == id)).first()
        if user:
            return user
        raise Missing(msg=f"User with id {id!r} not found")


def get_all_users() -> list[UserInDB]:
    """
    Get all users

    Returns:
        List[UserInDB]: List of UserInDB objects
    """
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return [UserInDB(**u.model_dump()) for u in users]


def create_user(user: UserCreate) -> UserInDB:
    """
    Create a new user

    Args:
        user (UserCreate): UserCreate object

    Returns:
        UserInDB: UserInDB object
    """
    with Session(engine) as session:
        try:
            # Check if username is unique
            if session.exec(
                select(User).where(User.username == user.username)
            ).first():
                raise Duplicate(
                    msg=f"User with username {user.username!r} already exists"
                )
            n_user = User(
                username=user.username,
                password_hash=hashpw(
                    user.password.encode("utf-8"), gensalt()
                ).decode("utf-8"),
                time_created=datetime.now(UTC),
                time_updated=datetime.now(UTC),
            )
            session.add(n_user)
            session.commit()
            session.refresh(n_user)
            return UserInDB(**n_user.model_dump())
        except Exception as e:
            print(e)
            session.rollback()
            raise e


def update_user(user: UserUpdate) -> UserInDB:
    """
    Update a user

    Args:
        user (UserUpdate): UserUpdate object

    Returns:
        UserInDB: UserInDB object
    """
    with Session(engine) as session:
        try:
            try:
                n_user = get_user_by_id(user.id)
            except Missing as e:
                raise e
            if user.username:
                try:
                    d_user = get_user_by_username(user.username)
                    if d_user.id != user.id:
                        raise Duplicate(
                            msg=f"User with username {user.username!r} already exists"
                        )
                except Missing:
                    pass
            if user.password:
                n_user.password_hash = hashpw(
                    user.password.encode("utf-8"), gensalt()
                ).decode("utf-8")
            if user.username:
                n_user.username = user.username
            n_user.time_updated = datetime.now(UTC)
            session.add(n_user)
            session.commit()
            session.refresh(n_user)
            return UserInDB(**n_user.model_dump())
        except Exception as e:
            session.rollback()
            raise e


def delete_user(user: UserInDB):
    """
    Delete a user

    Args:
        user (UserInDB): UserInDB object
    """
    with Session(engine) as session:
        try:
            n_user = session.exec(
                select(User).where(User.id == user.id)
            ).first()
            if not n_user:
                raise Missing(msg=f"User with id {user.id!r} not found")
            session.delete(n_user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
