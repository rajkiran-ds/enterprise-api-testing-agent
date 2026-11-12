"""Configuration from environment variables. No secrets in code."""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE: str = os.getenv("LOG_FILE", "logs/orchestrator.log")
MOCK_API_URL: str = os.getenv("MOCK_API_URL", "http://localhost:8001")


def setup_logging() -> None:
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")],
        force=True,
    )