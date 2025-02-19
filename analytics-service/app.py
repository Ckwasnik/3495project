from flask import Flask, jsonify
import mysql.connector
from pymongo import MongoClient

app = Flask(__name__)

db_config = {
    "host": "mysql",
    "user": "root",
    "password": "password",
    "database": "data_db",
}
mongo_client = MongoClient("mongodb://mongo:27017/")
mongo_db = mongo_client["analytics_db"]


@app.route("/analyze", methods=["GET"])
def analyze():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM records")
    data = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    max_val, min_val, avg_val = max(data), min(data), sum(data) / len(data)
    mongo_db.stats.insert_one({"max": max_val, "min": min_val, "avg": avg_val})

    return jsonify({"max": max_val, "min": min_val, "avg": avg_val})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
