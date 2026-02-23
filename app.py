from flask import Flask, render_template, request, jsonify
import requests
import os
from upstash_redis import Redis
from dotenv import load_dotenv

# Load local .env if it exists
load_dotenv()

app = Flask(__name__)

# --- SAFE REDIS CONNECTION ---
def init_redis():
    # Vercel looks for these exact names in its Settings > Environment Variables
    url = os.getenv("UPSTASH_REDIS_REST_URL")
    token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    
    if not url or not token:
        print("MISSING KEYS: Database tracking is disabled but site will stay online.")
        return None
        
    try:
        # Manually connecting is more stable on Vercel than .from_env()
        return Redis(url=url, token=token)
    except Exception as e:
        print(f"REDIS CONNECTION ERROR: {e}")
        return None

# Initialize the client once
redis = init_redis()

@app.route('/')
def index():
    # Only try to increment if redis connected successfully
    if redis:
        try:
            redis.incr('total_visits')
        except Exception as e:
            print(f"Counter Error: {e}")

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
    
    try:
        response = requests.get(url, params=params)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"results": [], "error": str(e)})

@app.route('/visits')
def admin_data():
    count = "0"
    if redis:
        try:
            # Fetch the current value from Upstash
            val = redis.get('total_visits')
            count = str(val) if val is not None else "0"
        except Exception as e:
            count = "Error"
    
    return jsonify({"count": count})

if __name__ == '__main__':
    # Local development settings
    app.run(debug=True, port=5000)