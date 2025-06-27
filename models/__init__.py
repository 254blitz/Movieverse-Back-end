from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is initialized
from .user import User
from .favorite import Favorite