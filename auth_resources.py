from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from models.user import User

def register_resources(api):
    """Register all auth resources with the given Api instance"""
    
    class Register(Resource):
        def post(self):
            data = request.get_json()
            required_fields = ['username', 'email', 'password']
            if not all(field in data for field in required_fields):
                return {'message': 'Missing required fields'}, 400

            if User.query.filter_by(username=data['username']).first():
                return {'message': 'Username already exists'}, 400

            if User.query.filter_by(email=data['email']).first():
                return {'message': 'Email already exists'}, 400
            
            try:
                user = User(
                    username=data['username'],
                    email=data['email']
                )
                user.set_password(data['password'])
                db.session.add(user)
                db.session.commit()
                return {
                    'message': 'User created successfully',
                    'user_id': user.id
                }, 201
            except Exception as e:
                db.session.rollback()
                return {'message': str(e)}, 500

    class Login(Resource):
        def post(self):
            data = request.get_json()
            if not all(field in data for field in ['username', 'password']):
                return {'message': 'Missing credentials'}, 400

            user = User.query.filter_by(username=data['username']).first()
            if not user or not user.check_password(data['password']):
                return {'message': 'Invalid username or password'}, 401
            
            access_token = create_access_token(identity=user.id)
            return {
                'access_token': access_token,
                'user_id': user.id
            }, 200

    class Profile(Resource):
        @jwt_required()
        def get(self):
            user = User.query.get(get_jwt_identity())
            if not user:
                return {'message': 'User not found'}, 404
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'member_since': user.created_at.isoformat() if user.created_at else None
            }, 200

    api.add_resource(Register, '/auth/register')
    api.add_resource(Login, '/auth/login')
    api.add_resource(Profile, '/auth/profile')