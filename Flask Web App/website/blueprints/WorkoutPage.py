from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from .. import db
from ..models import Exercises, UserWorkout
from flask_login import current_user
from ..access import DbAccessSingleton

dbInstance = DbAccessSingleton.get_instance()

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

    result = dbInstance.custom_query("SELECT DISTINCT WorkoutName FROM SavedWorkouts WHERE UserID = " + f"'{current_user.email}'")
    result = list(result)
    workoutNames = [name[0] for name in result]
    # Render the template for GET requests
    return render_template('WorkoutPage.html', user=current_user, workoutNames=workoutNames)
    
@WorkoutPage.route('/save_workout', methods=['POST'])
def save_workout():
    # Get the workout data from the request
    workoutData = request.json.get('workoutData')
    workoutObj = UserWorkout(workoutData)
    # Print the workout to the console
    # workoutObj.printWorkout()    
    # Save the workout to the database
    workoutObj.save_workout_db()
    return render_template('home.html', user=current_user)


@workoutPage.route('/save_workout_data', methods=['POST'])
def save_workout_data():
    if request.method == 'POST':
        # Extract recommendation data from the request
        workoutName = request.json.get('workoutName')
        workoutData = request.json.get('workoutData')
        recommendation = [exercise['exerciseName'] for exercise in workoutData['exercises']]
        
        preselectedInfo = {}

        for exercise in workoutData['exercises']:
            preselectedInfo[exercise['exerciseName']] = {'sets': exercise['sets'], 'reps': exercise['reps'], 'weights': exercise['weight'], 'loaded': False}
        # Save the recommendation data in the session
        session['recommendation'] = recommendation
        #Save the preselected info in the session
        session['preselectedInfo'] = preselectedInfo
        
        # Redirect to the same route with a GET request
        return redirect(url_for('WorkoutPage.save_workout_data'))

@workoutPage.route('/save_workout_data', methods=['GET'])
def get_recommendation():
    # Retrieve recommendation data from the session
    recommendation = session.get('recommendation', [])
    preselectedInfo = session.get('preselectedInfo', {})

    result = dbInstance.custom_query("SELECT DISTINCT WorkoutName FROM SavedWorkouts WHERE UserID = " + f"'{current_user.email}'")
    result = list(result)
    workoutNames = [name[0] for name in result]
    # Figure out the best place to clear session data
    return render_template('ModifiedWorkoutPage.html', recommendation=recommendation, preselectedInfo=preselectedInfo, workoutNames=workoutNames, user=current_user)

# Displays recommended workout based on user input
@workoutPage.route('/Result', methods=['GET', 'POST'])
def result():
    muscleGroup = request.args.get('muscleGroup') #muscle_groups = request.args.getlist('muscle_groups') for multi musc selec
    equipment = request.args.get('equipment')
    recommendation = fetch_recommendation(muscleGroup, equipment)#recommendation = fetch_recommendation(muscle_groups, equipment)
    recommendation = [sublist[0] for sublist in recommendation]
    user = current_user if current_user.is_authenticated else None

    result = dbInstance.custom_query("SELECT DISTINCT WorkoutName FROM SavedWorkouts WHERE UserID = " + f"'{current_user.email}'")
    result = list(result)
    workoutNames = [name[0] for name in result]
    return render_template('Result.html', recommendation=recommendation, workoutNames=workoutNames, muscleGroup=muscleGroup, user=user) #changed muscle_group=muscle_group to muscle_groups=muscle_groups

def fetch_recommendation(muscleGroup, equipment): #Changed muscle_group to muscle_groups for multi select
    # Use the search method from DbAccessSingleton to fetch data from the database
    #query = f"SELECT Name FROM Exercises WHERE EquipType = '{equipment}' AND MuscleGroup IN ({','.join(['?' for _ in muscle_groups])})" 
    #muscle_group_condition = "OR".join([f'MuscleGroup = "{group}"' for group in muscle_groups])#for multi select
    #query = f'SELECT Name FROM Exercises WHERE EquipType = "{equipment}" AND ({muscle_group_condition})' #For multi select
    result = dbInstance.custom_query(f'SELECT Name FROM Exercises WHERE EquipType = "{equipment}" AND MuscleGroup = "{muscleGroup}"')#result = db_instance.custom_query(query, muscle_groups)

    # Return the recommendation if found, otherwise return a default message
    return result if result else "No workout recommendation found for the selected Muscle Group and Equipment."