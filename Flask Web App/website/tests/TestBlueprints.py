# tests/test_blueprints.py

import time
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from website import create_app
from website.models import User
from .. import db
from flask_login import login_user
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


def test_sign_up_response(client):
    startTime = time.time()  # Record the start time
    response = client.post('/Sign-up', data={'email': 'test@example.com', 'firstName': 'New', 'password1': 'testpassword', 'password2': 'testpassword'})
    endTime = time.time()  # Record the end time
    assert response.status_code in [200, 302]  # Successful post and redirect to login page
    assert endTime - startTime < 0.5  # Ensure the response time is within 0.5 second

def test_login_response(client):
    startTime = time.time()  # Record the start time
    response = client.post('/Login', data={'email': 'test@example.com', 'password': 'testpassword'})
    endTime = time.time()  # Record the end time
    assert response.status_code == 302 # Successful redirect to home page
    assert endTime - startTime < 0.5  # Ensure the response time is within 0.5 second

def test_logout_response(client):
    startTime = time.time()  # Record the start time
    response = client.get('/logout')
    endTime = time.time()  # Record the end time
    assert response.status_code == 302 # Successful redirect to login page
    assert endTime - startTime < 0.5  # Ensure the response time is within 0.5 second

def test_home_page_response(client):
    # Simulate a logged-in user
    user = User(email='test@example.com', password='testpassword')
    login_user(user)
    startTime = time.time()  # Record the start time
    response = client.get('/')
    endTime = time.time()  # Record the end time
    assert response.status_code == 200 # Successful post request
    assert endTime - startTime < 0.5  # Ensure the response time is within 0.5 second

def test_workout_page_response(client):
    # Simulate a logged-in user
    user = User(email='test@example.com', password='testpassword')
    login_user(user)
    startTime = time.time()  # Record the start time
    response = client.get('/WorkoutPage')
    endTime = time.time()  # Record the end time
    assert response.status_code == 200 # Successful POST request to Workout Page
    assert endTime - startTime < 0.5  # Ensure the response time is within 0.5 second

def test_calender_page_response(client):
    # Simulate a logged-in user
    user = User(email='test@example.com', password='testpassword')
    login_user(user)
    startTime = time.time()  # Record the start time
    response = client.get('/Calender')
    endTime = time.time()  # Record the end time
    assert response.status_code == 200 # Successful POST request to Calender Page
    assert endTime - startTime < 0.5  # Ensure the response time is within 0.5 second

def test_recommender_page_response(client):
    # Simulate a logged-in user
    user = User(email='test@example.com', password='testpassword')
    login_user(user)
    startTime = time.time()  # Record the start time
    response = client.get('/Recommender')
    endTime = time.time()  # Record the end time
    assert response.status_code == 200 # Successful POST request to Recommender Page
    assert endTime - startTime < 0.5  # Ensure the response time is within 0.5 second