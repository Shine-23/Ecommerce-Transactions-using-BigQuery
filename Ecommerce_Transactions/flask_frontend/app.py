from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    response = requests.get("http://127.0.0.1:8000/api/transactions/")
    transactions = response.json().get('transactions', [])
    return render_template('index.html', transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)
