import os
import datetime
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
from models import LandListing, Funder, Fund, Contribution, setup_db

app = Flask(__name__)
setup_db(app)
CORS(app)

# TODO: couple inserts and deletes of land_listings with same of funds (b/c 1:1) 

## ROUTES

@app.route('/')
def hello():
    return jsonify({
            'success': True,
            'message': 'hello'
        }), 200

@app.route('/insertTest')
def insertTest():
    new_land_listing = LandListing(title='test land listing', sale_price=5000.00, listed_date=datetime.datetime(2020, 5, 17))
    new_fund = Fund(land_listing_id=new_land_listing.id)
    new_land_listing.fund = new_fund
    new_land_listing.insert()
    return jsonify({
        'success': True,
        'inserted_id': new_land_listing.id
    })

@app.route('/deleteTest/<int:land_listing_id>')
def deleteTest(land_listing_id):
    land_listing = LandListing.query.filter(LandListing.id == land_listing_id).one_or_none()
    land_listing.delete()

    return jsonify({
        'success': True,
        'deleted_id': land_listing_id
    })
    
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