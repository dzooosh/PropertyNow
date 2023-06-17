import json
import shutil
import os
import random
from models.property import Property

propertyClass = Property()

def store_property_image(id):
    image_name = random.randint(1, 46)
    image_directory = './images'
    output_directory = os.path.expanduser('./property_images')
    os.makedirs(output_directory, exist_ok=True)
    image_path = os.path.join(image_directory, f'{image_name}.png')
    new_image_path = os.path.join(output_directory, f"{id}{os.path.splitext(f'{image_name}.png')[1]}")
    if os.path.exists(image_path):
        shutil.copy2(image_path, new_image_path)
        print(f"Image '{f'{image_name}.png'}' copied and renamed to '{os.path.basename(new_image_path)}'.")

with open('properties.json', 'r') as file:
    data = json.load(file)
    properties = data['properties']


for property in properties:
   property_id = propertyClass.add_property(property).get('property id')
   store_property_image(property_id)
