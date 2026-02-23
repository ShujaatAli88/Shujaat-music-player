from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Mock database for local testing (Vercel KV would replace this in production)
# In production, you'd use: from vercel_kv import kv
VISITS_FILE = "visits.txt"

def get_and_increment_count():
    try:
        if not os.path.exists(VISITS_FILE):
            with open(VISITS_FILE, "w") as f: f.write("0")
        
        with open(VISITS_FILE, "r+") as f:
            count = int(f.read()) + 1
            f.seek(0)
            f.write(str(count))
            f.truncate()
            return count
    except:
        return "Error"

@app.route('/')
def index():
    # Secretly increment the count every time the page is loaded
    current_count = get_and_increment_count()
    
    seo_data = {
        "title": "MusicFlow | Premium Singer Search & Discovery",
        "description": "The most advanced engine to find and play your favorite songs instantly.",
        "keywords": "MusicFlow, song search, MP3 download, Shujaat music"
    }
    return render_template('index.html', seo=seo_data)

@app.route('/search')
def search():
    artist_name = request.args.get('artist')
    if not artist_name:
        return jsonify({"results": []})

    url = "https://itunes.apple.com/search"
    params = {
        "term": artist_name,
        "entity": "song",
        "limit": 100, # Increased limit for better UX
        "country": "IN"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return jsonify({"error": "External API Error"}), 500

@app.route('/admin_data')
def admin_data():
    # Only called by your secret trigger
    with open(VISITS_FILE, "r") as f:
        return jsonify({"count": f.read()})

if __name__ == '__main__':
    app.run(debug=True,port=5000)