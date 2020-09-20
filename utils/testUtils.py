import datetime
from models import LandListing, Funder, Fund, Contribution, setup_db, db_drop_and_create_all

def create_test_land_listing():
    land_listing = LandListing(
        title='Test Land Listing',
        address_1='123 Main Street',
        city='Asheville',
        state='NC',
        zipcode=28801,
        sale_price=5000.00,
        listed_date='06/02/2020'
    )
    land_listing.insert()

    return { 
        'land_listing_id': str(land_listing.id),
        'initial_fund_id': str(land_listing.funds[0].id)
    }

def delete_land_listing(land_listing_id):
    land_listing = LandListing.query.get(land_listing_id)
    land_listing.funds[0].delete()
    land_listing.delete()

def create_test_funder():
    funder = Funder(
        first_name='John',
        last_name='Smith',
        age=35,
        gender='Male',
        phone=1234567890,
        email='test@test.com'  
    )
    funder.insert()

    return str(funder.id)

def delete_funder(funder_id):
    Funder.query.get(funder_id).delete()

def create_test_contribution(funder_id, land_listing_id, fund_id):
    contribution = Contribution(
        funder_id=funder_id,
        land_listing_id=land_listing_id,
        fund_id=fund_id,
        date=datetime.date.today(),
        amount=10.25
    )
    contribution.insert()

    return str(contribution.id)

def delete_contribution(contribution_id):
    Contribution.query.get(contribution_id).delete()