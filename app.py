import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api()

load_dotenv()

def setup_logging(app):
    """Configure application logging"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    handler = RotatingFileHandler('logs/movieverse.log', maxBytes=10000, backupCount=3)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

def create_app():
    app = Flask(__name__)
    
    db_url = os.getenv('DATABASE_URL', 'sqlite:///instance/app.db')
    os.makedirs('instance', exist_ok=True)  
    
    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=7),
        JWT_TOKEN_LOCATION=['headers'],
        JWT_COOKIE_SECURE=os.getenv('FLASK_ENV') == 'production',
        JWT_COOKIE_CSRF_PROTECT=True
    )

    if not app.config['JWT_SECRET_KEY']:
        raise RuntimeError("JWT_SECRET_KEY must be set")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",
                "https://movieverse-frontend-8n88.onrender.com"
            ],
            "supports_credentials": True
        }
    })

    register_routes(app)
    setup_logging(app)

    @app.cli.command('init-db')
    def init_db():
        """Initialize database with test data"""
        from models.user import User
        with app.app_context():
            db.create_all()
            if not User.query.filter_by(username="testuser").first():
                user = User(username="testuser", email="test@example.com")
                user.set_password("test123")
                db.session.add(user)
                db.session.commit()
                app.logger.info("Created test user")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Resource not found"), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        app.logger.error(f"Server error: {str(e)}")
        return jsonify(error="Internal server error"), 500

    @app.route('/')
    def health_check():
        return jsonify(
            status="running",
            message="Movieverse API",
            environment=os.getenv('FLASK_ENV', 'development')
        )

    return app

def register_routes(app):
    """Register all application routes"""
    from routes.omdb import omdb_bp
    from routes.favorites import favorites_bp
    from auth_resources import register_resources
    
    app.register_blueprint(omdb_bp, url_prefix='/api')
    app.register_blueprint(favorites_bp, url_prefix='/api')
    
    register_resources(api)
    api.init_app(app)

app = create_app()

if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'false').lower() == 'true'
    )