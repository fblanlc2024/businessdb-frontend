from flask import Blueprint, jsonify, request, current_app, redirect, url_for, make_response
import pymongo
from pymongo import MongoClient
from pymongo.errors import WriteError
import bcrypt
from flask_jwt_extended import (jwt_required, create_access_token, 
                                create_refresh_token, get_jwt_identity, 
                                get_jwt, verify_jwt_in_request, set_access_cookies, set_refresh_cookies, get_csrf_token, decode_token)
from flask_jwt_extended.exceptions import JWTExtendedException
import logging
import datetime
import jwt

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Flask
from flask import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

from app import client, db
from app.models import Account

account_routes_bp = Blueprint('account_routes', __name__)

accounts_collection = db.accounts
refresh_tokens_collection = db.refresh_tokens

logging.basicConfig(level=logging.INFO)

# Create
@account_routes_bp.route('/account', methods=['POST'])
def create_account():
    data = request.json
    username = data['username']
    password = data['password']

    existing_user = accounts_collection.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_account = Account(username, hashed_pw)
    accounts_collection.insert_one(new_account.to_dict())

    return jsonify({'message': 'Account created successfully'}), 201

# Read (old login)
@account_routes_bp.route('/account', methods=['GET'])
def basic_login():
    username = request.args.get('username')
    password = request.args.get('password')

    account = accounts_collection.find_one({'username': username})
    if not account:
        return jsonify({'message': 'Username not found'}), 404

    if bcrypt.checkpw(password.encode('utf-8'), account['password_hash']):
        return jsonify({
            'message': 'Login successful',
            'user': {
                '_id': str(account['_id']),
                'username': account['username']
            }
        }), 200
    else:
        return jsonify({'message': 'Incorrect password'}), 401

# Update
@account_routes_bp.route('/account', methods=['PUT'])
def update_account():
    data = request.json
    username = data['username']
    new_username = data.get('new_username')
    new_password = data.get('new_password')

    # Google users cannot modify their accounts
    if db.google_accounts.find_one({'account_name': username}):
        return jsonify({'message': 'Updates not allowed for users logged in with Google'}), 403

    account = accounts_collection.find_one({'username': username})
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    updates = {}
    if new_username:
        updates['username'] = new_username
    if new_password:
        hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        updates['password_hash'] = hashed_pw

    accounts_collection.update_one({'username': username}, {'$set': updates})
    return jsonify({'message': 'Account updated successfully'}), 200

# Delete
@account_routes_bp.route('/account', methods=['DELETE'])
def delete_account():
    data = request.json
    username = data['username']

    # users cannot delete their Google accounts
    if db.google_accounts.find_one({'account_name': username}):
        return jsonify({'message': 'Deletion not allowed for users logged in with Google'}), 403

    result = accounts_collection.delete_one({'username': username})
    if result.deleted_count == 0:
        return jsonify({'message': 'Account not found'}), 404
    return jsonify({'message': 'Account deleted successfully'}), 200

# Reset password only (different from other put method, which resets username and password)
@account_routes_bp.route('/reset_password', methods=['PUT'])
def reset_password():
    data = request.json
    username = data['username']
    new_password = data.get('new_password')

    # Google users cannot modify their accounts
    if db.google_accounts.find_one({'account_name': username}):
        return jsonify({'message': 'Updates not allowed for users logged in with Google'}), 403

    account = accounts_collection.find_one({'username': username})
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    if not new_password:
        return jsonify({'message': 'New password is required'}), 400

    hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    accounts_collection.update_one({'username': username}, {'$set': {'password_hash': hashed_pw}})
    return jsonify({'message': 'Password updated successfully'}), 200

@account_routes_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        current_app.logger.info(f"Received headers (Protected Route): {request.headers}")
        current_user = get_jwt_identity()
        current_app.logger.info(f"[Protected Endpoint] - Current User: {current_user}")
        
        account = accounts_collection.find_one({'username': current_user})
        if not account:
            current_app.logger.error(f"[Protected Endpoint] - Account not found for username: {current_user}")
            return jsonify({'message': 'Account not found'}), 404
        
        user_id = str(account['_id'])
        return jsonify(logged_in_as=current_user, id=user_id), 200
    except Exception as e:
        current_app.logger.error(f"JWT verification error: {e}")
        current_app.logger.error(f"Error encountered: {str(e)}")
        current_app.logger.error(f"Request headers at the time of error: {request.headers}")
        current_app.logger.error(f"Request cookies at the time of error: {request.cookies}")
        return jsonify({'message': 'Token verification failed'}), 401
    
@account_routes_bp.route('/token_login_set', methods=['POST'])
def token_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    account = accounts_collection.find_one({'username': username})
    if not account:
        return jsonify({'message': 'Username not found'}), 404

    if bcrypt.checkpw(password.encode('utf-8'), account['password_hash']):
        access_token = create_access_token(identity=username)
        
        existing_refresh_token = refresh_tokens_collection.find_one({'userId': username})
        if existing_refresh_token:
            refresh_token = existing_refresh_token['token']
        else:
            refresh_token = create_refresh_token(identity=username)
            # Store the new refresh token in the database
            refresh_tokens_collection.insert_one({
                "token": refresh_token,
                "userId": username,
                "expiresAt": datetime.utcnow() + timedelta(days=30),
                "usage_count": 1
            })

        access_csrf = get_csrf_token(access_token)
        refresh_csrf = get_csrf_token(refresh_token)

        response_data = {
            'message': 'Login successful',
            'user': {'_id': str(account['_id']), 'username': account['username']},
            'csrf_tokens': {
                'access_csrf': access_csrf,
                'refresh_csrf': refresh_csrf
            }
        }
        response = make_response(jsonify(response_data))
        
        access_expiration_time = timedelta(days=1)
        refresh_expiration_time = timedelta(days=30)
        
        response.set_cookie('access_token_cookie', value=access_token, httponly=True, max_age=access_expiration_time, samesite='None', secure=True)
        response.set_cookie('refresh_token_cookie', value=refresh_token, httponly=True, max_age=refresh_expiration_time, samesite='None', secure=True)
        
        return response

# Rolling Refresh Token System
@account_routes_bp.route('/token_refresh', methods=['POST'])
def refresh_token():
    try:
        # Extract CSRF token from headers
        received_csrf_token = request.headers.get('X-CSRF-TOKEN')
        current_app.logger.info("CSRF TOKEN THAT WAS FOUND: %s", received_csrf_token)
        
        if not received_csrf_token:
            current_app.logger.error("CSRF token missing in headers.")
            return jsonify({'message': 'CSRF token missing'}), 403

        # Ensure that the JWT exists and is valid
        verify_jwt_in_request(refresh=True)
        
        # Extract CSRF token from the current JWT
        jwt_data = get_jwt()
        stored_csrf_token = jwt_data.get('csrf')

        # Compare the received CSRF token with the stored CSRF token
        if received_csrf_token != stored_csrf_token:
            current_app.logger.error("Invalid CSRF token.")
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
        response.set_cookie('access_token_cookie', value=new_access_token, httponly=True, max_age=access_expiration_time, samesite='None', secure=True)
        response.set_cookie('refresh_token_cookie', value=received_refresh_token, httponly=True, max_age=refresh_expiration_time, samesite='None', secure=True)
        
        return response

    except JWTExtendedException as e:
        current_app.logger.error(f"JWT Error in /token_refresh: {e}")
        return jsonify({'message': str(e)}), 401