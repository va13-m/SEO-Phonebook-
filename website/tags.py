from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_socketio import join_room, send
import socketio
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import socketio

import random 

 
tags = Blueprint('tags', __name__)

tag_messages = {}

@socketio.on("join_tag_room")
def join_tag_room(data):
    tag_name = data["tag"]
    join_room(tag_name)
    if tag_name not in tag_messages:
        tag_messages[tag_name] = []
    send({"name": "System", "message": f"{data['name']} has joined the chat"}, to=tag_name)

@socketio.on("message")
def handle_message(data):
    tag_name = data["tag"]
    content = {"name": data["name"], "message": data["message"]}
    tag_messages[tag_name].append(content)
    send(content, to=tag_name)


@tags.route('/tags/<tag_name>')
@login_required
def tag_page(tag_name):
    users = User.query.all()
    related_users = []
    for user in users:
        if user.tags and tag_name.lower() in [t.strip().lower() for t in user.tags.split(',')]:
            related_users.append(user)
    return render_template("tags/tag_page.html", tag_name=tag_name, users=related_users, user=current_user)

@tags.route('/tags')
@login_required
def all_tags():
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

    tag_cards = []
    for tag in unique_tags:
        card = {
            "name": tag,
            "quote": random.choice(random_quotes),
        }
        tag_cards.append(card)

    return render_template("tags/all_tags.html", tag_cards=tag_cards, user=current_user)
