from flask import Blueprint, jsonify, request
from requests.exceptions import RequestException

from app.core.pipeline import AnalysisPipeline
from app.utils.logger import logger

orchestration_bp = Blueprint("orchestration", __name__, url_prefix="/pipeline")

@orchestration_bp.route("/neo/analyze", methods=["POST"])
def analyze_neo_pipeline():
    logger.info("Received request: POST /pipeline/neo/analyze")

    limit = request.args.get("limit", default=100, type=int)

    if limit < 1 or limit > 1000:
        return jsonify({"error": "limit must be between 1 and 1000"}), 400

    try:
        stats = AnalysisPipeline.analyze_unprocessed_asteroids(limit=limit)

        logger.info(f"Pipeline completed successfully: {stats}")

        return jsonify(
            {
                "status": "success",
                "statistics": stats,
            }
        ), 200

    except RuntimeError as e:
        logger.error(f"Pipeline initialization error: {e}")
        return (
            jsonify(
                {
                    "error": "Pipeline not properly initialized",
                    "details": str(e),
                }
            ),
            500,
        )

    except RequestException as e:
        logger.error(f"Rust Engine communication error: {e}")
        return (
            jsonify(
                {
                    "error": "Rust Engine unreachable",
                    "details": str(e),
                }
            ),
            503,
        )

    except Exception as e:
        logger.critical(f"Unexpected pipeline error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@orchestration_bp.route("/neo/analyze/<asteroid_id>", methods=["POST"])
def analyze_single_neo(asteroid_id: str):
    logger.info(f"Received request: POST /pipeline/neo/analyze/{asteroid_id}")

    try:
        result = AnalysisPipeline.analyze_single_asteroid(asteroid_id)

        return (
            jsonify(
                {
                    "status": "success",
                    "asteroid_id": asteroid_id,
                    "risk_analysis": result,
                }
            ),
            200,
        )

    except ValueError as e:
        logger.warning(f"Asteroid {asteroid_id} not found or invalid: {e}")
        return (
            jsonify(
                {
                    "error": "Asteroid not found or invalid",
                    "details": str(e),
                }
            ),
            404,
        )

    except RequestException as e:
        logger.error(f"Rust Engine communication error: {e}")
        return (
            jsonify(
                {
                    "error": "Rust Engine unreachable",
                    "details": str(e),
                }
            ),
            503,
        )

    except Exception as e:
        logger.critical(f"Unexpected error analyzing asteroid {asteroid_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500

@orchestration_bp.route("/status", methods=["GET"])
def pipeline_status():
    logger.info("Received request: GET /pipeline/status")

    try:
        from flask import current_app

        mongo = current_app.extensions.get("mongo")

        if not mongo:
            return (
                jsonify(
                    {
                        "status": "unhealthy",
                        "reason": "MongoDB not initialized",
                    }
                ),
                503,
            )

        mongo.get_unprocessed_asteroids(limit=1)

        return (
            jsonify(
                {
                    "status": "healthy",
                    "components": {
                        "mongodb": "connected",
                        "rust_engine": "unknown",
                    },
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Pipeline status check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 503
