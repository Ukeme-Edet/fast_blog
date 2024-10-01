"""
Blog service

This module contains functions to interact with the blog data
"""

from model.blog import BlogInDB, BlogCreate, BlogUpdate, BlogOut
from data import blog


def create_blog(new_blog: BlogCreate) -> BlogOut:
    """
    Create a new blog

    Args:
        new_blog (BlogCreate): BlogCreate object

    Returns:
        BlogInDB: BlogInDB object
    """
    try:
        return BlogOut(**blog.create_blog(new_blog).model_dump())
    except Exception as e:
        raise e


def get_blog_by_id(id: str) -> BlogOut:
    """
    Get a blog by id

    Args:
        id (str): id of the blog

    Returns:
        BlogInDB: BlogInDB object
    """
    try:
        return BlogOut(**blog.get_blog_by_id(id).model_dump())
    except Exception as e:
        raise e


def get_blogs_by_user_id(user_id: str) -> list[BlogOut]:
    """
    Get all blogs by user id

    Args:
        user_id (str): id of the user

    Returns:
        List[BlogInDB]: List of BlogInDB objects
    """
    try:
        return [
            BlogOut(**b.model_dump())
            for b in blog.get_blogs_by_user_id(user_id)
        ]
    except Exception as e:
        raise e


def get_all_blogs() -> list[BlogOut]:
    """
    Get all blogs

    Returns:
        List[BlogOut]: List of BlogOut objects
    """
    try:
        return [BlogOut(**b.model_dump()) for b in blog.get_all_blogs()]
    except Exception as e:
        raise e


def update_blog(updated_blog: BlogUpdate) -> BlogOut:
    """
    Update a blog

    Args:
        blog (BlogUpdate): BlogUpdate object

    Returns:
        BlogInDB: BlogInDB object
    """
    try:
        return BlogOut(**blog.update_blog(updated_blog).model_dump())
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
        blog.delete_blog(BlogInDB(**delete_blog.model_dump()))
    except Exception as e:
        raise e
