from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100),unique = True,nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price' : self.price
            # Add all the fields you want to include
        }

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)