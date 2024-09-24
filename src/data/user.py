from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel, Session, select, Relationship
from . import engine


class User(SQLModel, table=True):
    id: str = Field(
        primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    username: str = Field(index=True, unique=True)
    password_hash: str = Field()
    time_created: datetime = Field(default=datetime.now())
    time_updated: datetime = Field(default=datetime.now())
    blogs: list["Blog"] = Relationship(back_populates="user")


def get_user_by_username(username: str):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == username)
        ).first()
        return user


def get_user_by_id(id: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == id)).first()
        return user


def get_all_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def update_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def delete_user(user: User):
    with Session(engine) as session:
        session.delete(user)
        session.commit()
        return user
