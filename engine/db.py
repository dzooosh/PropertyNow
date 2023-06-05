
import pymongo
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
        client = pymongo.MongoClient(f'mongodb://{DB_HOST}:{DB_PORT}')
        self.__dbClient = client[DB_DATABASE]


