import threading
from flask import Flask
from app.core.mongodb import MongoDBClient
from app.core.config import DEBUG, MONGO_URI, MONGO_DB_NAME
from app.core.nasa_client import get_neo_feed
from app.routes.nasa import nasa_bp
from app.routes.analysis import analysis_bp
from app.routes.orchestration import orchestration_bp
from app.utils.logger import logger


def _seed_asteroids_on_startup(app: Flask) -> None:
    """Fetch NASA NEO data and save to MongoDB if the collection is empty."""
    with app.app_context():
        try:
            mongo = app.extensions.get("mongo")
            if not mongo:
                logger.warning("Startup seed skipped: MongoDB not ready")
                return

            # Only fetch if the collection is empty — avoids duplicate work on restarts
            count = mongo.count_raw_asteroids()
            if count > 0:
                logger.info(f"Startup seed skipped: {count} asteroids already in DB")
                return

            logger.info("Startup seed: fetching NEO data from NASA...")
            feed = get_neo_feed()

            if not feed or "near_earth_objects" not in feed:
                logger.error("Startup seed failed: invalid response from NASA API")
                return

            total_saved = 0
            for date_str, asteroids in feed["near_earth_objects"].items():
                for asteroid in asteroids:
                    mongo.save_raw_asteroid(date_str, asteroid)
                    total_saved += 1

            logger.info(f"Startup seed complete: {total_saved} asteroids saved to MongoDB")

        except Exception as e:
            logger.error(f"Startup seed failed: {e}")


def create_app():
    app = Flask(__name__)

    mongo = MongoDBClient(MONGO_URI, MONGO_DB_NAME)
    mongo.init_app(app)

    app.register_blueprint(nasa_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(orchestration_bp)

    # Run the seed in a background thread so Flask starts immediately
    # and the seed doesn't block the first request
    seed_thread = threading.Thread(
        target=_seed_asteroids_on_startup,
        args=(app,),
        daemon=True,
        name="startup-seed",
    )
    seed_thread.start()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=DEBUG)