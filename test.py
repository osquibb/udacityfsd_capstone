import os
import unittest
import json
from utils.testUtils import *
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import create_app
from models import LandListing, Funder, Fund, Contribution, setup_db, db_drop_and_create_all

class PolyopsonyTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        # db_drop_and_create_all()
        pass

    def test_get_land_listings_200(self):
        test_ids = create_test_land_listing()

        res = self.client().get('/land_listings')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['land_listings'])

        delete_land_listing(test_ids['land_listing_id'])

    def test_get_land_listings_404(self):
        res = self.client().get('/land_listings')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_get_land_listing_details_200(self):
        test_ids = create_test_land_listing()

        res = self.client().get('/land_listings/' + test_ids['land_listing_id'])
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['land_listing'])

        delete_land_listing(test_ids['land_listing_id'])

    def test_get_land_listing_details_404(self):
        res = self.client().get('/land_listings/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_land_listing_200(self):
        valid_land_listing = {
            'title': 'Test Land Listing',
            'address_1': '123 Main Street',
            'city': 'Asheville',
            'state': 'NC',
            'zipcode': '28801',
            'sale_price': '5000.00',
            'listed_date': '06/02/2020'
        }

        res = self.client().post('/land_listings', json=valid_land_listing)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['land_listing_id'])
        self.assertTrue(data['initial_fund_id'])

        delete_land_listing(data['land_listing_id'])

    def test_create_land_listing_422(self):
        invalid_land_listing = {
            'title': 'Test Land Listing',
            'address': '123 Main Street',
            'city': 'Asheville',
            'state': 'NC',
            'zip': '28801'
        }

        res = self.client().post('/land_listings', json=invalid_land_listing)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_get_funders_200(self):
        funder_id = create_test_funder()

        res = self.client().get('/funders')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['funders'])

        delete_funder(funder_id)

    def test_get_funders_404(self):
        res = self.client().get('/funders')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_funder_200(self):

        valid_funder = {
            'first_name': 'John',
            'last_name': 'Smith',
            'age': '35',
            'gender': 'Male',
            'phone': '1234567890',
            'email': 'test@test.com',
        }

        res = self.client().post('/funders', json=valid_funder)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['funder_id'])

        delete_funder(data['funder_id'])

    def test_create_funder_422(self):

        invalid_funder = {
            'name': 'John',
            'phone_num': '1234567890',
            'email': 'test@test.com',
        }

        res = self.client().post('/funders', json=invalid_funder)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_get_funder_details_200(self):
        funder_id = create_test_funder()

        res = self.client().get('/funders/' + funder_id)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['funder'])

        delete_funder(funder_id)

    def test_get_funder_details_404(self):
        res = self.client().get('/funders/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_funder_200(self):
        funder_id = create_test_funder()

        valid_updates = {
            'last_name': 'Green',
            'age': '40'
        }

        res = self.client().patch('/funders/' + funder_id, json=valid_updates)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['funder'])

        delete_funder(funder_id)

    def test_update_funder_404(self):
        valid_updates = {
            'last_name': 'Green',
            'age': '40'
        }

        res = self.client().patch('/funders/10', json=valid_updates)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_contribute_to_fund_200(self):
        test_ids = create_test_land_listing()
        funder_id = create_test_funder()

        valid_contribution = {
            'amount': '10.25',
            'funder_id': funder_id
        }

        res = self.client().post('/land_listings/' +
            test_ids['land_listing_id'] + '/funds/' +
            test_ids['initial_fund_id'], json=valid_contribution)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['contribution'])

        delete_land_listing(test_ids['land_listing_id'])
        delete_funder(funder_id)

    def test_contribute_to_fund_422(self):
        test_ids = create_test_land_listing()
        funder_id = create_test_funder()

        invalid_contribution = {
            'amount': 'abcd',
            'funder_id': funder_id
        }

        res = self.client().post('/land_listings/' +
            test_ids['land_listing_id'] + '/funds/' +
            test_ids['initial_fund_id'], json=invalid_contribution)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

        delete_land_listing(test_ids['land_listing_id'])
        delete_funder(funder_id)

    def test_delete_contribution_200(self):
        test_ids = create_test_land_listing()
        funder_id = create_test_funder()
        contribution_id = create_test_contribution(funder_id, test_ids['land_listing_id'], test_ids['initial_fund_id'])

        res = self.client().delete('/contributions/' + contribution_id)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['deleted_contribution_id'])

        delete_land_listing(test_ids['land_listing_id'])
        delete_funder(funder_id)

    def test_delete_contribution_404(self):
        res = self.client().delete('/contributions/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

if __name__ == "__main__":
    unittest.main()