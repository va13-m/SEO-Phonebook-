from flask import Blueprint, render_template, flash, redirect, url_for,flash
from flask_login import login_required, current_user
from website import db  
from website.models import User  
from website.forms import UpdateProfileForm 
from .forms import UpdateProfileForm 

# Create a Blueprint for the profile routes
profile = Blueprint('profile', __name__)

# Route to view the profile page of the current user
@profile.route('/profile')
@login_required
def profile_view():
    return render_template("profile.html", user=current_user)

# Route to update the profile of the current user
@profile.route('/profile/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_profile(id):
    user = User.query.get_or_404(id)
    # Check if the current user is trying to update their own profile
    if current_user.id != user.id:
        flash("You are not authorized to edit this profile.", "danger")
        return redirect(url_for('profile.profile_view'))

    form = UpdateProfileForm(obj=user)

    # If the form is submitted and valid, update the user profile
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data
        user.city = form.city.data
        user.state = form.state.data
        user.tags = form.tags.data
        user.interests = form.interests.data
        try:
            # Update the user in the database
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for('profile.profile_view'))
        except:
            # If there is an error, rollback the session and flash an error message
            db.session.rollback()
            flash("Error updating profile.", "danger")

    return render_template("profile_update.html", form=form, user=user)

# Route to delete a user profile
@profile.route('/delete/<int:id>')
@login_required
def delete(id):
    # Check if the current user is trying to delete their own profile
    if id != current_user.id:
        flash("Sorry, you can't delete that user!")
        return redirect(url_for('profile'))

    user_to_delete = User.query.get_or_404(id)
    # Attempt to delete the user
    try:
        # Delete the user from the database
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!")
    except Exception as e:
        # If there is an error, flash an error message
        db.session.rollback()
        flash("Whoops! There was a problem deleting the user, try again...")
        print(f"Delete Error: {e}")
    
    return redirect(url_for("auth.sign_up"))

# Route to view a specific user's profile by ID
@profile.route('/profile/<int:id>')
@login_required
def view_profile(id):
    # Fetch the user by ID or return a 404 error if not found
    user = User.query.get_or_404(id)
    return render_template("profile.html", user=user)


