"""
Dynamic Recommendation Engine - Flask app with templates.
"""
from flask import Flask, request, render_template

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
    """Top 5 by popularity (default algo)."""
    sorted_catalog = sorted(CATALOG, key=lambda p: p["popularity"], reverse=True)
    return sorted_catalog[:5]


@app.route("/")
def index():
    """Form: user_key and user_type (standard/power)."""
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    """Show top 5 by popularity and which algo was used."""
    user_key = request.form.get("user_key", "")
    user_type = request.form.get("user_type", "standard")

    recs = get_simple_recommendations()
    algorithm = "simple"

    return render_template(
        "results.html",
        user_key=user_key,
        user_type=user_type,
        recs=recs,
        algorithm=algorithm,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
