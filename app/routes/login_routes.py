from flask import Flask, Blueprint, redirect, request, session, url_for, jsonify, make_response, current_app
from flask_jwt_extended import create_refresh_token, get_jwt, verify_jwt_in_request, get_jwt_identity, create_access_token, get_csrf_token, set_access_cookies, set_refresh_cookies, jwt_required
import requests
from requests_oauthlib import OAuth2Session
import uuid
from app import client, db
from app.models import GoogleAccount
from datetime import datetime, timedelta
import logging

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import WebApplicationClient

# OAuth2 client setup
CLIENT_ID = '898438500076-f6on6105fpi2e913mi7kudtva2ti0qve.apps.googleusercontent.com'  # Get this from Google Developers Console
CLIENT_SECRET = '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'  # Get this from Google Developers Console
REDIRECT_URI = 'https://localhost:5000/login/callback'  # This should match the URI you set in Google Developers Console


AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'

login_routes_bp = Blueprint('login_routes_bp', __name__)
refresh_tokens_collection = db.refresh_tokens

@login_routes_bp.route("/login")
def login():
    oauth_state = OAuth2Session(CLIENT_ID).new_state()
    scope = "https://www.googleapis.com/auth/userinfo.profile"
    google = OAuth2Session(CLIENT_ID, state=oauth_state, redirect_uri=REDIRECT_URI, scope=scope)
    authorization_url, state = google.authorization_url(
        AUTH_URI,
        access_type="offline",
        prompt="select_account"
    )
    current_app.logger.info(f"Received AUTH_URI: {AUTH_URI}")
    response = make_response(redirect(authorization_url))
    # Set the state in a secure cookie
    response.set_cookie('oauth_state', oauth_state, httponly=True, samesite='Lax', secure=True)
    
    return response

@login_routes_bp.route("/login/callback")
def callback():
    oauth_state_from_cookie = request.cookies.get('oauth_state')
    google = OAuth2Session(CLIENT_ID, state=oauth_state_from_cookie, redirect_uri=REDIRECT_URI)
    token = google.fetch_token(TOKEN_URI, client_secret=CLIENT_SECRET, authorization_response=request.url)
    user_info = google.get(USER_INFO).json()

    existing_account = db.google_accounts.find_one({"google_id": user_info['id']})
    logging.debug(f"Existing account: {existing_account}")


    access_expiration_time = timedelta(seconds=5)
    refresh_expiration_time = timedelta(days=30)
    # Create new user if not exists
    if not existing_account:
        unique_account_id = str(uuid.uuid4())
        google_account = {
            "google_id": user_info['id'],
            "account_name": user_info['name'],
            "account_id": unique_account_id
        }
        db.google_accounts.insert_one(google_account)
        existing_account = google_account

    try:
            # Generate tokens
        access_token = create_access_token(identity=existing_account["account_id"])
        refresh_token = create_refresh_token(identity=existing_account["account_id"])

        # Store the refresh token in the database with an initial usage count of 0
        refresh_token_data = {
            "account_id": existing_account["account_id"],
            "token": refresh_token,
            "expiresAt": datetime.utcnow() + refresh_expiration_time,
            "usage_count": 0
        }
        refresh_tokens_collection.insert_one(refresh_token_data)
    except Exception as e:
        logging.error(f"Failed to insert refresh token into the database: {e}")
        return 500

    response = make_response()
    set_access_cookies(response, access_token, max_age=access_expiration_time.total_seconds())
    set_refresh_cookies(response, refresh_token, max_age=refresh_expiration_time.total_seconds())

    # Set user details in non-HttpOnly cookies for frontend access
    response.set_cookie('google_id', value=existing_account["google_id"], max_age=access_expiration_time.total_seconds(), samesite='None', secure=True)
    response.set_cookie('account_name', value=existing_account["account_name"], max_age=access_expiration_time.total_seconds(), samesite='None', secure=True)
    response.set_cookie('account_id', value=existing_account["account_id"], max_age=access_expiration_time.total_seconds(), samesite='None', secure=True)

    # Redirect to the frontend application with the cookies set
    response.headers["Location"] = "https://localhost:8080/posting"
    return response, 302

