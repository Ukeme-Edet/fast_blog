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
from model.user_role import UserRoleCreate, UserRoleInDB, UserRoleUpdate


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
    role_id: str = Field(min_length=2, foreign_key="user_role.id")
    time_created: datetime = Field(default=datetime.now())
    time_updated: datetime = Field(default=datetime.now())
    blogs: list["Blog"] = Relationship(back_populates="user")
    role: "UserRole" = Relationship(back_populates="users")


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
        from data.user_role import get_user_role_by_name

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
                role_id=get_user_role_by_name("user").id,
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


def get_role_by_user_id(user_id: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if user:
            return user.role_id
        raise Missing(msg=f"User with id {user_id!r} not found")


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


def create_user_role(user_role: UserRoleCreate) -> UserRoleInDB:
    """
    Create a new user role

    Args:
        user_role (UserRoleCreate): UserRoleCreate object

    Returns:
        UserRoleInDB: UserRoleInDB object
    """
    from data.user_role import create_user_role

    return create_user_role(user_role)


def get_user_role_by_id(role_id: str) -> UserRoleInDB:
    """
    Get a user role by id

    Args:
        role_id (str): id of the user role

    Returns:
        UserRoleInDB: UserRoleInDB object
    """
    from data.user_role import get_user_role_by_id

    return get_user_role_by_id(role_id)


def get_user_role_by_name(name: str) -> UserRoleInDB:
    """
    Get a user role by name

    Args:
        name: str - name of the user role

    Returns:
        UserRoleInDB: UserRoleInDB object
    """
    from data.user_role import get_user_role_by_name

    return get_user_role_by_name(name)


def get_all_user_roles() -> list[UserRoleInDB]:
    """
    Get all user roles

    Returns:
        list[UserRoleInDB]: List of UserRoleInDB objects
    """
    from data.user_role import get_all_user_roles

    return get_all_user_roles()


def update_user_role(
    user_role_id: str, user_role: UserRoleUpdate
) -> UserRoleInDB:
    """
    Update a user role

    Args:
        user_role_id (str): id of the user role
        user_role (UserRoleCreate): UserRoleCreate object

    Returns:
        UserRoleInDB: UserRoleInDB object
    """
    from data.user_role import update_user_role

    return update_user_role(user_role_id, user_role)


def delete_user_role(user_role_id: str):
    """
    Delete a user role

    Args:
        user_role_id (str): id of the user role
    """
    from data.user_role import delete_user_role

    delete_user_role(user_role_id)


def user_role_update(user_id: str, role_name: str):
    """
    Update a user role

    Args:
        user_id (str): id of the user
        role_name (str): name of the role
    """
    from data.user_role import get_user_role_by_name

    with Session(engine) as session:
        try:
            user = session.exec(select(User).where(User.id == user_id)).first()
            if not user:
                raise Missing(msg=f"User with id {user_id!r} not found")
            role = get_user_role_by_name(role_name)
            user.role_id = role.id
            session.add(user)
            session.commit()
            session.refresh(user)
            return UserInDB(**user.model_dump())
        except Exception as e:
            session.rollback()
            raise e
