import os
from typing import List, Dict, Optional

from flask import Blueprint, jsonify, request

from app.core.config import LOG_DIRECTORY
from app.utils.logger import logger


logs_bp = Blueprint("logs", __name__)


def _parse_log_line(line: str) -> Dict[str, str]:
    parts = line.strip().split(" | ", 3)
    if len(parts) == 4:
        timestamp, level, name, message = parts
        return {
            "timestamp": timestamp,
            "level": level,
            "logger": name,
            "message": message,
        }

    return {
        "timestamp": "",
        "level": "INFO",
        "logger": "",
        "message": line.strip(),
    }


def _read_log_file(limit: int = 100, level: Optional[str] = None, query: Optional[str] = None) -> List[Dict[str, str]]:
    log_path = os.path.join(LOG_DIRECTORY, "python_api.log")
    if not os.path.exists(log_path):
        return []

    entries: List[Dict[str, str]] = []
    with open(log_path, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if not line.strip():
                continue
            entry = _parse_log_line(line)
            entries.append(entry)

    if level:
        entries = [entry for entry in entries if entry["level"].upper() == level.upper()]

    if query:
        query_lower = query.lower()
        entries = [
            entry
            for entry in entries
            if query_lower in entry["message"].lower()
            or query_lower in entry["logger"].lower()
        ]

    return entries[-limit:]


@logs_bp.route("/logs", methods=["GET"])
def recent_logs():
    logger.info("Received request: GET /logs")

    limit = request.args.get("limit", default=100, type=int)
    level = request.args.get("level", default=None, type=str)
    query = request.args.get("query", default=None, type=str)

    logs = _read_log_file(limit=limit, level=level, query=query)
    logs.reverse()

    return jsonify(logs), 200
