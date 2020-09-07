import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
from models import LandListing, Funder, Fund, Contribution, setup_db

app = Flask(__name__)
setup_db(app)
CORS(app)

## ROUTES

@app.route('/')
def hello():
    return jsonify({
            'success': True,
            'message': 'hello'
        }), 200


## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401