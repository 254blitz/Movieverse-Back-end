import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config.update(
        SQLALCHEMY_DATABASE_URI=database_url or 'sqlite:///app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'your-secret-key-here'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=int(os.getenv('JWT_EXPIRES_MINUTES', 30))),
        JWT_TOKEN_LOCATION=['headers', 'cookies'],
        JWT_COOKIE_SECURE=os.getenv('FLASK_ENV', 'production') == 'production',
        JWT_COOKIE_CSRF_PROTECT=True
    )

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    cors = CORS(app, supports_credentials=True)
    
    api = Api(app)

    from routes.favorites import favorites_bp
    from routes.omdb import omdb_bp
    app.register_blueprint(favorites_bp, url_prefix='/api')
    app.register_blueprint(omdb_bp, url_prefix='/api')

    from auth_resources import register_resources
    register_resources(api)  

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return "Movieverse API is running", 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', os.getenv('FLASK_PORT', 5000))),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )