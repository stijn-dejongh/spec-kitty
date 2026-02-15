"""JSONL file writer for structured events."""

from __future__ import annotations

import logging
from pathlib import Path

from specify_cli.core.events.models import BaseEvent

logger = logging.getLogger(__name__)


class JsonlEventWriter:
    """Appends Pydantic event models as JSONL to a file."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path

    def handle(self, event: BaseEvent) -> None:
        """Append event as single JSON line. Log warning on write failure."""
        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(event.model_dump_json() + "\n")
        except OSError as e:
            logger.warning("Failed to write event to %s: %s", self.log_path, e)
