from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Mock data for system metrics (replace with real queries if available)
def get_mock_data():
    return {
        "scalability": {"active_nodes": 5, "total_requests": 1200},
        "fault_tolerance": {"failed_nodes": 1, "recovered_nodes": 3},
        "security": {"secure_requests": 1400, "total_requests": 1500},
        "load_balancing": {"server_1": 300, "server_2": 500, "server_3": 200},
    }

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scalability')
def scalability():
    return render_template('scalability.html')

@app.route('/fault-tolerance')
def fault_tolerance():
    return render_template('fault_tolerance.html')

@app.route('/security')
def security():
    return render_template('security.html')

@app.route('/load-balancing')
def load_balancing():
    return render_template('load_balancing.html')

@app.route('/api/system_metrics')
def system_metrics():
    data = get_mock_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
