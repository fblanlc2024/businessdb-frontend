import os
from flask import Flask, jsonify, session, request
from flask_session import Session
from flask_cors import CORS
from pymongo import MongoClient
import dotenv
from flask_jwt_extended import JWTManager
import logging
from datetime import timedelta
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address
from datetime import datetime
from redis import Redis

dotenv_path = "D:\\Projects\\Python\\math-quiz\\app\\important_variables.env"
dotenv.load_dotenv(dotenv_path)
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800)))

app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

Session(app)

if not app.secret_key:
    raise ValueError("No secret key set for Flask application")
if not app.config['JWT_SECRET_KEY']:
    raise ValueError("No JWT secret key set")
if not app.config['JWT_ACCESS_TOKEN_EXPIRES']:
    raise ValueError("No JWT access token expiration time set")

CORS(app, resources={r"/*": {"origins": "https://localhost:8080"}}, supports_credentials=True)
client = MongoClient("mongodb+srv://wombat:Glc4GncM@womcluster.vdiu8vi.mongodb.net/")
db = client.get_database('mathQuizDatabase')
rate_limiting = db.get_collection('rate_limiting')

redis_client = Redis(host='localhost', port=6379, db=0)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits_exempt_when=lambda: False
)

from app.routes import main_route, account_routes, login_routes

app.register_blueprint(main_route.bp)
app.register_blueprint(account_routes.account_routes_bp)
app.register_blueprint(login_routes.login_routes_bp)

from flask import request, jsonify
from datetime import datetime

@app.before_request
def check_rate_limit():
    try:
        limit_per_hour = 100
        limit_per_day = 1000
        current_ip = request.remote_addr
        current_time = datetime.utcnow()

        # Find or initialize the rate limit document
        rate_limit_record = rate_limiting.find_one({'ip_address': current_ip})

        if rate_limit_record:
            # Check if within the same hour
            if rate_limit_record['window_start_hour'].hour == current_time.hour and rate_limit_record['window_start_hour'].day == current_time.day:
                new_count_hourly = rate_limit_record['request_count_hourly'] + 1
            else:
                # Reset count for a new hour
                rate_limit_record['window_start_hour'] = current_time.replace(minute=0, second=0, microsecond=0)
                new_count_hourly = 1

            # Check if within the same day
            if rate_limit_record['window_start_day'].day == current_time.day:
                new_count_daily = rate_limit_record['request_count_daily'] + 1
            else:
                # Reset count for a new day
                rate_limit_record['window_start_day'] = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
                new_count_daily = 1

            # Update the record
            rate_limiting.update_one(
                {'ip_address': current_ip},
                {'$set': {
                    'request_count_hourly': new_count_hourly, 
                    'window_start_hour': rate_limit_record['window_start_hour'],
                    'request_count_daily': new_count_daily, 
                    'window_start_day': rate_limit_record['window_start_day']
                }}
            )
        else:
            # Create a new record for a new IP
            new_record = {
                'ip_address': current_ip,
                'request_count_hourly': 1,
                'window_start_hour': current_time.replace(minute=0, second=0, microsecond=0),
                'request_count_daily': 1,
                'window_start_day': current_time.replace(hour=0, minute=0, second=0, microsecond=0)
            }
            rate_limiting.insert_one(new_record)
            new_count_hourly, new_count_daily = 1, 1

        # Check if either limit is exceeded
        if new_count_hourly > limit_per_hour or new_count_daily > limit_per_day:
            return jsonify({'error': 'Rate limit exceeded'}), 429
    except Exception as e:
        print(f"Error checking rate limit: {e}")
    
@app.errorhandler(RateLimitExceeded)
def ratelimit_handler(e):
    return jsonify(error="You have been rate limited. Please limit your requests to this application."), 429