from datetime import UTC, datetime
import uuid
from sqlmodel import Field, SQLModel, Session, select, Relationship
from model.user import UserCreate, UserInDB, UserUpdate
from bcrypt import hashpw, checkpw, gensalt

from errors.errors import Duplicate, Missing
from data import engine
from model.blog import Blog


class User(SQLModel, table=True):
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
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == username)
        ).first()
        if user:
            return user
        raise Missing(msg=f"User with username {username!r} not found")


def get_user_by_id(id: str) -> UserInDB:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == id)).first()
        if user:
            return user
        raise Missing(msg=f"User with id {id!r} not found")


def get_all_users() -> list[UserInDB]:
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


def create_user(user: UserCreate) -> UserInDB:
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
            return n_user
        except Exception as e:
            session.rollback()
            raise e


def update_user(user: UserUpdate) -> UserInDB:
    with Session(engine) as session:
        try:
            try:
                n_user = get_user_by_id(user.id)
            except Missing as e:
                raise e
            try:
                get_user_by_username(user.username)
            except Missing:
                pass
            else:
                raise Duplicate(
                    f"User with username {user.username!r} already exists"
                )
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
            return n_user
        except Exception as e:
            session.rollback()
            raise e


def delete_user(user: UserInDB):
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
