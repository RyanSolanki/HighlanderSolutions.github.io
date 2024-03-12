from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from .. import db
from ..models import Exercises, ScheduledWorkouts, UserWorkout
from flask_login import current_user
from ..access import DbAccessSingleton
from sqlalchemy.exc import IntegrityError

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
    dbInstance = DbAccessSingleton.get_instance()
    result = dbInstance.custom_query("SELECT DISTINCT workoutName FROM SavedWorkouts WHERE UserID = " + f"'{current_user.email}'")
    workoutNames = [row[0] for row in result]
    return jsonify(workoutNames)

@calender.route('/save_scheduled_workout', methods=['POST'])
def save_scheduled_workout():
    try:
        workoutData = request.get_json()['workoutData']
        scheduledWorkout = ScheduledWorkouts(date=workoutData['date'], workoutName=workoutData['workoutName'], userID=current_user.email)
        db.session.add(scheduledWorkout)
        db.session.commit()
        return 'Scheduled workout data saved successfully.', 200
    except IntegrityError:
        db.session.rollback()
        return 'Error: A workout for the selected date already exists.', 400
    except Exception as e:
        db.session.rollback()
        return f'Error: {str(e)}', 500
