"""
a view for `admin` that handles all admins REST API
actions
Admin - Add (properties)
        Remove (properties)
        Update(properties, User (change user to admin))
"""
from views import admin
from flask import request, jsonify


from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.property import Property
from models.image import Image
from auth.auth import Auth

AUTH = Auth()
userClass = User()
propertyClass = Property()
imageClass = Image()


# user section


@admin.route('/users/', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
    """
    returns a list of users from the database
    """
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('limit', default=20, type=int)
    users = userClass.get_users(page - 1, page_size)
    if type(users) is dict:
        return jsonify(users), 401
    return jsonify(users)


@admin.route('/users/search/', methods=['GET'], strict_slashes=False)
@jwt_required()
def search_for_user():
        """
        search for specific users in the database
        """
        query = request.args.get('query')

        if not query:
                return jsonify({"error": "No search query provided"}), 400
        
        result = []
        # Perform the search logic based on the query parameter
        query = query.lower()
        for user in userClass.get_users():
                if query in user['email'].lower():
                      result.append(user)
                if query in user['first_name'].lower():
                       result.append(user)
                if query in user['last_name'].lower():
                       result.append(user)
        
        return jsonify(result)


# Property section

@admin.route('/properties/add', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_properties():
        """
        adds property to the database
        """
        property_details = {}
        for key, value in request.form.items():
                if key == 'city' or key == 'neighborhood':
                       continue
                property_details[key] = value
        property_details['location'] = {'city': request.form.get('city'), 'neighborhood': request.form.get('neighborhood')}
        images = request.files.getlist('images')
        property_details['image_url'] = imageClass.add_images(admin.config['UPLOAD_FOLDER'], admin.config['ALLOWED_EXTENSIONS'], images)
        property_id = propertyClass.add_property(property_details)
        if 'error' in property_id.keys():
                return jsonify(property_id)
        property = propertyClass.get_property(property_id.get('property id'))
        result = {'message': 'property and images sucefully added', 'property': property}
        return jsonify(result)

@admin.route('/properties/<string:property_id>/update', methods=['POST'], strict_slashes=False)
@jwt_required()
def update_property(property_id: str):
        """
        update property with new details
        """
        property_details = request.form
        result = propertyClass.update_property(property_id, property_details)
        if 'error' in result.keys():
               return jsonify(result), 400
        return jsonify(result)

@admin.route('/properties/<string:property_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_property(property_id: str):
        """
        delete property
        """
        result = propertyClass.delete_property(property_id)
        if not result:
               return jsonify({'error': 'failed to delete'}), 400
        return jsonify({'message': 'property deleted'}), 204

@admin.route('/properties/search', methods=['GET'], strict_slashes=False)
@jwt_required
def search_for_properties():
        """
        get specified properties in the database
        """
        query = request.args.get('query')

        if not query:
                return jsonify({"error": "No search query provided"}), 400
        
        result = []
        # Perform the search logic based on the query parameter
        query = query.lower()
        for props in propertyClass.get_users():
                if query in props['city'].lower():
                      result.append(props)
                if query in props['location'].lower():
                       result.append(props)
                if query in props['price'].lower():
                        result.append(props)
        
        return jsonify(result)
