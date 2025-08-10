from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random 



interests = Blueprint('interest', __name__)

@interests.route('/interests/<interest_name>')
@login_required
def interest_page(interest_name):
    users = User.query.all()
    related_users = []
    for user in users:
        if user.interests and interest_name.lower() in [t.strip().lower() for t in user.interests.split(',')]:
            related_users.append(user)
    return render_template("interests/interest_page.html", interest_name=interest_name, users=related_users, user=current_user)


@interests.route('/interests')
@login_required
def all_interests():
    users = User.query.all()
    all_interests = []
    for user in users:
        if user.interests:
            all_interests.extend(user.interests.split(','))
    unique_interests = set(interest.strip().lower() for interest in all_interests)
    random_quotes = [
        "Creativity is intelligence having fun.",
        "Design is thinking made visual.",
        "Every tag tells a story.",
        "Simplicity is the ultimate sophistication.",
        "Express yourself with style."
    ]
    
    
    interests_cards = []
    for tag in unique_interests:
        card = {
            "name": tag,
            "quote": random.choice(random_quotes),
        }
        interests_cards.append(card)

    return render_template("interests/all_interests.html", interests_cards=interests_cards, user=current_user)
    
