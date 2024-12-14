from flask import Flask, render_template, jsonify
from google.cloud import bigquery

app = Flask(__name__)

# BigQuery Client Setup
client = bigquery.Client()

# Fetch some sample data from BigQuery (e.g., Customer count)
def get_customer_count():
    query = "SELECT COUNT(customer_id) as customer_count FROM `your_dataset.Customer`"
    query_job = client.query(query)
    result = query_job.result()
    for row in result:
        return row.customer_count

# Routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/system_metrics')
def system_metrics():
    # Mock Data for Dashboard Metrics
    data = {
        "scalability": {"active_nodes": 5, "total_requests": 1200},
        "fault_tolerance": {"failed_nodes": 1, "recovered_nodes": 3},
        "security": {"total_requests": 1500, "secure_requests": 1400},
        "load_balancing": {"server_1": 300, "server_2": 500, "server_3": 200},
    }
    return jsonify(data)

@app.route('/api/customer_count')
def customer_count():
    count = get_customer_count()
    return jsonify({"customer_count": count})

if __name__ == "__main__":
    app.run(debug=True)
