# recommender.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from . import db
from .models import Exercises
from flask_login import current_user

DATABASE = 'Flask Web App\instance\database.db'

# Create a Blueprint object
RecommenderBP = Blueprint('recommender', __name__)

@RecommenderBP.route('/Recommender')
def recommender():
    return render_template('Recommender.html', user=current_user)

@RecommenderBP.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercises.query.all()
    exercisesList = [{'name': exercise.name, 'muscleGroup': exercise.muscleGroup, 'equipType': 
                       exercise.equipType} for exercise in exercises]
    return jsonify(exercisesList)
