"""
`Storage` module
"""


from pymongo import MongoClient, collection
from bson import ObjectId
from typing import Dict, Any
from os import environ


class Storage:
    """
    A class for storing and managing data.

    Attributes:
        dbClient (private class attribute): MongoDb client
    
    """

    def __init__(self):
        """
        Initialize `Storage` class
        """
        DB_HOST = environ.get('DB_HOST', 'localhost')
        DB_PORT = environ.get('DB_PORT', '27017')
        DB_DATABASE = environ.get('DB_DATABASE', 'propertyNow')
        client = MongoClient(f'mongodb://{DB_HOST}:{DB_PORT}')
        self.__dbClient = client[DB_DATABASE]

    def _Storage__getCollection(self, collection_name: str) -> collection.Collection:
        """
        returns mongodb collection by collection name

        args:
            collection_name (str): Name of the collection
        
        return:
            (collection.Collection): collecttion associated with `collection_name`
        """
        if collection_name != 'users' and collection_name != 'property':
            return None
        return self.__dbClient[collection_name]

    def add_user(self, user_credentials: Dict[str, Any]) -> bool:
        """
        creates a new user in the database

        args:
            user_credentials (Dict): A dictionary with user credentialise
        
        return:
            (bool): True if succeful or False if failed
        """
        if not user_credentials or not isinstance(user_credentials, dict):
            return False
        collection = self._Storage__getCollection('users')
        try:
            result = collection.insert_one(user_credentials)
            return result.acknowledged
        except Exception:
            return False

    def get_user(self, email: str) -> Dict[str, Any]:
        """
        return user matching email

        args:
            email (str): user email
        
        return:
            user (dict): user details
        """
        if not email or type(email) is not str:
            return
        collection = self._Storage__getCollection('users')
        user = collection.find_one({ 'email': email })
        return user

    def add_property(self, property_details: Dict[str, Any]) -> str:
        """
        adds a new property in the database

        args:
            property_details (dict): a dictionary with property details
        
        return:
            (str): 
        """
        if not property_details or not isinstance(property_details, dict):
            return 
        collection = self._Storage__getCollection('property')
        try:
            result = collection.insert_one(property_details)
            return str(result.inserted_id)
        except Exception:
            return

    def get_property(self, property_id: str) -> Dict[str, Any]:
        """
        retreives property by id

        args:
            property_id (str): id for the property
        
        return:
            property (dict): property linked with the property id
        """
        if not property_id or type(property_id) is not str:
            return
        collection = self._Storage__getCollection('property')
        property = collection.find_one({ '_id': ObjectId(property_id) })
        return property

