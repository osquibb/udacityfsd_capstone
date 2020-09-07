import os
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv

if os.environ['FLASK_ENV'] == 'development':
    load_dotenv()

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def format(obj):
    return vars(obj)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# TODO: Complete models

class LandListing(db.Model):
    __tablename__ = 'land_listing'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    sale_price = Column(Numeric, nullable=False)
    listed_date = Column(Date, nullable=False)
    fund = relationship('Fund', backref='land_listing', uselist=False)

class Funder(db.Model):
    __tablename__ = 'funder'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    phone = Column(Integer)
    email = Column(Integer, nullable=False)

class Fund(db.Model):
    __tablename__ = 'fund'

    id = Column(Integer, primary_key=True)
    land_listing = Column(Integer, ForeignKey('land_listing.id'))
    transaction_fee = Column(Numeric)
    
class Contribution(db.Model):
    # association table
    __tablename__ = 'contribution'

    id = Column(Integer, primary_key=True)
    funder_id = Column(db.Integer, db.ForeignKey('funder.id'))
    fund_id = Column(db.Integer, db.ForeignKey('fund.id'))