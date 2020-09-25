import os
import datetime
from flask import Flask, request, jsonify, abort, redirect, url_for
import json
from flask_cors import CORS
from models import LandListing, Funder, Fund, Contribution, \
    setup_db, db_drop_and_create_all
from auth import AuthError, requires_auth

# TODO: extend CORS - see trivia api

# (un)comment below for testing
# db_drop_and_create_all()


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # ROUTES

    @app.route('/')
    def index():
        return redirect(url_for('health_check'))

    @app.route('/health')
    def health_check():
        return jsonify({
            'success': True,
            'status': 'connected'
        }), 200

    @app.route('/land_listings')
    @requires_auth('get:listings')
    def get_land_listings():
        formatted_land_listings = [land_listing.format()
                                   for land_listing in LandListing.query.all()]

        if len(formatted_land_listings) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'land_listings': formatted_land_listings
        }), 200

    @app.route('/land_listings/<int:land_listing_id>')
    @requires_auth('get:listings')
    def get_land_listing_details(land_listing_id):
        land_listing = LandListing.query.get(land_listing_id)

        if land_listing is None:
            abort(404)

        try:
            formatted_contributions = [
                contribution.format()
                for contribution in land_listing.contributions
            ]
            total_contributions = sum(
                [
                    contribution.amount
                    for contribution in land_listing.contributions
                ])

            return jsonify({
                'success': True,
                'land_listing': land_listing.format(),
                'contributions': formatted_contributions,
                'total_contributions': str(total_contributions)
            }), 200

        except BaseException:
            abort(422)

    @app.route('/land_listings', methods=['POST'])
    @requires_auth('post:listings')
    def create_land_listing():
        try:
            body = request.get_json()
            title = body.get('title', None)
            address_1 = body.get('address_1', None)
            address_2 = body.get('address_2', None)
            city = body.get('city', None)
            state = body.get('state', None)
            zipcode = body.get('zipcode', None)
            sale_price = body.get('sale_price', None)
            listed_date = body.get('listed_date', None)

            new_land_listing = LandListing(
                title=title,
                address_1=address_1,
                address_2=address_2,
                city=city,
                state=state,
                zipcode=zipcode,
                sale_price=sale_price,
                listed_date=listed_date)
            new_land_listing.insert()

            return jsonify({
                'success': True,
                'land_listing_id': new_land_listing.id,
                'initial_fund_id': new_land_listing.funds[0].id
            }), 200

        except BaseException:
            abort(422)

    @app.route('/funders')
    @requires_auth('get:funders')
    def get_funders():
        formatted_funders = [funder.format() for funder in Funder.query.all()]

        if len(formatted_funders) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'funders': formatted_funders
        }), 200

    @app.route('/funders', methods=['POST'])
    @requires_auth('post:funders')
    def create_funder():
        try:
            body = request.get_json()
            first_name = body.get('first_name', None)
            last_name = body.get('last_name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            phone = body.get('phone', None)
            email = body.get('email', None)

            new_funder = Funder(
                first_name=first_name,
                last_name=last_name,
                age=age,
                gender=gender,
                phone=phone,
                email=email)
            new_funder.insert()

            return jsonify({
                'success': True,
                'funder_id': new_funder.id
            }), 200

        except BaseException:
            abort(422)

    @app.route('/funders/<int:funder_id>')
    @requires_auth('get:funders')
    def get_funder_details(funder_id):
        funder = Funder.query.get(funder_id)
        if funder is None:
            abort(404)

        try:
            formatted_contributions = [
                contribution.format() for contribution in funder.contributions]
            total_contributions = sum(
                [contribution.amount for contribution in funder.contributions])

            return jsonify({
                'success': True,
                'funder': funder.format(),
                'contributions': formatted_contributions,
                'total_contributions': str(total_contributions)
            }), 200

        except BaseException:
            abort(422)

    @app.route('/funders/<int:funder_id>', methods=['PATCH'])
    @requires_auth('patch:funders')
    def update_funder(funder_id):
        funder = Funder.query.get(funder_id)

        if funder is None:
            abort(404)

        try:
            body = request.get_json()
            updates = {
                'first_name': body.get('first_name', None),
                'last_name': body.get('last_name', None),
                'age': body.get('age', None),
                'gender': body.get('gender', None),
                'phone': body.get('phone', None),
                'email': body.get('email', None)
            }

            for attribute in updates:
                if updates[attribute] is not None:
                    setattr(funder, attribute, updates[attribute])

            funder.update()

            return jsonify({
                'success': True,
                'funder': funder.format()
            }), 200

        except BaseException:
            abort(422)

    @app.route('/land_listings/<int:land_listing_id>/funds/<int:fund_id>',
               methods=['POST'])
    @requires_auth('post:contributions')
    def contribute_to_fund(land_listing_id, fund_id):
        body = request.get_json()
        amount = body.get('amount', None)
        funder_id = body.get('funder_id', None)

        try:
            amount = float(amount)
        except BaseException:
            abort(422)

        land_listing = LandListing.query.get(land_listing_id)
        fund = Fund.query.get(fund_id)
        funder = Funder.query.get(funder_id)

        if (land_listing is None) or (fund is None) or (funder is None):
            abort(404)

        land_listing_fund_ids = [fund.id for fund in land_listing.funds]

        if fund_id not in land_listing_fund_ids:
            abort(422)

        try:
            new_contribution = Contribution(
                funder_id=funder.id,
                land_listing_id=land_listing.id,
                fund_id=fund.id,
                date=datetime.date.today(),
                amount=amount)
            new_contribution.insert()

            return jsonify({
                'success': True,
                'contribution': new_contribution.format(),
            }), 200

        except BaseException:
            abort(422)

    @app.route('/contributions/<int:contribution_id>', methods=['DELETE'])
    @requires_auth('delete:contributions')
    def delete_contribution(contribution_id):
        contribution = Contribution.query.get(contribution_id)

        if contribution is None:
            abort(404)

        try:
            contribution.delete()

            return jsonify({
                'success': True,
                'deleted_contribution_id': contribution_id
            }), 200

        except BaseException:
            abort(422)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
