from flask import Flask, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os

from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')
app.json.compact = False


db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)

api = Api(app, prefix="/api")

class Register(Resource):
    def post(self):
        data = request.get_json()

        if User.query.filter_by(username=data.get('username')).first():
            return {'message': 'Username already exists'}, 400

        if User.query.filter_by(email=data.get('email')).first():
            return {'message': 'Email already exists'}, 400

        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()

        if not user or not user.check_password(data.get('password')):
            return {'message': 'Invalid username or password'}, 401

        return {'access_token': user.generate_token()}, 200

class Profile(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get(get_jwt_identity())
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }, 200

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Profile, '/profile')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
