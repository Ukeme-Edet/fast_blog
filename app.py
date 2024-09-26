"""
This is the main file for the application.

This file is responsible for creating the FastAPI application and running it.
"""

from web import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
