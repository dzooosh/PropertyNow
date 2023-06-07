import unittest
from pymongo.collection import Collection
from engine import storage

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.storage = storage
        user_credentials = {
            'email': 'test@example6.com',
            'password': 'password123'
        }
        result = self.storage.add_user(user_credentials)
        self.user = self.storage.get_user(user_credentials['email'])

    
    def teardown(self):
        user_emails = [
            'test@example.com',
            'test@example2.com',
            'test@example3.com',
            'test@example4.com',
            'test@example5.com',
            'test@example6.com'
        ]

        for email in user_emails:
            user_id = str(self.storage.get_user(email)['_id'])
            self.storage.delete_user(user_id)

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
        user_credentials = {
            'email': 'test@example2.com',
            'password': 'password123'
        }
        result = self.storage.add_user(user_credentials)
        self.assertTrue(result)
        user = self.storage.get_user(user_credentials['email'])
        self.assertIsInstance(user, dict)
        self.assertEqual(user['email'], user_credentials['email'])

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

    def test_delete_user(self):
        """
        Test the delete_user method.
        """
        user_credentials = {
            'email': 'test@example3.com',
            'password': 'password123'
        }
        result = self.storage.add_user(user_credentials)
        self.assertTrue(result)
        user_id = str(self.storage.get_user('test@example3.com')['_id'])
        result = self.storage.delete_user(user_id)

        self.assertTrue(result)
        user = self.storage.get_user('test@example3.com')
        self.assertIsNone(user)

    def test_delete_user_invalid_id(self):
        """
        Test the behavior of delete_user method when an invalid user ID is provided.
        """
        user_id = None
        result = self.storage.delete_user(user_id)

        self.assertFalse(result)

    def test_update_user(self):
        """
        Test updating user details with valid inputs.
        """
        user_credentials = {
            'email': 'test@example4.com',
            'password': 'password123'
        }
        result = self.storage.add_user(user_credentials)
        self.assertTrue(result)
        user_id = str(self.storage.get_user('test@example4.com')['_id'])

        user_details = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "age": 30
        }
        result = self.storage.update_user(user_id, user_details)
        self.assertTrue(result)

    def test_update_user_invalid_id(self):
        """
        Test updating user details with an invalid user ID.
        """
        user_id = None
        user_details = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "age": 30
        }
        result = self.storage.update_user(user_id, user_details)
        self.assertFalse(result)

    def test_update_user_invalid_details(self):
        """
        Test updating user details with invalid user details.
        """
        user_credentials = {
            'email': 'test@example5.com',
            'password': 'password123'
        }
        result = self.storage.add_user(user_credentials)
        self.assertTrue(result)
        user_id = str(self.storage.get_user('test@example5.com')['_id'])

        user_details = None
        result = self.storage.update_user(user_id, user_details)
        self.assertFalse(result)

        user_details = "invalid"
        result = self.storage.update_user(user_id, user_details)
        self.assertFalse(result)

    def test_delete_property(self):
        property_id = self.storage.add_property({"title": "Test Property", "seller_id": self.user['_id']})
        result = self.storage.delete_property(property_id)
        self.assertTrue(result)
        deleted_property = self.storage.get_property(property_id)
        self.assertIsNone(deleted_property)

    def test_get_properties_for_seller(self):
        seller_id = self.user['_id']
        self.storage.add_property({"title": "Property 1", "seller_id": seller_id})
        self.storage.add_property({"title": "Property 2", "seller_id": seller_id})
        self.storage.add_property({"title": "Property 3", "seller_id": seller_id})

        properties = self.storage.get_properties_for_seller(str(seller_id))
        self.assertIsInstance(properties, list)
        self.assertEqual(len(properties), 3)

        for property in properties:
            self.assertEqual(property["seller_id"], seller_id)

    def test_delete_properties_for_seller(self):
        seller_id = self.user['_id']
        self.storage.add_property({"title": "Property 1", "seller_id": seller_id})
        self.storage.add_property({"title": "Property 2", "seller_id": seller_id})
        self.storage.add_property({"title": "Property 3", "seller_id": seller_id})

        result = self.storage.delete_properties_for_seller(str(seller_id))
        self.assertTrue(result)

        deleted_properties = self.storage.get_properties_for_seller(str(seller_id))
        self.assertEqual(len(deleted_properties), 0)

if __name__ == '__main__':
    unittest.main()
