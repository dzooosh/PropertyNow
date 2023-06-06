"""
`user` module tests
"""

import unittest
from unittest.mock import MagicMock
from engine import storage
from models.user import User

class UserTests(unittest.TestCase):
    def setUp(self):
        self.storage = storage
        self.user = User()

    def test_add_user(self):
        """
        Test the add_user method of the User class.
        """
        user_details = {
            "email": "test@example.com",
            "name": "Test User"
        }
        result = self.user.add_user(user_details)
        self.assertTrue(result)
        self.storage.add_user.assert_called_once_with(user_details)

    def test_add_user_invalid_details(self):
        """
        Test the behavior of the add_user method when invalid user details are provided.
        """
        user_details = None
        result = self.user.add_user(user_details)
        print(result)
        self.assertFalse(result)

        user_details = "Invalid details"
        result = self.user.add_user(user_details)
        self.assertFalse(result)

    def test_get_user(self):
        """
        Test the get_user method of the User class.
        """
        email = "test@example.com"
        user_data = {
            "email": "test@example.com",
            "name": "Test User"
        }
        self.storage.get_user = MagicMock(return_value=user_data)
        result = self.user.get_user(email)
        self.assertEqual(result, user_data)
        self.storage.get_user.assert_called_once_with(email)

if __name__ == '__main__':
    unittest.main()
