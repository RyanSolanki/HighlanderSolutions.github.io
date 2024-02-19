from .models import Exercises
from flask import jsonify
from flask import Blueprint, render_template

DATABASE = '/path/to/your/database.db'

# Create a Blueprint object
calender = Blueprint('calender', __name__)

@calender.route('/Calender')
def calendar():
    return render_template('calender.html')

@calender.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercises.query.all()
    exercisesList = [{'name': exercise.name, 'muscleGroup': exercise.muscleGroup, 'equipType': 
                       exercise.equipType} for exercise in exercises]
    return jsonify(exercisesList)