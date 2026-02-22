"""Glossary alignment tests for shipped agent profile controlled vocabularies."""

from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML


REPO_ROOT = Path(__file__).resolve().parents[2]
SHIPPED_PROFILES_DIR = REPO_ROOT / "src" / "doctrine" / "agent_profiles" / "shipped"
GLOSSARY_CONTEXTS_DIR = REPO_ROOT / "glossary" / "contexts"
CONTEXTIVE_CONTEXTS_DIR = REPO_ROOT / ".kittify" / "memory" / "contexts"
CONTEXTIVE_INDEX = REPO_ROOT / ".kittify" / "memory" / "spec-kitty.glossary.yml"

FIELD_MARKDOWN_SOURCES: dict[str, tuple[Path, ...]] = {
    "domain-keywords": (GLOSSARY_CONTEXTS_DIR / "identity.md",),
    "writing-style": (GLOSSARY_CONTEXTS_DIR / "identity.md",),
    "canonical-verbs": (GLOSSARY_CONTEXTS_DIR / "identity.md",),
    "operating-procedures": (GLOSSARY_CONTEXTS_DIR / "identity.md",),
    "output-artifacts": (GLOSSARY_CONTEXTS_DIR / "identity.md",),
}

FIELD_CONTEXTIVE_SOURCES: dict[str, tuple[Path, ...]] = {
    "domain-keywords": (CONTEXTIVE_CONTEXTS_DIR / "identity.glossary.yml",),
    "writing-style": (CONTEXTIVE_CONTEXTS_DIR / "identity.glossary.yml",),
    "canonical-verbs": (CONTEXTIVE_CONTEXTS_DIR / "identity.glossary.yml",),
    "operating-procedures": (
        CONTEXTIVE_CONTEXTS_DIR / "identity.glossary.yml",
        CONTEXTIVE_CONTEXTS_DIR / "doctrine-artifacts.glossary.yml",
    ),
    "output-artifacts": (CONTEXTIVE_CONTEXTS_DIR / "identity.glossary.yml",),
}


def _load_yaml(path: Path) -> dict:
    yaml = YAML(typ="safe")
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.load(handle) or {}
    assert isinstance(payload, dict), f"Expected mapping root in {path}"
    return payload


def _collect_shipped_profile_vocab() -> dict[str, set[str]]:
    """Collect controlled-vocabulary values from shipped agent profiles."""
    vocab: dict[str, set[str]] = {
        "domain-keywords": set(),
        "writing-style": set(),
        "canonical-verbs": set(),
        "operating-procedures": set(),
        "output-artifacts": set(),
    }

    for profile_file in sorted(SHIPPED_PROFILES_DIR.glob("*.agent.yaml")):
        profile = _load_yaml(profile_file)
        specialization_context = profile.get("specialization-context") or {}
        collaboration = profile.get("collaboration") or {}

        assert isinstance(specialization_context, dict), (
            f"Expected specialization-context mapping in {profile_file}"
        )
        assert isinstance(collaboration, dict), (
            f"Expected collaboration mapping in {profile_file}"
        )

        for field in ("domain-keywords", "writing-style"):
            for value in specialization_context.get(field, []) or []:
                text = str(value).strip()
                if text:
                    vocab[field].add(text)

        for field in ("canonical-verbs", "operating-procedures", "output-artifacts"):
            for value in collaboration.get(field, []) or []:
                text = str(value).strip()
                if text:
                    vocab[field].add(text)

    return vocab


def _contains_value(haystack: str, value: str) -> bool:
    """Lenient containment for hyphen/space equivalent vocabulary values."""
    lowered = haystack.lower()
    source = value.strip().lower()
    candidates = {
        source,
        source.replace("-", " "),
        source.replace(" ", "-"),
        source.replace("_", "-"),
    }
    return any(candidate and candidate in lowered for candidate in candidates)


def _assert_vocab_present(
    vocab: dict[str, set[str]],
    field_sources: dict[str, tuple[Path, ...]],
    source_label: str,
) -> None:
    missing: list[str] = []

    for field, values in vocab.items():
        assert field in field_sources, f"No source mapping configured for field '{field}'"
        sources = field_sources[field]
        assert sources, f"Empty source mapping for field '{field}'"

        for source in sources:
            assert source.exists(), f"Missing expected {source_label} source: {source}"

        merged_text = "\n".join(
            source.read_text(encoding="utf-8") for source in sources
        )

        for value in sorted(values):
            if not _contains_value(merged_text, value):
                missing.append(
                    f"field={field} value={value!r} sources={[str(source) for source in sources]}"
                )

    assert missing == [], (
        f"Missing shipped profile vocabulary in {source_label}:\n"
        + "\n".join(f"  - {entry}" for entry in missing)
    )


def test_shipped_profile_vocab_documented_in_glossary_markdown() -> None:
    """Controlled profile vocab must be documented in glossary markdown SSOT."""
    vocab = _collect_shipped_profile_vocab()
    _assert_vocab_present(vocab, FIELD_MARKDOWN_SOURCES, "glossary markdown")


def test_shipped_profile_vocab_included_in_contextive_glossary_outputs() -> None:
    """Controlled profile vocab must be present in compiled Contextive YAML outputs."""
    vocab = _collect_shipped_profile_vocab()
    _assert_vocab_present(vocab, FIELD_CONTEXTIVE_SOURCES, "Contextive glossary outputs")


def test_contextive_index_includes_profile_vocab_contexts() -> None:
    """Contextive root index must include contexts carrying profile vocab terms."""
    index = _load_yaml(CONTEXTIVE_INDEX)
    imports = index.get("imports", [])

    assert isinstance(imports, list), f"Expected 'imports' list in {CONTEXTIVE_INDEX}"

    required_suffixes = {
        "contexts/identity.glossary.yml",
        "contexts/doctrine-artifacts.glossary.yml",
    }
    missing = [
        suffix
        for suffix in sorted(required_suffixes)
        if not any(str(item).endswith(suffix) for item in imports)
    ]

    assert missing == [], (
        "Missing required Contextive imports for profile vocabulary contexts:\n"
        + "\n".join(f"  - {suffix}" for suffix in missing)
    )
