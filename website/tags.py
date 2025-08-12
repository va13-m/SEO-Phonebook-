from flask import Blueprint, render_template
from flask_socketio import join_room, send
from .models import User
from flask_login import  login_required, current_user
from . import socketio
import random 

# Blueprint for tags
tags = Blueprint('tags', __name__)

# Dictionary to hold messages for each tag room
tag_messages = {}

# Called when a user joins a tag room
@socketio.on("join_tag_room")
def join_tag_room(data):
    # Check if the tag exists in the messages dictionary
    tag_name = data["tag"]
    # given the tag, subscribe the user to the tag room
    join_room(tag_name)
    # If the tag does not exist, create an empty list for it
    if tag_name not in tag_messages:
        tag_messages[tag_name] = []
    #User has joined message
    send({"name": "System", "message": f"{data['name']} has joined the chat"}, to=tag_name)

# Handle incoming messages in a tag room
@socketio.on("message")
def handle_message(data):
    # Check if the tag exists in the messages dictionary
    tag_name = data["tag"]
    
    #package the message content
    content = {"name": data["name"], "message": data["message"]}
    tag_messages[tag_name].append(content)
    send(content, to=tag_name)

# Route to render the tag page
# This page shows users associated with a specific tag and chat 
@tags.route('/tags/<tag_name>')
@login_required
def tag_page(tag_name):
    # Fetch users associated with the tag
    users = User.query.all()
    related_users = []
    for user in users:
        if user.tags and tag_name.lower() in [t.strip().lower() for t in user.tags.split(',')]:
            related_users.append(user)
    return render_template("tags/tag_page.html", tag_name=tag_name, users=related_users, user=current_user)

# Route to display all tags and their associated quotes
@tags.route('/tags')
@login_required
def all_tags():
    # Fetch all users and their tags, then create a unique set of tags
    users = User.query.all()
    all_tags = []
    for user in users:
        if user.tags:
            all_tags.extend(user.tags.split(','))
    unique_tags = set(tag.strip().lower() for tag in all_tags)
    
    random_quotes = [
        "Creativity is intelligence having fun.",
        "Design is thinking made visual.",
        "Every tag tells a story.",
        "Simplicity is the ultimate sophistication.",
        "Express yourself with style."
    ]

    # Build tag cards with random quotes
    tag_cards = []
    for tag in unique_tags:
        card = {
            "name": tag,
            "quote": random.choice(random_quotes),
        }
        tag_cards.append(card)

    return render_template("tags/all_tags.html", tag_cards=tag_cards, user=current_user)
