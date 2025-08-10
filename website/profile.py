from flask import Blueprint, render_template, request, flash, redirect, url_for,flash
from flask_login import login_required, current_user
from website import db  # if db is initialized in app.py
from website.models import User  # replace with your actual model import
from website.forms import UpdateProfileForm  # assuming you made a WTForm
from .forms import UpdateProfileForm 
profile = Blueprint('profile', __name__)

@profile.route('/profile')
@login_required
def profile_view():
    return render_template("profile.html", user=current_user)


@profile.route('/profile/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_profile(id):
    user = User.query.get_or_404(id)

    if current_user.id != user.id:
        flash("You are not authorized to edit this profile.", "danger")
        return redirect(url_for('profile.profile_view'))

    form = UpdateProfileForm(obj=user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data
        user.city = form.city.data
        user.state = form.state.data
        user.tags = form.tags.data
        user.interests = form.interests.data
        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for('profile.profile_view'))
        except:
            db.session.rollback()
            flash("Error updating profile.", "danger")

    return render_template("profile_update.html", form=form, user=user)



@profile.route('/delete/<int:id>')
@login_required
def delete(id):
    if id != current_user.id:
        flash("Sorry, you can't delete that user!")
        return redirect(url_for('profile'))

    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!")
    except Exception as e:
        db.session.rollback()
        flash("Whoops! There was a problem deleting the user, try again...")
        print(f"Delete Error: {e}")
        

    return redirect(url_for("auth.sign_up"))

