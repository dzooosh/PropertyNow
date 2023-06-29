import secrets
import json

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
    create_access_token
)
from flask_mail import Mail, Message
from auth import auth
from views import property_views, admin, auth_views
from models.user import User
from flask_cors import CORS

userClass = User()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'alongejoshua@gmail.com'
app.config['MAIL_PASSWORD'] = '*gutxqezdybimqlib*'

app.register_blueprint(property_views, url_prefix="/properties")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(auth_views, url_prefix="/auth")

AUTH = auth.Auth()
mail = Mail(app)  # handles mailing token to the user


# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
jwt = JWTManager(app)


@app.route('/forgot-password', methods=['POST'], strict_slashes=False)
def forgot_password():
    email = request.json.get('email')

    # checks email with the db
    user = userClass.get_user(email)
    if user:
        # Generate a random reset token
        token = AUTH.get_reset_token(email)
        # Send password reset email
        msg = Message('Password Reset',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email]
                      )
        reset_link = f'http://localhost:5173/auth/reset_password/{token}'
        msg.body = f"Click the link to reset your password: {reset_link}"
        js_msg = {"message":
                  "Password reset instructions have been sent to your email."
                  }
        # Send the email
        mail.send(msg)
        return jsonify(js_msg)
    else:
        return jsonify({"error": "The email does not exist"}), 404

@app.route('/user/profile', methods=['GET'], strict_slashes=False)
@jwt_required()
def user_profile():
    # Retrieve the user from the database
    current_user = get_jwt_identity()
    user = userClass.get_user(current_user['email'])

    user['_id'] = str(user['_id'])
    return jsonify(user)
    
@app.route('/user/profile', methods=['POST'], strict_slashes=False)
def update_profile():
    """ Updates profile
    """
    expected_fields = ['email', 'first_name', 'last_name']
    updated_data = {}
    for key, value in request.json.items():
        if key not in expected_fields:
            continue
        updated_data[key] = value
    user = userClass.get_user(updated_data['email'])
    user['_id'] = str(user['_id'])
    result = userClass.update_user(user['_id'], updated_data)
    if result:
        user = userClass.get_user(updated_data['email'])
        user['_id'] = str(user['_id'])
        return jsonify(user)
    else:
        return jsonify({"error": "Failed to update profile. Please try again."})



if __name__ == '__main__':
    app.run(debug=True)
