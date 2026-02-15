"""Telemetry consumers for Spec Kitty event system."""

from .jsonl_writer import JsonlEventWriter

__all__ = ["JsonlEventWriter"]
