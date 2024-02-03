from flask import Blueprint, render_template, request, flash # Import the Blueprint class from the flask package

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
auth = Blueprint('auth', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@auth.route('/login', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
def login():
    return render_template("login.html", text="Testing", user="Jake", boolean = True) # This is the function that will be triggered when the URL is visited

@auth.route('/logout') # This is a decorator that tells Flask what URL to trigger the function
def logout():
    return "<p>Logout</p>" # This is the function that will be triggered when the URL is visited

@auth.route('/sign-up', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be longer than 3 characters!', category='error')
        elif len(firstName) < 2:
            flash('First Name must be at least 2 characters long!', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            # add user to database
            flash('Account created!', category='success')

    return render_template("sign_up.html") # This is the function that will be triggered when the URL is visited