import unittest
from werkzeug.security import check_password_hash
from models.user import User
from auth.auth import Auth

class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.auth = Auth()
        cls.user = User()

    def tearDownClass(cls):
        # Clean up any test data or resources
        pass

    def test_signup_user_valid(self):
        email = "test@example.com"
        password = "password"

        result = self.auth.signup_user(email, password)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["email"], email)
        self.assertTrue(check_password_hash(result["password"], password))
        # Additional assertions for other properties

    def test_signup_user_invalid(self):
        email = "test@example.com"
        password = "password"

        # Add a user with the same email to simulate a duplicate user
        self.auth.signup_user(email, password)

        result = self.auth.signup_user(email, password)
        self.assertIsNone(result)

    def test_validate_login_valid(self):
        email = "test@example.com"
        password = "password"
        self.auth.signup_user(email, password)

        result = self.auth.validate_login(email, password)
        self.assertTrue(result)

    def test_validate_login_invalid(self):
        email = "test@example.com"
        password = "password"

        result = self.auth.validate_login(email, password)
        self.assertFalse(result)

    def test_get_reset_token_valid(self):
        email = "test@example.com"
        self.auth.signup_user(email, "password")

        token = self.auth.get_reset_token(email)
        self.assertIsInstance(token, str)
        # Additional assertions

    def test_get_reset_token_invalid(self):
        email = "test@example.com"
        token = self.auth.get_reset_token(email)
        self.assertIsNone(token)

    def test_validate_token_valid(self):
        email = "test@example.com"
        self.auth.signup_user(email, "password")
        token = self.auth.get_reset_token(email)

        result = self.auth.validate_token(token)
        self.assertEqual(result, email)

    def test_validate_token_invalid(self):
        token = "invalid_token"
        result = self.auth.validate_token(token)
        self.assertIsNone(result)

    def test_update_password_valid(self):
        email = "test@example.com"
        self.auth.signup_user(email, "password")
        token = self.auth.get_reset_token(email)
        new_password = "new_password"

        self.auth.update_password(email, new_password)
        result = self.auth.validate_login(email, new_password)
        self.assertTrue(result)

    def test_update_password_invalid(self):
        email = "test@example.com"
        new_password = "new_password"

        # Trying to update the password for a non-existing user
        with self.assertRaises(ValueError):
            self.auth.update_password(email, new_password)

if __name__ == '__main__':
    unittest.main()
