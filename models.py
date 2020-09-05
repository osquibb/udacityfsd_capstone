import os
from sqlalchemy import Column, Integer, String, Numeric, Date
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

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

# TODO: tighten up constraints 
# TODO: complete one-to-many relationship between funder and landlistings 

class LandListing(db.Model):  
  __tablename__ = 'land_listings'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  sale_price = Column(Numeric, nullable=False)
  listed_date = Column(Date, nullable=False)
  funders = db.relationship('Funder', backref='land_listings', lazy=True)

  def __init__(self, id, title, sale_price, listed_date):
    self.id = id
    self.title = title
    self.sale_price = sale_price
    self.listed_date = listed_date

  def format(self):
    return {
      'id': self.id,
      'title': self.name,
      'sale_price': self.sale_price,
      'listed_date': self.date
    }

class Funder(db.Model):
    __tablename__ = 'funders'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    phone = Column(Integer)
    email = Column(Integer, nullable=False),

