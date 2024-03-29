from flask import Blueprint, render_template, request, flash, redirect, url_for # Import the Blueprint class from the flask package
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
auth = Blueprint('auth', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@auth.route('/Login', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
def login():
    # If there is a POST request get email and password from user
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        # If user has an account, check if password is correct
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        # If user does not have an account, tell them email is invalid
        else:
            flash('Email is not associated with an account!', category='error')

    return render_template("Login.html", user=current_user) # This is the function that will be triggered when the URL is visited

@auth.route('/logout') # This is a decorator that tells Flask what URL to trigger the function
@login_required # This is a decorator that tells Flask that we need to login in order to logout
def logout():
    logout_user()
    return redirect(url_for('auth.login')) # This is the function that will be triggered when the URL is visited

@auth.route('/Sign-up', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
def sign_up():
    # If there is a POST request get user email, first name, password, and confirmed password
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        # Check if user exists and if first name and password are valid
        if user:
            flash('Email already in use.', category='error')
        elif len(email) < 4:
            flash('Email must be longer than 3 characters!', category='error')
        elif len(firstName) < 2:
            flash('First Name must be at least 2 characters long!', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            # add user credentials to database if all criteria is met
            db.create_all()
            newUser = User(email=email, firstName=firstName, 
                        password=generate_password_hash(password1, method ='pbkdf2:sha256'))
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("SignUp.html", user=current_user) # This is the function that will be triggered when the URL is visited