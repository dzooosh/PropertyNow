""" User Authentication """
from werkzeug.security import generate_password_hash, check_password_hash

from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    url_for,
    request
)
from models.user import User
from typing import Dict, Any
import uuid
from engine.redis import LRUCache


def _encode_password(password: str):
    """encodes any password which needs
    to be stored in the database
    Arg:
        password: the given password
    Returns:
        the encoded password
    """
    return generate_password_hash(password)


def _generate_uuid() -> str:
    """ Generates a uuid
    """
    return str(uuid.uuid4())


class Auth:
    """ Authentication class"""
    def __init__(self):
        """ initialising the Auth class"""
        self.user = User()
        self.lru = LRUCache()

    def signup_user(self, email: str,
                    password: str, **kwargs):
        """ registers user by adding to the database or checking
        if already exists
        Args:
            email (str): email string arguments
            password(str): password
            kwargs: dict containing other required fields
        Return:
            return json from user model
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
        if check_password_hash(db_pswd, password):
            return True
        else:
            return False

    def get_reset_token(self, email: str) -> str:
        """ generates the user's reset password token
        Args:
            email (str) - user's email
        Return:
            token (str) - the reset password token
        """
        # find the user corresponding to the email
        user = self.user.get_user(email=email)
        if not user:
            raise ValueError()
        reset_token = _generate_uuid()
        self.lru.put(reset_token, user['email'])
        return reset_token

    def validate_token(self, token: str) -> str:
        """ validates token by checking for match in
        the database
        Args:
            token (str): token to validate
        Return:
            email (str): the user email
        """
        email = self.lru.get(token)
        if email is None or email == '':
            return None
        return email

    def update_password(self, email: str, password: str) -> None:
        """ updates the user's password
        Args:
            email (str): reset password token
            password (str): new password to be updated
        Return:
            True if successful or false if not 
        """
        user = self.user.get_user(email=email)
        if not user:
            raise ValueError()
        pswd = _encode_password(password)
        return self.user.update_user(str(user['_id']), {'password': pswd})
