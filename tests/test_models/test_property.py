import unittest
from engine import storage
from bson import ObjectId
from models.property import Property
from typing import Dict, Any, List


class TestProperty(unittest.TestCase):
    def setUp(self):
        self.__storage = storage
        self.property = Property()
        user_credentials = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        result = self.__storage.add_user(user_credentials)
        self.user = self.__storage.get_user(user_credentials['email'])

    
    def teardown(self):
        user_emails = [
            'test@example.com',
        ]
        self.__storage.delete_properties_for_seller(str(self.user['_id']))
        for email in user_emails:
            user_id = str(self.storage.get_user(email)['_id'])
            self.storage.delete_user(user_id)

    def test_add_property(self):
        property_details = {
            "title": "House for Sale",
            "price": 200000,
            "location": "New York",
            "seller_id": self.user['_id']
        }
        result = self.property.add_property(property_details)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "")

    def test_get_property(self):
        property_details = {
            "title": "House for Sale",
            "price": 200000,
            "location": "New York",
            "seller_id": self.user['_id']
        }
        property_id = self.property.add_property(property_details)
        result = self.property.get_property(property_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['_id'], ObjectId(property_id))

    def test_delete_property(self):
        property_details = {
            "title": "House for Sale",
            "price": 200000,
            "location": "New York",
            "seller_id": self.user['_id']
        }
        property_id = self.property.add_property(property_details)
        result = self.property.delete_property(property_id)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_get_properties_for_seller(self):
        seller_id = self.user['_id']
        property_details = {
            "title": "House for Sale",
            "price": 200000,
            "location": "New York",
            "seller_id": self.user['_id']
        }
        self.property.add_property(property_details)
        result = self.property.get_properties_for_seller(str(seller_id))
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 2)
        for property in result:
            self.assertEqual(property["seller_id"], seller_id)


if __name__ == "__main__":
    unittest.main()
