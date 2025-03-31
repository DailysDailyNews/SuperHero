import time
import logging
from flask import Flask, request, jsonify
from functools import wraps

class RequestEnforcer:
    def __init__(self, log_file="request_enforcer.log", rate_limit=10, rate_interval=1, authorized_keys=None):
        self.log_file = log_file
        self.rate_limit = rate_limit
        self.rate_interval = rate_interval
        self.request_timestamps = {}
        self.authorized_keys = authorized_keys or []
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("RequestEnforcer")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def rate_limit_decorator(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()

            if client_ip not in self.request_timestamps:
                self.request_timestamps[client_ip] = []

            self.request_timestamps[client_ip] = [
                ts for ts in self.request_timestamps[client_ip]
                if ts > current_time - self.rate_interval
            ]

            if len(self.request_timestamps[client_ip]) >= self.rate_limit:
                self.logger.warning(f"Rate limit exceeded for {client_ip}")
                return jsonify({"error": "Rate limit exceeded"}), 429 # Too Many Requests

            self.request_timestamps[client_ip].append(current_time)
            return f(*args, **kwargs)
        return decorated_function

    def authorization_decorator(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                self.logger.warning("Authorization header missing")
                return jsonify({"error": "Authorization header missing"}), 401 # Unauthorized

            auth_key = auth_header.split("Bearer ")[-1] # Assuming Bearer token

            if auth_key not in self.authorized_keys:
                self.logger.warning("Invalid authorization key")
                return jsonify({"error": "Invalid authorization key"}), 403 # Forbidden

            return f(*args, **kwargs)
        return decorated_function

# Example Usage (with Flask):

app = Flask(__name__)
enforcer = RequestEnforcer(rate_limit=5, rate_interval=1, authorized_keys=["secret_key_123", "another_key_456"])

@app.route("/protected", methods=["GET"])
@enforcer.authorization_decorator
@enforcer.rate_limit_decorator
def protected_route():
    return jsonify({"message": "Access granted"})

if __name__ == "__main__":
    app.run(debug=False) #debug = false for production.
