# import secrets
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user
from .auth import Auth
from engine.db import Storage
from forms import RegistrationForm

app = Flask(__name__)
# app.config['SECRET_KEY'] = secrets.token_hex(32)

storage = Storage()
auth = Auth()
login_manager = LoginManager()
login_manager.init_app(app)


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
    user = Storage.get_user(email=email)
    return user


# @app.route('/')
# def home():
#     return 'Home Page'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():  # if details entered are valid
            # process your signup form data
            firstName = form.firstName.data
            lastName = form.lastName.data
            email = form.email.data
            password = form.password.data

            # encrypt the password
            hashed_password = auth.encode_password(password)
            # check if the email provided exists
            if auth.check_email(email):
                # Save the data into the database
                storage.add_user({
                    'firstName': firstName,
                    'lastName': lastName,
                    'email': email,
                    'password': hashed_password,
                })
                return render_template(url_for(signup), form=form)
            else:
                return render_template(url_for(signup), form=form)
        return render_template(url_for(signup), form=form)
    return render_template(url_for(home), form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if auth.check_email(email) and auth.check_password(email, password):
            user = Storage.get_user(email)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html',
                                   error='Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
