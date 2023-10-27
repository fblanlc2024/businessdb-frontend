from flask import Blueprint, jsonify

# Create a new Blueprint
bp = Blueprint('main', __name__)

# Define a route on this Blueprint
@bp.route('/welcome')
def home():
    return jsonify(message="Welcome to the Math Quiz App!")