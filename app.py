import os
import datetime
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
from models import LandListing, Funder, Fund, Contribution, setup_db, db_drop_and_create_all

app = Flask(__name__)
setup_db(app)
CORS(app)

# TODO: Implement non-null FKs to prevent orphaned funds or land listings since 1:1 relationship between them?

# (un)comment below for testing
# db_drop_and_create_all()

## ROUTES

@app.route('/')
def hello():
    return jsonify({
            'success': True,
            'message': 'hello'
        }), 200

@app.route('/insert', methods=['POST'])
def insertTest():
    new_land_listing = LandListing(title='test land listing', sale_price=5000.00, listed_date=datetime.datetime(2020, 5, 17))
    new_fund = Fund(land_listing_id=new_land_listing.id)
    new_land_listing.fund = new_fund
    new_land_listing.insert()
    return jsonify({
        'success': True,
        'inserted_id': new_land_listing.id
    })

@app.route('/delete/<int:land_listing_id>', methods=['POST'])
def deleteTest(land_listing_id):
    land_listing = LandListing.query.filter(LandListing.id == land_listing_id).one_or_none()
    land_listing.delete()

    return jsonify({
        'success': True,
        'deleted_id': land_listing_id
    })

@app.route('/fund/<int:land_listing_id>')
def getFundByLandListingID(land_listing_id):
    fund = Fund.query.filter(Fund.land_listing_id == land_listing_id).one_or_none()
    return jsonify({
        'success': True,
        'fund_id': fund.id,
        'transaction_fee': str(fund.transaction_fee)
    })

@app.route('/fundAlt/<int:land_listing_id>')
def getFundByLandListingIDAlt(land_listing_id):
    land_listing = LandListing.query.filter(LandListing.id == land_listing_id).one_or_none()
    fund = land_listing.fund
    return jsonify({
        'success': True,
        'fund_id': fund.id,
        'transaction_fee': str(fund.transaction_fee)
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