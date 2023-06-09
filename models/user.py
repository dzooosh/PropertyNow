"""
`user` module
"""
from engine import storage
from typing import Dict, Any, List, Optional


class User():
    """
    Abstraction layer for managing user-related operations.

        storage (Storage): An instance of the Storage class for interacting with the database.
    """

    def __init__(self):
        """
        Initialize the User class
        """
        self.__storage = storage

    def add_user(self, user_credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new user.

        Args:
            user_credentials (Dict[str, Any]): A dictionary containing user details.

        Returns:
            bool: True if the user is successfully added, False otherwise.
        """
        if user_credentials is None or not isinstance(user_credentials, dict):
            return {'error': 'Invalid user credentials'}
        fields = user_credentials.keys()
        required_fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'account_type'
        ]
        missing_fields = [field for field in required_fields if field.lower() not in fields]
        if missing_fields:
            return {'error': f'Missing {", ".join(missing_fields)}'}

        if user_credentials['account_type'] not in ['buyer', 'seller', 'admin']:
            return {'error': 'Invalid account type, accepted accounts buyer, seller and admin'}

        if self.__storage.add_user(user_credentials):
            return {'result': 'user created'}
        else:
            return {'error': 'failed to create user'}

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user details by user ID.

        Args:
            email (str): The ID of the user.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the user details if found, None otherwise.
        """
        return self.__storage.get_user(email)
    
    def get_users(self, page: int, page_size: int) -> List[Dict[str, Any]]:
        """
        retreives users for admin page

        args:
            page (int): current page
            page_size (int): page size
        
        return:
            users (list): list of users
        """
        if type(page) is not int:
            return {'error': 'page must be int'}
        if type(page_size) is not int:
            return {'error': 'page_size must be int'}
        if page < 0:
            return {'error': 'page must be >= 0'}
        if page_size < 0:
            return {'error': 'page_size must be >= 0'}
        users = self.__storage.get_users(page, page_size)
        return users

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """
        deletes a user

        Args:
            user_id (str): user id

        Returns:
            (bool): result of the delete operation
        """
        user = self.__storage.get_user(None, user_id)
        if not user:
            return {'error': "user doesn't exist"}
        if user['account_type'] == 'seller':
            self.__storage.delete_properties_for_seller(user_id)
        if self.__storage.delete_user(user_id):
            return {'result': 'user deleted'}
        else:
            return {'error': 'failed to delete user'}

      
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
