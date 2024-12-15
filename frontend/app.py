from flask import Flask, render_template, jsonify, redirect, url_for, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests

app = Flask(__name__)
app.secret_key = "d00f67eb7d79c534176e314373b9ffec"

# Backend services for Fault Tolerance
BACKENDS = [
    "http://127.0.0.1:8000",  # Primary backend
    "http://127.0.0.1:8001"   # Backup backend
]

# Fault-Tolerance Function
def fetch_data_with_failover(endpoint):
    for service in BACKENDS:
        try:
            print(f"Attempting to connect to {service}{endpoint}...")
            response = requests.get(f"{service}{endpoint}", timeout=5)  # Add timeout
            if response.status_code == 200:
                # Notify the backend to log request type
                if "8000" in service:
                    requests.get(f"{service}/log-request?type=primary")
                elif "8001" in service:
                    requests.get(f"{service}/log-request?type=backup")
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {service}: {e}")
            continue
    print("All services failed.")
    return {"error": "All services are unavailable. Please try again later."}

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customers')
def customers():
    access_token = session.get('access_token')
    if not access_token:
        return render_template('customers.html', error="You are not logged in. Please log in to access customer data.")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BACKENDS[0]}/customers/", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return render_template('customers.html', data=data, role="admin")
    elif response.status_code == 403:
        return render_template('customers.html', error="Access denied. Admins only.")
    else:
        return render_template('customers.html', error="Session expired or unauthorized. Please log in again.")


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

# Simulate Fault Tolerance
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

# Metrics Visualization
@app.route('/metrics')
def metrics():
    data = fetch_data_with_failover("/metrics/")
    return jsonify(data)

@app.route('/metrics-dashboard')
def metrics_dashboard():
    return render_template('metrics.html')

# Login route to fetch JWT
@app.route('/login', methods=['GET', 'POST'])
def login():
    credentials = {"username": "admin", "password": "admin"}  # Replace with actual admin credentials
    response = requests.post(f"{BACKENDS[0]}/api/token/", data=credentials)
    if response.status_code == 200:
        tokens = response.json()
        session['access_token'] = tokens['access']
        session['refresh_token'] = tokens['refresh']
        return redirect(url_for('home'))
    return "Login failed. Invalid credentials."

@app.route('/secure-data')
def secure_data():
    access_token = session.get('access_token')
    if not access_token:
        return render_template('secure_data.html', error="You are not logged in. Please log in to access secure data.")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BACKENDS[0]}/secure-data/", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return render_template('secure_data.html', data=data['data'], role="admin")
    elif response.status_code == 403:
        return render_template('secure_data.html', error="Access denied. Admins only.")
    else:
        return render_template('secure_data.html', error="Session expired or unauthorized. Please log in again.")


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
