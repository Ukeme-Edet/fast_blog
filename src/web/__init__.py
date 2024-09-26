"""
This package contains the web application.

The web application is a FastAPI application that serves the API and the web interface.
"""

from fastapi import FastAPI


def create_app():
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    from web.user import user

    app.include_router(user)

    return app
