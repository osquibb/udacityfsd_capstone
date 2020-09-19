import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, abort
from app import create_app
from models import LandListing, Funder, Fund, Contribution, setup_db, db_drop_and_create_all

# TODO: create common setup_db() function

def create_test_land_listing():
    land_listing = LandListing(
        title='Test Land Listing',
        address_1='123 Main Street',
        city='Asheville',
        state='NC',
        zipcode=28801,
        sale_price=5000.00,
        listed_date="06/02/2020"
    )
    land_listing.insert()

    return land_listing.id

def delete_land_listing(land_listing_id):
    land_listing = LandListing.query.get(land_listing_id)
    fund = land_listing.funds[0].delete()
    land_listing.delete()

class PolyopsonyTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client
        self.database_name = "polyop_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        # db_drop_and_create_all()
        pass

    def test_success_get_land_listings(self):
        land_listing_id = create_test_land_listing()

        res = self.client().get('/land_listings')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['land_listings'])

        delete_land_listing(land_listing_id)

    def test_error_get_land_listings(self):
        res = self.client().get('/land_listings')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertFalse(data['land_listings'])
    
    def test_success_create_land_listing(self):
        pass