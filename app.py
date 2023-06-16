import secrets
import json

from flask import (
    Flask, flash, abort,
    render_template, redirect,
    url_for, request, jsonify
)

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required
)

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from auth import Auth
from views import property_views
from models.user import User
from models.property import Property
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = secrets.token_hex(32)

app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'
app.register_blueprint(property_views, url_prefix="/property")

AUTH = Auth()
mail = Mail(app)  # handles mailing token to the user
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
jwt = JWTManager(app)


@app.route('/auth/signup', methods=['POST'], strict_slashes=False)
def signup():
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        account_type = request.form.get('account_type')

        # check if user already exists
        user = User()
        user_exist = user.get_user(email)
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
            if reged_user:
                return jsonify({"message": "User Successfully Created"}), 201
            else:
                # if the form is not validated, reload the signup form
                return jsonify({"error": "Failed to Create User"})

@app.route('/auth/login', methods=['POST'], strict_slashes=False)
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not AUTH.validate_login(email, password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({'access_token': access_token}), 200


@app.route('/logout')
def logout():
    
    return jsonify({"message": "You have been Logged Out"})


@app.route('/auth/update_password', methods=['POST'], strict_slashes=False)
@jwt_required()
def update_password():
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
        user = User()
        user_exist = user.get_user(current_user)
        if check_password_hash(user_exist['password'], old_password):
            user_exist['password'] = new_password
            return jsonify({"messge": "Password updated successfully!"}), 200

        return jsonify({"message": "Invalid old password"}), 400


@app.route('/forgot-password', methods=['POST'], strict_slashes=False)
def forgot_password():
    email = request.json.get('email')

    # checks email with the db
    user = user.get_user(email)
    if user:
        # Send password reset email
        # send_password_reset_email(user)
        return jsonify({"message": "Password reset instructions have been sent to your email."})
    else:
        return jsonify({"error": "The email does not exist"})


@app.route('/reset-password/<token>', methods=['GET', 'POST'],
           strict_slashes=False)
def reset_password(token):
    # Handle password reset logic
    pass


if __name__ == '__main__':
    app.run(debug=True)
