from flask import Blueprint, render_template
from .models import User
from flask_socketio import join_room, send
from flask_login import login_required, current_user
from . import socketio
import random 
import socketio

# Create a Blueprint for interests
interests = Blueprint('interest', __name__)

interest_messages = {}

# Called when a user joins an interest room
@socketio.on("join_interest_room")
def join_interest_room(data):
    # Check if the interest exists in the messages dictionary
    interest_name = data["interest"]
    # given the interest, subscribe the user to the interest room
    join_room(interest_name)
    # If the interest does not exist, create an empty list for it
    if interest_name not in interest_messages:
        interest_messages[interest_name] = []
    #User has joined message
    send({"name": "System", "message": f"{data['name']} has joined the chat"}, to=interest_name)


# Handle incoming messages in the interest room
@socketio.on("interest_message")
def handle_interest_message(data):
    # Check if the interest exists in the messages dictionary
    interest_name = data["interest"]
    
    #package the message content
    content = {"name": data["name"], "message": data["message"]}
    interest_messages[interest_name].append(content)
    send(content, to=interest_name)

# Route to render the interest page
# This page shows users associated with a specific interest and chat 
@interests.route('/interests/<interest_name>')
@login_required
def interest_page(interest_name):
    # Fetch users associated with the interest
    users = User.query.all()
    related_users = []
    for user in users:
        if user.interests and interest_name.lower() in [t.strip().lower() for t in user.interests.split(',')]:
            related_users.append(user)
    return render_template("interests/interest_page.html", interest_name=interest_name, users=related_users, user=current_user)

# Route to display all interests and their associated quotes
@interests.route('/interests')
@login_required
def all_interests():
    # Fetch all users and their interests, then create a unique set of interests
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
    
    # Build interests cards with random quotes
    interests_cards = []
    for tag in unique_interests:
        card = {
            "name": tag,
            "quote": random.choice(random_quotes),
        }
        interests_cards.append(card)

    return render_template("interests/all_interests.html", interests_cards=interests_cards, user=current_user)
    
