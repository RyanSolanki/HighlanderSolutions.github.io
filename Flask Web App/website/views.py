from flask import Blueprint, render_template, request, flash, jsonify # Import the Blueprint class from the flask package
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
views = Blueprint('views', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@views.route('/', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
@login_required # This is a decorator that tells Flask we need to login before accessing the home page
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("Home.html", user=current_user) # This is the function that will be triggered when the URL is visited

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) #Take in data from a post request
    noteId = note['noteId'] #load the above as a python dictionary and access the noteId attribute found in index.js
    note = Note.query.get(noteId) #look for the note that has the id
    if note: #check if the note exists
        if note.user_id == current_user.id: #if the currently signed in user owns the note delete the note
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({}) #return an empty response because we have to return something