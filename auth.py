""" User Authentication """
from .app import app
from models.user import User
from flask_bcrypt import Bcrypt
from uuid import uuid4
bcrypt = Bcrypt(app)

def _encode_password(password: str):
        """ encodes any password which needs to be stored in the database
        Arg:
            password: the given password
        Returns:
            the encoded password
        """
        return bcrypt.generate_password_hash(password).decode('utf-8')

def _generate_uuid() -> str:
    """ Generates a uuid
    """
    return str(uuid4())

class Auth:
    """ Authentication class"""
    def __init__(self):
        """ initialising the Auth class"""
        self.user = User()
    
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
