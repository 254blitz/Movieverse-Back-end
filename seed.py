from app import app, db

from models import User, Comment, Favorite, Rating
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    hashed_pw = bcrypt.generate_password_hash("password123").decode("utf-8")
    user = User(username="testuser", email="test@mail.com", password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()

    fav = Favorite(
        user_id=user.id,
        movie_id="tt0133093",
        title="The Matrix",
        poster_url="https://image.tmdb.org/t/p/w500/matrix-poster.jpg"
    )
    db.session.add(fav)

    rating = Rating(user_id=user.id, imdb_id="tt0133093", rating_value=5)
    db.session.add(rating)

    comment = Comment(user_id=user.id, imdb_id="tt0133093", comment_text="This movie is goated 🐐")
    db.session.add(comment)

    db.session.commit()
    print("✅ Seed data created successfully!")
