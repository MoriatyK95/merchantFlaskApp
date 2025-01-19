# tests/test_app.py
import sys
import os
import unittest
from flask import json
from bson import ObjectId

# Add the parent directory to the system path to import the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app  # Import create_app and mongo instance from app.py

def test_home():
    """
    Test the home route to ensure it returns the expected greeting message.
    """
    client = app.test_client()
    response = client.get('/')
    assert response.data == b"Hello, Flask!"


class FlaskTestCase(unittest.TestCase):
    """
    Test case for the Flask application.
    """

    def setUp(self):
        """
        Set up the test client and add a test user to the database.
        This method is called before each test.
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        # Add a test user to the database
        with self.app.app_context():
            self.test_user = {"username": "Test User", "email": "testuser@example.com", "role": "merchant"}
            self.user_id = self.app.mongo.db.users.insert_one(self.test_user).inserted_id

    def tearDown(self):
        """
        Remove the test user from the database.
        This method is called after each test.
        """
        with self.app.app_context():
            self.app.mongo.db.users.delete_one({"_id": self.user_id})

    def test_home(self):
        """
        Test the home route to ensure it returns the expected greeting message.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello, Flask!")

    def test_get_users(self):
        """
        Test the GET /users endpoint to ensure it returns a list of users.
        """
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("username", data[0])
        self.assertIn("email", data[0])
        self.assertIn("role", data[0])

    def test_create_user(self):
        """
        Test the POST /users endpoint to ensure it creates a new user.
        """
        new_user = {"username": "newuser", "email": "newuser@example.com", "role": "admin"}
        response = self.client.post('/users', json=new_user)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("_id", data)

        # Clean up by deleting the created user
        with self.app.app_context():
            self.app.mongo.db.users.delete_one({"_id": ObjectId(data["_id"])})

    def test_get_user_by_email(self):
        """
        Test the GET /user endpoint to retrieve a user by email.
        """
        response = self.client.get(f'/user?email={self.test_user["email"]}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["email"], self.test_user["email"])

    def test_get_user_by_id(self):
        """
        Test the GET /user endpoint to retrieve a user by userId.
        """
        response = self.client.get(f'/user?userId={self.user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["_id"], str(self.user_id))
        self.assertEqual(data["username"], self.test_user["username"])
        self.assertEqual(data["email"], self.test_user["email"])
        self.assertEqual(data["role"], self.test_user["role"])

if __name__ == '__main__':
    unittest.main()

