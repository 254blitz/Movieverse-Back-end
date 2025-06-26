from app import app, db
from models import User
from datetime import datetime, timezone

def seed_users():
    with app.app_context():
        print("🌱 Seeding test users...")
        
        db.create_all()
        
        test_users = [
            {"username": "movie_fan", "email": "fan@movieverse.com", "password": "Password123!"},
            {"username": "film_critic", "email": "critic@movieverse.com", "password": "Reviewer456@"},
            {"username": "cinema_lover", "email": "lover@movieverse.com", "password": "ILoveMovies789"}
        ]

        for user_data in test_users:
            try:
                if User.query.filter_by(username=user_data["username"]).first():
                    print(f" User {user_data['username']} already exists")
                    continue
                    
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    created_at=datetime.now(timezone.utc)
                )
                user.set_password(user_data["password"])
                db.session.add(user)
                print(f" Created user: {user_data['username']}")
            except Exception as e:
                print(f" Error creating user {user_data['username']}: {str(e)}")
                db.session.rollback()

        db.session.commit()
        print(" User seeding complete!")

if __name__ == "__main__":
    seed_users()