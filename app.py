# app.py
from flask import Flask, render_template, jsonify
import requests
import datetime

app = Flask(__name__)

# Function to fetch Bitcoin data from the CoinGecko API
def get_bitcoin_data():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '30',  # You can change this to any number of days you want to display
        'interval': 'daily'  # Daily data points
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    prices = data['prices']
    timestamps = [datetime.datetime.fromtimestamp(item[0] / 1000) for item in prices]
    values = [item[1] for item in prices]
    
    return timestamps, values

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    timestamps, values = get_bitcoin_data()
    data = {
        'labels': [timestamp.strftime('%Y-%m-%d') for timestamp in timestamps],
        'prices': values
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Changed port to 8080
