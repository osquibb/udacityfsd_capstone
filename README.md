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

**To login**:
https://dev-r2v8kom9.auth0.com/authorize?audience=polyop&response_type=token&client_id=ddwa7LxBL2pxmRMyEk53tF7SI4JrN0N6&redirect_uri=https://polyopsony.herokuapp.com/health

**Postman Collections (RBAC Tests) are available in /postman_rbac_tests**

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
- Example request body:
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
- Example request body:
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
- Example request body:
```json
{
    "funder_id": 1,
    "amount": 10.50
}
```

**PATCH**
* /funders/**{funder_id}**
- Example request body:
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