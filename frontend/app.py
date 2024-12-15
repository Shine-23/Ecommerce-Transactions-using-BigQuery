from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Backend services
BACKENDS = [
    "http://127.0.0.1:8000",  # Primary backend
    "http://127.0.0.1:8001"   # Backup backend
]
def fetch_data_with_failover(endpoint):
    for service in BACKENDS:
        try:
            print(f"Attempting to connect to {service}{endpoint}...")  # Debugging info
            response = requests.get(f"{service}{endpoint}", timeout=5)  # Add timeout
            if response.status_code == 200:
                print(f"Response received from {service}")
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {service}: {e}")
            continue  # Try the next backend
    print("All services failed.")
    return {"error": "All services are unavailable. Please try again later."}

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customers')
def customers():
    data = fetch_data_with_failover("/customers/")
    return render_template('customers.html', data=data)

@app.route('/products')
def products():
    data = fetch_data_with_failover("/products/")
    return render_template('products.html', data=data)

@app.route('/transactions')
def transactions():
    data = fetch_data_with_failover("/transactions/")
    return render_template('transactions.html', data=data)

@app.route('/clickstream')
def clickstream():
    data = fetch_data_with_failover("/clickStream/")
    return render_template('clickstream.html', data=data)

@app.route('/simulateFailure')
def simulate_failure():
    print("Simulating failure for primary backend...")
    try:
        response = requests.get(f"{BACKENDS[0]}/simulateFailure/")  # Stop primary backend
        if response.status_code == 200:
            print("Primary backend stopped. Testing backup...")
            return jsonify({"message": "Primary backend stopped. Backup is being used."})
        else:
            return jsonify({"error": "Failed to simulate primary failure."})
    except requests.exceptions.RequestException as e:
        print(f"Primary backend is down. Testing backup: {e}")
        # Test the backup backend
        backup_response = fetch_data_with_failover("/metrics")  # Use metrics to check the backup
        if "error" not in backup_response:
            return jsonify({"message": "Backup service is active and functional."})
        return jsonify({"error": "Both services are unavailable. Failover failed."})


@app.route('/metrics')
def metrics():
    data = fetch_data_with_failover("/metrics/")
    return jsonify(data)

@app.route('/visualization/service-status')
def service_status():
    return render_template('service_status.html')

@app.route('/visualization/request-distribution')
def request_distribution():
    return render_template('request_distribution.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
