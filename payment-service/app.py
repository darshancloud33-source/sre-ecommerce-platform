from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest
import time

app = Flask(__name__)

payment_requests = Counter(
    "payment_requests_total",
    "Total payment requests"
)

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/payment")
def payment():
    payment_requests.inc()

    return jsonify({
        "status": "success",
        "transaction": "TXN-12345"
    })


@app.route("/metrics")
def metrics():
    return generate_latest()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)