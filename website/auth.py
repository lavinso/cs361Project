from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ Renders login page. Flashes success or error messages based on login form data """
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
            flash('No profile matches that email.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    """ Log's user out of site. Renders login page and success message when user is logged out. """
    logout_user()
    flash('You are now logged out!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """ Renders and handles sign up page for new user. """
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        error = validate_signup_form(email, first_name, last_name, password1, password2)
        if error:
            flash(error, category='error')
        else:
            create_user(email, first_name, last_name, password1)
            flash('Account created! You are now logged in.', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


def validate_signup_form(email, first_name, last_name, password1, password2):
    """ Validates form data from sign up form. """
    user = User.query.filter_by(email=email).first()
    if user:
        return 'Email already exists.'
    elif len(email) < 4:
        return 'Email must be greater than 3 characters.'
    elif len(first_name) < 2:
        return 'Please enter first name.'
    elif len(last_name) < 2:
        return 'Please enter last name.'
    elif password1 != password2:
        return 'Passwords don\'t match.'
    elif len(password1) < 7:
        return 'Password must be at least 7 characters.'


def create_user(email, first_name, last_name, password):
    """ Adds new user to database using information gathered from sign up page """
    new_user = User(email=email, first_name=first_name, last_name=last_name,
                    password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True)
