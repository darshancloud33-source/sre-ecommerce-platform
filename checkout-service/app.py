from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest
import requests

app = Flask(__name__)

checkout_requests = Counter(
    "checkout_requests_total",
    "Total checkout requests"
)

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/checkout", methods=["POST"])
def checkout():
    checkout_requests.inc()

    payment_response = requests.get(
        "http://payment-service:5001/payment"
    )

    return jsonify({
        "message": "Checkout completed",
        "payment": payment_response.json()
    })


@app.route("/metrics")
def metrics():
    return generate_latest()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)