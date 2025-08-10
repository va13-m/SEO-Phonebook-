from typing import Counter
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import requests
import random
import os

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

    # tag_images = [
    #     "https://img.freepik.com/free-vector/paper-style-wavy-red-background_52683-74121.jpg?semt=ais_hybrid&w=740&q=80",
    #     "https://img.freepik.com/free-vector/abstract-red-wave-background_343694-4197.jpg",
    #     "https://img.freepik.com/premium-vector/red-paper-cut-abstract-background_142989-137.jpg?semt=ais_hybrid&w=740&q=80",
    #     "https://img.freepik.com/free-vector/abstract-wavy-red-background_53876-96409.jpg?semt=ais_hybrid&w=740&q=80",
    #     "https://img.freepik.com/free-vector/paper-cut-abstract-background_125964-562.jpg?semt=ais_hybrid&w=740&q=80",
    #     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOwBsPoV2wK9P-V119KuFDQNJIzeiPLbXC7RXlbMab51tneJW6zrEJ84KLYDYEY25LVDc&usqp=CAU",
    #     "https://img.freepik.com/free-vector/red-business-abstract-banner-background-with-fluid-gradient-wavy-shapes-vector-design-post_1340-22823.jpg",
    #     "https://png.pngtree.com/background/20211217/original/pngtree-red-burgundy-background-gradient-slash-picture-image_1589772.jpg",
    #     "https://img.freepik.com/premium-photo/minimalist-red-wallpaper-with-subtle-splash-pattern-8k-high-quality_899449-47056.jpg"
    # ]
    

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
