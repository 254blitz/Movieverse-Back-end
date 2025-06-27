from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token

db = SQLAlchemy()

__all__ = ["User", "Comment", "Favorite", "Rating"]

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade="all, delete-orphan")
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        return create_access_token(identity=self.id)

    def __repr__(self):
        return f"<User {self.username}>"


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    imdb_id = db.Column(db.String(20), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Comment by User {self.user_id} on {self.imdb_id}>"


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    poster_url = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Favorite {self.title} by User {self.user_id}>"


class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    imdb_id = db.Column(db.String(20), nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Rating {self.rating_value} for {self.imdb_id} by User {self.user_id}>"
