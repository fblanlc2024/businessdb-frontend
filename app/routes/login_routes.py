from flask import Flask, Blueprint, redirect, request, jsonify, make_response, current_app
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests
import os
from app import db
from app.models import GoogleAccount
from datetime import datetime, timedelta
import logging
from google.auth.transport import requests as google_auth_requests
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
import json

# OAuth2 client setup
CLIENT_ID = '898438500076-f6on6105fpi2e913mi7kudtva2ti0qve.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'https://localhost:5000/login/callback'


AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'

login_routes_bp = Blueprint('login_routes_bp', __name__)
refresh_tokens_collection = db.refresh_tokens

@login_routes_bp.route("/login")
def login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": AUTH_URI,
                "token_uri": TOKEN_URI,
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=["https://www.googleapis.com/auth/userinfo.profile"],
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes='true',
        prompt='select_account consent'
    )
    response = make_response(redirect(authorization_url))
    response.set_cookie('state', state, httponly=True)
    return response

@login_routes_bp.route("/login/callback")
def callback():
    state = request.cookies.get('state')
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": AUTH_URI,
                "token_uri": TOKEN_URI,
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=["https://www.googleapis.com/auth/userinfo.profile"],
        state=state,
    )

    flow.redirect_uri = REDIRECT_URI
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session = google_requests.AuthorizedSession(credentials)
    user_info = session.get(USER_INFO).json()

    existing_account = db.google_accounts.find_one({"google_id": user_info['id']})

    if not existing_account:
        google_account = {
            "google_id": user_info['id'],
            "account_name": user_info['name'],
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_expiry": credentials.expiry,
        }
        db.google_accounts.insert_one(google_account)
    else:
        db.google_accounts.update_one(
            {"google_id": user_info['id']},
            {
                "$set": {
                    "access_token": credentials.token,
                    "refresh_token": credentials.refresh_token,
                    "token_expiry": credentials.expiry
                }
            }
        )

    response = make_response(redirect("https://localhost:8080/posting"))

    # Set access token in HttpOnly cookie
    expiry_timestamp = credentials.expiry.timestamp()
    current_timestamp = datetime.utcnow().timestamp()
    seconds_until_expiry = expiry_timestamp - current_timestamp

    access_token_expiration = datetime.utcnow() + timedelta(seconds=seconds_until_expiry)
    response.set_cookie('access_token', credentials.token, expires=access_token_expiration, httponly=True, secure=True, samesite='Lax')

    # Set refresh token in HttpOnly cookie
    # Note: Refresh tokens typically don't expire, but you can set a long duration
    refresh_token_expiration = datetime.utcnow() + timedelta(days=30)  # Example: 30 days
    response.set_cookie('refresh_token', credentials.refresh_token, expires=refresh_token_expiration, httponly=True, secure=True, samesite='Lax')

    return response

@login_routes_bp.route('/google_token_refresh', methods=['POST'])
def google_token_refresh():
    try:
        # Retrieve the refresh token from the HttpOnly cookie
        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            return jsonify({'message': 'Refresh token not found'}), 401

        # Fetch the user's data from the database using the refresh token
        user_data = db.google_accounts.find_one({"refresh_token": refresh_token})
        if not user_data:
            return jsonify({'message': 'User not found'}), 401

        user_id = user_data['account_id']

        # Create credentials object
        credentials = Credentials(
            None,  # No access token, we want to refresh
            refresh_token=refresh_token,
            token_uri=TOKEN_URI,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )

        # Request a new access token
        request_client = google_auth_requests.Request()
        credentials.refresh(request_client)

        # Update the new access token in the database
        db.google_accounts.update_one(
            {"account_id": user_id},
            {"$set": {"access_token": credentials.token, "token_expiry": credentials.expiry}}
        )

        return jsonify({'message': 'Token refreshed successfully', 'access_token': credentials.token})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@login_routes_bp.route('/google_user_data')
def google_user_data():
    try:
        current_app.logger.info("Fetching Google user data...")

        # Extract the Google access token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            current_app.logger.warning("Authorization header is missing")
            return jsonify({'message': 'Authorization header is missing'}), 401

        # Extract the token part from the header
        google_access_token = auth_header.split(" ")[1]
        current_app.logger.info(f"Received Google access token: {google_access_token}")

        # Verify the token
        request_client = google_auth_requests.Request()
        try:
            current_app.logger.info("Verifying Google token...")
            # This will throw an error if the token is invalid or expired
            idinfo = id_token.verify_oauth2_token(google_access_token, request_client, CLIENT_ID)

            # ID Token is valid, get the Google user ID from it
            google_user_id = idinfo['sub']
            current_app.logger.info(f"Verified Google token. User ID: {google_user_id}")

            # Fetch the user data from the database using the Google user ID
            user_data = db.google_accounts.find_one({"google_id": google_user_id})
            if not user_data:
                current_app.logger.warning(f"User not found for Google ID: {google_user_id}")
                return jsonify({'message': 'User not found'}), 404

            # Prepare the user data to send back to the client
            response_data = {
                'google_id': user_data["google_id"],
                'account_name': user_data["account_name"],
                'account_id': user_data["account_id"]
            }

            current_app.logger.info("Successfully fetched Google user data.")
            return jsonify(response_data), 200

        except ValueError as e:
            # Invalid token
            current_app.logger.error(f"Invalid Google token. Error: {e}")
            return jsonify({'message': 'Invalid Google token'}), 403

    except Exception as e:
        current_app.logger.error(f"Error in google_user_data endpoint: {e}")
        return jsonify({'message': 'Internal server error'}), 500
