""" User Authentication """
from .app import app
from models.user import User
from flask_bcrypt import Bcrypt
from uuid import uuid4
from typing import Dict, Any


bcrypt = Bcrypt(app)


def _encode_password(password: str):
        """ encodes any password which needs to be stored in the database
        Arg:
            password: the given password
        Returns:
            the encoded password
        """
        return bcrypt.generate_password_hash(password).decode('utf-8')


class Auth:
    """ Authentication class"""
    def __init__(self):
        """ initialising the Auth class"""
        self.user = User()

    def signup_user(self, email: str, password: str, **kwargs) -> Dict[User, Any]:
        """ registers user by adding to the database or checking
        if already exists
        Args:
            email (str): email string arguments
            password(str): password
        Return:
            User (user object)
        """
        # check if user is present in the db
        user = self.user.get_user(email=email)
        # if user does not exist, add user
        if user is None:
            user_detail = {}
            user_detail['email'] = email
            user_detail['password'] = _encode_password(password)

            for key, value in kwargs.items():
                user_detail[str(key)] = value
            return self.user.add_user(user_detail)
        else:
            return None
        
    def validate_login(self, email: str, password: str) -> bool:
        """ validates the login credentials
        Args:
            email (str): email to validate
            password (str): password to validate
        Returns:
            True - if it matches with user details
            False - if it does not match
        """
        user = self.user.get_user(email=email)
        if user is None:
            return False
        # use bcrypt to check the password against database
        db_pswd = user.get('password')
        if bcrypt.check_password_hash(db_pswd, password):
            return True
        else:
            return False
        
