from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from . import db
from .models import Exercises
from flask_login import current_user

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

@WorkoutPage.route('/WorkoutPage', methods=['GET','POST'])
def workoutPage():
    if request.method == 'POST':
        name = request.form['name']
        muscleGroup = request.form['muscleGroup']
        equipType = request.form['equipType']

        exercises = Exercises(name=name, muscleGroup=muscleGroup, equipType=equipType)
        db.session.add(exercises)
        db.session.commit()

        return redirect(url_for('WorkoutPage'))

    return render_template('WorkoutPage.html', user=current_user)