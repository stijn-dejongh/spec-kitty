"""Compatibility alias for legacy feature_creation imports.

The canonical implementation lives in ``mission_creation.py``.
"""

from __future__ import annotations

import sys

from . import mission_creation as _mission_creation

sys.modules[__name__] = _mission_creation
