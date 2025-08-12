from operator import or_
from typing import Counter
from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import requests
import random
import os
from . import db 
from website.models import User

import random 

views = Blueprint('views', __name__)
UNSPLASH_ACCESS_KEY = "KjWYQ8pXPRSEnJlxAqpuYhyQP0_8QPucP0YojCYwoyk"
CACHE = {}
CACHE_DURATION = timedelta(hours=5)

def get_unsplash_image(query):
    """Get a random Unsplash image for a given search term (cached)."""
    now = datetime.now()

    if query in CACHE:
        img_url, timestamp = CACHE[query]
        if now - timestamp < CACHE_DURATION:
            return img_url

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "page": 1,
        "per_page": 10,
        "client_id": UNSPLASH_ACCESS_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json().get("results", [])

    if results:
        img_url = random.choice(results)["urls"]["regular"]
    else:
        img_url = "https://img.freepik.com/free-vector/paper-style-wavy-red-background_52683-74121.jpg?semt=ais_hybrid&w=740&q=80"

    CACHE[query] = (img_url, now)
    return img_url





@views.route('/')
@login_required
def home():
    users = User.query.all()

    all_tags = []
    all_interests = []

    for user in users:
        if user.tags:
            all_tags.extend(user.tags.split(','))
        if user.interests:
            all_interests.extend(user.interests.split(','))

    tag_counts = Counter(all_tags)
    interest_counts = Counter(all_interests)

    top_tags = tag_counts.most_common(3)
    top_interests = interest_counts.most_common(3)
    tag_images = [get_unsplash_image(tag) for tag, _ in top_tags]
    interest_images = [get_unsplash_image(interest) for interest, _ in top_interests]
    
    return render_template("home.html", top_tags=top_tags, top_interests=top_interests, user=current_user,random_pic2=interest_images, random_pic=tag_images)

@views.route('/search_users')
@login_required
def search_users():
    q = request.args.get('q', '').strip()

    if not q:
        return jsonify([])

    results = User.query.filter(
        (User.first_name.ilike(f"%{q}%")) |
        (User.email.ilike(f"%{q}%")) |
        (User.phone_number.ilike(f"%{q}%")) |
        (User.city.ilike(f"%{q}%")) |
        (User.state.ilike(f"%{q}%")) |
        (User.tags.ilike(f"%{q}%")) |
        (User.interests.ilike(f"%{q}%")) |
        (User.id.cast(db.String).ilike(f"%{q}%"))
    ).all()

    # Return JSON (only what’s needed for display)
    return jsonify([
        {
            "id": user.id,
            "name": user.first_name,
            "email": user.email
        }
        for user in results
    ])