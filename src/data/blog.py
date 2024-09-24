import uuid
from sqlmodel import Field, SQLModel, Session, select, Relationship
from datetime import datetime
from . import engine


class Blog(SQLModel, table=True):
    id: str = Field(
        primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    user_id: str = Field(foreign_key="user.id")
    title: str = Field()
    content: str = Field()
    time_created: datetime = Field(default=datetime.now())
    time_updated: datetime = Field(default=datetime.now())
    user: "User" = Relationship(back_populates="blogs")


def get_blog_by_id(id: str):
    with Session(engine) as session:
        blog = session.exec(select(Blog).where(Blog.id == id)).first()
        return blog


def get_blogs_by_user_id(user_id: str):
    with Session(engine) as session:
        blogs = session.exec(select(Blog).where(Blog.user_id == user_id)).all()
        return blogs


def get_all_blogs():
    with Session(engine) as session:
        blogs = session.exec(select(Blog)).all()
        return blogs


def create_blog(blog: Blog):
    with Session(engine) as session:
        session.add(blog)
        session.commit()
        session.refresh(blog)
        return blog


def update_blog(blog: Blog):
    with Session(engine) as session:
        session.add(blog)
        session.commit()
        session.refresh(blog)
        return blog


def delete_blog(blog: Blog):
    with Session(engine) as session:
        session.delete(blog)
        session.commit()
        return blog
