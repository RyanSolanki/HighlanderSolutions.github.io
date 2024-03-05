from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from .. import db
from ..models import Exercises, UserWorkout
from flask_login import current_user
from ..access import DbAccessSingleton

db_instance = DbAccessSingleton.get_instance()

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
# The first argument is the name of the blueprint, and the second argument is the name of the module
#  or package where the blueprint is located
WorkoutPage = Blueprint('WorkoutPage', __name__) 
    
@WorkoutPage.route('/exercises')
def get_exercises():
    exercises = Exercises.query.all()
    exercisesList = [{'name': exercise.name, 'muscleGroup': exercise.muscleGroup, 'equipType': 
                       exercise.equipType} for exercise in exercises]
    return jsonify(exercisesList)

@WorkoutPage.route('/WorkoutPage', methods=['GET', 'POST'])
def workoutPage():
    if request.method == 'POST':
        name = request.form['name']
        muscleGroup = request.form['muscleGroup']
        equipType = request.form['equipType']

        exercises = Exercises(name=name, muscleGroup=muscleGroup, equipType=equipType)
        db.session.add(exercises)
        db.session.commit()

        return redirect(url_for('WorkoutPage.workoutPage'))

    # Render the template for GET requests
    return render_template('WorkoutPage.html', user=current_user)
    
@WorkoutPage.route('/save_workout', methods=['POST'])
def save_workout():
    # Get the workout data from the request
    workout_data = request.json.get('workoutData')
    workoutObj = UserWorkout(workout_data)
    # Print the workout to the console
    # workoutObj.printWorkout()    
    # Save the workout to the database
    workoutObj.saveWorkoutDB()
    return render_template('home.html', user=current_user)


@WorkoutPage.route('/save_workout_data', methods=['POST'])
def save_workout_data():
    if request.method == 'POST':
        # Extract recommendation data from the request
        workout_name = request.json.get('workoutName')
        workout_data = request.json.get('workoutData')
        recommendation = [exercise['exerciseName'] for exercise in workout_data['exercises']]
        
        # Save the recommendation data in the session
        session['recommendation'] = recommendation
        
        # Redirect to the same route with a GET request
        return redirect(url_for('WorkoutPage.save_workout_data'))

@WorkoutPage.route('/save_workout_data', methods=['GET'])
def get_recommendation():
    # Retrieve recommendation data from the session
    recommendation = session.get('recommendation', [])
    return render_template('Result.html', recommendation=recommendation, user=current_user)

# Displays recommended workout based on user input
@WorkoutPage.route('/Result', methods=['GET', 'POST'])
def result():
    muscle_group = request.args.get('muscle_group')
    equipment = request.args.get('equipment')
    recommendation = fetch_recommendation(muscle_group, equipment)
    recommendation = [sublist[0] for sublist in recommendation]
    print(recommendation)

    user = current_user if current_user.is_authenticated else None
    return render_template('Result.html', recommendation=recommendation, user=user)

def fetch_recommendation(muscle_group, equipment):
    # Use the search method from DbAccessSingleton to fetch data from the database
    result = db_instance.custom_query(f'SELECT Name FROM Exercises WHERE EquipType = "{equipment}" AND MuscleGroup = "{muscle_group}"')

    # Return the recommendation if found, otherwise return a default message
    return result if result else "No workout recommendation found for the selected Muscle Group and Equipment."