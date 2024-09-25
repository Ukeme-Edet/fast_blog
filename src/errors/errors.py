"""
This module contains custom exceptions that are raised when an error occurs.
"""


class Missing(Exception):
    """
    Missing exception

    Args:
        Exception (Exception): Base exception class

    Attributes:
        msg (str): Error message
    """

    def __init__(self, msg: str, *args: object) -> None:
        """
        Constructor

        Args:
            msg (str): Error message
        """
        super().__init__(*args)
        self.msg = msg


class Duplicate(Exception):
    """
    Duplicate exception

    Args:
        Exception (Exception): Base exception class

    Attributes:
        msg (str): Error message
    """

    def __init__(self, msg: str, *args: object) -> None:
        """
        Constructor

        Args:
            msg (str): Error message
        """
        super().__init__(*args)
        self.msg = msg
