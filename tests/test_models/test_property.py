import unittest
from engine import storage
from engine.redis import LRUCache
from bson import ObjectId
from models.property import Property
from typing import Dict, Any, List


class TestProperty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__storage = storage
        cls.property = Property()
        user_credentials = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password': 'password123',
            'account type': 'buyer'
        }
        result = cls.__storage.add_user(user_credentials)
        cls.user = cls.__storage.get_user(user_credentials['email'])
        cls.cache = LRUCache()

    @classmethod
    def tearDownClass(cls):
        user_emails = [
            'test@example.com',
        ]
        for email in user_emails:
            user_id = str(cls.__storage.get_user(email)['_id'])
            cls.__storage.delete_user(user_id)
        cls.cache.flush_database()
        

    def test_add_property(self):
        property_details = {
            'title': 'Spacious Apartment',
            'description': 'A beautiful apartment with modern amenities.',
            'price': 200000,
            'seller id': str(self.user['_id']),
            'location': {
                'city': 'New York',
                'neighborhood': 'Manhattan'
            }
        }
        result = self.property.add_property(property_details)
        self.assertIsInstance(result, dict)
        self.assertTrue('property id' in result.keys())

    def test_add_property_missing_fields(self):
        property_details = {
            'title': 'Spacious Apartment',
            'description': 'A beautiful apartment with modern amenities.',
            'price': 200000
        }
        result = self.property.add_property(property_details)
        self.assertEqual(result, {'error': 'Missing location'})

    def test_get_property(self):
        property_details = {
            'title': 'Spacious Apartment',
            'description': 'A beautiful apartment with modern amenities.',
            'price': 200000,
            'location': {
                'city': 'New York',
                'neighborhood': 'Manhattan'
            }
        }
        result = self.property.add_property(property_details)
        self.assertIsInstance(result, dict)
        self.assertTrue('property id' in result.keys())
        property_id = result['property id']
        property = self.property.get_property(property_id)
        self.assertEqual(property['_id'], property_id)

    def test_delete_property(self):
        property_details = {
            'title': 'Spacious Apartment',
            'description': 'A beautiful apartment with modern amenities.',
            'price': 200000,
            'location': {
                'city': 'New York',
                'neighborhood': 'Manhattan'
            }
        }
        property_id = self.property.add_property(property_details).get('property id')
        result = self.property.delete_property(property_id)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)



if __name__ == "__main__":
    unittest.main()
