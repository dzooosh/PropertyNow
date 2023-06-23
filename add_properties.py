import json
import shutil
import os
import zipfile
import uuid
import random
from models.property import Property

propertyClass = Property()

def store_property_image():
    url = 'http://localhost:5000/properties/images/'
    image_urls = {'image_url': []}
    image_name = random.randint(1, 46)
    image_directory = './images'
    output_directory = os.path.expanduser('./property_images')
    os.makedirs(output_directory, exist_ok=True)
    image_files = [f for f in os.listdir(image_directory) if f.endswith('.png')]
    random.shuffle(image_files)
    selected_images = image_files[:5]
    for image_name in selected_images:
        id = str(uuid.uuid4())
        image_path = os.path.join(image_directory, image_name)
        new_image_path = os.path.join(output_directory, f"{id}{os.path.splitext(image_name)[1]}")
        if os.path.exists(image_path):
            shutil.copy2(image_path, new_image_path)
            image_urls['image_url'].append(url + f'{id}.png')
            print(f"Image '{f'{image_name}.png'}' copied and renamed to '{os.path.basename(new_image_path)}'.")
    return image_urls

with open('properties.json', 'r') as file:
    data = json.load(file)
    properties = data['properties']


for property in properties:
   property.update(store_property_image())
   property_id = propertyClass.add_property(property).get('property id')
   print('done')
   
