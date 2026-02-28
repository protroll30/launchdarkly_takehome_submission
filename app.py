"""
Dynamic Recommendation Engine - minimal Flask app (Step 1: no LaunchDarkly).
"""
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# Hardcoded product catalog: id, name, category, popularity (higher = more popular)
CATALOG = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics", "popularity": 95},
    {"id": 2, "name": "Running Shoes", "category": "Sports", "popularity": 88},
    {"id": 3, "name": "Coffee Maker", "category": "Home", "popularity": 82},
    {"id": 4, "name": "Desk Lamp", "category": "Home", "popularity": 70},
    {"id": 5, "name": "Yoga Mat", "category": "Sports", "popularity": 65},
    {"id": 6, "name": "USB-C Charger", "category": "Electronics", "popularity": 60},
    {"id": 7, "name": "Water Bottle", "category": "Sports", "popularity": 55},
    {"id": 8, "name": "Notebook Set", "category": "Office", "popularity": 50},
    {"id": 9, "name": "Bluetooth Speaker", "category": "Electronics", "popularity": 45},
    {"id": 10, "name": "Desk Organizer", "category": "Office", "popularity": 40},
]


def get_simple_recommendations():
    """Top 5 by popularity (default algorithm)."""
    sorted_catalog = sorted(CATALOG, key=lambda p: p["popularity"], reverse=True)
    return sorted_catalog[:5]


@app.route("/")
def index():
    """Form: user_key and user_type (standard/power)."""
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Recommendations</title></head>
    <body>
    <h1>Get Recommendations</h1>
    <form method="POST" action="/recommend">
        <label>User Key: <input name="user_key" required /></label><br><br>
        <label>User Type:
            <select name="user_type">
                <option value="standard">standard</option>
                <option value="power">power</option>
            </select>
        </label><br><br>
        <button type="submit">Get Recommendations</button>
    </form>
    </body>
    </html>
    """
    return html


@app.route("/recommend", methods=["POST"])
def recommend():
    """Show top 5 by popularity and which algorithm was used."""
    user_key = request.form.get("user_key", "")
    user_type = request.form.get("user_type", "standard")

    recs = get_simple_recommendations()
    algorithm = "simple"

    lines = [
        "<h1>Recommendations</h1>",
        f"<p><b>User:</b> {user_key} | <b>Type:</b> {user_type}</p>",
        f"<p><b>Algorithm:</b> {algorithm}</p>",
        "<ul>",
    ]
    for p in recs:
        lines.append(f"<li>{p['name']} ({p['category']}) — popularity {p['popularity']}</li>")
    lines.append("</ul>")
    lines.append('<p><a href="/">Back</a></p>')

    return "\n".join(lines)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
