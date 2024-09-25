"""
Blog service

This module contains functions to interact with the blog data
"""

from model.blog import BlogInDB, BlogCreate, BlogUpdate
from data import blog


def create_blog(new_blog: BlogCreate) -> BlogInDB:
    """
    Create a new blog

    Args:
        new_blog (BlogCreate): BlogCreate object

    Returns:
        BlogInDB: BlogInDB object
    """
    try:
        return blog.create_blog(new_blog)
    except Exception as e:
        raise e


def get_blog_by_id(id: str) -> BlogInDB:
    """
    Get a blog by id

    Args:
        id (str): id of the blog

    Returns:
        BlogInDB: BlogInDB object
    """
    try:
        return blog.get_blog_by_id(id)
    except Exception as e:
        raise e


def get_all_blogs() -> list[BlogInDB]:
    """
    Get all blogs

    Returns:
        List[BlogInDB]: List of BlogInDB objects
    """
    try:
        return blog.get_all_blogs()
    except Exception as e:
        raise e


def update_blog(updated_blog: BlogUpdate) -> BlogInDB:
    """
    Update a blog

    Args:
        blog (BlogUpdate): BlogUpdate object

    Returns:
        BlogInDB: BlogInDB object
    """
    try:
        return blog.update_blog(updated_blog)
    except Exception as e:
        raise e


def delete_blog(id: str) -> None:
    """
    Delete a blog

    Args:
        id (str): id of the blog
    """
    try:
        delete_blog = blog.get_blog_by_id(id)
        blog.delete_blog(delete_blog)
    except Exception as e:
        raise e
