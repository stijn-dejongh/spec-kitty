"""GlossaryScope enum and scope resolution utilities."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

from ruamel.yaml import YAML

from .models import Provenance, SenseStatus, TermSense, TermSurface
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class GlossaryScope(Enum):
    """Glossary scope levels in the hierarchy."""
    MISSION_LOCAL = "mission_local"
    TEAM_DOMAIN = "team_domain"
    AUDIENCE_DOMAIN = "audience_domain"
    SPEC_KITTY_CORE = "spec_kitty_core"


# Resolution order (highest to lowest precedence)
SCOPE_RESOLUTION_ORDER: List[GlossaryScope] = [
    GlossaryScope.MISSION_LOCAL,
    GlossaryScope.TEAM_DOMAIN,
    GlossaryScope.AUDIENCE_DOMAIN,
    GlossaryScope.SPEC_KITTY_CORE,
]


def get_scope_precedence(scope: GlossaryScope) -> int:
    args = [scope]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_scope_precedence__mutmut_orig, x_get_scope_precedence__mutmut_mutants, args, kwargs, None)


def x_get_scope_precedence__mutmut_orig(scope: GlossaryScope) -> int:
    """
    Get numeric precedence for a scope (lower number = higher precedence).

    Args:
        scope: GlossaryScope enum value

    Returns:
        Precedence integer (0 = highest precedence)
    """
    try:
        return SCOPE_RESOLUTION_ORDER.index(scope)
    except ValueError:
        # Unknown scope defaults to lowest precedence
        return len(SCOPE_RESOLUTION_ORDER)


def x_get_scope_precedence__mutmut_1(scope: GlossaryScope) -> int:
    """
    Get numeric precedence for a scope (lower number = higher precedence).

    Args:
        scope: GlossaryScope enum value

    Returns:
        Precedence integer (0 = highest precedence)
    """
    try:
        return SCOPE_RESOLUTION_ORDER.index(None)
    except ValueError:
        # Unknown scope defaults to lowest precedence
        return len(SCOPE_RESOLUTION_ORDER)


def x_get_scope_precedence__mutmut_2(scope: GlossaryScope) -> int:
    """
    Get numeric precedence for a scope (lower number = higher precedence).

    Args:
        scope: GlossaryScope enum value

    Returns:
        Precedence integer (0 = highest precedence)
    """
    try:
        return SCOPE_RESOLUTION_ORDER.rindex(scope)
    except ValueError:
        # Unknown scope defaults to lowest precedence
        return len(SCOPE_RESOLUTION_ORDER)

x_get_scope_precedence__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_scope_precedence__mutmut_1': x_get_scope_precedence__mutmut_1, 
    'x_get_scope_precedence__mutmut_2': x_get_scope_precedence__mutmut_2
}
x_get_scope_precedence__mutmut_orig.__name__ = 'x_get_scope_precedence'


def should_use_scope(scope: GlossaryScope, configured_scopes: List[GlossaryScope]) -> bool:
    args = [scope, configured_scopes]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_should_use_scope__mutmut_orig, x_should_use_scope__mutmut_mutants, args, kwargs, None)


def x_should_use_scope__mutmut_orig(scope: GlossaryScope, configured_scopes: List[GlossaryScope]) -> bool:
    """
    Check if a scope should be used in resolution.

    Args:
        scope: Scope to check
        configured_scopes: List of active scopes

    Returns:
        True if scope is configured and should be used
    """
    return scope in configured_scopes


def x_should_use_scope__mutmut_1(scope: GlossaryScope, configured_scopes: List[GlossaryScope]) -> bool:
    """
    Check if a scope should be used in resolution.

    Args:
        scope: Scope to check
        configured_scopes: List of active scopes

    Returns:
        True if scope is configured and should be used
    """
    return scope not in configured_scopes

x_should_use_scope__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_should_use_scope__mutmut_1': x_should_use_scope__mutmut_1
}
x_should_use_scope__mutmut_orig.__name__ = 'x_should_use_scope'


def validate_seed_file(data: Dict[str, Any]) -> None:
    args = [data]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_validate_seed_file__mutmut_orig, x_validate_seed_file__mutmut_mutants, args, kwargs, None)


def x_validate_seed_file__mutmut_orig(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_1(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "XXtermsXX" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_2(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "TERMS" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_3(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_4(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError(None)

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_5(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("XXSeed file must have 'terms' keyXX")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_6(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_7(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("SEED FILE MUST HAVE 'TERMS' KEY")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_8(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["XXtermsXX"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_9(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["TERMS"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_10(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "XXsurfaceXX" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_11(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "SURFACE" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_12(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_13(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError(None)
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_14(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("XXTerm must have 'surface' keyXX")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_15(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_16(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("TERM MUST HAVE 'SURFACE' KEY")
        if "definition" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_17(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "XXdefinitionXX" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_18(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "DEFINITION" not in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_19(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" in term:
            raise ValueError("Term must have 'definition' key")


def x_validate_seed_file__mutmut_20(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError(None)


def x_validate_seed_file__mutmut_21(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("XXTerm must have 'definition' keyXX")


def x_validate_seed_file__mutmut_22(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("term must have 'definition' key")


def x_validate_seed_file__mutmut_23(data: Dict[str, Any]) -> None:
    """
    Validate seed file schema.

    Args:
        data: Parsed YAML data

    Raises:
        ValueError: If seed file schema is invalid
    """
    if "terms" not in data:
        raise ValueError("Seed file must have 'terms' key")

    for term in data["terms"]:
        if "surface" not in term:
            raise ValueError("Term must have 'surface' key")
        if "definition" not in term:
            raise ValueError("TERM MUST HAVE 'DEFINITION' KEY")

x_validate_seed_file__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_validate_seed_file__mutmut_1': x_validate_seed_file__mutmut_1, 
    'x_validate_seed_file__mutmut_2': x_validate_seed_file__mutmut_2, 
    'x_validate_seed_file__mutmut_3': x_validate_seed_file__mutmut_3, 
    'x_validate_seed_file__mutmut_4': x_validate_seed_file__mutmut_4, 
    'x_validate_seed_file__mutmut_5': x_validate_seed_file__mutmut_5, 
    'x_validate_seed_file__mutmut_6': x_validate_seed_file__mutmut_6, 
    'x_validate_seed_file__mutmut_7': x_validate_seed_file__mutmut_7, 
    'x_validate_seed_file__mutmut_8': x_validate_seed_file__mutmut_8, 
    'x_validate_seed_file__mutmut_9': x_validate_seed_file__mutmut_9, 
    'x_validate_seed_file__mutmut_10': x_validate_seed_file__mutmut_10, 
    'x_validate_seed_file__mutmut_11': x_validate_seed_file__mutmut_11, 
    'x_validate_seed_file__mutmut_12': x_validate_seed_file__mutmut_12, 
    'x_validate_seed_file__mutmut_13': x_validate_seed_file__mutmut_13, 
    'x_validate_seed_file__mutmut_14': x_validate_seed_file__mutmut_14, 
    'x_validate_seed_file__mutmut_15': x_validate_seed_file__mutmut_15, 
    'x_validate_seed_file__mutmut_16': x_validate_seed_file__mutmut_16, 
    'x_validate_seed_file__mutmut_17': x_validate_seed_file__mutmut_17, 
    'x_validate_seed_file__mutmut_18': x_validate_seed_file__mutmut_18, 
    'x_validate_seed_file__mutmut_19': x_validate_seed_file__mutmut_19, 
    'x_validate_seed_file__mutmut_20': x_validate_seed_file__mutmut_20, 
    'x_validate_seed_file__mutmut_21': x_validate_seed_file__mutmut_21, 
    'x_validate_seed_file__mutmut_22': x_validate_seed_file__mutmut_22, 
    'x_validate_seed_file__mutmut_23': x_validate_seed_file__mutmut_23
}
x_validate_seed_file__mutmut_orig.__name__ = 'x_validate_seed_file'


_STATUS_MAP = {
    "active": SenseStatus.ACTIVE,
    "deprecated": SenseStatus.DEPRECATED,
    "draft": SenseStatus.DRAFT,
}


def _parse_sense_status(raw: str | None) -> SenseStatus:
    args = [raw]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__parse_sense_status__mutmut_orig, x__parse_sense_status__mutmut_mutants, args, kwargs, None)


def x__parse_sense_status__mutmut_orig(raw: str | None) -> SenseStatus:
    """Map a status string to the corresponding SenseStatus enum value.

    Args:
        raw: Status string from seed file or event payload (e.g. "active",
            "deprecated", "draft"). None or unrecognised values default
            to DRAFT.

    Returns:
        Matching SenseStatus enum member.
    """
    if raw is None:
        return SenseStatus.DRAFT
    return _STATUS_MAP.get(raw, SenseStatus.DRAFT)


def x__parse_sense_status__mutmut_1(raw: str | None) -> SenseStatus:
    """Map a status string to the corresponding SenseStatus enum value.

    Args:
        raw: Status string from seed file or event payload (e.g. "active",
            "deprecated", "draft"). None or unrecognised values default
            to DRAFT.

    Returns:
        Matching SenseStatus enum member.
    """
    if raw is not None:
        return SenseStatus.DRAFT
    return _STATUS_MAP.get(raw, SenseStatus.DRAFT)


def x__parse_sense_status__mutmut_2(raw: str | None) -> SenseStatus:
    """Map a status string to the corresponding SenseStatus enum value.

    Args:
        raw: Status string from seed file or event payload (e.g. "active",
            "deprecated", "draft"). None or unrecognised values default
            to DRAFT.

    Returns:
        Matching SenseStatus enum member.
    """
    if raw is None:
        return SenseStatus.DRAFT
    return _STATUS_MAP.get(None, SenseStatus.DRAFT)


def x__parse_sense_status__mutmut_3(raw: str | None) -> SenseStatus:
    """Map a status string to the corresponding SenseStatus enum value.

    Args:
        raw: Status string from seed file or event payload (e.g. "active",
            "deprecated", "draft"). None or unrecognised values default
            to DRAFT.

    Returns:
        Matching SenseStatus enum member.
    """
    if raw is None:
        return SenseStatus.DRAFT
    return _STATUS_MAP.get(raw, None)


def x__parse_sense_status__mutmut_4(raw: str | None) -> SenseStatus:
    """Map a status string to the corresponding SenseStatus enum value.

    Args:
        raw: Status string from seed file or event payload (e.g. "active",
            "deprecated", "draft"). None or unrecognised values default
            to DRAFT.

    Returns:
        Matching SenseStatus enum member.
    """
    if raw is None:
        return SenseStatus.DRAFT
    return _STATUS_MAP.get(SenseStatus.DRAFT)


def x__parse_sense_status__mutmut_5(raw: str | None) -> SenseStatus:
    """Map a status string to the corresponding SenseStatus enum value.

    Args:
        raw: Status string from seed file or event payload (e.g. "active",
            "deprecated", "draft"). None or unrecognised values default
            to DRAFT.

    Returns:
        Matching SenseStatus enum member.
    """
    if raw is None:
        return SenseStatus.DRAFT
    return _STATUS_MAP.get(raw, )

x__parse_sense_status__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__parse_sense_status__mutmut_1': x__parse_sense_status__mutmut_1, 
    'x__parse_sense_status__mutmut_2': x__parse_sense_status__mutmut_2, 
    'x__parse_sense_status__mutmut_3': x__parse_sense_status__mutmut_3, 
    'x__parse_sense_status__mutmut_4': x__parse_sense_status__mutmut_4, 
    'x__parse_sense_status__mutmut_5': x__parse_sense_status__mutmut_5
}
x__parse_sense_status__mutmut_orig.__name__ = 'x__parse_sense_status'


def load_seed_file(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    args = [scope, repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_load_seed_file__mutmut_orig, x_load_seed_file__mutmut_mutants, args, kwargs, None)


def x_load_seed_file__mutmut_orig(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_1(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = None

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_2(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" * f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_3(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" * "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_4(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root * ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_5(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / "XX.kittifyXX" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_6(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".KITTIFY" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_7(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "XXglossariesXX" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_8(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "GLOSSARIES" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_9(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_10(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = None
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_11(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = None
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_12(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = False
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_13(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = None

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_14(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(None)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_15(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(None)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_16(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = None
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_17(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get(None, []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_18(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", None):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_19(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get([]):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_20(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", ):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_21(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("XXtermsXX", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_22(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("TERMS", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_23(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = None
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_24(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=None,
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_25(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=None,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_26(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=None,
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_27(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=None,
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_28(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=None,
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_29(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=None,
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_30(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_31(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_32(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_33(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_34(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_35(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_36(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(None),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_37(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["XXsurfaceXX"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_38(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["SURFACE"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_39(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["XXdefinitionXX"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_40(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["DEFINITION"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_41(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id=None,
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_42(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=None,
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_43(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source=None,
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_44(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_45(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_46(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_47(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="XXsystem:seed_fileXX",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_48(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="SYSTEM:SEED_FILE",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_49(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="XXseed_fileXX",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_50(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="SEED_FILE",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_51(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get(None, 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_52(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", None),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_53(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get(1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_54(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", ),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_55(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("XXconfidenceXX", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_56(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("CONFIDENCE", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_57(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 2.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_58(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(None),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_59(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get(None)),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_60(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("XXstatusXX")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_61(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("STATUS")),
        )
        senses.append(sense)

    return senses


def x_load_seed_file__mutmut_62(scope: GlossaryScope, repo_root: Path) -> List[TermSense]:
    """
    Load seed file for a scope.

    Args:
        scope: GlossaryScope to load
        repo_root: Repository root path

    Returns:
        List of TermSense objects from seed file
    """
    seed_path = repo_root / ".kittify" / "glossaries" / f"{scope.value}.yaml"

    if not seed_path.exists():
        return []  # Skip cleanly if not configured

    yaml = YAML()
    yaml.preserve_quotes = True
    data = yaml.load(seed_path)

    validate_seed_file(data)

    senses = []
    for term_data in data.get("terms", []):
        sense = TermSense(
            surface=TermSurface(term_data["surface"]),
            scope=scope.value,
            definition=term_data["definition"],
            provenance=Provenance(
                actor_id="system:seed_file",
                timestamp=datetime.now(),
                source="seed_file",
            ),
            confidence=term_data.get("confidence", 1.0),
            status=_parse_sense_status(term_data.get("status")),
        )
        senses.append(None)

    return senses

x_load_seed_file__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_load_seed_file__mutmut_1': x_load_seed_file__mutmut_1, 
    'x_load_seed_file__mutmut_2': x_load_seed_file__mutmut_2, 
    'x_load_seed_file__mutmut_3': x_load_seed_file__mutmut_3, 
    'x_load_seed_file__mutmut_4': x_load_seed_file__mutmut_4, 
    'x_load_seed_file__mutmut_5': x_load_seed_file__mutmut_5, 
    'x_load_seed_file__mutmut_6': x_load_seed_file__mutmut_6, 
    'x_load_seed_file__mutmut_7': x_load_seed_file__mutmut_7, 
    'x_load_seed_file__mutmut_8': x_load_seed_file__mutmut_8, 
    'x_load_seed_file__mutmut_9': x_load_seed_file__mutmut_9, 
    'x_load_seed_file__mutmut_10': x_load_seed_file__mutmut_10, 
    'x_load_seed_file__mutmut_11': x_load_seed_file__mutmut_11, 
    'x_load_seed_file__mutmut_12': x_load_seed_file__mutmut_12, 
    'x_load_seed_file__mutmut_13': x_load_seed_file__mutmut_13, 
    'x_load_seed_file__mutmut_14': x_load_seed_file__mutmut_14, 
    'x_load_seed_file__mutmut_15': x_load_seed_file__mutmut_15, 
    'x_load_seed_file__mutmut_16': x_load_seed_file__mutmut_16, 
    'x_load_seed_file__mutmut_17': x_load_seed_file__mutmut_17, 
    'x_load_seed_file__mutmut_18': x_load_seed_file__mutmut_18, 
    'x_load_seed_file__mutmut_19': x_load_seed_file__mutmut_19, 
    'x_load_seed_file__mutmut_20': x_load_seed_file__mutmut_20, 
    'x_load_seed_file__mutmut_21': x_load_seed_file__mutmut_21, 
    'x_load_seed_file__mutmut_22': x_load_seed_file__mutmut_22, 
    'x_load_seed_file__mutmut_23': x_load_seed_file__mutmut_23, 
    'x_load_seed_file__mutmut_24': x_load_seed_file__mutmut_24, 
    'x_load_seed_file__mutmut_25': x_load_seed_file__mutmut_25, 
    'x_load_seed_file__mutmut_26': x_load_seed_file__mutmut_26, 
    'x_load_seed_file__mutmut_27': x_load_seed_file__mutmut_27, 
    'x_load_seed_file__mutmut_28': x_load_seed_file__mutmut_28, 
    'x_load_seed_file__mutmut_29': x_load_seed_file__mutmut_29, 
    'x_load_seed_file__mutmut_30': x_load_seed_file__mutmut_30, 
    'x_load_seed_file__mutmut_31': x_load_seed_file__mutmut_31, 
    'x_load_seed_file__mutmut_32': x_load_seed_file__mutmut_32, 
    'x_load_seed_file__mutmut_33': x_load_seed_file__mutmut_33, 
    'x_load_seed_file__mutmut_34': x_load_seed_file__mutmut_34, 
    'x_load_seed_file__mutmut_35': x_load_seed_file__mutmut_35, 
    'x_load_seed_file__mutmut_36': x_load_seed_file__mutmut_36, 
    'x_load_seed_file__mutmut_37': x_load_seed_file__mutmut_37, 
    'x_load_seed_file__mutmut_38': x_load_seed_file__mutmut_38, 
    'x_load_seed_file__mutmut_39': x_load_seed_file__mutmut_39, 
    'x_load_seed_file__mutmut_40': x_load_seed_file__mutmut_40, 
    'x_load_seed_file__mutmut_41': x_load_seed_file__mutmut_41, 
    'x_load_seed_file__mutmut_42': x_load_seed_file__mutmut_42, 
    'x_load_seed_file__mutmut_43': x_load_seed_file__mutmut_43, 
    'x_load_seed_file__mutmut_44': x_load_seed_file__mutmut_44, 
    'x_load_seed_file__mutmut_45': x_load_seed_file__mutmut_45, 
    'x_load_seed_file__mutmut_46': x_load_seed_file__mutmut_46, 
    'x_load_seed_file__mutmut_47': x_load_seed_file__mutmut_47, 
    'x_load_seed_file__mutmut_48': x_load_seed_file__mutmut_48, 
    'x_load_seed_file__mutmut_49': x_load_seed_file__mutmut_49, 
    'x_load_seed_file__mutmut_50': x_load_seed_file__mutmut_50, 
    'x_load_seed_file__mutmut_51': x_load_seed_file__mutmut_51, 
    'x_load_seed_file__mutmut_52': x_load_seed_file__mutmut_52, 
    'x_load_seed_file__mutmut_53': x_load_seed_file__mutmut_53, 
    'x_load_seed_file__mutmut_54': x_load_seed_file__mutmut_54, 
    'x_load_seed_file__mutmut_55': x_load_seed_file__mutmut_55, 
    'x_load_seed_file__mutmut_56': x_load_seed_file__mutmut_56, 
    'x_load_seed_file__mutmut_57': x_load_seed_file__mutmut_57, 
    'x_load_seed_file__mutmut_58': x_load_seed_file__mutmut_58, 
    'x_load_seed_file__mutmut_59': x_load_seed_file__mutmut_59, 
    'x_load_seed_file__mutmut_60': x_load_seed_file__mutmut_60, 
    'x_load_seed_file__mutmut_61': x_load_seed_file__mutmut_61, 
    'x_load_seed_file__mutmut_62': x_load_seed_file__mutmut_62
}
x_load_seed_file__mutmut_orig.__name__ = 'x_load_seed_file'


def activate_scope(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    args = [scope, version_id, mission_id, run_id, repo_root]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_activate_scope__mutmut_orig, x_activate_scope__mutmut_mutants, args, kwargs, None)


def x_activate_scope__mutmut_orig(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=scope.value,
        glossary_version_id=version_id,
        mission_id=mission_id,
        run_id=run_id,
        repo_root=repo_root,
    )


def x_activate_scope__mutmut_1(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=None,
        glossary_version_id=version_id,
        mission_id=mission_id,
        run_id=run_id,
        repo_root=repo_root,
    )


def x_activate_scope__mutmut_2(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=scope.value,
        glossary_version_id=None,
        mission_id=mission_id,
        run_id=run_id,
        repo_root=repo_root,
    )


def x_activate_scope__mutmut_3(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=scope.value,
        glossary_version_id=version_id,
        mission_id=None,
        run_id=run_id,
        repo_root=repo_root,
    )


def x_activate_scope__mutmut_4(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=scope.value,
        glossary_version_id=version_id,
        mission_id=mission_id,
        run_id=None,
        repo_root=repo_root,
    )


def x_activate_scope__mutmut_5(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=scope.value,
        glossary_version_id=version_id,
        mission_id=mission_id,
        run_id=run_id,
        repo_root=None,
    )


def x_activate_scope__mutmut_6(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        glossary_version_id=version_id,
        mission_id=mission_id,
        run_id=run_id,
        repo_root=repo_root,
    )


def x_activate_scope__mutmut_7(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=scope.value,
        mission_id=mission_id,
        run_id=run_id,
        repo_root=repo_root,
    )


def x_activate_scope__mutmut_8(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=scope.value,
        glossary_version_id=version_id,
        run_id=run_id,
        repo_root=repo_root,
    )


def x_activate_scope__mutmut_9(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=scope.value,
        glossary_version_id=version_id,
        mission_id=mission_id,
        repo_root=repo_root,
    )


def x_activate_scope__mutmut_10(
    scope: GlossaryScope,
    version_id: str,
    mission_id: str,
    run_id: str,
    repo_root: Path | None = None,
) -> None:
    """
    Activate a glossary scope and emit GlossaryScopeActivated event.

    Args:
        scope: Scope to activate
        version_id: Glossary version ID
        mission_id: Mission ID
        run_id: Run ID
        repo_root: Repository root for event log persistence. If None,
            events are logged but not persisted to disk.
    """
    from .events import emit_scope_activated

    emit_scope_activated(
        scope_id=scope.value,
        glossary_version_id=version_id,
        mission_id=mission_id,
        run_id=run_id,
        )

x_activate_scope__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_activate_scope__mutmut_1': x_activate_scope__mutmut_1, 
    'x_activate_scope__mutmut_2': x_activate_scope__mutmut_2, 
    'x_activate_scope__mutmut_3': x_activate_scope__mutmut_3, 
    'x_activate_scope__mutmut_4': x_activate_scope__mutmut_4, 
    'x_activate_scope__mutmut_5': x_activate_scope__mutmut_5, 
    'x_activate_scope__mutmut_6': x_activate_scope__mutmut_6, 
    'x_activate_scope__mutmut_7': x_activate_scope__mutmut_7, 
    'x_activate_scope__mutmut_8': x_activate_scope__mutmut_8, 
    'x_activate_scope__mutmut_9': x_activate_scope__mutmut_9, 
    'x_activate_scope__mutmut_10': x_activate_scope__mutmut_10
}
x_activate_scope__mutmut_orig.__name__ = 'x_activate_scope'
