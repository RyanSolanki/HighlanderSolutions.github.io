from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for # Import the Blueprint class from the flask package
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from .access import DbAccessSingleton

db_instance = DbAccessSingleton.get_instance()

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
views = Blueprint('views', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@views.route('/', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
@login_required # This is a decorator that tells Flask we need to login before accessing the home page
def home():
    if request.method == 'POST':
        # note = request.form.get('note')
        
        # if len(note) < 1:
        #     flash('Note is too short!', category='error')
        # else:
        #     new_note = Note(data=note, user_id=current_user.id)
        #     db.session.add(new_note)
        #     db.session.commit()
        #     flash('Note added!', category='success')
        muscle_group = request.form.get('MuscleGroup')
        equipment = request.form.get('Equipment')

        return redirect(url_for('views.result', muscle_group=muscle_group, equipment=equipment))

    else:
        return render_template("Home.html", user=current_user) # This is the function that will be triggered when the URL is visited

@views.route('/Result')
def result():
    muscle_group = request.args.get('muscle_group')
    equipment = request.args.get('equipment')
    recommendation = fetch_recommendation(muscle_group, equipment)
    user = current_user if current_user.is_authenticated else None
    return render_template('Result.html', recommendation=recommendation, user=user)

def fetch_recommendation(muscle_group, equipment):
    # Use the search method from DbAccessSingleton to fetch data from the database
    result = db_instance.custom_query(f'SELECT * FROM Exercises WHERE EquipType = "{equipment}" AND MuscleGroup = "{muscle_group}"')
    print(result)

    # Return the recommendation if found, otherwise return a default message
    return result[0] if result else "No workout recommendation found for the selected Muscle Group and Equipment."

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data) #Take in data from a post request
#     noteId = note['noteId'] #load the above as a python dictionary and access the noteId attribute found in index.js
#     note = Note.query.get(noteId) #look for the note that has the id
#     if note: #check if the note exists
#         if note.user_id == current_user.id: #if the currently signed in user owns the note delete the note
#             db.session.delete(note)
#             db.session.commit()
            
#     return jsonify({}) #return an empty response because we have to return something