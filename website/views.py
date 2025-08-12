from collections import Counter
from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from . import db 
from website.models import User
import requests
import random
import random 

# Blueprint for views
views = Blueprint('views', __name__)

# Unsplash API configuration
UNSPLASH_ACCESS_KEY = "KjWYQ8pXPRSEnJlxAqpuYhyQP0_8QPucP0YojCYwoyk"
# Used to avoid hitting the API too frequently
CACHE = {}
# Cache duration for Unsplash images
CACHE_DURATION = timedelta(hours=5)

"""
Gets an image URL from Unsplash based on a search query.
If the query is cached and the cache is still valid, it returns the cached image URL.
"""
def get_unsplash_image(query):
    
    # timestamp for cache validation
    now = datetime.now()

    # Check if the query is in the cache and if it's still valid
    if query in CACHE:
        img_url, timestamp = CACHE[query]
        if now - timestamp < CACHE_DURATION:
            return img_url

    # If not cached or cache expired, fetch a new image
    # Unsplash API endpoint for searching photos
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "page": 1,
        "per_page": 10,
        "client_id": UNSPLASH_ACCESS_KEY
    }
    
    # Make the request to Unsplash API
    response = requests.get(url, params=params)
    response.raise_for_status()
    # Parse the JSON response
    results = response.json().get("results", [])
    
    # If results are found, select a random image URL
    if results:
        img_url = random.choice(results)["urls"]["regular"]
    else:
        img_url = "https://img.freepik.com/free-vector/paper-style-wavy-red-background_52683-74121.jpg?semt=ais_hybrid&w=740&q=80"

    # Update the cache with the new image URL and current timestamp
    # This ensures that the next time the same query is made, it will return the cached
    CACHE[query] = (img_url, now)
    return img_url

# Route for the home page
@views.route('/')
@login_required
def home():
    # Get all users from the database
    users = User.query.all()
    
    # Collect all tags and interests from users
    # Using a set to avoid duplicates
    all_tags = []
    all_interests = []

    # Iterate through each user to gather tags and interests
    for user in users:
        if user.tags:
            all_tags.extend(user.tags.split(','))
        if user.interests:
            all_interests.extend(user.interests.split(','))

    # Count occurrences of each tag and interest
    tag_counts = Counter(all_tags)
    interest_counts = Counter(all_interests)

    # Get the top 3 tags and interests
    top_tags = tag_counts.most_common(3)
    top_interests = interest_counts.most_common(3)
    
    # Fetch images for the top tags and interests using Unsplash API
    tag_images = [get_unsplash_image(tag) for tag, _ in top_tags]
    interest_images = [get_unsplash_image(interest) for interest, _ in top_interests]
    
    # Render the home page with the top tags, interests, and images
    return render_template("home.html", top_tags=top_tags, top_interests=top_interests, user=current_user,random_pic2=interest_images, random_pic=tag_images)


# Route for searching users
@views.route('/search_users')
@login_required
def search_users():
    
    # Get the search query from the request arguments
    # Strip whitespace from the query
    q = request.args.get('q', '').strip()

    # If the query is empty, return an empty JSON response
    if not q:
        return jsonify([])

    # Perform a case-insensitive search across multiple fields in the User model
    # Using ilike for case-insensitive matching
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