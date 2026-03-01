"""
Dynamic Recommendation Engine - Flask app with LD feature flag + which algo to use.
"""
import os
import random
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# LD: init SDK from env. if missing or error, we fall back to simple algo
LD_CLIENT = None
try:
    import ldclient
    from ldclient.config import Config
    from ldclient import Context
except ImportError:
    ldclient = None
    Context = None
    Config = None

if ldclient and os.getenv("LD_SDK_KEY"):
    try:
        # LD Python SDK: set_config + get() init the client
        ldclient.set_config(Config(os.getenv("LD_SDK_KEY")))
        LD_CLIENT = ldclient.get()
    except Exception:
        LD_CLIENT = None
else:
    LD_CLIENT = None

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


def get_complex_popularity_recs():
    """Complex A: weighted toward high popularity (weighted sampling w/o replacement)."""
    remaining = list(CATALOG)
    recs = []
    for _ in range(5):
        if not remaining:
            break
        total = sum(p["popularity"] for p in remaining)
        r = random.uniform(0, total)
        for p in remaining:
            r -= p["popularity"]
            if r <= 0:
                recs.append(p)
                remaining.remove(p)
                break
    return recs


def get_complex_diversity_recs():
    """Complex B: try to include different categories first (round-robin)."""
    from collections import defaultdict
    by_cat = defaultdict(list)
    for p in CATALOG:
        by_cat[p["category"]].append(p)
    for c in by_cat:
        by_cat[c] = sorted(by_cat[c], key=lambda p: p["popularity"], reverse=True)
    categories = sorted(by_cat.keys())
    recs = []
    round_index = 0
    while len(recs) < 5:
        for c in categories:
            if len(recs) >= 5:
                break
            if round_index < len(by_cat[c]):
                recs.append(by_cat[c][round_index])
        round_index += 1
    return recs


@app.route("/")
def index():
    """Form: user_key and user_type (standard/power)."""
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    """Show recs, use simple or complex based on LD flag (use-complex-recs)."""
    user_key = request.form.get("user_key", "")
    user_type = request.form.get("user_type", "standard")

    # if LD not initialized or variation errors, default to simple algo (safety fallback)
    use_complex = False
    if LD_CLIENT:
        try:
            # LD: context = user identity + attributes for targeting (ex: user_type)
            context = Context.builder(user_key or "anonymous").set("user_type", user_type).build()
            # LD: eval boolean flag use-complex-recs. default: False
            use_complex = LD_CLIENT.variation("use-complex-recs", context, False)
        except Exception:
            use_complex = False

    variation = None  # experiment variation (only set when complex)
    if use_complex:
        # LD: experiment flag chooses which complex algo (popularity vs diversity)
        EXPERIMENT_FLAG_KEY = "recomm_algo_experiment" 
        try:
            variation_raw = LD_CLIENT.variation(EXPERIMENT_FLAG_KEY, context, "popularity")
            variation = (variation_raw if variation_raw is not None else "popularity")
            variation = (str(variation) if not isinstance(variation, str) else variation).strip().lower()
        except Exception:
            variation = "popularity"
        # safety net for case where LD returns "Diversity" or "div"
        if variation in ("diversity", "div"):
            recs = get_complex_diversity_recs()
            algorithm = "complex (diversity)"
        else:
            recs = get_complex_popularity_recs()
            algorithm = "complex (popularity)"
    else:
        recs = get_simple_recommendations()
        algorithm = "simple"

    return render_template(
        "results.html",
        user_key=user_key,
        user_type=user_type,
        recs=recs,
        algorithm=algorithm,
        variation=variation,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
