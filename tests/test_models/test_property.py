import unittest
from engine import storage
from bson import ObjectId
from models.property import Property
from typing import Dict, Any, List


class TestProperty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__storage = storage
        cls.property = Property()
        user_credentials = {
            'first name': 'John',
            'last name': 'Doe',
            'email': 'test@example.com',
            'password': 'password123',
            'account type': 'buyer'
        }
        result = cls.__storage.add_user(user_credentials)
        cls.user = cls.__storage.get_user(user_credentials['email'])

    @classmethod
    def tearDownClass(cls):
        user_emails = [
            'test@example.com',
        ]
        cls.__storage.delete_properties_for_seller(str(cls.user['_id']))
        for email in user_emails:
            user_id = str(cls.__storage.get_user(email)['_id'])
            cls.__storage.delete_user(user_id)

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
        self.assertEqual(result, {'error': 'Missing seller id, location'})

    def test_add_property_invalid_seller(self):
        property_details = {
            'title': 'Spacious Apartment',
            'description': 'A beautiful apartment with modern amenities.',
            'price': 200000,
            'seller id': '123456789012',
            'location': {
                'city': 'New York',
                'neighborhood': 'Manhattan'
            }
        }
        result = self.property.add_property(property_details)
        self.assertEqual(result, {'error': "seller doesn't exist"})

    def test_get_property(self):
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
        property_id = result['property id']
        property = self.property.get_property(property_id)
        self.assertEqual(property['_id'], ObjectId(property_id))

    def test_delete_property(self):
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
        property_id = self.property.add_property(property_details).get('property id')
        result = self.property.delete_property(property_id)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_get_properties_for_seller(self):
        seller_id = str(self.user['_id'])
        property_details = {
            'title': 'Spacious Apartment',
            'description': 'A beautiful apartment with modern amenities.',
            'price': 200000,
            'seller id': seller_id,
            'location': {
                'city': 'New York',
                'neighborhood': 'Manhattan'
            }
        }
        self.property.add_property(property_details)
        result = self.property.get_properties_for_seller(seller_id)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        for property in result:
            self.assertEqual(property["seller id"], seller_id)


if __name__ == "__main__":
    unittest.main()
