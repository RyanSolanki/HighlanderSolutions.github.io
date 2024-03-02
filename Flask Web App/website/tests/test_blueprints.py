# test_blueprints.py
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from website import create_app
from website.models import User
from .. import db
import pytest

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    with app.app_context():
        db.create_all()  # Create tables in the in-memory database
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

# tests/test_blueprints.py
def test_sign_up(client):
    response = client.post('/Sign-up', data={'email': 'newuser@example.com', 'firstName': 'New', 'password1': 'testpassword', 'password2': 'testpassword'})
    assert response.status_code == 200  # Check of code == 200 (Successful Sign-up)

def test_login(client):
    response = client.post('/Login', data={'email': 'newuser@example.com', 'password': 'testpassword'})
    assert response.status_code == 302  # Check of code == 302 (302 represents redirect to /views home page)

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302  # Check of code == 302 (302 represents redirect to /Login page)