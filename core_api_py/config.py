import os

class Config:
    # Rust service configuration
    RUST_SERVICE_URL = os.environ.get('RUST_SERVICE_URL', 'http://pricing_engine:8080')
    
    # MongoDB configuration
    MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
    MONGO_PORT = os.environ.get('MONGO_PORT', '27017')
    MONGO_DB = os.environ.get('MONGO_DB', 'pyrust_db')
    MONGO_USER = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'user')
    MONGO_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'password')
    
    # Build MongoDB URI
    MONGO_URI = os.environ.get(
        'MONGO_URI',
        f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}'
    )
