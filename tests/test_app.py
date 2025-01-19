# tests/test_app.py
import sys
import os
import unittest
from flask import json

# Add the parent directory to the system path to import the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, mongo #import mongo instance from app.py

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
        self.app = app.test_client()
        self.app.testing = True

        # Add a test user to the database
        self.test_user = {"username": "Test User", "email": "testuser@example.com"}
        self.user_id = mongo.db.users.insert_one(self.test_user).inserted_id

    

    def tearDown(self):
        """
        Remove the test user from the database.
        This method is called after each test.
        """
        mongo.db.users.delete_one({"_id": self.user_id})


    def test_get_users(self):
        """
        Test the GET /users endpoint to ensure it returns a list of users.
        """
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("username", data[0])
        self.assertIn("email", data[0])

if __name__ == '__main__':
    unittest.main()