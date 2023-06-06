"""
`user` module
"""
from engine import storage
from typing import Dict, Any, Optional


class User:
    """
    Abstraction layer for managing user-related operations.

    Attributes:
        storage (Storage): An instance of the Storage class for interacting with the database.
    """

    def __init__(self):
        """
        Initialize the User class
        """
        self.storage = storage

    def add_user(self, user_details: Dict[str, Any]) -> bool:
        """
        Add a new user.

        Args:
            user_details (Dict[str, Any]): A dictionary containing user details.

        Returns:
            bool: True if the user is successfully added, False otherwise.
        """
        return self.storage.add_user(user_details)

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user details by user ID.

        Args:
            email (str): The ID of the user.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the user details if found, None otherwise.
        """
        return storage.get_user(email)