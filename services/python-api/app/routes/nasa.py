from flask import Blueprint, jsonify, request, current_app
from requests.exceptions import RequestException

from app.core.nasa_client import get_neo_feed
from app.utils.logger import logger

nasa_bp = Blueprint("nasa", __name__, url_prefix="/nasa")


@nasa_bp.route("/neo/feed", methods=["GET"])
def neo_feed():
    logger.info("Received request: GET /nasa/neo/feed")

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    try:
        data = get_neo_feed(start_date=start_date, end_date=end_date)

        logger.info("Returning response for /nasa/neo/feed")
        return jsonify(data), 200

    except RequestException as e:
        logger.error(f"NASA API network error: {e}")
        return (
            jsonify({"error": "Failed to connect to NASA API", "details": str(e)}),
            503,
        )

    except Exception as e:
        logger.critical(f"Unexpected error in /nasa/neo/feed: {e}")
        return jsonify({"error": "Internal server error"}), 500


@nasa_bp.route("/neo/save", methods=["POST"])
def save_neo_data():
    logger.info("Received request: POST /nasa/neo/save")

    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        feed = get_neo_feed(start_date=start_date, end_date=end_date)
        if not feed or "near_earth_objects" not in feed:
            logger.error("Invalid feed received from NASA API")
            return jsonify({"error": "Invalid feed from NASA"}), 502

        mongo = current_app.extensions.get("mongo")
        if not mongo:
            raise RuntimeError("Mongo extension not initialized.")

        total_saved = 0

        for date_str, asteroids in feed["near_earth_objects"].items():
            for asteroid in asteroids:
                mongo.save_raw_asteroid(date_str, asteroid)
                total_saved += 1

        logger.info(f"Saved {total_saved} asteroids into MongoDB")

        return jsonify({
            "status": "success",
            "stored_documents": total_saved
        }), 200

    except RequestException as e:
        logger.error(f"NASA API request failed: {e}")
        return jsonify({"error": "NASA API unreachable"}), 503

    except Exception as e:
        logger.critical(f"Unexpected error in /nasa/neo/save: {e}")
        return jsonify({"error": "Internal server error"}), 500
