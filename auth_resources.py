from flask import request, db
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from models.user import User
from models.favorite import Favorite
from datetime import timedelta
import logging

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            return {"message": "Username, email and password required"}, 400

        if User.query.filter_by(username=data['username']).first():
            return {"message": "Username already exists"}, 409

        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email already exists"}, 409

        try:
            user = User(
                username=data['username'],
                email=data['email']
            )
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()

            logging.info(f"New user registered: {user.username}")
            
            return {
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {str(e)}")
            return {"message": "Failed to create user"}, 500

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"message": "Username and password required"}, 400

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        try:
            access_token = user.generate_token()
            
            logging.info(f"User logged in: {user.username}")
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, 200
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            return {"message": "Login failed"}, 500

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return {"message": "User not found"}, 404
            
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat()
            }
        }, 200

def register_resources(api):
    api.add_resource(UserRegistration, '/auth/register')
    api.add_resource(UserLogin, '/auth/login')
    api.add_resource(UserProfile, '/auth/profile')