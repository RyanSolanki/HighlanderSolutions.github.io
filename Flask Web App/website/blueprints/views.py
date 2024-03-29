from flask import Blueprint, render_template, request, redirect, url_for # Import the Blueprint class from the flask package
from flask_login import login_required, current_user
from ..models import Note, UserWorkout
from .. import db
import json
from ..access import DbAccessSingleton

dbInstance = DbAccessSingleton.get_instance()

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
views = Blueprint('views', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@views.route('/', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
@login_required # This is a decorator that tells Flask we need to login before accessing the home page
def home():
    if request.method == 'POST':
        muscle_group = request.form.get('MuscleGroup') #get to getlist and muscle_group to muscle_groups for multi selec
        equipment = request.form.get('Equipment')

        return redirect(url_for('WorkoutPage.result', muscle_group=muscle_group, equipment=equipment)) #return redirect(url_for('WorkoutPage.result', muscle_groups=','.join(muscle_groups), equipment=equipment))#for multi musc selec

    else:
        workoutNames = []
        workoutList = []
        dbInstance = DbAccessSingleton.get_instance()
        result = dbInstance.custom_query("SELECT DISTINCT WorkoutName FROM SavedWorkouts WHERE UserID = " + f"'{current_user.email}'")
        result = list(result)
        for name in result:
            tempName = name[0]
            workoutNames.append(tempName)
        for name in workoutNames:
            workoutObj = UserWorkout({'name': name, 'exercises': []})
            workoutObj.get_workout_db()
            workoutList.append(workoutObj)
        # print(workoutList)
        # workoutObj = UserWorkout({'name': workoutName, 'exercises': []})
        # workoutObj.getWorkoutDB(workoutName)
        # workoutObj.printWorkout()#Below was WorkoutViewer
        return render_template("WorkoutViewer.html", user=current_user, workoutList=workoutList)