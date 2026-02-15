"""Factory function for creating configured EventBridge instances."""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from .bridge import CompositeEventBridge, EventBridge, NullEventBridge
from specify_cli.telemetry.jsonl_writer import JsonlEventWriter

logger = logging.getLogger(__name__)

DEFAULT_LOG_PATH = ".kittify/events.jsonl"


def load_event_bridge(repo_root: Path) -> EventBridge:
    """Load EventBridge from .kittify/config.yaml telemetry settings.

    Returns NullEventBridge if telemetry is not configured or disabled.
    """
    config_path = repo_root / ".kittify" / "config.yaml"
    try:
        if not config_path.exists():
            return NullEventBridge()

        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            return NullEventBridge()

        telemetry = config.get("telemetry", {})
        if not isinstance(telemetry, dict) or not telemetry.get("enabled"):
            return NullEventBridge()

        log_path_str = telemetry.get("log_path", DEFAULT_LOG_PATH)
        log_path = repo_root / log_path_str

        writer = JsonlEventWriter(log_path)
        bridge = CompositeEventBridge()
        bridge.register(writer.handle)
        return bridge

    except Exception:
        logger.warning("Failed to load event bridge config", exc_info=True)
        return NullEventBridge()
