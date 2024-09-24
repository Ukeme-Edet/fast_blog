from dotenv import load_dotenv
import os


class Config:
    def __init__(self):
        pass

    def get_db_uri(self):
        load_dotenv()
        if os.getenv("ENV") == "dev":
            return os.getenv("DEV_DB_URI")
        elif os.getenv("ENV") == "test":
            return os.getenv("TEST_DB_URI")
        else:
            return os.getenv("PROD_DB_URI")
