"""
a view for `admin` that handles all admins REST API
actions
Admin - Add (user, admin, properties)
        Remove (user, properties)
        Update(properties, User (change user to admin))
"""
from flask import jsonify
from views import admin
from auth import userClass
from property import propertyClass


@admin.route('/')
def admin_home():
    return "Welcome To Admin Home"

# user section

@admin.route('/users/<int:user_id>', methods=['DELETE'],
             strict_slashes=False)
def delete_user(user_id):
    user = userClass.get_user(user_id)
    if not user:
        return jsonify(error='Property not found'), 404

    del_user = userClass.delete_user(user)
    if 
    return '', 204