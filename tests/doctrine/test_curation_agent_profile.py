"""
End-to-end tests verifying curation pipeline compatibility with agent-profile.

These tests confirm that:
- Import candidates targeting "agent-profile" validate against the
  import-candidate schema (no enum constraint on target_concepts).
- A resulting .agent.yaml validates against the agent-profile schema.
- An adopted candidate with empty resulting_artifacts is rejected.
- An adopted candidate with valid resulting_artifacts passes.
- A round-trip: candidate -> adapt -> validate -> adopt -> verify linkage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from doctrine.agent_profiles.profile import AgentProfile
from doctrine.agent_profiles.validation import validate_agent_profile_yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "src" / "doctrine" / "schemas"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"

IMPORT_CANDIDATE_SCHEMA = SCHEMA_DIR / "import-candidate.schema.yaml"
EXAMPLE_CANDIDATE_FIXTURE = FIXTURE_DIR / "example-agent-import-candidate.yaml"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data, dict), f"{path}: expected mapping root"
    return data


def _import_candidate_validator() -> Draft202012Validator:
    schema = _load_yaml(IMPORT_CANDIDATE_SCHEMA)
    return Draft202012Validator(schema)


def _candidate_with_status(status: str, **overrides: Any) -> dict[str, Any]:
    """Return a minimal WP03-style candidate with the given status."""
    base: dict[str, Any] = {
        "id": "imp-doctrine-ref-agent-profile-001",
        "source": {
            "title": "Agent Profile Import Example",
            "type": "internal",
            "url": "doctrine_ref/agents/",
            "accessed_on": "2026-02-22",
        },
        "classification": {
            "target_concepts": ["agent-profile"],
            "rationale": "External agent profile to import into doctrine",
        },
        "adaptation": {
            "summary": "Convert .agent.md format to .agent.yaml for schema validation",
            "notes": [
                "Map frontmatter fields to top-level YAML keys",
                "Map markdown sections to YAML structure",
            ],
        },
        "status": status,
        "source_references": [
            {
                "kind": "local",
                "path": "doctrine_ref/agents/example.agent.md",
                "lines": "1-50",
                "note": "Source agent profile definition",
            }
        ],
    }
    base.update(overrides)
    return base


def _minimal_agent_profile_data() -> dict[str, Any]:
    """Return the minimal valid agent-profile YAML dict."""
    return {
        "profile-id": "example-curator",
        "name": "Example Curator",
        "purpose": "Curate and adapt external agent profiles into doctrine",
        "specialization": {
            "primary-focus": "Doctrine curation and agent profile adaptation",
        },
    }


# ---------------------------------------------------------------------------
# Test suite
# ---------------------------------------------------------------------------


class TestImportCandidateSchemaAcceptsAgentProfile:
    """Import-candidate schema accepts 'agent-profile' as a target_concept."""

    def test_fixture_file_exists(self) -> None:
        """The example agent import candidate fixture exists on disk."""
        assert EXAMPLE_CANDIDATE_FIXTURE.exists(), (
            f"Expected fixture at {EXAMPLE_CANDIDATE_FIXTURE}"
        )

    def test_example_candidate_fixture_validates(self) -> None:
        """The on-disk example fixture validates against import-candidate schema."""
        validator = _import_candidate_validator()
        instance = _load_yaml(EXAMPLE_CANDIDATE_FIXTURE)
        errors = sorted(validator.iter_errors(instance), key=str)
        assert not errors, "\n".join(str(e) for e in errors)

    def test_agent_profile_target_concept_is_valid(self) -> None:
        """A candidate with target_concepts: ['agent-profile'] passes schema validation.

        The import-candidate schema uses a free-form string array with no enum
        constraint on target_concepts, so 'agent-profile' is inherently valid.
        """
        validator = _import_candidate_validator()
        candidate = _candidate_with_status("proposed")
        errors = sorted(validator.iter_errors(candidate), key=str)
        assert not errors, (
            "Expected 'agent-profile' to be a valid target_concept, "
            f"but got errors: {errors}"
        )

    def test_multiple_concepts_including_agent_profile_valid(self) -> None:
        """A candidate targeting multiple concepts (agent-profile + tactic) is valid."""
        validator = _import_candidate_validator()
        candidate = _candidate_with_status("proposed")
        candidate["classification"]["target_concepts"] = ["agent-profile", "tactic"]
        errors = sorted(validator.iter_errors(candidate), key=str)
        assert not errors, "\n".join(str(e) for e in errors)

    def test_empty_target_concepts_fails(self) -> None:
        """An empty target_concepts array fails (minItems: 1)."""
        validator = _import_candidate_validator()
        candidate = _candidate_with_status("proposed")
        candidate["classification"]["target_concepts"] = []
        errors = list(validator.iter_errors(candidate))
        assert errors, "Expected validation error for empty target_concepts"

    def test_candidate_reviewing_status_valid(self) -> None:
        """Status 'reviewing' is valid for WP03-format candidates."""
        validator = _import_candidate_validator()
        candidate = _candidate_with_status("reviewing")
        errors = sorted(validator.iter_errors(candidate), key=str)
        assert not errors, "\n".join(str(e) for e in errors)


class TestAdoptedCandidateResultingArtifacts:
    """Adopted import candidates must have non-empty resulting_artifacts."""

    def test_adopted_with_empty_artifacts_fails(self) -> None:
        """Adopted candidate with resulting_artifacts: [] fails schema."""
        validator = _import_candidate_validator()
        candidate = _candidate_with_status(
            "adopted",
            resulting_artifacts=[],  # empty list should fail (minItems: 1)
        )
        errors = list(validator.iter_errors(candidate))
        assert errors, (
            "Expected validation error when adopted candidate has empty resulting_artifacts"
        )

    def test_adopted_without_artifacts_key_fails(self) -> None:
        """Adopted candidate missing resulting_artifacts entirely fails schema."""
        validator = _import_candidate_validator()
        candidate = _candidate_with_status("adopted")
        # Ensure no resulting_artifacts key
        candidate.pop("resulting_artifacts", None)
        errors = list(validator.iter_errors(candidate))
        assert errors, (
            "Expected validation error when adopted candidate has no resulting_artifacts"
        )

    def test_adopted_with_valid_artifacts_passes(self) -> None:
        """Adopted candidate with at least one artifact passes schema."""
        validator = _import_candidate_validator()
        candidate = _candidate_with_status(
            "adopted",
            resulting_artifacts=["src/doctrine/agent_profiles/shipped/example-curator.agent.yaml"],
        )
        errors = sorted(validator.iter_errors(candidate), key=str)
        assert not errors, "\n".join(str(e) for e in errors)


class TestResultingAgentProfileSchemaValidation:
    """The .agent.yaml produced by curation validates against agent-profile schema."""

    def test_minimal_agent_profile_validates(self) -> None:
        """Minimal resulting agent profile passes YAML schema validation."""
        data = _minimal_agent_profile_data()
        errors = validate_agent_profile_yaml(data)
        assert errors == [], f"Expected no schema errors, got: {errors}"

    def test_full_agent_profile_validates(self) -> None:
        """Full agent profile (simulating curated output) validates via schema."""
        data: dict[str, Any] = {
            "profile-id": "example-curator",
            "name": "Example Curator",
            "purpose": "Curate and adapt external agent profiles into doctrine",
            "role": "curator",
            "routing-priority": 60,
            "max-concurrent-tasks": 3,
            "context-sources": {
                "doctrine-layers": ["curation-guidelines"],
                "directives": ["CURATION_FIRST"],
            },
            "specialization": {
                "primary-focus": "Doctrine curation and agent profile adaptation",
                "secondary-awareness": "Schema validation and YAML structure",
                "avoidance-boundary": "Code implementation",
                "success-definition": "Profiles validated and adopted into doctrine",
            },
            "collaboration": {
                "handoff-to": ["reviewer"],
                "handoff-from": ["researcher"],
                "output-artifacts": ["agent-profile-yaml"],
                "canonical-verbs": ["curate", "adapt", "validate"],
            },
            "mode-defaults": [
                {
                    "mode": "curation",
                    "description": "Adapt external agent definitions to doctrine format",
                    "use-case": "Processing import candidates targeting agent-profile",
                }
            ],
            "initialization-declaration": (
                "I am Example Curator. I adapt external agent profiles into "
                "doctrine-compliant .agent.yaml artifacts."
            ),
            "directive-references": [
                {
                    "code": "CURATION_FIRST",
                    "name": "Curation First Principle",
                    "rationale": "All external profiles must pass schema validation before adoption",
                }
            ],
        }
        errors = validate_agent_profile_yaml(data)
        assert errors == [], f"Expected no schema errors, got: {errors}"

    def test_profile_loads_via_model_validate(self) -> None:
        """Resulting profile can be loaded into AgentProfile.model_validate()."""
        data = _minimal_agent_profile_data()
        profile = AgentProfile.model_validate(data)
        assert profile.profile_id == "example-curator"
        assert profile.name == "Example Curator"
        assert profile.purpose == "Curate and adapt external agent profiles into doctrine"
        assert profile.specialization.primary_focus == "Doctrine curation and agent profile adaptation"

    def test_full_profile_model_validate_round_trip(self) -> None:
        """Full curated profile round-trips through AgentProfile model_validate."""
        data: dict[str, Any] = {
            "profile-id": "example-curator",
            "name": "Example Curator",
            "purpose": "Curate and adapt external agent profiles into doctrine",
            "role": "curator",
            "specialization": {
                "primary-focus": "Doctrine curation and agent profile adaptation",
                "avoidance-boundary": "Code implementation",
            },
            "mode-defaults": [
                {
                    "mode": "curation",
                    "description": "Adapt external agent definitions",
                    "use-case": "Processing import candidates targeting agent-profile",
                }
            ],
        }
        profile = AgentProfile.model_validate(data)
        assert profile.profile_id == "example-curator"
        assert len(profile.mode_defaults) == 1
        assert profile.mode_defaults[0].mode == "curation"
        assert profile.specialization.avoidance_boundary == "Code implementation"


class TestCurationRoundTrip:
    """End-to-end round-trip: candidate -> adapt -> validate -> adopt -> verify linkage."""

    def test_round_trip_propose_to_adopt_with_artifact_link(self) -> None:
        """Full round-trip from proposed candidate to adopted with artifact link."""
        validator = _import_candidate_validator()

        # Step 1: Create a proposed import candidate
        candidate = _candidate_with_status("proposed")
        errors = sorted(validator.iter_errors(candidate), key=str)
        assert not errors, f"Proposed candidate failed schema: {errors}"

        # Step 2: Move to reviewing
        candidate["status"] = "reviewing"
        errors = sorted(validator.iter_errors(candidate), key=str)
        assert not errors, f"Reviewing candidate failed schema: {errors}"

        # Step 3: Simulate adaptation - produce a valid .agent.yaml
        adapted_profile_data = _minimal_agent_profile_data()
        profile_errors = validate_agent_profile_yaml(adapted_profile_data)
        assert profile_errors == [], f"Adapted profile failed YAML schema: {profile_errors}"

        # Step 4: Load via AgentProfile.model_validate (confirm domain model is happy)
        profile = AgentProfile.model_validate(adapted_profile_data)
        assert profile.profile_id == "example-curator"

        # Step 5: Move to adopted with artifact link
        artifact_path = "src/doctrine/agent_profiles/shipped/example-curator.agent.yaml"
        candidate["status"] = "adopted"
        candidate["resulting_artifacts"] = [artifact_path]

        errors = sorted(validator.iter_errors(candidate), key=str)
        assert not errors, f"Adopted candidate failed schema: {errors}"

        # Step 6: Verify linkage: resulting_artifacts references the adapted profile
        assert artifact_path in candidate["resulting_artifacts"]
        assert candidate["classification"]["target_concepts"] == ["agent-profile"]
        assert candidate["status"] == "adopted"

    def test_round_trip_verify_concept_is_preserved(self) -> None:
        """target_concept 'agent-profile' is preserved through the round-trip."""
        candidate = _candidate_with_status(
            "adopted",
            resulting_artifacts=["src/doctrine/agent_profiles/shipped/example-curator.agent.yaml"],
        )
        # The target_concept should remain agent-profile through all stages
        assert candidate["classification"]["target_concepts"] == ["agent-profile"]

    def test_partial_adoption_fails_schema(self) -> None:
        """Adopted status with no resulting_artifacts is rejected at any stage."""
        validator = _import_candidate_validator()
        candidate = _candidate_with_status("adopted")
        # No resulting_artifacts added - should fail
        errors = list(validator.iter_errors(candidate))
        assert errors, (
            "Expected schema to reject adopted candidate missing resulting_artifacts"
        )
