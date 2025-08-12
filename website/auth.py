from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint for authentication routes
auth = Blueprint('auth', __name__)

# Route to handle user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # read posted form values 
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            #check if the password is correct
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category ='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("auth/login.html", user=current_user)

# Route to handle user logout
@auth.route('/logout')
@login_required
def logout():
    # Log out the current user
    logout_user()
    return redirect(url_for('auth.login'))

# Route to handle user sign-up
@auth.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():
    # pull the form values from the request
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone_number = request.form.get('phone_number')
        city = request.form.get('city')
        state = request.form.get('state')
        tags = request.form.get('tags')
        interests = request.form.get('interests')
        seo = request.form.get('seo')
        
        # Check if the email already exists
        user = User.query.filter_by(email=email).first()

        # Validate the form data
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4: 
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 characters', category='error')
        elif len(phone_number) != 10:
            flash('Phone number must be 10 characters', category='error')
        elif len(state) != 2:
            flash('Use state abbreviation', category='error')  
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            # Create a new user instance and hash the password
            new_user = User(
                email=email,
                first_name=first_name,
                phone_number=phone_number,
                city=city,
                state=state,
                tags=tags,
                interests=interests,
                seo=seo,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template("auth/sign_up.html", user=current_user)
