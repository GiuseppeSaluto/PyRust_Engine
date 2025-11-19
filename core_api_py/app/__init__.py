from flask import Flask
from flask_cors import CORS
# from pymongo import MongoClient
import logging

def create_app():
    app = Flask(__name__)
    
    from config import Config
    app.config.from_object(Config)
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["*"],  # In production, specify exact origins
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "max_age": 3600
        }
    })
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup Mongo (placeholder)
    # app.mongo_client = MongoClient(app.config['MONGO_URI'])

    # Register routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    return app
