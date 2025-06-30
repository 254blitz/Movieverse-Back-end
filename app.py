import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db, User
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()

def configure_logging(app):
    """Configure application logging"""
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/movieverse.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Movieverse startup')

def create_app():
    app = Flask(__name__)
    
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config.update(
        SQLALCHEMY_DATABASE_URI=database_url or 'sqlite:///app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=int(os.getenv('JWT_ACCESS_EXPIRES_MINUTES', 30))),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=int(os.getenv('JWT_REFRESH_EXPIRES_DAYS', 7))),
        JWT_TOKEN_LOCATION=['headers', 'cookies'],
        JWT_COOKIE_SECURE=os.getenv('FLASK_ENV', 'production') == 'production',
        JWT_COOKIE_SAMESITE='Lax',
        JWT_COOKIE_CSRF_PROTECT=True,
        JWT_CSRF_CHECK_FORM=True,
        PROPAGATE_EXCEPTIONS=True
    )

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    
    cors = CORS(app, 
               supports_credentials=True,
               resources={
                   r"/api/*": {
                       "origins": os.getenv('FRONTEND_URL', 'http://localhost:3000'),
                       "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                       "allow_headers": ["Content-Type", "Authorization"],
                       "expose_headers": ["X-CSRF-TOKEN"]
                   }
               })
    
    api = Api(app)
    
    register_routes(app, api)
    
    configure_logging(app)

    @app.cli.command('init-db')
    def init_db():
        """Initialize the database with test data"""
        with app.app_context():
            db.create_all()
            if not User.query.filter_by(username="testuser").first():
                test_user = User(
                    username="testuser",
                    email="test@example.com"
                )
                test_user.set_password("test123")
                db.session.add(test_user)
                db.session.commit()
                app.logger.info("Created test user: testuser / test123")

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f"Server error: {error}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    @app.route('/')
    def home():
        """Health check endpoint"""
        return jsonify({
            "status": "running",
            "message": "Movieverse API is operational",
            "version": "1.0.0",
            "environment": os.getenv('FLASK_ENV', 'development'),
            "routes": {
                "public": ["/api/movies"],
                "protected": ["/api/favorites", "/api/auth/profile"]
            }
        }), 200

    return app

def register_routes(app, api):
    """Register all routes and blueprints"""
    from routes.omdb import omdb_bp
    app.register_blueprint(omdb_bp, url_prefix='/api')
    
    from routes.favorites import favorites_bp
    app.register_blueprint(favorites_bp, url_prefix='/api')
    
    from auth_resources import register_resources
    register_resources(api)

app = create_app()

if __name__ == '__main__':
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', os.getenv('FLASK_PORT', 5000))),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )