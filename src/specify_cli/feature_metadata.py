"""Compatibility alias for legacy feature_metadata imports.

The canonical implementation lives in ``mission_metadata.py``.
"""

from __future__ import annotations

import sys

from . import mission_metadata as _mission_metadata

sys.modules[__name__] = _mission_metadata
