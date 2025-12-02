import os
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_BASE_URL = "https://api.nasa.gov"

NASA_APOD_ENDPOINT = "/planetary/apod"
NASA_NEO_FEED_ENDPOINT = "/neo/rest/v1/feed"

RUST_ENGINE_URL = os.getenv("RUST_ENGINE_URL")

LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "./logs")

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

if not NASA_API_KEY:
    raise ValueError("NASA_API_KEY is not set in environment variables.")