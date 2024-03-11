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
    db_instance = DbAccessSingleton.get_instance()
    result = db_instance.custom_query("SELECT DISTINCT workoutName FROM SavedWorkouts WHERE UserID = " + f"'{current_user.email}'")
    workout_names = [row[0] for row in result]
    return jsonify(workout_names)

@calender.route('/save_scheduled_workout', methods=['POST'])
def save_scheduled_workout():
    try:
        workout_data = request.get_json()['workoutData']
        scheduled_workout = ScheduledWorkouts(date=workout_data['date'], workoutName=workout_data['workoutName'], userID=current_user.email)
        db.session.add(scheduled_workout)
        db.session.commit()
        return 'Scheduled workout data saved successfully.', 200
    except IntegrityError:
        db.session.rollback()
        return 'Error: A workout for the selected date already exists.', 400
    except Exception as e:
        db.session.rollback()
        return f'Error: {str(e)}', 500

@calender.route('/get_scheduled_workouts', methods=['GET'])
def get_scheduled_workouts():
    try:
        date = request.args.get('date')
        user_id = current_user.email
        scheduled_workouts = ScheduledWorkouts.query.filter_by(date=date, userID=user_id).all()
        workout_names = [workout.workoutName for workout in scheduled_workouts]
        return jsonify(workout_names), 200
    except Exception as e:
        return f'Error: {str(e)}', 500
