"""
`user` module tests
"""

import unittest
from engine import storage
from models.user import User

class UserTests(unittest.TestCase):
    def setUp(self):
        self.storage = storage
        self.user = User()

    def teardown(self):
        user_emails = [
            'test@example.com',
            'test@example2.com',
            'test@example3.com',
            'test@example4.com'
        ]

        for email in user_emails:
            user_id = str(self.storage.get_user(email)['_id'])
            self.storage.delete_user(user_id)

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

    def test_add_user_invalid_details(self):
        """
        Test the behavior of the add_user method when invalid user details are provided.
        """
        user_details = None
        result = self.user.add_user(user_details)
        self.assertFalse(result)

        user_details = "Invalid details"
        result = self.user.add_user(user_details)
        self.assertFalse(result)

    def test_get_user(self):
        """
        Test the get_user method of the User class.
        """
        user_details = {
            "email": "test@example2.com",
            "name": "Test User"
        }
        result = self.user.add_user(user_details)
        self.assertTrue(result)
        result = self.user.get_user(user_details['email'])
        del result['_id']
        del user_details['_id']
        self.assertEqual(result, user_details)

    def test_delete_user(self):
        """
        Test deleting a user with a valid user ID.
        """
        user_details = {
            "email": "test@example3.com",
            "name": "Test User"
        }
        result = self.user.add_user(user_details)
        self.assertTrue(result)
        user_id = str(self.user.get_user(user_details['email'])['_id'])

        result = self.user.delete_user(user_id)
        self.assertTrue(result)

        result = self.user.get_user(user_details['email'])
        self.assertIsNone(result)

    def test_delete_user_invalid_id(self):
        """
        Test deleting a user with an invalid user ID.
        """
        user_id = None
        result = self.user.delete_user(user_id)
        self.assertFalse(result)

    def test_update_user(self):
        """
        Test updating a user with a valid user ID and user details.
        """
        user_details = {
            "email": "test@example4.com",
            "name": "Test User"
        }
        result = self.user.add_user(user_details)
        self.assertTrue(result)
        user_id = str(self.user.get_user(user_details['email'])['_id'])
        new_details = {"name": "John Doe", "age": 30}

        result = self.user.update_user(user_id, new_details)
        self.assertTrue(result)

        user = self.user.get_user(user_details['email'])
        self.assertEqual(new_details['name'], user['name'])
        self.assertEqual(new_details['age'], user['age'])

    def test_update_user_invalid_id(self):
        """
        Test updating a user with an invalid user ID.
        """
        user_id = None
        user_details = {"name": "John Doe", "age": 30}
        result = self.user.update_user(user_id, user_details)
        self.assertFalse(result)


    

if __name__ == '__main__':
    unittest.main()
