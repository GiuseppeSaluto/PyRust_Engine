from flask import Blueprint, jsonify, request
from requests.exceptions import RequestException

from app.core.rust_client import process_data_with_rust_engine
from app.utils.logger import logger

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")


@analysis_bp.route("/asteroids/feed", methods=["POST"])
def analyze_asteroid_feed():
    logger.info("Received request: POST /analysis/asteroids/feed")

    # Parse raw NASA data
    try:
        nasa_data = request.get_json()
    except Exception as e:
        logger.error(f"Invalid JSON body: {e}")
        return jsonify({"error": "Invalid JSON payload"}), 400

    if not nasa_data:
        logger.warning("Empty JSON payload received for asteroid feed analysis")
        return jsonify({"error": "Request body must not be empty"}), 400

    # Send data to Rust engine
    logger.info("Sending NASA NEO feed data to Rust Engine for analysis")

    try:
        rust_result = process_data_with_rust_engine(
            data=nasa_data,
            endpoint="/analysis/asteroids/feed"
        )

        logger.info("Rust Engine returned asteroid feed analysis successfully")
        return jsonify(rust_result), 200

    except ValueError as e:
        logger.critical(f"Misconfiguration in Rust engine: {e}")
        return jsonify({"error": "Rust Engine configuration error"}), 500

    except RequestException as e:
        logger.error(f"Rust Engine connection error: {e}")
        return jsonify({
            "error": "Failed to communicate with Rust Engine",
            "details": str(e)
        }), 503

    except Exception as e:
        logger.critical(f"Unexpected error in asteroid feed analysis: {e}")
        return jsonify({"error": "Internal server error"}), 500
