import uuid
from flask import Flask, jsonify, request
import redis

import time

app = Flask(__name__)

# Redis setup (default localhost; adjust for production)
r = redis.Redis(host='localhost', port=6379)

# Rate limit config
RATE_LIMIT = 10
TIME_WINDOW = 60
REDIS_KEY = "global:request_timestamps"

@app.before_request
def global_rate_limiter():
    now = int(time.time() * 1000)  # milliseconds for better resolution
    window_start = now - (TIME_WINDOW * 1000)

    r.zremrangebyscore(REDIS_KEY, 0, window_start)
    current_count = r.zcard(REDIS_KEY)

    if current_count >= RATE_LIMIT:
        return jsonify({"error": "Rate limit exceeded"}), 429

    r.zadd(REDIS_KEY, {now: now})

@app.route("/api/data")
def get_data():
    return jsonify({"message": "OK"}), 200

if __name__ == "__main__":
    app.run(debug=True)
