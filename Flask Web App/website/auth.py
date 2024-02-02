from flask import Blueprint, render_template # Import the Blueprint class from the flask package

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
auth = Blueprint('auth', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@auth.route('/login') # This is a decorator that tells Flask what URL to trigger the function
def login():
    return render_template("login.html", text="Testing", user="Jake", boolean = True) # This is the function that will be triggered when the URL is visited

@auth.route('/logout') # This is a decorator that tells Flask what URL to trigger the function
def logout():
    return "<p>Logout</p>" # This is the function that will be triggered when the URL is visited

@auth.route('/sign-up') # This is a decorator that tells Flask what URL to trigger the function
def sign_up():
    return render_template("sign_up.html") # This is the function that will be triggered when the URL is visited