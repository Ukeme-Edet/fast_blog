"""
This module contains the Config class which is responsible for loading the environment variables and returning the
"""

from dotenv import load_dotenv
import os


class Config:
    """
    Config class
    """

    def __init__(self):
        """
        Constructor
        """
        roles_permissions = {
            "admin": ["create", "read", "update", "delete"],
            "user": ["create", "read", "update"],
        }

    def get_db_uri(self):
        """
        Get the database URI
        """
        load_dotenv()
        if os.getenv("ENV") == "dev":
            return os.getenv("DEV_DB_URI", "sqlite:///dev.db")
        elif os.getenv("ENV") == "test":
            return os.getenv("TEST_DB_URI", "sqlite:///:memory:")
        else:
            return os.getenv("PROD_DB_URI", "sqlite:///prod.db")
