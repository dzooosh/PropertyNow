import secrets
import json

from flask import (
    Flask, flash,
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
from models.user import User
from models.property import Property


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'

AUTH = Auth()
mail = Mail(app)  # handles mailing token to the user
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
jwt = JWTManager(app)

# flask-Login loads user object to know current_user
@login_manager.user_loader
def load_user(email):
    """ load user object for flask-login to call for each
    authentication request
    Args:
        email: the email attached to a user
    Return:
        User object
    """
    user = User()
    return user.get_user(email)


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
    # Authenticate the user by checking the credentials against the storage
    user = User()
    user = user.get_user(email)

    access_token = create_access_token(identity=email)
    return jsonify({'access_token': access_token}), 200


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "You have been Logged Out"})


@app.route('/update_password', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            return jsonify({'error': 'New password do not match'})

        # check if old password matches password in database
        if check_password_hash(current_user['password'], old_password):
            current_user['password'] = new_password
            msg = {"messge": "Password updated successfully!"}
            return jsonify(msg)

        return jsonify({"message": "Invalid old password"})
    return render_template(url_for('update_password'))


@app.route('/forgot-password', methods=['GET', 'POST'], strict_slashes=False)
def forgot_password():
    # would ask for email to reset password
    if request.method == 'POST':
        email = request.form.get('email')

        # checks email with the db
        user = user.get_user(email)
        if user:
            # Send password reset email
            # send_password_reset_email(user)
            msg = {"email": f"{email}", 'message': 'Password reset instructions have been sent to your email.'}
            return jsonify(msg)
        else:
            return jsonify({"error": "The email does not exist"})

    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'],
           strict_slashes=False)
def reset_password(token):
    # Handle password reset logic
    pass


if __name__ == '__main__':
    app.run(debug=True)
