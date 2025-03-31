import hashlib
import secrets
import time
import logging
from functools import wraps
from flask import request, jsonify, Flask # Assuming Flask for web API context

class AccessControl:
    def __init__(self, secret_key, log_file="access_control.log", token_expiration=3600): # 1 hour expiration
        self.secret_key = secret_key
        self.log_file = log_file
        self.token_expiration = token_expiration
        self.user_tokens = {} # In-memory token storage (replace with database for production)
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("AccessControl")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def generate_token(self, username):
        """Generates a secure access token for a user."""
        timestamp = str(time.time())
        data = f"{username}:{timestamp}:{self.secret_key}"
        token_hash = hashlib.sha256(data.encode()).hexdigest()
        token = f"{username}:{timestamp}:{token_hash}"
        self.user_tokens[username] = {"token": token, "expiry": time.time() + self.token_expiration}
        self.logger.info(f"Generated token for {username}")
        return token

    def verify_token(self, token):
        """Verifies an access token."""
        try:
            username, timestamp, token_hash = token.split(":")
            data = f"{username}:{timestamp}:{self.secret_key}"
            expected_hash = hashlib.sha256(data.encode()).hexdigest()

            if token_hash != expected_hash:
                self.logger.warning("Invalid token hash")
                return None

            if username not in self.user_tokens or self.user_tokens[username]["token"] != token:
                self.logger.warning("Token not found or does not match")
                return None

            if self.user_tokens[username]["expiry"] < time.time():
                self.logger.warning("Token expired")
                del self.user_tokens[username] #remove expired token
                return None

            return username # Token is valid

        except ValueError:
            self.logger.warning("Invalid token format")
            return None

    def authorization_decorator(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                self.logger.warning("Authorization header missing")
                return jsonify({"error": "Authorization header missing"}), 401

            try:
                token = auth_header.split("Bearer ")[1] # Assuming Bearer token
                username = self.verify_token(token)

                if not username:
                    return jsonify({"error": "Invalid or expired token"}), 403

                kwargs["username"] = username # Pass username to the decorated function
                return f(*args, **kwargs)

            except IndexError:
                self.logger.warning("Invalid Authorization header format")
                return jsonify({"error": "Invalid Authorization header"}), 401

        return decorated_function

# Example Usage (with Flask):

app = Flask(__name__)
secret_key = secrets.token_hex(32) # Generate a secure random key.
access_control = AccessControl(secret_key)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    # In a real app, verify username/password against a database...

    if username:
        token = access_control.generate_token(username)
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/protected", methods=["GET"])
@access_control.authorization_decorator
def protected_route(username): #username is passed from the decorator
    return jsonify({"message": f"Access granted to {username}"})

if __name__ == "__main__":
    app.run(debug=False) #debug = false for production.
