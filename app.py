from flask import Flask, render_template, request, jsonify
import requests
import os
from upstash_redis import Redis
from dotenv import load_dotenv

# 1. Load the keys from your .env file
load_dotenv()

app = Flask(__name__)

# 2. Connect to Redis (it will now find the keys in your .env)
redis = Redis.from_env()

@app.route('/')
def index():
    try:
        # Increment global visits
        redis.incr('total_visits')
    except Exception as e:
        print(f"Redis Error: {e}")

    seo = {
        "title": "MusicFlow | Search",
        "description": "Premium Search Engine",
        "keywords": "music, shujaat"
    }
    return render_template('index.html', seo=seo)

@app.route('/search')
def search():
    artist_name = request.args.get('artist')
    if not artist_name:
        return jsonify({"results": []})

    url = "https://itunes.apple.com/search"
    params = {"term": artist_name, "entity": "song", "limit": 50}
    response = requests.get(url, params=params)
    return jsonify(response.json())

@app.route('/visits')
def admin_data():
    # Fetch count from Upstash
    count = redis.get('total_visits') or 0
    return jsonify({"count": str(count)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)