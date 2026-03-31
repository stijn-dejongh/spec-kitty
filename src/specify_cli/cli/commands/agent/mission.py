"""Compatibility alias for the legacy agent mission module path.

The canonical implementation lives in ``mission_run.py``. This module exists
solely so older imports patch the same module object rather than a copy.
"""

from __future__ import annotations

import sys

from . import mission_run as _mission_run

sys.modules[__name__] = _mission_run
