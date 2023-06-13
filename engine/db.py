"""
`Storage` module
"""


from pymongo import MongoClient, collection
from bson import ObjectId
from typing import Dict, Any, List
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
            (bool): True if successful or False if failed
        """
        if user_credentials is None or not isinstance(user_credentials, dict):
            return False
        collection = self._Storage__getCollection('users')
        try:
            result = collection.insert_one(user_credentials)
            return result.acknowledged
        except Exception:
            return False

    def get_user(self, email: str, user_id=None) -> Dict[str, Any]:
        """
        return user matching email

        args:
            email (str): user email
        
        return:
            user (dict): user details
        """
        collection = self._Storage__getCollection('users')
        if email:
            if type(email) is not str:
                return
            user = collection.find_one({ 'email': email })
        elif user_id:
            if type(user_id) is not str:
                return
            try:
                user = collection.find_one({ '_id': ObjectId(user_id) })
            except Exception:
                return
        else:
            return
        return user

    def delete_user(self, user_id: str) -> bool:
        """
        deletes a user

        args:
            user_id (str): user id
        
        return:
            (bool): return result of operation
        """
        if not user_id or type(user_id) is not str:
            return False
        collection = self._Storage__getCollection('users')
        result = collection.delete_one({ '_id': ObjectId(user_id) })
        return result.acknowledged
    
    def update_user(self, user_id: str, user_details: Dict[str, Any]) -> bool:
        """
        update user details

        Args:
            user_id (str): user id
            user_details (dict): user fields to update

        Return:
            (bool): result of the operation
        """
        if not user_id or type(user_id) is not str:
            return False
        if user_details is None or not isinstance(user_details, dict):
            return False
        collection = self._Storage__getCollection('users')
        result = collection.update_one({'_id': ObjectId(user_id)}, {'$set': user_details})
        return result.acknowledged

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
        try:
            property_id = ObjectId(property_id)
        except Exception:
            return
        property = collection.find_one({ '_id': property_id })
        return property
    
    def delete_property(self, property_id: str) -> bool:
        """
        deletes property

        args:
            property_id (str): id for the property

        return:
            (bool): result of the operation
        """
        if not property_id or type(property_id) is not str:
            return
        collection = self._Storage__getCollection('property')
        result = collection.delete_one({'_id': ObjectId(property_id)})
        return result.acknowledged

    def get_properties_for_seller(self, seller_id: str) -> List[Dict[str, Any]]:
        """
        returns all of the properties linked to a seller

        args:
            seller_id (str): user id for all of the properties to be deleted
        
        return:
            (list): list of all properties linked to a user
        """
        if not seller_id or type(seller_id) is not str:
            return []
        collection = self._Storage__getCollection('property')
        properties = collection.find({'seller id': seller_id})
        return list(properties)

    def delete_properties_for_seller(self, seller_id: str) -> bool:
        """
        deletes all properties related to a specific seller

        args:
            seller_id (str): user id for all of the properties to be deleted
        
        return:
            (bool): result of the operation
        """
        if not seller_id or type(seller_id) is not str:
            return False
        collection = self._Storage__getCollection('property')
        result = collection.delete_many({'seller id': seller_id})
        return result.acknowledged

    def update_property(self, property_id: str, property_details: Dict[str, Any]) -> bool:
        """
        updates property details

        Args:
            property_id (str): id of the property to update
            property_details (dict): fields and values to update

        Return:
            (bool): result of the operation
        """
        if not property_id or type(property_id) is not str:
            return False
        if not property_details or type(property_details) is not dict:
            return False
        collection = self._Storage__getCollection('property')
        result = collection.update_one({'_id': ObjectId(property_id)}, {'$set': property_details})
        return result.acknowledged

