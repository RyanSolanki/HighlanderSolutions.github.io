from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from .. import db
from ..models import Exercises, ScheduledWorkouts, UserWorkout
from flask_login import current_user
from ..access import DbAccessSingleton

DATABASE = 'Flask Web App\instance\database.db'

# Create a Blueprint object
calender = Blueprint('calender', __name__)

@calender.route('/Calender')
def calendar():
    return render_template('Calender.html', user=current_user)

@calender.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercises.query.all()
    exercisesList = [{'name': exercise.name, 'muscleGroup': exercise.muscleGroup, 'equipType': 
                       exercise.equipType} for exercise in exercises]
    return jsonify(exercisesList)

@calender.route('/workout_names', methods=['GET'])
def get_workout_names():
    db_instance = DbAccessSingleton.get_instance()  # Get the DBAccessSingleton instance
    result = db_instance.custom_query("SELECT DISTINCT workoutName FROM SavedWorkouts WHERE UserID = " + f"'{current_user.email}'")
    workout_names = [row[0] for row in result]  # Extract workout names from the query result
    return jsonify(workout_names)

@calender.route('/save_scheduled_workout', methods=['POST'])
def save_scheduled_workout():
    workout_data = request.get_json()['workoutData']

    scheduled_workout = ScheduledWorkouts(date=workout_data['date'], workoutName=workout_data['workoutName'])

    db.session.add(scheduled_workout)

    db.session.commit()

    return 'Scheduled workout data saved successfully.', 200
