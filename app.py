from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    artist_name = request.args.get('artist')
    if not artist_name:
        return jsonify({"results": []})

    url = "https://itunes.apple.com/search"
    params = {
        "term": artist_name,
        "entity": "song",
        "limit": 50 # Start with 50 for performance
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)