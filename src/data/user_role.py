"""
User Role Data

This module contains the data layer for the User Role model.
"""

import uuid
from sqlmodel import Field, Relationship, SQLModel, Session, select
from model.user_role import UserRoleInDB, UserRoleCreate, UserRoleUpdate
from errors.errors import Missing, Duplicate
from . import engine


class UserRole(SQLModel, table=True):
    """
    User Role Table

    Attributes:
        id: str - primary key
        name: str
    """

    id: str = Field(
        primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    name: str = Field(min_length=2, max_length=100, unique=True, index=True)
    users: list["User"] = Relationship(back_populates="role_id")


def get_user_role_by_id(id: str) -> UserRoleInDB:
    """
    Get a user role by id

    Args:
        id: str - id of the user role

    Returns:
        UserRole: UserRole object
    """
    with Session(engine) as session:
        user_role = session.exec(
            select(UserRole).where(UserRole.id == id)
        ).first()
        if user_role:
            return UserRoleInDB(**user_role.model_dump())
        raise Missing(msg=f"User role with id {id!r} not found")


def get_user_role_by_name(name: str) -> UserRoleInDB:
    """
    Get a user role by name

    Args:
        name: str - name of the user role

    Returns:
        UserRole: UserRole object
    """
    with Session(engine) as session:
        user_role = session.exec(
            select(UserRole).where(UserRole.name == name)
        ).first()
        if user_role:
            return UserRoleInDB(**user_role.model_dump())
        raise Missing(msg=f"User role with name {name!r} not found")


def get_all_user_roles() -> list[UserRoleInDB]:
    """
    Get all user roles

    Returns:
        list[UserRole]: List of UserRole objects
    """
    with Session(engine) as session:
        user_roles = session.exec(select(UserRole)).all()
        return [
            UserRoleInDB(**user_role.model_dump()) for user_role in user_roles
        ]


def create_user_role(user_role_create: UserRoleCreate) -> UserRoleInDB:
    """
    Create a user role

    Args:
        user_role_create: UserRoleCreate - user role create object

    Returns:
        UserRole: UserRole object
    """
    user_role = UserRole.model_validate(user_role_create)
    with Session(engine) as session:
        try:
            session.add(user_role)
            session.commit()
            session.refresh(user_role)
            return UserRoleInDB(**user_role.model_dump())
        except Exception as e:
            session.rollback()
            raise Duplicate(
                msg=f"User role with name {user_role.name!r} exists"
            )


def update_user_role(
    id: str, user_role_update: UserRoleUpdate
) -> UserRoleInDB:
    """
    Update a user role

    Args:
        id: str - id of the user role
        user_role_update: UserRoleCreate - user role create object

    Returns:
        UserRole: UserRole object
    """
    with Session(engine) as session:
        user_role = session.exec(
            select(UserRole).where(UserRole.id == id)
        ).first()
        if user_role:
            if session.exec(
                select(UserRole).where(UserRole.name == user_role_update.name)
            ).first():
                raise Duplicate(
                    msg=f"User role with name {user_role_update.name!r} exists"
                )
            user_role.name = user_role_update.name
            session.add(user_role)
            session.commit()
            session.refresh(user_role)
            return UserRoleInDB(**user_role.model_dump())
        raise Missing(msg=f"User role with id {id!r} not found")


def delete_user_role(id: str) -> UserRoleInDB:
    """
    Delete a user role

    Args:
        id: str - id of the user role

    Returns:
        UserRole: UserRole object
    """
    with Session(engine) as session:
        user_role = session.exec(
            select(UserRole).where(UserRole.id == id)
        ).first()
        if user_role:
            session.delete(user_role)
            session.commit()
            return UserRoleInDB(**user_role.model_dump())
        raise Missing(msg=f"User role with id {id!r} not found")
