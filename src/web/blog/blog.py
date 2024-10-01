"""
Blog API endpoints

This module contains the blog API endpoints
"""

from fastapi import APIRouter, HTTPException, status
from errors.errors import Duplicate, Missing
from model.blog import BlogCreate, BlogOut, BlogUpdate
from service import blog as blog_service

blog = APIRouter(prefix="/blog", tags=["blog"])


@blog.get("/")
async def blog_root():
    """
    Root endpoint
    """
    return {"Hello": "Blog"}


@blog.get("/all")
async def read_all_blogs() -> list[BlogOut]:
    """
    Get all blogs

    Returns:
        List[BlogOut]: List of BlogOut objects
    """
    try:
        return blog_service.get_all_blogs()
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )


@blog.post("/", status_code=status.HTTP_201_CREATED)
async def create_blog(blog: BlogCreate) -> BlogOut:
    """
    Create a new blog

    Args:
        blog (BlogCreate): BlogCreate object

    Returns:
        BlogOut: BlogOut object
    """
    try:
        return blog_service.create_blog(blog)
    except Duplicate as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@blog.get("/{blog_id}")
async def read_blog(blog_id: str) -> BlogOut:
    """
    Get a blog by id

    Args:
        blog_id (str): id of the blog

    Returns:
        BlogOut: BlogOut object
    """
    try:
        return blog_service.get_blog_by_id(blog_id)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )


@blog.get("/user/{user_id}")
async def read_blog_by_user(user_id: str) -> list[BlogOut]:
    """
    Get a blog by user

    Args:
        user_id (str): id of the user

    Returns:
        List[BlogOut]: List of BlogOut objects
    """
    try:
        return blog_service.get_blogs_by_user_id(user_id)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )


@blog.patch("/{blog_id}")
async def update_blog(blog_id: str, blog: BlogUpdate) -> BlogOut:
    """
    Update a blog

    Args:
        blog_id (str): id of the blog
        blog (BlogUpdate): BlogUpdate object

    Returns:
        BlogOut: BlogOut object
    """
    blog.id = blog_id
    try:
        return blog_service.update_blog(blog)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )


@blog.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: str):
    """
    Delete a blog

    Args:
        blog_id (str): id of the blog
    """
    try:
        blog_service.delete_blog(blog_id)
    except Missing as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
