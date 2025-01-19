# tests/test_app.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.data == b"Hello, Flask!"