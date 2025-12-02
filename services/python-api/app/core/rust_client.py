import requests
from typing import Dict, Any

from app.core.config import (
    RUST_ENGINE_URL,
    REQUEST_TIMEOUT,
)

from app.utils.logger import logger

def process_data_with_rust_engine(data: Dict[str, Any], endpoint: str = "/process") -> Dict[str, Any]:
    if not RUST_ENGINE_URL:
        raise ValueError("RUST_ENGINE_URL is not configured.")

    url = f"{RUST_ENGINE_URL}{endpoint}"

    logger.info(f"Sending data to Rust Engine at {url}")

    try:
        response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error communicating with Rust Engine: {e}")
        raise

    logger.info("Received response from Rust Engine")

    return response.json()