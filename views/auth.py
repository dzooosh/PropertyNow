"""
a view for `Auth` objects that handles all authentication REST API
actions
"""

from flask import request, jsonify, abort
from engine.redis import LRUCache
from auth.auth import Auth
from views import auth_views
from models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
)
lru = LRUCache()
userClass = User()
AUTH = Auth()


@auth_views.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')
    account_type = request.json.get('account_type', 'buyer')

    # check if user already exists
    user_exist = userClass.get_user(email)
    if user_exist:
        return jsonify({"error": "Email already exists!"})
    else:
        # Authenticate and register the user to the db
        reged_user = AUTH.signup_user(email=email,
                                      password=password,
                                      first_name=first_name,
                                      last_name=last_name,
                                      account_type=account_type,
                                      )
        if 'result' in reged_user.keys():
            return jsonify({"message": "User Successfully Created"}), 201
        else:
            # if the form is not validated, reload the signup form
            return jsonify({"error": "Failed to Create User"})


@auth_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not AUTH.validate_login(email, password):
        return jsonify({"message": "Invalid email or password"}), 401
    
    access_token = create_access_token(identity=email)
    # check if user is an admin
    if userClass.get_user(email)['account_type'] == 'admin':
        redirect_url = 'http://localhost:5173/admin/'
        return jsonify({'redirect': redirect_url,
                        'access_token': access_token}), 302
    
    return jsonify({'redirect': 'http://localhost:5173/properties/',
                    'access_token': access_token}), 302


@auth_views.route('/logout')
def logout():
    # handle the logout functionality
    return jsonify({"message": "You have been Logged Out"})


@auth_views.route('/change_password', methods=['POST'], strict_slashes=False)
@jwt_required()
def change_password():
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    confirm_password = request.json.get('confirm_password')

    if new_password != confirm_password:
        return jsonify({'error': 'New password do not match'}), 400

    # check if it's current user accessing this
    current_user = get_jwt_identity()
    if not current_user:
        abort(403, message="Not authorized")

    # check if old password is same as provided one
    user_exist = userClass.get_user(current_user)
    if check_password_hash(user_exist['password'], old_password):
        user_exist['password'] = new_password
        return jsonify({"messge": "Password updated successfully!"}), 200

    return jsonify({"message": "Invalid old password"}), 400


@auth_views.route('/reset-password/<token>', methods=['POST'],
                  strict_slashes=False)
def reset_password(token):
    # Handle password reset logic
    new_password = request.json.get('new_password')
    confirm_password = request.json.get('confirm_password')

    if new_password != confirm_password:
        return jsonify({'error': 'New password do not match'}), 400

    # validate the token
    user_email = AUTH.validate_token(token)
    if user_email:
        AUTH.update_password(user_email, new_password)
        lru.delete(token)
        return jsonify({"message": "Password changed successfully!"})
    return
