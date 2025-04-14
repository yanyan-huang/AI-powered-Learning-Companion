"""
This module initializes the Firebase Firestore database connection.
It uses the Firebase Admin SDK to authenticate and access the Firestore database.
It requires a service account key in JSON format for authentication.
The service account key should be stored in a file named 'firebase_creds.json'.
The database connection is established using the credentials from the service account key.
The Firestore client is created and can be used to perform database operations.
"""

import os
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app

load_dotenv()  # Loads vars from .env

print("📦 Initializing Firebase connection...", flush=True)

try:
    cred_path = os.getenv("FIREBASE_CRED_PATH", "firebase_creds.json")
    cred = credentials.Certificate(cred_path)
    initialize_app(cred)

    db = firestore.client()
except Exception as e:
    print("❌ Firebase init failed:", e, flush=True)