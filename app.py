import os
from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, User

load_dotenv()

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
    JWT_ACCESS_TOKEN_EXPIRES=int(os.getenv('JWT_EXPIRES_MINUTES', 30)),
    JWT_TOKEN_LOCATION=['headers', 'cookies'],
    JWT_COOKIE_SECURE=True,
    JWT_COOKIE_CSRF_PROTECT=True
)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
api = Api(app)
CORS(app, supports_credentials=True)

from routes.favorites import favorites_bp
app.register_blueprint(favorites_bp, url_prefix='/api')

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
                'user_id': user.id,
                'username': user.username
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to create user'}, 500

class Login(Resource):
    def post(self):
        data = request.get_json()
        
        if not all(field in data for field in ['username', 'password']):
            return {'message': 'Missing credentials'}, 400

        user = User.query.filter_by(username=data['username']).first()

        if not user or not user.check_password(data['password']):
            return {'message': 'Invalid username or password'}, 401
        
        return {
            'access_token': user.generate_token(),
            'user_id': user.id,
            'username': user.username
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
            'member_since': user.created_at.strftime('%B %d, %Y')
        }, 200

api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(Profile, '/auth/profile')

@app.errorhandler(404)
def not_found(e):
    return {'message': 'Resource not found'}, 404

@app.errorhandler(500)
def server_error(e):
    return {'message': 'Internal server error'}, 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )