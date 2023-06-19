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
from auth.auth import Auth

AUTH = Auth()
userClass = User()
propertyClass = Property()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in admin.config['ALLOWED_EXTENSIONS']

# user section

@admin.route('/users/', methods=['GET'], strict_slashes=False)
@jwt_required
def get_users():
    """
    returns a list of users from the database
    """
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('limit', default=20, type=int)
    users = userClass.get_users(page - 1, page_size)
    if users is None:
        return jsonify({'error': 'Failed to retreive users'}), 500
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

@admin.route('/users/search/', methods=['GET'], strict_slashes=False)
@jwt_required
def search_for_users():
        """
        get all users in the database
        """
        query = request.args.get('query')

        if not query:
                return jsonify({"error": "No search query provided"}), 400
        
        result = []
        # Perform the search logic based on the query parameter
        for user in userClass.get_users():
                if query.lower() in user['email'].lower():
                      result.append(user)
                if query.lower() in user['first_name'].lower():
                       result.append(user)
                if query.lower() in user['last_name'].lower():
                       result.append(user)
        
        return jsonify(result)

@admin.route('properties/add', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_properties():
        """
        adds property to the database
        """
        id = str(uuid.uuid4())
        property_details = {}
        for key, value in request.form.items():
                if key == 'city' or key == 'neighborhood':
                       continue
                property_details[key] = value
        property_details['location'] = {'city': request.form.get('city'), 'neighborhood': request.form.get('neighborhood')}
        images = request.files.getlist('images')
        if len(images) == 0:
                property_id = propertyClass.add_property(property_details)
                if 'error' in property_id.keys():
                        return jsonify(property_id)
                return jsonify({'message': 'property added'})
        if images[0] and allowed_file(images[0].filename):
                filename = id + '.' + images[0].filename.rsplit('.', 1)[1].lower()
                images[0].save(os.path.join(admin.config['UPLOAD_FOLDER'], filename))
                image_urls = [f'http://localhost:5000/properties/images/{filename}']
        property_details['image_url'] = image_urls
        if len(images) == 1:
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

@admin.route('/properties/<string:property_id>/update', methods=['POST'], strict_slashes=False)
@jwt_required()
def update_property(property_id: str):
        """
        update property with new details
        """
        property_details = request.json
        result = propertyClass.update_property(property_id, property_details)
        if 'error' in result.keys():
               return jsonify(result), 400
        return jsonify(result)

@admin.route('/properties/<string:property_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_property(property_id: str):
        """
        delete property with new details
        """
        property_details = request.json
        result = propertyClass.delete_property(property_id, property_details)
        if not result:
               return jsonify({'error': 'failed to delete'}), 400
        return jsonify({'message': 'property deleted'}), 204