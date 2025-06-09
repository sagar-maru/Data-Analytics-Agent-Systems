import os
import time
import hmac
import hashlib
import secrets
from dotenv import load_dotenv

load_dotenv()

# === Environment Variables ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_ID = os.getenv("SECRET_ID")
SECRET_KEY = os.getenv("SECRET_KEY")

print("OPENAI_API_KEY Setup is Completed..!!!")

if not SECRET_ID or not SECRET_KEY:
    raise RuntimeError("SECRET_ID and SECRET_KEY must be set in environment variables")

# === Token Cache ===
TOKEN_STORE = {
    "token": None,
    "expires_at": 0  # Unix timestamp
}

# === Generate Bearer Token ===
def generate_bearer_token():
    current_time = time.time()

    # Refresh token if expired or not generated
    if TOKEN_STORE["token"] is None or current_time > TOKEN_STORE["expires_at"]:
        # Generate random salt
        salt = secrets.token_hex(8)  # 16 hex chars

        # Create a message using secret_id, current timestamp, and salt
        msg = f"{SECRET_ID}:{int(current_time)}:{salt}".encode("utf-8")

        # Use HMAC with SHA256 and secret_key to create token
        token = hmac.new(SECRET_KEY.encode("utf-8"), msg, hashlib.sha256).hexdigest()

        # Cache token and its expiry
        TOKEN_STORE["token"] = token
        TOKEN_STORE["expires_at"] = current_time + 360 # valid for 1 hour
        print(TOKEN_STORE["expires_at"])

    return TOKEN_STORE["token"]