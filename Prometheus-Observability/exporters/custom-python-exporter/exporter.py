from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Flask, Response
import random, time, threading

app = Flask(__name__)
my_queue = Gauge('my_queue_length', 'A sample gauge showing queue length')

def update_metrics():
    while True:
        my_queue.set(random.randint(0, 100))
        time.sleep(5)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/")
def index():
    return "Custom exporter running. /metrics exposes Prometheus metrics.\n"

if __name__ == "__main__":
    t = threading.Thread(target=update_metrics, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=8000)