from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Backend services
BACKENDS = [
    "http://127.0.0.1:8000",  # Primary backend
    "http://127.0.0.1:8001"   # Backup backend
]

# Function to fetch data with failover
def fetch_data_with_failover(endpoint):
    for service in BACKENDS:
        try:
            response = requests.get(f"{service}{endpoint}")
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {service}: {e}")
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
    response = requests.get(f"{BACKENDS[0]}/simulateFailure/")
    return jsonify({"message": "Backend failure simulated"}) if response.status_code == 200 else jsonify({"error": "Failed to simulate failure"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
