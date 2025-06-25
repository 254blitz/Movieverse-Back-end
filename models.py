from app import db
from datetime import datetime, timezone

class User(db.Model):
    id = db.Column(db.Integer ,primary_key = True)
    username = db.Column(db.String(120), nullable = False, unique = True)
    email = db.Column(db.String(120), nullable = False, unique = True)
    password_hash = db.Column(db.String(120), nullable = False)
    created_at = db.Column(db.Datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User {self.username}>'