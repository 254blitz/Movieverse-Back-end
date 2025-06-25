from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
# from flask_limiter import Limiter
# from flask_limiter.util get_remote_address
import os
from models import User
from flask import request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', '')
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

jwt = JWTManager(app)
api = Api(app)
CORS(app)

class Register(Resource):
    def post(self):
        data = request.get_json()

        if User.query.filter_by(username = data.get('username')).first():
            return {'messsage' : 'Username already exists'}, 400

        if User.query.filter_by(email = data.get('email')).first(): 
            return {'message' : 'Email already exists'}, 400
        
        user = User(
            username = data['username'],
            email = data['email']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return {'message' : 'User created successfully'}
    
class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by( username = data.get('username')).first()

        if not user or not user.check_password(data.get('password')):
            return {'message' : 'Invalid Username or password'}, 401
        
        token = user.generate_token()
        return {'access_token' : token}, 200

