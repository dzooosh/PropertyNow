import unittest
from pymongo.collection import Collection
from pymongo import MongoClient, collection
from bson import ObjectId
from engine import storage
from engine.redis import LRUCache

class TestStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storage = storage
        user_credentials = {
            'email': 'test@example6.com',
            'password': 'password123'
        }
        result = cls.storage.add_user(user_credentials)
        cls.user = cls.storage.get_user(user_credentials['email'])
        cls.client = MongoClient('mongodb://localhost:27017')

    @classmethod
    def tearDownClass(cls):
        user_emails = [
            'test@example.com',
            'test@example2.com',
            'test@example4.com',
            'test@example5.com',
            'test@example6.com'
        ]

        for email in user_emails:
            user_id = str(cls.storage.get_user(email).get('_id'))
            cls.storage.delete_user(user_id)

    def setUp(self):
        self.db = self.client['propertyNow']
        self.cache = LRUCache()
        self.properties = [
            {
                'title': 'Spacious Apartment',
                'description': 'A beautiful apartment with modern amenities.',
                'price': 200000,
                'location': {
                    'city': 'New York',
                    'neighborhood': 'Manhattan'
                }
            },
            {
                'title': 'Spacious Apartment',
                'description': 'A beautiful apartment with modern amenities.',
                'price': 200000,
                'location': {
                    'city': 'New York',
                    'neighborhood': 'Manhattan'
                }
            },
            {
                'title': 'Spacious Apartment',
                'description': 'A beautiful apartment with modern amenities.',
                'price': 200000,
                'location': {
                    'city': 'New York',
                    'neighborhood': 'Manhattan'
                }
            }
        ]
        self.db['property'].insert_many(self.properties)

        self.storage = storage
        self.storage._Storage__dbClient = self.db
        self.storage._Storage__cacheClient = self.cache

    def tearDown(self):
        self.db['property'].delete_many({})


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
                'title': 'Spacious Apartment',
                'description': 'A beautiful apartment with modern amenities.',
                'price': 200000,
                'location': {
                    'city': 'New York',
                    'neighborhood': 'Manhattan'
                }
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
                'title': 'Spacious Apartment',
                'description': 'A beautiful apartment with modern amenities.',
                'price': 200000,
                'location': {
                    'city': 'New York',
                    'neighborhood': 'Manhattan'
                }
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
        property_id = self.storage.add_property({
                'title': 'Spacious Apartment',
                'description': 'A beautiful apartment with modern amenities.',
                'price': 200000,
                'location': {
                    'city': 'New York',
                    'neighborhood': 'Manhattan'
                }
        })
        result = self.storage.delete_property(property_id)
        self.assertTrue(result)
        deleted_property = self.storage.get_property(property_id)
        self.assertIsNone(deleted_property)

    def test_update_property_valid_input(self):
        property_details = {
                'title': 'Spacious Apartment',
                'description': 'A beautiful apartment with modern amenities.',
                'price': 200000,
                'location': {
                    'city': 'New York',
                    'neighborhood': 'Manhattan'
                }
        }
        property_id = self.storage.add_property(property_details)
        new_property_details = {
            'name': 'another example property',
            'type': 'apartment',
        }
        result = self.storage.update_property(property_id, new_property_details)
        self.assertTrue(result)

        updated_property = self.storage.get_property(property_id)
        self.assertEqual(updated_property['name'], 'another example property')
        self.assertEqual(updated_property['type'], 'apartment')
        self.assertEqual(updated_property['location']['city'], 'New York')

    def test_update_property_invalid_id(self):
        result = self.storage.update_property(None, {'name': 'Example Property'})
        self.assertFalse(result)

    def test_update_property_invalid_details(self):
        result = self.storage.update_property('property_id', None)
        self.assertFalse(result)

    def test_get_properties_page_0_page_size_2(self):
        page = 0
        page_size = 2
        expected_properties = self.properties[:2]
        properties = self.storage.get_properties(page, page_size)
        self.assertEqual(properties, expected_properties)

    def test_get_properties_page_1_page_size_2(self):
        page = 1
        page_size = 2
        expected_properties = self.properties[2:]
        properties = self.storage.get_properties(page, page_size)
        self.assertEqual(properties, expected_properties)

    def test_get_properties_invalid_page_and_page_size(self):
        page = -1
        page_size = 0
        properties = self.storage.get_properties(page, page_size)
        self.assertIsNone(properties)

    def test_get_properties_page_size_larger_than_properties(self):
        page = 0
        page_size = 10
        expected_properties = self.properties
        properties = self.storage.get_properties(page, page_size)
        self.assertEqual(properties, expected_properties)

    def test_get_properties_page_size_larger_than_remaining_properties(self):
        page = 1
        page_size = 10
        expected_properties = []
        properties = self.storage.get_properties(page, page_size)
        self.assertEqual(properties, expected_properties)

if __name__ == '__main__':
    unittest.main()
