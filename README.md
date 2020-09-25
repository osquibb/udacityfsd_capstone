# udacityfsd_capstone

## Overview
**Polyopsony** models a company that is responsible for listing land availabe for sale and managing crowdsourced funding in order to purchase and convert the land into nature preserves.  Funders will be able to browse listings and contribute to funds associated with each.  API endpoints provide information such as all listings, contributions and total contributions associcated with each listing and contributions associated with each funder.

To install dependencies, in the project directory, execute:
```bash
pip install -r requirements.txt
```

This project requires postgres.  To install postgres, with homebrew installed:
```
brew install postgres
```

This project requires two postgres databases running locally:
```
createdb polyop
createdb polyop_test
```

To run the server, execute:
```bash
source setup.sh
export FLASK_ENV=development
export FLASK_APP=app.py
flask run --reload
```

To run tests, execute:
```bash
source setup.sh
export FLASK_ENV=development
python test.py
```

To run initial db migration, execute:
```bash
source setup.sh
export FLASK_ENV=development
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

**Herkou URL**
https://polyopsony.herokuapp.com/

**To login**
https://dev-r2v8kom9.auth0.com/authorize?audience=polyop&response_type=token&client_id=ddwa7LxBL2pxmRMyEk53tF7SI4JrN0N6&redirect_uri=https://polyopsony.herokuapp.com/health

**Postman Collections (RBAC Tests) are available in /postman_rbac_tests**

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

*Example request body:*
```json
{
    "title": "land listing title",
    "address_1": "",
    "address_2": "",
    "city": "New York",
    "state": "NY",
    "zipcode": 10101,
    "sale_price": 5000,
    "listed_date": "01/01/2020"
}
```
* /funders

*Example request body:*
```json
{
    "first_name": "John",
    "last_name": "Smith",
    "age": 20,
    "gender": "Male",
    "phone": 1021231212,
    "email": "john@test.com"
}
```
* /land_listings/**{land_listing_id}**/funds/**{fund_id}**

*Example request body:*
```json
{
    "funder_id": 1,
    "amount": 10.50
}
```

**PATCH**
* /funders/**{funder_id}**

*Example request body:*
```json
{
    "first_name": "John",
    "last_name": "Smith",
    "age": 20,
    "gender": "Male",
    "phone": 1021231212,
    "email": "john@test.com"
}
```

**DELETE**
* /contributions/**{contribution_id}**

## Roles & Permissions

#### Funder
* get:funders
* post:funders
* get:listings
* patch:funders
* post:contributions	

#### Listing Manager
* get:funders	
* get:listings
* post:listings

#### Admin
* get:funders
* post:funders
* patch:funders
* get:listings
* post:listings
* post:contributions
* delete:contributions