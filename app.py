import secrets
import json

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
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

@app.route('/user/profile', methods=['GET', 'POST'], strict_slashes=False)
@jwt_required()
def profile():
    # Retrieve the user from the database
    current_user = get_jwt_identity()
    user = userClass.get_user(current_user['email'])

    if request.method == 'POST':
        # Retrieve the submitted form data
        new_firstname = request.form.get('first_name')
        new_lastname = request.form.get('last_name')
        new_email = request.form.get('email')

        if user:
            # Update the user data with the submitted changes
            updated_data = {}
            if new_firstname:
                updated_data['first_name'] = new_firstname
            if new_lastname:
                updated_data['last_name'] = new_lastname
            if new_email:
                updated_data['email'] = new_email
            
            expected_fields = ['email', 'first_name', 'last_name']

            # check if no other field is being changed
            for field in request.form:
                if field not in expected_fields:
                    return jsonify({"error": 
                                    "Invalid field: {}".format(field)}), 403

            # Update the user in the database
            if userClass.update_user(user['_id'], updated_data):
                return jsonify({'success': 'Profile updated successfully.'})
            else:
                return jsonify({"error": "Failed to update profile. Please try again."})
        else:
            return jsonify({'error': 'User not found.'}), 404

    # if the request is `GET`
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user), 200
    else:
        return jsonify({'error':'No such User'}), 404


if __name__ == '__main__':
    app.run(debug=True)
