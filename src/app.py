from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/", methods=["GET"])
def root():
    return jsonify(status="ok", service="user")


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
