"""
a view for `admin` that handles all admins REST API
actions
Admin - Add (user, admin, properties)
        Remove (user, properties)
        Update(properties, User (change user to admin))
"""
from views import admin
from flask import request, jsonify
import os
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity
import zipfile
from models.user import User
from models.property import Property

userClass = User()
propertyClass = Property()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in admin.config['ALLOWED_EXTENSIONS']

# user section

@admin.route('/users/<int:user_id>', methods=['DELETE'],
             strict_slashes=False)
def delete_user(user_id):
    user = userClass.get_user(user_id)
    if not user:
        return jsonify(error='Property not found'), 404

    del_user = userClass.delete_user(user)
    
    if 'result' in del_user.keys():
        return '', 204

@admin.route('properties/add', methods=['POST'], strict_slashes=False)
@jwt_required
def add_properties():
        """
        adds property to the database
        """
        id = uuid.uuid4()
        property_details = request.json
        images = list(request.files.values())
        if len(images) == 0:
                property_id = propertyClass.add_property(property_details)
                if 'error' in property_id.keys():
                        return jsonify(property_id)
                return jsonify({'message': 'property added'})
        if images[0] and allowed_file(images[0].filename):
                filename = id + '.' + images[0].filename.rsplit('.', 1)[1].lower()
                images[0].save(os.path.join(admin.config['UPLOAD_FOLDER'], filename))
                image_urls = [f'http://localhost:5000/properties/images/{filename}']
        if len(images) == 1:
                property_details['image_url'] = image_urls
                property_id = propertyClass.add_property(property_details)
                if 'error' in property_id.keys():
                        return jsonify(property_id)
                return jsonify({'message': 'property and image sucefully added'})
        zip_path = os.path.join(admin.config['UPLOAD_FOLDER'], f'{id}.zip')
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
                for image in images:
                        if image.filename != '' and allowed_file(image.filename):
                                file_data = image.read()
                                zip_file.writestr(image.filename, file_data)
        property_details['image_url'].append(f'http://localhost:5000/properties/images/{id}.zip')
        property_id = propertyClass.add_property(property_details)
        if 'error' in property_id.keys():
                return jsonify(property_id)
        return jsonify({'message': 'property and images sucefully added'})

