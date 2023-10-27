from flask import Flask, Blueprint, redirect, request, session, url_for, jsonify, make_response
import requests
from requests_oauthlib import OAuth2Session
import uuid
from app import client, db
from app.models import GoogleAccount
from datetime import datetime, timedelta

# OAuth2 client setup
CLIENT_ID = '898438500076-f8ptrarn9h2q47t4i30pdcv5r9qsgbpc.apps.googleusercontent.com'  # Get this from Google Developers Console
CLIENT_SECRET = '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'  # Get this from Google Developers Console
REDIRECT_URI = 'http://localhost:5000/login/callback'  # This should match the URI you set in Google Developers Console

AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'

login_routes_bp = Blueprint('login_routes_bp', __name__)

@login_routes_bp.route("/login")
def login():
    session['oauth_state'] = OAuth2Session(CLIENT_ID).new_state()
    scope = "https://www.googleapis.com/auth/userinfo.profile"
    google = OAuth2Session(CLIENT_ID, state=session['oauth_state'], redirect_uri=REDIRECT_URI, scope=scope)
    
    authorization_url, state = google.authorization_url(
        AUTH_URI,
        access_type="offline",
        prompt="select_account"
    )
    
    return redirect(authorization_url)

from flask_jwt_extended import create_access_token

from flask import Flask, session, request, redirect, make_response
from requests_oauthlib import OAuth2Session
from pymongo import MongoClient
from flask_jwt_extended import create_access_token
import os
import uuid

# Your other imports and configurations...

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('YOUR_REDIRECT_URI')
TOKEN_URI = "https://oauth2.googleapis.com/token"
USER_INFO = "https://www.googleapis.com/oauth2/v3/userinfo"

@login_routes_bp.route("/login/callback")
def callback():
    google = OAuth2Session(CLIENT_ID, state=session['oauth_state'], redirect_uri=REDIRECT_URI)
    token = google.fetch_token(TOKEN_URI, client_secret=CLIENT_SECRET, authorization_response=request.url)
    user_info = google.get(USER_INFO).json()

    existing_account = db.google_accounts.find_one({"google_id": user_info['id']})
    
    # Step 4: Create new user if not exists
    if not existing_account:
        unique_account_id = str(uuid.uuid4())
        google_account = {
            "google_id": user_info['id'],
            "account_name": user_info['name'],
            "account_id": unique_account_id
        }
        db.google_accounts.insert_one(google_account)
        existing_account = google_account

    jwt_token = create_access_token(identity=existing_account["account_id"])

    response = make_response(redirect('https://localhost:8080/posting'))
    expiration = datetime.now() + timedelta(days=7)

    response.set_cookie('username', existing_account["account_name"], expires=expiration, samesite='None', secure=True)
    response.set_cookie('id', existing_account["account_id"], expires=expiration, samesite='None', secure=True)
    response.set_cookie('jwt_token', jwt_token, expires=expiration, samesite='None', secure=True)

    return response

@login_routes_bp.route('/get_user_from_session', methods=['GET'])
def get_user_from_session():
    user = session.get('user', {})
    print("Returning from session:", user)
    return jsonify(user)

@login_routes_bp.route('/google_token', methods=['GET'])
def google_token():
    # Check if a user session exists
    if 'user' in session:
        # Create JWT token for authenticated Google user
        jwt_token = create_access_token(identity=session['user']['id'])
        return jsonify(access_token=jwt_token), 200
    else:
        return jsonify(msg="User not authenticated"), 401