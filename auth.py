""" User Authentication """
from .app import app
from engine import storage
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


class Auth:
    """ Authentication class"""
    def encode_password(self, password: str):
        """ encodes any password which needs to be stored in the database
        Arg:
            password: the given password
        Returns:
            the encoded password
        """
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_email(self, email: str) -> bool:
        """ check if the given email exists in the database
        Args:
            email: the guest's/user's email
        Return:
            True if valid, False if not
        """
        user = storage.get_user(email=email)
        if email == user['email']:
            return True
        else:
            return False

    def check_password(self, email: str, password: str) -> bool:
        """ validates password
        Args:
            password: guest's/user's passwords given
        Returns:
            True if valid, False if not
        """
        user = storage.get_user(email=email)
        db_password = user['password']
        if bcrypt.check_password_hash(db_password, password):
            return True
        else:
            return False
