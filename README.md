# udacityfsd_capstone

To install dependencies, execute:
```bash
pip install -r requirements.txt
```

The following environment variables are required:
```bash
DATABASE_URL
TEST_DATABASE_URL
AUTH0_DOMAIN
API_AUDIENCE
```

To run the server, execute:
```bash
export FLASK_ENV=development
export FLASK_APP=app.py
flask run --reload
```

To run tests, execute:
```bash
export FLASK_ENV=development
python test.py
```

To run initial db migration, execute:
```bash
export FLASK_ENV=development
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Overview
**Polyopsony** models a company that is responsible for listing land availabe for sale and managing crowdsourced funding in order to purchase and convert the land into nature preserves.

## Models

* Land Listings 
* Funders
* Funds
* Contributions 

## Endpoints
**GET**
* /land_listings
* /land_listings/**{land_listing_id}**
* /funders
* /funders/**{funder_id}**

**POST**
* /land_listings
* /funders
* /land_listings/**{land_listing_id}**/funds/**{fund_id}**

**PATCH**
* /funders/**{funder_id}**

**DELETE**
* /contributions/**{contribution_id}**

## Roles

#### Funder
* Can view land listings and funds
* Can view land listings, funds and funders
* Can modify own funder data
* Can add a contribution

#### Listing Manager
* Can Add, modify or delete land listings and view funders

#### Admin
* Can do all of the above & delete contributions