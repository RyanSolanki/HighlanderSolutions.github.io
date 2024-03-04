from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from .. import db
from ..models import Exercises, ScheduledWorkouts, SavedWorkouts
from flask_login import current_user

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

@calender.route('/save_scheduled_workout', methods=['POST'])
def save_scheduled_workout():
    workout_data = request.get_json()['workoutData']

    scheduled_workout = ScheduledWorkouts(date=workout_data['date'], workoutName=workout_data['workoutName'])

    db.session.add(scheduled_workout)

    db.session.commit()

    return 'Scheduled workout data saved successfully.', 200

@calender.route('/get_workout_names', methods=['GET'])
def get_workout_names():
    saved_workouts = SavedWorkouts.query.all()
    workout_names = [workout.WorkoutName for workout in saved_workouts]
    return jsonify(workout_names)
