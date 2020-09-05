# udacityfsd_capstone

To run the server, execute:
```bash
export FLASK_APP=api.py;
flask run --reload
```
## Overview
**Polyopsony** models a company that is responsible for listing land availabe for sale and managing crowdsourced funding in order to purchase and convert the land into nature preserves.

## Models

* Land Listings with attributes title, sale price and current funding level
* Funders with attributes name, age, gender, email, phone, funding amount & land listing id

## Endpoints
* GET /landListings and /funders
* DELETE /landListings/ and /funders/
* POST /landListings and /funders and
* PATCH /landListings/ and /funders/

## Roles
#### Anonymous User
* Can view land listings

#### Funder
* Can view land listings and funders
* Can modify own funder data

#### Listing Manager
* Can Add, modify or delete land listings

#### Admin
* Can Add, modifiy or delete land listings and funders

## Tests:
* One test for success behavior of each endpoint
* One test for error behavior of each endpoint
* At least two tests of RBAC for each role