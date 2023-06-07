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
        self.__storage = storage

    def add_user(self, user_details: Dict[str, Any]) -> bool:
        """
        Add a new user.

        Args:
            user_details (Dict[str, Any]): A dictionary containing user details.

        Returns:
            bool: True if the user is successfully added, False otherwise.
        """
        return self.__storage.add_user(user_details)

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user details by user ID.

        Args:
            email (str): The ID of the user.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the user details if found, None otherwise.
        """
        return self.__storage.get_user(email)

    def delete_user(self, user_id: str) -> bool:
        """
        deletes a user

        Args:
            user_id (str): user id

        Returns:
            (bool): result of the delete operation
        """
        return self.__storage.delete_user(user_id)

      
    def update_user(self, user_id: str, user_details: Dict[str, Any]) -> bool:
        """
        update user details

        Args:
            user_id (str): user id
            user_details (dict): user fields to update

        Return:
            (bool): result of the operation
        """
        return self.__storage.update_user(user_id, user_details)