import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError
from flask import current_app

from app.utils.logger import logger


class MongoDBClient:

    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name

        self.client: MongoClient | None = None
        self.db: Database | None = None

    # -------------------------------------------------------------------------
    # Flask integration
    # -------------------------------------------------------------------------
    def init_app(self, app):

        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=3000)
            self.db = self.client[self.db_name]

            logger.info(f"Connected to MongoDB at {self.uri}, using DB '{self.db_name}'")

            self._ensure_collections()

            # Make this instance accessible via current_app.extensions
            if not hasattr(app, 'extensions'):
                app.extensions = {}
            app.extensions["mongo"] = self

        except PyMongoError as e:
            logger.critical(f"Failed to initialize MongoDB: {e}")
            raise

    # -------------------------------------------------------------------------
    # Database Validation
    # -------------------------------------------------------------------------
    def _ensure_collections(self):

        if self.db is None:
            raise RuntimeError("Database not initialized. Call init_app() first.")
        
        required_collections = {
            "nasa_feeds": self._init_nasa_feeds,
            "asteroid_analyses": self._init_asteroid_analyses,
        }

        existing = self.db.list_collection_names()

        for name, initializer in required_collections.items():
            if name not in existing:
                self.db.create_collection(name)
                logger.info(f"Created MongoDB collection '{name}'")
            initializer()

    def _init_nasa_feeds(self):
       
        if self.db is None:
            raise RuntimeError("Database not initialized")
            
        collection = self.db["nasa_feeds"]

        collection.create_index("retrieved_at")
        collection.create_index("feed_start_date")
        collection.create_index("feed_end_date")

        logger.debug("Initialized indexes for 'nasa_feeds'")

    def _init_asteroid_analyses(self):
        
        if self.db is None:
            raise RuntimeError("Database not initialized")
            
        collection = self.db["asteroid_analyses"]

        collection.create_index("neo_reference_id")
        collection.create_index("analysis_timestamp")

        logger.debug("Initialized indexes for 'asteroid_analyses'")

    # -------------------------------------------------------------------------
    # CRUD Operations
    # -------------------------------------------------------------------------
    def save_nasa_feed(self, feed: dict):
        
        if self.db is None:
            raise RuntimeError("Database not initialized. Call init_app() first.")
            
        try:
            collection = self.db["nasa_feeds"]
            result = collection.insert_one(feed)
            logger.info(f"Inserted NASA feed with id {result.inserted_id}")
            return result.inserted_id

        except PyMongoError as e:
            logger.error(f"Failed to save NASA feed: {e}")
            raise

    def close(self):
        
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")