# udacityfsd_capstone

To run the server, execute:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
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
#### Anonymous User
* Can view land listings and funds

#### Funder
* Can view land listings, funds and funders
* Can modify own funder data
* Can add a contribution

#### Listing Manager
* Can Add, modify or delete land listings

#### Admin
* Can Add, modifiy or delete land listings, funders and contributions

## Tests:
* One test for success behavior of each endpoint
* One test for error behavior of each endpoint
* At least two tests of RBAC for each role