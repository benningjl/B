from flask import Flask, jsonify, request
from auth_manager import AuthManager
from session_manager import SessionManager
from data_manager import DataManager

app = Flask(__name__)

# Example route for user registration
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        auth_manager = AuthManager()
        auth_manager.register_user(data['username'], data['email'], data['password'])
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Example route for user login
@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        auth_manager = AuthManager()
        session_manager = SessionManager()
        if auth_manager.login_user(data['username'], data['password']):
            token = session_manager.create_session(data['username'])
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Example route to fetch data
@app.route('/data', methods=['GET'])
def fetch_data():
    try:
        data_manager = DataManager()
        data = data_manager.fetch_data()
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