@login_routes_bp.route('/google_token_refresh', methods=['POST'])
def google_token_refresh():
    try:
        # Extract CSRF token from headers
        received_csrf_token = request.headers.get('X-CSRF-TOKEN')
        refresh_token_cookie = request.cookies.get('refresh_token_cookie')
        current_app.logger.info(f'Received refresh CSRF cookie: {received_csrf_token}')
        current_app.logger.info(f'Received refresh token cookie: {refresh_token_cookie}')
        
        if not received_csrf_token:
            return jsonify({'message': 'CSRF token missing'}), 403

        # Ensure that the JWT exists and is valid
        verify_jwt_in_request(refresh=True)
        
        # Extract CSRF token from the current JWT
        jwt_data = get_jwt()
        stored_csrf_token = jwt_data.get('csrf')

        # Compare the received CSRF token with the stored CSRF token
        if received_csrf_token != stored_csrf_token:
            return jsonify({'message': 'Invalid CSRF token'}), 403

        current_user = get_jwt_identity()

        received_refresh_token = request.cookies.get('refresh_token_cookie')
        token_data = refresh_tokens_collection.find_one({"token": received_refresh_token})
        
        if not token_data:
            return jsonify({'message': 'Invalid refresh token'}), 401
        
        # Check if the token has been used too many times
        if token_data.get('usage_count', 0) >= 5:
            refresh_tokens_collection.delete_one({"token": received_refresh_token})
            return jsonify({'message': 'Refresh token has been used too many times. Please re-authenticate.'}), 401

        # Try to refresh the Google token
        google = OAuth2Session(CLIENT_ID, token={
            'access_token': '',  # Not used in the refresh request
            'refresh_token': received_refresh_token,
            'token_type': 'Bearer',
            'expires_in': -30  # Force the token to be expired
        })
        try:
            token = google.refresh_token(TOKEN_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        except Exception as e:
            # If we can't refresh the Google token, invalidate our own session
            refresh_tokens_collection.delete_one({"token": received_refresh_token})
            return jsonify({'message': 'Could not refresh Google token. Please re-authenticate.'}), 401

        # Generate a new access token
        new_access_token = create_access_token(identity=current_user)

        # Update the existing refresh token's expiration and usage count
        refresh_tokens_collection.update_one(
            {'token': received_refresh_token},
            {
                '$set': {
                    'expiresAt': datetime.utcnow() + timedelta(days=30)
                },
                '$inc': {'usage_count': 1}  # Increment the usage_count here
            }
        )

        # Create a response
        response = jsonify({'message': 'Token refreshed successfully'})

        # Explicitly setting the access and refresh cookies
        access_expiration_time = timedelta(hours=1)
        refresh_expiration_time = timedelta(days=30)
        response.set_cookie('access_token_cookie', value=new_access_token, httponly=True, max_age=access_expiration_time.total_seconds(), samesite='None', secure=True)
        response.set_cookie('refresh_token_cookie', value=received_refresh_token, httponly=True, max_age=refresh_expiration_time.total_seconds(), samesite='None', secure=True)
        
        return response

    except Exception as e:
        return jsonify({'message': str(e)}), 401

@login_routes_bp.route('/google_user_data')
@jwt_required()  # Require a valid access token to access this route
def google_user_data():
    try:
        # Get the identity of the current user from the access token
        current_user_id = get_jwt_identity()
        
        # Fetch the user data from the database using the identity
        user_data = db.google_accounts.find_one({"account_id": current_user_id})
        
        if not user_data:
            return jsonify({'message': 'User not found'}), 404
        
        # Prepare the user data to send back to the client
        response_data = {
            'google_id': user_data["google_id"],
            'account_name': user_data["account_name"],
            'account_id': user_data["account_id"]
        }
        
        return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f'Error fetching user data: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500