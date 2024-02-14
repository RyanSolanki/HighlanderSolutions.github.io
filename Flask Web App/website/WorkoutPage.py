import os
from flask import Blueprint,Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask import Blueprint, render_template, request, flash, redirect, url_for # Import the Blueprint class from the flask package

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
WorkoutPage = Blueprint('WorkoutPage', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

class Workouts(db.Model):
    __tablename__ = 'Workouts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, name='Name')
    muscle_group = db.Column(db.String(100), nullable=False, name='Muscle Group')
    equip_type = db.Column(db.String(100), nullable=False, name='EquipType')  

    def __repr__(self):
        return f"Workouts(name={self.name}, muscle_group={self.muscle_group}, equip_type={self.equip_type})"
    
@WorkoutPage.route('/exercises')
def get_exercises():
    exercises = Workouts.query.all()
    exercises_list = [{'name': exercise.name, 'muscle_group': exercise.muscle_group, 'equip_type': exercise.equip_type} for exercise in exercises]
    return jsonify(exercises_list)

@WorkoutPage.route('/WorkoutPage', methods=['GET','POST'])
def workoutPage():
    if request.method == 'POST':
        name = request.form['name']
        muscle_group = request.form['muscle_group']
        equip_type = request.form['equip_type']

        workout = Workouts(name=name, muscle_group=muscle_group, equip_type=equip_type)
        db.session.add(workout)
        db.session.commit()

        return redirect(url_for('WorkoutPage'))

    return render_template('WorkoutPage.html')