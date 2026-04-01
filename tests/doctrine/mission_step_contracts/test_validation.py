"""Schema validation tests for MissionStepContract.

Tests validate:
- Valid fixtures pass schema validation
- Invalid fixtures are rejected
- YAML round-trip idempotency (parse -> serialize -> parse produces identical result)
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator
from ruamel.yaml import YAML

from doctrine.shared.schema_utils import SchemaUtilities

pytestmark = [pytest.mark.fast, pytest.mark.doctrine]

FIXTURE_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "mission-step-contract"


class TestMissionStepContractSchemaValidation:
    """Validate YAML fixtures against the mission-step-contract schema."""

    @pytest.fixture
    def validator(self) -> Draft202012Validator:
        schema = SchemaUtilities.load_schema("mission-step-contract")
        return Draft202012Validator(schema)

    def test_valid_fixtures_pass(self, validator: Draft202012Validator) -> None:
        valid_dir = FIXTURE_DIR / "valid"
        fixture_paths = sorted(valid_dir.glob("*.yaml"))
        assert fixture_paths, "No valid fixtures found"

        for fixture_path in fixture_paths:
            with fixture_path.open() as f:
                instance = yaml.safe_load(f)
            errors = sorted(validator.iter_errors(instance), key=str)
            assert not errors, f"fixture={fixture_path.name}: " + "; ".join(e.message for e in errors)

    def test_invalid_fixtures_fail(self, validator: Draft202012Validator) -> None:
        invalid_dir = FIXTURE_DIR / "invalid"
        fixture_paths = sorted(invalid_dir.glob("*.yaml"))
        assert fixture_paths, "No invalid fixtures found"

        for fixture_path in fixture_paths:
            with fixture_path.open() as f:
                instance = yaml.safe_load(f)
            errors = sorted(validator.iter_errors(instance), key=str)
            assert errors, f"fixture={fixture_path.name}: expected validation errors but got none"


class TestMissionStepContractYamlRoundTrip:
    """YAML round-trip: parse -> serialize -> parse produces identical result."""

    @pytest.mark.parametrize(
        "fixture_name",
        ["minimal.yaml", "full-with-delegation.yaml"],
    )
    def test_yaml_round_trip_idempotency(self, fixture_name: str) -> None:
        fixture_path = FIXTURE_DIR / "valid" / fixture_name
        ryaml = YAML()
        ryaml.default_flow_style = False

        # First parse
        with fixture_path.open() as f:
            first_parse = ryaml.load(f)

        # Serialize to string
        buf = StringIO()
        ryaml.dump(first_parse, buf)
        serialized = buf.getvalue()

        # Second parse
        second_parse = ryaml.load(serialized)

        assert first_parse == second_parse, f"Round-trip mismatch for {fixture_name}"

    def test_pydantic_model_round_trip(self, full_step_contract_data: dict) -> None:
        """Pydantic model -> dict -> model produces identical result."""
        from doctrine.mission_step_contracts.models import MissionStepContract

        first = MissionStepContract.model_validate(full_step_contract_data)
        dumped = first.model_dump(by_alias=True)
        second = MissionStepContract.model_validate(dumped)
        assert first == second
