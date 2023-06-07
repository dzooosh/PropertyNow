"""
This script is to setup mongodb database for the `propertyNow` project
"""
from pymongo import MongoClient, IndexModel
from pymongo.errors import CollectionInvalid
from os import environ


# connect to the database
DB_HOST = environ.get('DB_HOST', 'localhost')
DB_PORT = environ.get('DB_PORT', '27017')
DB_DATABASE = environ.get('DB_DATABASE', 'propertyNow')
client = MongoClient(f'mongodb://{DB_HOST}:{DB_PORT}')

# Access the database
dbClient = client[DB_DATABASE]

# setup `users` collection and indexes
try:
    usersCollection = dbClient.create_collection('users')
    print('users collection created')
except CollectionInvalid:
    print('Collection `users` already exists')
    usersCollection = dbClient['users']
usersCollection.create_index('email', unique=True)

# setup `property` collection and indexes
try:
    propertyCollection = dbClient.create_collection('property')
    print('`property` collection created')
except CollectionInvalid:
    print('Collection `property` already exists')
    propertyCollection = dbClient['property']

propertyCollection.create_index('seller_id')
propertyCollection.create_index('price')
propertyCollection.create_index('location.city')

# Create indexes
index1 = IndexModel([("location.city", 1)])
index2 = IndexModel([("location.neighborhood", 1)])
index3 = IndexModel([("price", 1)])

propertyCollection.create_indexes([index1, index2, index3])

client.close()