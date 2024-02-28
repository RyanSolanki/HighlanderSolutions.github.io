from flask import Blueprint, render_template, request, redirect, url_for # Import the Blueprint class from the flask package
from flask_login import login_required, current_user

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
views = Blueprint('views', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@views.route('/', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
@login_required # This is a decorator that tells Flask we need to login before accessing the home page
def home():
    if request.method == 'POST':
        muscle_group = request.form.get('MuscleGroup')
        equipment = request.form.get('Equipment')

        return redirect(url_for('WorkoutPage.result', muscle_group=muscle_group, equipment=equipment))

    else:
        return render_template("Home.html", user=current_user) # This is the function that will be triggered when the URL is visited