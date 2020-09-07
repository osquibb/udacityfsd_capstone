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

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class LandListing(db.Model):
    __tablename__ = 'land_listing'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    sale_price = Column(Numeric, nullable=False)
    listed_date = Column(Date, nullable=False)
    fund = relationship('Fund', uselist=False, back_populates='land_listing')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'sale_price': self.sale_price,
            'listed_date': self.listed_date
        }

class Funder(db.Model):
    __tablename__ = 'funder'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    phone = Column(Integer)
    email = Column(Integer, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email
        }

class Fund(db.Model):
    __tablename__ = 'fund'

    id = Column(Integer, primary_key=True)
    land_listing_id = Column(Integer, ForeignKey('land_listing.id'))
    land_listing = relationship("LandListing", back_populates="fund")
    transaction_fee = Column(Numeric, default=50)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'land_listing_id': self.land_listing_id,
            'transaction_fee': self.transaction_fee
        }
    
class Contribution(db.Model):
    # association table
    __tablename__ = 'contribution'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    amount = Column(Numeric)
    funder_id = Column(Integer, ForeignKey('funder.id'))
    fund_id = Column(Integer, ForeignKey('fund.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'date': self.date,
            'amount': self.amount,
            'funder_id': self.funder_id,
            'fund_id': self.fund_id
        }