from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Gets the variables from the Log In form
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Sucessfully!', category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again.', category="error")
        else:
            flash('Email does not exist.', category="error")
    
    return render_template('login.html', user=current_user)
    
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        # Gets the variables from the Sign Up form
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # Runs through conditons to ensure user should be created
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email alredy exists.', category="error")
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif (len(firstName) or len(lastName)) < 2:
            flash('First and Last names must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Password\'s do not match.')
        elif len(password1) < 7 or len(password2) < 7:
            flash('Passwords must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
            
        
    return render_template('sign-up.html', user=current_user)
