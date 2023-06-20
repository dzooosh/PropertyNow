"""
`Storage` module
"""


from pymongo import MongoClient, collection
from engine.redis import LRUCache
from bson import ObjectId
from typing import Dict, Any, List
import uuid
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
        self.__cacheClient = LRUCache()

    def _Storage__getCollection(self, collection_name: str) -> collection.Collection:
        """
        returns mongodb collection by collection name

        args:
            collection_name (str): Name of the collection
        
        return:
            (collection.Collection): collecttion associated with `collection_name`
        """
        if collection_name != 'users' and collection_name != 'property' and collection_name != 'locations':
            return None
        return self.__dbClient[collection_name]

    def _Storage__add_location(self, property_details):
        """
        update the locations in the location collection
        """
        collection = self._Storage__getCollection('locations')
        neighborhoods = list(collection.find({'city': property_details.get('city')}))
        if len(neighborhoods) == 0:
            collection.insert_one({'city': property_details.get('city'), 'neighborhoods': []})
        else:
            neighborhoods = neighborhoods[0]['neighborhoods']
        for i in range(len(neighborhoods)):
            if property_details['neighborhood'] in neighborhoods[i]:
                neighborhoods[i][property_details['neighborhood']] += 1
                break
        else:
            neighborhoods.append({property_details['neighborhood']: 1})
        result = collection.update_one({'city': property_details['city']}, {'$set': {'neighborhoods': neighborhoods}})
        return result.acknowledged
    
    def _Storage__delete_location(self, property_details):
        """
        delete location
        """
        collection = self._Storage__getCollection('locations')
        neighborhoods = list(collection.find({'city': property_details.get('city')}))
        if len(neighborhoods) == 0:
            return False
        else:
            neighborhoods = neighborhoods[0]['neighborhoods']
        if len(neighborhoods) == 1:
            if property_details['neighborhood'] in neighborhoods[0]:
                collection.delete_one({'city': property_details.get('city')})
                return True
            return False
        for i in range(len(neighborhoods)):
            if property_details['neighborhood'] in neighborhoods[i]:
                if neighborhoods[i][property_details['neighborhood']] == 1:
                    del neighborhoods[i]
                else:
                    neighborhoods[i][property_details['neighborhood']] -= 1
                break
        result = collection.update_one({'city': property_details['city']}, {'$set': {'neighborhoods': neighborhoods}})
        return result.acknowledged

    def get_locations(self):
        """
        retreive cities and neighborhoods
        """
        collection = self._Storage__getCollection('locations')
        locations = []
        cities = list(collection.find())
        for city in cities:
            city_location = {}
            city_location['city'] = city['city']
            neighborhoods = []
            for neighborhood in city['neighborhoods']:
                neighborhoods.append(list(neighborhood.keys())[0])
            city_location['neighborhoods'] = neighborhoods
            locations.append(city_location)
        return locations

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
        user_id = uuid.uuid4()
        user_credentials['_id'] = str(user_id)
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
                user = collection.find_one({ '_id': user_id })
            except Exception:
                return
        else:
            return
        return user
    
    def get_users(self, page: int, page_size: int) -> List[Dict[str, Any]]:
        """
        retreives users for admin page

        args:
            page (int): current page
            page_size (int): page size
        
        return:
            users (list): list of users
        """
        if page < 0 or page_size < 0:
            return
        collection = self._Storage__getCollection('users')
        try:
            users = collection.find().skip(page * page_size).limit(page_size)
        except Exception:
            return
        return list(users)
    

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
        result = collection.delete_one({ '_id': user_id })
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
        result = collection.update_one({'_id': user_id}, {'$set': user_details})
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
        property_details['_id'] = str(uuid.uuid4())
        result = collection.insert_one(property_details)
        self._Storage__add_location(property_details['location'])
        property_id = str(result.inserted_id)
        self.__cacheClient.put(property_id, self.get_property(property_id))
        return property_id
    

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
        property = self.__cacheClient.get(property_id)
        if not property:
            collection = self._Storage__getCollection('property')
            try:
                object_id = property_id
            except Exception:
                return
            property = collection.find_one({ '_id': object_id })
            if property:
                self.__cacheClient.put(property_id, property)
        return property

    def get_properties(self, page: int, page_size: int) -> List[Dict[str, Any]]:
        """
        retreives properties for page

        args:
            page (int): current page
            page_size (int): page size
        
        return:
            properties (list): list of properties
        """
        if page < 0 or page_size < 0:
            return
        collection = self._Storage__getCollection('property')
        try:
            pipeline = [
                {"$skip": page * page_size},
                {"$limit": page_size},
                {
                    "$addFields": {
                        "image_url": {"$cond": {"if": {"$isArray": "$image_url"}, "then": {"$arrayElemAt": ["$image_url", 0]}, "else": "$image_url"}}
                    }
                }
            ]
            properties = collection.aggregate(pipeline)
            return list(properties)
        except Exception as e:
            return {'error': 'failed to retreive'}
    
    def delete_property(self, property_id: str) -> bool:
        """
        deletes property

        args:
            property_id (str): id for the property

        return:
            (bool): result of the operation
        """
        if not property_id or type(property_id) is not str:
            return False
        collection = self._Storage__getCollection('property')
        property = collection.find_one({'_id': property_id})
        self._Storage__delete_location(property['location'])
        result = collection.delete_one({'_id': property_id})
        self.__cacheClient.delete(property_id)
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
        result = collection.update_one({'_id': property_id}, {'$set': property_details})
        property = collection.find_one({'_id': property_id})
        if property:
            self.__cacheClient.update(property_id, property)
        return result.acknowledged

