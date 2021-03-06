import os
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
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


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class LandListing(db.Model):
    __tablename__ = 'land_listings'

    # PK
    id = Column('land_listing_id', Integer, primary_key=True)

    # non-key fields
    title = Column(String(120), nullable=False)
    address_1 = Column(String(40))
    address_2 = Column(String(40))
    city = Column(String(20), nullable=False)
    state = Column(String(12), nullable=False)
    zipcode = Column(Integer, nullable=False)
    sale_price = Column(Numeric, nullable=False)
    listed_date = Column(Date, nullable=False)

    def insert(self):
        db.session.add(self)
        funds = Fund.query.filter(
            Fund.land_listing_id == self.id).one_or_none()

        if funds is None:
            new_fund = Fund(land_listing_id=self.id)
            db.session.add(new_fund)

        db.session.commit()

    def delete(self):
        funds = Fund.query.filter(Fund.land_listing_id == self.id).all()

        if len(funds) > 0:
            raise Exception('Cannot delete LandListing with associated funds.')
        else:
            db.session.delete(self)
            db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'address': {
                'address_1': self.address_1,
                'address_2': self.address_2,
                'city': self.city,
                'state': self.state,
                'zipcode': self.zipcode
            },
            'sale_price': str(self.sale_price),
            'listed_date': self.listed_date
        }


class Funder(db.Model):
    __tablename__ = 'funders'

    # PK
    id = Column('funder_id', Integer, primary_key=True)

    # non-key fields
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    phone = Column(Integer, nullable=False)
    email = Column(String(25), nullable=False)

    # relationships
    funds = relationship('Fund', secondary='contributions')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
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
    __tablename__ = 'funds'

    # PK
    id = Column('fund_id', Integer, primary_key=True)

    # FK
    land_listing_id = Column(Integer, ForeignKey(
        'land_listings.land_listing_id'), nullable=False)

    # non-key fields
    transaction_fee = Column(Numeric, default=50.00)

    # relationships
    land_listing = relationship('LandListing', backref='funds')
    funders = relationship('Funder', secondary='contributions')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'land_listing_id': self.land_listing_id,
            'transaction_fee': str(self.transaction_fee)
        }


class Contribution(db.Model):
    # associative table
    __tablename__ = 'contributions'

    # PK
    id = Column('contribution_id', Integer, primary_key=True)

    # FKs
    funder_id = Column(Integer, ForeignKey('funders.funder_id'))
    land_listing_id = Column(
        Integer, ForeignKey('land_listings.land_listing_id'))
    fund_id = Column(Integer, ForeignKey('funds.fund_id'))

    # non-key fields
    date = Column(Date, nullable=False)
    amount = Column(Numeric, default=0.00)

    # relationships
    land_listing = relationship('LandListing', backref='contributions')
    funder = relationship('Funder', backref='contributions')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'contribution_id': self.id,
            'funder_id': self.funder_id,
            'fund_id': self.fund_id,
            'date': self.date,
            'amount': str(self.amount)
        }
