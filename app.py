import os
import math
import datetime
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
from models import LandListing, Funder, Fund, Contribution, setup_db, db_drop_and_create_all

app = Flask(__name__)
setup_db(app)
CORS(app)

# (un)comment below for testing
# db_drop_and_create_all()

## ROUTES

@app.route('/')
def hello():
    return jsonify({
            'success': True,
            'message': 'hello'
        }), 200

@app.route('/land_listings')
def get_land_listings():
    formatted_land_listings = [ land_listing.format() for land_listing in LandListing.query.all() ]

    if len(formatted_land_listings) == 0:
        abort(404)

    return jsonify({
            'success': True,
            'land_listings': formatted_land_listings
        }), 200

@app.route('/land_listings/<int:land_listing_id>')
def get_land_listing_details(land_listing_id):
    land_listing = LandListing.query.get(land_listing_id)
    formatted_contributions = [ contribution.format() for contribution in land_listing.contributions  ]
    total_contributions = sum([ contribution.amount for contribution in land_listing.contributions ])

    return jsonify({
            'success': True,
            'land_listing': land_listing.format(),
            'contributions': formatted_contributions,
            'total_contributions': str(total_contributions)
        }), 200

@app.route('/land_listings', methods=['POST'])
def create_land_listing():
    body = request.get_json()
    title = body.get('title', None)
    address_1 = body.get('address_1', None)
    address_2 = body.get('address_2', None)
    city = body.get('city', None)
    state = body.get('state', None)
    zipcode = body.get('zipcode', None)
    sale_price = body.get('sale_price', None)
    listed_date = body.get('listed_date', None)

    new_land_listing = LandListing(title=title, address_1=address_1, address_2=address_2, city=city, state=state, zipcode=zipcode, sale_price=sale_price, listed_date=listed_date)
    new_land_listing.insert()

    return jsonify({
        'success': True,
        'land_listing_id': new_land_listing.id
    }), 200

@app.route('/funders')
def get_funders():
    formatted_funders = [ funder.format() for funder in Funder.query.all() ]

    if len(formatted_funders) == 0:
        abort(404)

    return jsonify({
            'success': True,
            'funders': formatted_funders
        }), 200

@app.route('/funders', methods=['POST'])
def create_funder():
    body = request.get_json()
    first_name = body.get('first_name', None)
    last_name = body.get('last_name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    phone = body.get('phone', None)
    email = body.get('email', None)

    new_funder = Funder(first_name=first_name, last_name=last_name, phone=phone, email=email)
    new_funder.insert()

    return jsonify({
        'success': True,
        'funder_id': new_funder.id
    }), 200

@app.route('/funds/<int:fund_id>', methods=['POST'])
def contribute_to_fund(fund_id):
    body = request.get_json()
    amount = body.get('amount', None)
    funder_id = body.get('funder_id', None)
    land_listing_id = body.get('land_listing_id', None)
    funder = Funder.query.filter(Funder.id == funder_id).one_or_none()
    land_listing = LandListing.query.filter(LandListing.id == land_listing_id).one_or_none()
    fund = Fund.query.filter(Fund.id == fund_id).one_or_none()
    # TODO: verify that fund is associated with the listing

    if fund is None or funder is None or land_listing is None or math.isnan(amount):
        abort(422)

    contribution = Contribution(funder_id=funder.id, land_listing_id=land_listing.id, fund_id=fund.id, date=datetime.date.today(), amount=amount)
    contribution.insert()

    return jsonify({
            'success': True,
            'contribution': contribution.format(),
        }), 200

# testing START...

@app.route('/insert', methods=['POST'])
def insertTest():
    new_land_listing = LandListing(
        title='test land listing',
        city='Asheville',
        state='NC',
        zipcode=28801,
        sale_price=5000.00,
        listed_date=datetime.datetime(2020, 5, 17)
    )
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

# testing END


    
## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def not_found(error):
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