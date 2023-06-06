import unittest
from pymongo.collection import Collection
from engine.db import Storage

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.storage = Storage()

    def test_add_user(self):
        """
        Test adding a user to the database with valid credentials
        """
        user_credentials = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        result = self.storage.add_user(user_credentials)
        self.assertTrue(result)

    def test_add_user_invalid_credentials(self):
        """
        Test adding a user to the database with invalid credentials
        """
        user_credentials = "invalid"
        result = self.storage.add_user(user_credentials)
        self.assertFalse(result)

    def test_get_user(self):
        """
        Test retrieving a user from the database based on email
        """
        email = 'test@example.com'
        user = self.storage.get_user(email)
        self.assertIsInstance(user, dict)
        self.assertEqual(user['email'], email)

    def test_get_user_invalid_email(self):
        """
        Test retrieving a user from the database with an invalid email
        """
        email = None
        user = self.storage.get_user(email)
        self.assertIsNone(user)

    def test_add_property(self):
        """
        Test adding a new property to the database with valid details
        """
        property_details = {
            'name': 'Sample Property',
            'location': 'Sample Location',
            'price': 100000
        }
        result = self.storage.add_property(property_details)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, '')

    def test_add_property_invalid_details(self):
        """
        Test adding a new property to the database with invalid details
        """
        property_details = "invalid"
        result = self.storage.add_property(property_details)
        self.assertIsNone(result)

    def test_get_property(self):
        """
        Test retrieving a property from the database based on property ID
        """
        property_details = {
            'name': 'Sample Property',
            'location': 'Sample Location',
            'price': 100000
        }
        property_id = self.storage.add_property(property_details)
        property = self.storage.get_property(property_id)
        self.assertIsInstance(property, dict)
        self.assertEqual(str(property['_id']), property_id)

    def test_get_property_invalid_id(self):
        """
        Test retrieving a property from the database with an invalid property ID
        """
        property_id = None
        property = self.storage.get_property(property_id)
        self.assertIsNone(property)

if __name__ == '__main__':
    unittest.main()
