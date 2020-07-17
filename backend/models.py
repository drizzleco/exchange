from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User Model
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    auctions = db.relationship("Auction", backref="user")
    bids = db.relationship("Bid", backref="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        """returns dict representation of User"""
        return {
            "id": self.id,
            "username": self.username,
            "created": self.created,
            "auctions": [auction.to_dict() for auction in self.auctions],
            "bids": [bid.to_dict() for bid in self.bids],
        }


class Auction(db.Model):
    """
    Auction Model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    bids = db.relationship("Bid", backref="auction")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        """returns dict representation of Auction"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "starting_price": self.starting_price,
            "created": self.created,
            "end_time": self.end_time,
            "bids": [bid.to_dict() for bid in self.bids],
            "user_id": self.user_id,
        }

    def get_current_price(self):
        """
        returns current price of auction(returns starting 
        price or amount of highest bid)
        """
        highest_bid = sorted([bid.amount for bid in self.bids])[-1] if self.bids else 0
        return max(self.starting_price, highest_bid)


class Bid(db.Model):
    """
    Bid Model
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey("auction.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        """returns dict representation of Bid"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "auction_id": self.auction_id,
            "amount": self.amount,
            "created": self.created,
        }
