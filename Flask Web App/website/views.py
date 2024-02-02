from flask import Blueprint, render_template # Import the Blueprint class from the flask package

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
views = Blueprint('views', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@views.route('/') # This is a decorator that tells Flask what URL to trigger the function
def home():
    return render_template("home.html") # This is the function that will be triggered when the URL is visited