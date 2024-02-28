from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for # Import the Blueprint class from the flask package
from flask_login import login_required, current_user
from .access import DbAccessSingleton

db_instance = DbAccessSingleton.get_instance()

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
views = Blueprint('views', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@views.route('/', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
@login_required # This is a decorator that tells Flask we need to login before accessing the home page
def home():
    if request.method == 'POST':
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
    recommendation = [sublist[0] for sublist in recommendation]

    user = current_user if current_user.is_authenticated else None
    return render_template('Result.html', recommendation=recommendation, user=user)

def fetch_recommendation(muscle_group, equipment):
    # Use the search method from DbAccessSingleton to fetch data from the database
    result = db_instance.custom_query(f'SELECT Name FROM Exercises WHERE EquipType = "{equipment}" AND MuscleGroup = "{muscle_group}"')

    # Return the recommendation if found, otherwise return a default message
    return result if result else "No workout recommendation found for the selected Muscle Group and Equipment."