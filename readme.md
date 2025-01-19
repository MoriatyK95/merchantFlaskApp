# Merchant Flask App

This is a simple Flask application that demonstrates the use of Flask Blueprints and MongoDB for managing user (merchants or shopist) data. The application includes endpoints for creating, retrieving, and listing users. It also includes a CI pipeline for automated testing.

## Key Features

- **Flask Blueprints**: The application is organized using Flask Blueprints to separate different parts of the application.
- **MongoDB Integration**: The application uses MongoDB to store user data.
- **CI Pipeline**: The application includes a CI pipeline for automated testing.

## Project Structure
merchantFlaskApp/ 
├── app.py 
├── requirements.txt ├
── users/ 
│ ├── init.py 
│ ├── routes.py 
├── tests/ 
│ ├── init.py 
│ ├── test_app.py


app.py
The main application file where the Flask app is created and configured. It initializes the MongoDB connection and registers the Blueprints.

users/routes.py
Contains the routes for managing users. It uses the MongoDB instance from the application context to perform database operations.

test_app.py
Contains the unit tests for the application. It uses the Flask test client to make requests to the application and verify the responses.

CI Pipeline
The CI pipeline is configured to run automated tests whenever changes are pushed to the repository. Here is an example of a GitHub Actions workflow file (.github/workflows/main.yml):


MongoDB users Collections stores user data: _id, username, email, role

How to run the application

pip3 install -r requirements.txt
python3 app.py

Run the tests:
python -m unittest discover -s tests -p "test_*.py"