import unittest
from werkzeug.security import check_password_hash
from models.user import User
from engine import storage
from auth.auth import Auth


class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storage = storage
        cls.user = User()
        cls.auth = Auth()

    @classmethod
    def tearDownClass(cls):
        user_emails = [
            'test@example.com',
            'test2@example.com'
        ]
        for email in user_emails:
            user_id = str(cls.user.get_user(email)['_id'])
            cls.user.delete_user(user_id)

    def test_signup_user_valid(self):
        """ test signup with valid user details
        """
        email = 'test@example.com'
        password = 'password123'

        result = self.auth.signup_user(
            email=email,
            password=password,
            first_name='John',
            last_name='Doe',
            account_type='buyer'
            )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {'result': 'user created'})
        
        # check if detail in db are matching
        user = self.user.get_user(email)
        self.assertIsInstance(user, dict)
        self.assertEqual(user["email"], email)
        self.assertTrue(check_password_hash(user["password"], password))


    def test_signup_user_invalid(self):
        email = 'test@example.com'
        password = 'password123'

        result = self.auth.signup_user(
            email=email,
            password=password,
            first_name='John',
            last_name='Doe'
            )

        self.assertEqual(result, {'error': 'Missing account_type'})

    def test_validate_login_valid(self):
        email = "test@example.com"
        password = "password123"

        result = self.auth.validate_login(email, password)
        self.assertTrue(result)

    def test_validate_login_invalid(self):
        email = "test@example.com"
        password = "invalid"

        result = self.auth.validate_login(email, password)
        self.assertFalse(result)

    def test_get_reset_token(self):
        email = "test@example.com"
        password = "password123"

        if self.auth.validate_login(email, password):
            token = self.auth.get_reset_token(email)
            self.assertIsInstance(token, str)


    def test_validate_token(self):
        email = "test@example.com"
        password = "password123"

        if self.auth.validate_login(email, password):
            token = self.auth.get_reset_token(email)
            result = self.auth.validate_token(token)
            self.assertEqual(result, email)

    def test_validate_token_invalid(self):
        token = "invalid_token"
        result = self.auth.validate_token(token)
        self.assertIsNone(result)

    def test_update_password_valid(self):
        email = "test2@example.com"
        password = "passwrd"

        self.auth.signup_user(
            email=email,
            password=password,
            first_name='Test',
            last_name='Jay',
            account_type='buyer'
            )

        if self.auth.validate_login(email, password):
            new_password = "new_password"
            self.auth.update_password(email=email, password=new_password)
        
            result = self.auth.validate_login(email, new_password)
            self.assertTrue(result)

    def test_update_password_invalid(self):
        """ Trying to update the password for a non-existing user
        """
        email = "test4@example.com"
        new_password = "new_password1"

        with self.assertRaises(ValueError):
            self.auth.update_password(email, new_password)

if __name__ == '__main__':
    unittest.main()
