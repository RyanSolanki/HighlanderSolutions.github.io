from flask import Blueprint, render_template, request, flash, redirect, url_for # Import the Blueprint class from the flask package
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint object --> meaning it has a bunch of routes/URLs
auth = Blueprint('auth', __name__) # The first argument is the name of the blueprint, and the second argument is the name of the module or package

@auth.route('/login', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user) # This is the function that will be triggered when the URL is visited

@auth.route('/logout') # This is a decorator that tells Flask what URL to trigger the function
@login_required # This is a decorator that tells Flask that we need to login in order to logout
def logout():
    logout_user()
    return redirect(url_for('auth.login')) # This is the function that will be triggered when the URL is visited

@auth.route('/sign-up', methods=['GET', 'POST']) # This is a decorator that tells Flask what URL to trigger the function
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already in use.', category='error')
        elif len(email) < 4:
            flash('Email must be longer than 3 characters!', category='error')
        elif len(first_name) < 2:
            flash('First Name must be at least 2 characters long!', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            # add user to database
            db.create_all()
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method ='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user) # This is the function that will be triggered when the URL is visited