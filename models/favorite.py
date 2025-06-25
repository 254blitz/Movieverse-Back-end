from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    poster_url = db.Column(db.String)

    user = db.relationship('User', back_populates='favorites')
