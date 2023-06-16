import json
from models.property import Property

propertyClass = Property()


with open('properties.json', 'r') as file:
    data = json.load(file)
    properties = data['properties']


for property in properties:
   propertyClass.add_property(property)