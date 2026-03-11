"""YAML schema validation utilities for styleguides."""

from functools import lru_cache
from pathlib import Path
from typing import Any

import jsonschema  # type: ignore[import-untyped]
from importlib.resources import files
from ruamel.yaml import YAML


@lru_cache(maxsize=1)
def _load_styleguide_schema() -> dict[str, Any]:
    """Load the styleguide JSON schema (cached)."""
    try:
        resource = files("doctrine.schemas")
        if hasattr(resource, "joinpath"):
            schema_path = Path(str(resource.joinpath("styleguide.schema.yaml")))
        else:
            schema_path = Path(str(resource)) / "styleguide.schema.yaml"
    except Exception:
        schema_path = (
            Path(__file__).parent.parent / "schemas" / "styleguide.schema.yaml"
        )

    yaml = YAML(typ="safe")
    with schema_path.open() as f:
        schema_data: dict[str, Any] = yaml.load(f)

    return schema_data


def validate_styleguide(data: dict[str, Any]) -> list[str]:
    """Validate a dict against the styleguide YAML schema.

    Args:
        data: Dictionary loaded from styleguide YAML file.

    Returns:
        List of validation error messages (empty if valid).
    """
    schema = _load_styleguide_schema()
    validator = jsonschema.Draft202012Validator(schema)

    errors: list[str] = []
    for error in validator.iter_errors(data):
        field_path = (
            ".".join(str(p) for p in error.path) if error.path else "root"
        )
        errors.append(f"{field_path}: {error.message}")

    return errors
