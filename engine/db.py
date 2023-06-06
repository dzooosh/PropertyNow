"""
`Storage` module
"""


from pymongo import MongoClient, collection
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

    def _Storage__getCollection(self, collectionName: str) -> collection.Collection:
        """
        returns mongodb collection by collection name

        args:
            collectionName (str): Name of the collection
        
        return:
            (collection.Collection): collecttion associated with `collectionName`
        """
        if collectionName != 'users' and collectionName != 'property':
            return None
        return self.__dbClient[collectionName]

    def add_user(self, userCredentials: Dict[str, Any]) -> bool:
        """
        creates a new user in the database

        args:
            userCredentials (Dict): A dictionary with user credentialise
        
        return:
            (bool): True if successful or False if failed
        """
        if not userCredentials or not isinstance(userCredentials, dict):
            return False
        collection = self._Storage__getCollection('users')
        result = collection.insert_one(userCredentials)
        return result.acknowledged

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
        






