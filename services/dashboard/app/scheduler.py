import asyncio
import logging

from app.client.api_client import run_pipeline

logger = logging.getLogger(__name__)


class PipelineScheduler:
    def __init__(self, interval_seconds: int = 300):
        self.interval = interval_seconds
        self._task = None

    async def start(self):
        logger.info("Pipeline scheduler started")
        while True:
            try:
                logger.info("Running scheduled pipeline")
                run_pipeline(limit=100)
            except Exception as e:
                logger.error(f"Scheduled pipeline failed: {e}")

            await asyncio.sleep(self.interval)

    def run_background(self):
        self._task = asyncio.create_task(self.start())
