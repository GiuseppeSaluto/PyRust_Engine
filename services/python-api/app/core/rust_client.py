import requests
from typing import Dict, Any

from app.core.config import RUST_ENGINE_URL, REQUEST_TIMEOUT
from app.utils.logger import logger


def process_asteroid_with_rust(asteroid_dto: Dict[str, Any]) -> Dict[str, Any]:
    if not RUST_ENGINE_URL:
        raise ValueError("RUST_ENGINE_URL is not configured.")

    url = f"{RUST_ENGINE_URL}/api/process/asteroid"
    asteroid_id = asteroid_dto.get("id", "unknown")

    logger.info(f"Sending asteroid {asteroid_id} to Rust Engine")

    try:
        response = requests.post(url, json=asteroid_dto, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Rust Engine request failed for asteroid {asteroid_id}: {e}")
        raise

    try:
        result = response.json()
    except ValueError as e:
        logger.error(
            f"Invalid JSON response from Rust Engine for asteroid {asteroid_id}"
        )
        raise RuntimeError("Rust Engine returned invalid JSON") from e

    if "asteroid_id" not in result:
        logger.warning(
            f"Rust Engine response missing asteroid_id field: {result}"
        )

    logger.info(
        f"Received risk analysis for asteroid {result.get('asteroid_id', 'unknown')}"
    )

    return result