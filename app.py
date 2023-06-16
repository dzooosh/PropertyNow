import secrets
import json

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from Auth.auth import Auth
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
app.config['MAIL_PASSWORD'] = 'gutxqezdybimqlib'

app.register_blueprint(property_views, url_prefix="/property")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(auth_views, url_prefix="/auth")

AUTH = Auth()
mail = Mail(app)  # handles mailing token to the user


# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
jwt = JWTManager(app)


@auth_views.route('/forgot-password', methods=['POST'], strict_slashes=False)
def forgot_password():
    email = request.json.get('email')

    # checks email with the db
    user = User()
    user = user.get_user(email)
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
        return jsonify(js_msg)
    else:
        return jsonify({"error": "The email does not exist"}), 404


if __name__ == '__main__':
    app.run(debug=True)
