"""
This file is used to create the database engine and to import the models.
"""

from bcrypt import gensalt, hashpw
from config import Config
from sqlmodel import SQLModel, Session, create_engine, select

DB_URI = Config().get_db_uri()

engine = create_engine(DB_URI, echo=True)

from .user_role import UserRole
from .user import User
from .blog import Blog

SQLModel.metadata.create_all(engine)

with engine.connect() as connection:
    user_roles = [
        UserRole(name="admin"),
        UserRole(name="user"),
        UserRole(name="moderator"),
    ]
    # Add roles if they do not exist
    with Session(engine) as session:
        for role in user_roles:
            if not session.exec(
                select(UserRole).where(UserRole.name == role.name)
            ).first():
                try:
                    session.add(role)
                    session.commit()
                    print(f"Added role {role.name}")
                except Exception as e:
                    print(e)
                    session.rollback()
                    raise e
            else:
                print(f"Role {role.name} already exists")
    print("Roles added")
    # Add admin user if it does not exist
    admin_role = session.exec(
        select(UserRole).where(UserRole.name == "admin")
    ).first()
    if not session.exec(select(User).where(User.username == "admin")).first():
        try:
            admin = User(
                username="admin",
                password_hash=hashpw(
                    "admin".encode("utf-8"), gensalt()
                ).decode("utf-8"),
                role_id=admin_role.id if admin_role else "lol",
            )
            session.add(admin)
            session.commit()
            print("Added admin user")
        except Exception as e:
            print(e)
            session.rollback()
            raise e
    else:
        print("Admin user already exists")
