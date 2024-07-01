from flask import Flask, jsonify
from threading import Lock
import requests

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
QUALIFIED_IDS = {'p', 'f', 'e', 'r'}
TEST_SERVER_URL = 'http://example.com/testserver'  # Replace with the actual test server URL
REQUEST_TIMEOUT = 0.5

# Global state
numbers = []
lock = Lock()

# Function to fetch numbers from the test server
def fetch_numbers(number_id):
    try:
        response = requests.get(f"{TEST_SERVER_URL}/{number_id}", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get('numbers', [])
    except requests.RequestException:
        return []

# Function to update the window with new numbers
def update_window(new_numbers):
    global numbers
    unique_numbers = list(set(numbers + new_numbers))
    if len(unique_numbers) > WINDOW_SIZE:
        unique_numbers = unique_numbers[-WINDOW_SIZE:]
    return unique_numbers

# Route to handle requests
@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in QUALIFIED_IDS:
        return jsonify({"error": "Invalid number ID"}), 400

    with lock:
        prev_state = numbers.copy()
        new_numbers = fetch_numbers(number_id)
        if new_numbers:
            numbers[:] = update_window(new_numbers)

        curr_state = numbers
        avg = sum(curr_state) / len(curr_state) if curr_state else 0.0

    response = {
        "numbers": new_numbers,
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "avg": avg
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=9876)
