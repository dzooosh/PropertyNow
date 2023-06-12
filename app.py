import secrets
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from auth import Auth, bcrypt
from models.user import User
from models.property import Property
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'

mail = Mail(app)  # handles mailing token to the user
AUTH = Auth()
user = User()
login_manager = LoginManager()
login_manager.init_app(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# flask-Login loads user object to know current_user
@login_manager.user_loader
def load_user(email):
    """ load user object for flask-login to call for each
    authentication request
    Args:
        user_id: the id attached to a user
    Return:
        User object
    """
    user = User()
    user = user.get_user(email=email)
    return user


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():  # if details entered are valid
            # Retrieve form data
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            account_type = request.form.get('account_type')

            # check if user already exists
            user = User()
            user_exist = user.get_user(email)
            if user_exist:
                flash("Email already exists!", "error")
                return render_template(url_for('signup'), form=form)
            
            # Authenticate and register the user to the db
            reged_user = AUTH.signup_user(email=email,
                                          password=password,
                                          first_name=first_name,
                                          last_name=last_name,
                                          account_type = account_type
                                          )
            if reged_user:
                flash("User Successfully Created", "succes")
                return render_template(url_for('home'), reged_user=reged_user)
            else:
                # if the form is not validated, reload the signup form 
                flash("Failed to Create User", "error")
                return render_template(url_for('signup'), form=form)
    # if request.method is GET
    return render_template(url_for('signup'), form=form)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Authenticate the user by checking the credentials against the storage
        if AUTH.validate_login(email, password):
            user = User()
            user = user.get_user(email)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html',
                                   error='Invalid username or password')
    # if request method is GET
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/change-password', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password  = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        user = user.get_user(current_user.email)
        if bcrypt.check_password_hash(user['password'], old_password):
            if new_password == confirm_password:
                user['password'] = new_password
                flash("Password has been successfully changed!", "success")
                return redirect(url_for('home'))
            
    return render_template(url_for('change_password'))

@app.route('/forgot-password', methods=['GET', 'POST'], strict_slashes=False)
def forgot_password():
    # would ask for email to reset password
    if request.method == 'POST':
        email = request.form.get('email')
        # checks email with the db
        # generate, save and send token to email
        # redirect to the reset password page
        

@app.route('/reset-password/<token>', methods=['GET', 'POST'], strict_slashes=False)
def reset_password(token):
    # Handle password reset logic
    pass


if __name__ == '__main__':
    app.run(debug=True)
