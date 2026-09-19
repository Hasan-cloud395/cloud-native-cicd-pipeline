"""
Sample microservice for the CI/CD demo pipeline.

Exposes:
  GET /        -> basic welcome payload
  GET /health  -> liveness/readiness probe target
  GET /metrics -> Prometheus-compatible metrics
"""
import os
import time

from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
START_TIME = time.time()

REQUEST_COUNT = Counter(
    "app_requests_total", "Total HTTP requests", ["endpoint", "method", "status"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Request latency in seconds", ["endpoint"]
)


@app.route("/")
def index():
    with REQUEST_LATENCY.labels(endpoint="/").time():
        payload = {
            "service": "cloud-native-cicd-demo",
            "version": APP_VERSION,
            "uptime_seconds": round(time.time() - START_TIME, 2),
        }
        REQUEST_COUNT.labels(endpoint="/", method="GET", status="200").inc()
        return jsonify(payload), 200


@app.route("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health", method="GET", status="200").inc()
    return jsonify({"status": "healthy"}), 200


@app.route("/ready")
def ready():
    REQUEST_COUNT.labels(endpoint="/ready", method="GET", status="200").inc()
    return jsonify({"status": "ready"}), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
