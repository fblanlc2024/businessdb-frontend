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
counters_collection = db.counters
data_routes_bp = Blueprint('data_routes', __name__)

@data_routes_bp.route('/api/businesses', methods=['GET'])
def get_businesses():
    businesses = businesses_collection.find({}, {'_id': 0, 'business_id': 1, 'business_name': 1})
    business_list = list(businesses)

    return jsonify(business_list)

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


@data_routes_bp.route('/add_business', methods=['POST'])
def add_business():
    data = request.json
    required_fields = ['business_name', 'address', 'organization_type', 'resources_available', 'has_available_resources', 'contact_info']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        new_business = Business(
            business_name=data['business_name'],
            address=data['address'],
            organization_type=data['organization_type'],
            resources_available=data['resources_available'],
            has_available_resources=data['has_available_resources'],
            contact_info=data['contact_info']
        )

        new_business.business_id = get_next_business_id()

        # Insert the new business and retrieve the inserted ID if possible
        insert_result = businesses_collection.insert_one(new_business.to_dict())
        inserted_id = insert_result.inserted_id

        # Retrieve the inserted business data
        inserted_business = businesses_collection.find_one({'_id': inserted_id})

        if inserted_business:
            # Convert the MongoDB document to a JSON-friendly format
            inserted_business['_id'] = str(inserted_business['_id'])  # Convert ObjectId to string

            return jsonify(inserted_business), 201
        else:
            return jsonify({'error': 'Failed to retrieve the added business'}), 500

    except KeyError as e:
        return jsonify({'error': f'Missing address component: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_next_business_id():
    result = counters_collection.find_one_and_update(
        {'_id': 'business_id'},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result['seq']
