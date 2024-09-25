import uuid
from sqlmodel import Field, SQLModel, Session, select, Relationship
from datetime import UTC, datetime
from model.blog import Blog, BlogCreate, BlogUpdate, BlogInDB
from model.user import User
from errors.errors import Missing, Duplicate
from . import engine


class Blog(SQLModel, table=True):
    id: str = Field(
        primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    user_id: str = Field(foreign_key="user.id")
    title: str = Field(min_length=2, max_length=100, index=True)
    content: str = Field(min_length=2)
    time_created: datetime = Field(default=datetime.now())
    time_updated: datetime = Field(default=datetime.now())
    user: "User" = Relationship(back_populates="blogs")


def get_blog_by_id(id: str) -> BlogInDB:
    with Session(engine) as session:
        blog = session.exec(select(Blog).where(Blog.id == id)).first()
        if blog:
            return blog
        raise Missing(msg=f"Blog with id {id!r} not found")


def get_blogs_by_user_id(user_id: str):
    with Session(engine) as session:
        blogs = session.exec(select(Blog).where(Blog.user_id == user_id)).all()
        return blogs


def get_all_blogs():
    with Session(engine) as session:
        blogs = session.exec(select(Blog)).all()
        return blogs


def create_blog(blog: BlogCreate) -> BlogInDB:
    with Session(engine) as session:
        try:
            new_blog = Blog(
                id=str(uuid.uuid4()),
                time_created=datetime.now(UTC),
                time_updated=datetime.now(UTC),
                **blog.model_dump(),
            )
            session.add(new_blog)
            session.commit()
            session.refresh(new_blog)
            return new_blog
        except Exception as e:
            raise e


def update_blog(blog: BlogUpdate) -> BlogInDB:
    with Session(engine) as session:
        try:
            try:
                blog_db = get_blog_by_id(blog.id)
            except Missing as e:
                raise Missing(msg=f"Blog with id {blog.id!r} not found")
            if blog.title:
                blog_db.title = blog.title
            if blog.content:
                blog_db.content = blog.content
            blog_db.time_updated = datetime.now(UTC)
            session.add(blog_db)
            session.commit()
            session.refresh(blog_db)
            return blog_db
        except Exception as e:
            session.rollback()
            raise e


def delete_blog(blog: BlogInDB):
    with Session(engine) as session:
        try:
            try:
                blog_db = get_blog_by_id(blog.id)
            except Missing as e:
                raise e
            session.delete(blog_db)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
