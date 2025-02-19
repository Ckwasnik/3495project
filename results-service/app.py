from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
mongo_client = MongoClient("mongodb://mongo:27017/")
mongo_db = mongo_client["analytics_db"]


@app.route("/results", methods=["GET"])
def get_results():
    """Fetch the latest analytics results from MongoDB."""
    latest_result = mongo_db.stats.find_one({}, sort=[("_id", -1)])

    if not latest_result:
        return jsonify({"message": "No analytics data available yet"}), 404

    return jsonify(
        {
            "max": latest_result.get("max"),
            "min": latest_result.get("min"),
            "avg": latest_result.get("avg"),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
