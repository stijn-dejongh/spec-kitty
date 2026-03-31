"""Compatibility alias for the legacy mission command module path."""

from __future__ import annotations

import sys

from . import mission_type as _mission_type

sys.modules[__name__] = _mission_type
