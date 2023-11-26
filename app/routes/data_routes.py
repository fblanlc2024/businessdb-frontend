from flask import Blueprint, jsonify, request, current_app, redirect, url_for, make_response
import pymongo
from pymongo import MongoClient
from pymongo.errors import WriteError
import bcrypt
from flask_jwt_extended import (jwt_required, create_access_token, 
                                create_refresh_token, get_jwt_identity, 
                                get_jwt, verify_jwt_in_request, get_csrf_token)
from flask_jwt_extended.exceptions import JWTExtendedException
import logging
import datetime
import jwt
from flask_limiter import RateLimitExceeded

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Flask
from flask import jsonify

from app import client, db
from app.models import Business
businesses_collection = db.businesses
data_routes_bp = Blueprint('data_routes', __name__)

@data_routes_bp.route('/api/businesses', methods=['GET'])
def get_businesses():
    businesses = businesses_collection.find({}, {'business_name': 1, '_id': 0})
    business_names = [business['business_name'] for business in businesses]
    return jsonify(business_names)

@data_routes_bp.route('/api/business_info', methods=['GET'])
def get_business_info():
    business_name = request.args.get('name')

    # Query to find the document for the given business name
    business_info = businesses_collection.find_one(
        {"business_name": business_name},
        {"business_name": 0, "_id": 0}
    )

    if business_info:
        return jsonify(business_info)
    else:
        return jsonify({"error": "Business not found"}), 404
