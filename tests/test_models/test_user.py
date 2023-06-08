"""
`user` module tests
"""

import unittest
from engine import storage
from models.user import User

class UserTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.storage = storage
        cls.user = User()

    @classmethod
    def tearDownClass(cls):
        user_emails = [
            'test@example.com',
            'test@example2.com',
            'test@example4.com'
        ]

        for email in user_emails:
            user_id = str(cls.storage.get_user(email)['_id'])
            cls.storage.delete_user(user_id)

    def test_add_user(self):
        """
        Test the add_user method of the User class.
        """
        user_credentials = {
            'first name': 'John',
            'last name': 'Doe',
            'email': 'test@example.com',
            'password': 'password123',
            'account type': 'buyer'
        }
        result = self.user.add_user(user_credentials)
        self.assertEqual(result, {'result': 'user created'})

    def test_add_user_missing_fields(self):
        user_credentials = {
            'first name': 'John',
            'last name': 'Doe',
            'email': 'test@example.com'
        }
        result = self.user.add_user(user_credentials)
        self.assertEqual(result, {'error': 'Missing password, account type'})

    def test_add_user_invalid_details(self):
        """
        Test the behavior of the add_user method when invalid user details are provided.
        """
        user_credentials = 'invalid credentials'
        result = self.user.add_user(user_credentials)
        self.assertEqual(result, {'error': 'Invalid user credentials'})

    def test_get_user(self):
        """
        Test the get_user method of the User class.
        """
        user_credentials = {
            'first name': 'John',
            'last name': 'Doe',
            'email': 'test@example2.com',
            'password': 'password123',
            'account type': 'buyer'
        }
        result = self.user.add_user(user_credentials)
        self.assertEqual(result, {'result': 'user created'})
        result = self.user.get_user(user_credentials['email'])
        del result['_id']
        del user_credentials['_id']
        self.assertEqual(result, user_credentials)

    def test_delete_user(self):
        """
        Test deleting a user with a valid user ID.
        """
        user_credentials = {
            'first name': 'John',
            'last name': 'Doe',
            'email': 'test@example3.com',
            'password': 'password123',
            'account type': 'buyer'
        }
        result = self.user.add_user(user_credentials)
        self.assertEqual(result, {'result': 'user created'})
        user_id = str(self.user.get_user(user_credentials['email'])['_id'])

        result = self.user.delete_user(user_id)
        self.assertEqual({'result': 'user deleted'}, result)

        result = self.user.get_user(user_credentials['email'])
        self.assertIsNone(result)

    def test_delete_user_invalid_id(self):
        """
        Test deleting a user with an invalid user ID.
        """
        user_id = None
        result = self.user.delete_user(user_id)
        self.assertEqual({'error': "user doesn't exist"}, result)

    def test_update_user(self):
        """
        Test updating a user with a valid user ID and user details.
        """
        user_credentials = {
            'first name': 'unknown',
            'last name': 'Doe',
            'email': 'test@example4.com',
            'password': 'password123',
            'account type': 'buyer'
        }
        result = self.user.add_user(user_credentials)
        self.assertEqual(result, {'result': 'user created'})
        user_id = str(self.user.get_user(user_credentials['email'])['_id'])
        new_details = {"name": "John", "age": 30}

        result = self.user.update_user(user_id, new_details)
        self.assertTrue(result)

        user = self.user.get_user(user_credentials['email'])
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
