from flask import Blueprint, jsonify, request
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