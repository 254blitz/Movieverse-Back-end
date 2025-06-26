from app import app, db
from models import User, Favorite
from datetime import datetime

def seed_favorites():
    with app.app_context():
        print("🌱 Seeding favorites...")

        
        favorites_data = [
            {
                "username": "movie_fan",
                "movies": [
                    {"movie_id": "tt0111161", "title": "The Shawshank Redemption", "poster_url": "https://example.com/shawshank.jpg"},
                    {"movie_id": "tt0068646", "title": "The Godfather", "poster_url": "https://example.com/godfather.jpg"}
                ]
            },
            {
                "username": "film_critic",
                "movies": [
                    {"movie_id": "tt0468569", "title": "The Dark Knight", "poster_url": "https://example.com/darkknight.jpg"}
                ]
            }
        ]

        for fav in favorites_data:
            user = User.query.filter_by(username=fav["username"]).first()
            if not user:
                print(f"User {fav['username']} not found.")
                continue

            for movie in fav["movies"]:
                existing = Favorite.query.filter_by(user_id=user.id, movie_id=movie["movie_id"]).first()
                if existing:
                    print(f"Favorite for {movie['title']} already exists for {user.username}")
                    continue

                favorite = Favorite(
                    user_id=user.id,
                    movie_id=movie["movie_id"],
                    title=movie["title"],
                    poster_url=movie["poster_url"]
                )
                db.session.add(favorite)
                print(f"Added favorite '{movie['title']}' for {user.username}")

        db.session.commit()
        print("Favorites seeding complete!")

if __name__ == "__main__":
    seed_favorites()
