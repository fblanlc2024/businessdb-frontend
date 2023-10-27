import os
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import dotenv
from flask_jwt_extended import JWTManager
import logging
from datetime import timedelta

dotenv_path = "D:\\Projects\\Python\\math-quiz\\app\\important_variables.env"
dotenv.load_dotenv(dotenv_path)
logging.basicConfig(level=logging.DEBUG)
# For countering the HTTPS error/secure transport - comment out when in production mode!!!!
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
# app.secret_key = dotenv.get_key(dotenv_path, 'FLASK_SECRET_KEY')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Ensure you're getting a valid integer from the environment variable or provide a default.
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))  # default to 1 hour
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800)))  # default to 7 days

app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'


if not app.secret_key:
    raise ValueError("No secret key set for Flask application")
if not app.config['JWT_SECRET_KEY']:
    raise ValueError("No JWT secret key set")
if not app.config['JWT_ACCESS_TOKEN_EXPIRES']:
    raise ValueError("No JWT access token expiration time set")

CORS(app, resources={r"/*": {"origins": "*", "expose_headers": ["Authorization"]}}, supports_credentials=True)
client = MongoClient("mongodb+srv://wombat:Glc4GncM@womcluster.vdiu8vi.mongodb.net/")
db = client.get_database('mathQuizDatabase')

# Import and register the Blueprint
from app.routes import main_route, account_routes, login_routes

app.register_blueprint(main_route.bp)
app.register_blueprint(account_routes.account_routes_bp)
app.register_blueprint(login_routes.login_routes_bp)
