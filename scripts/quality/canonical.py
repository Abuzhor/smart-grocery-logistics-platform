"""Canonical lists and normalization helpers for quality gates and planning."""
from __future__ import annotations

import re
from typing import Dict, Iterable, Optional, Tuple


PHASES = [
    "PHASE 0",
    "PHASE 1",
    "PHASE 2",
    "PHASE 3",
    "PHASE 4",
]

DOMAINS = [
    "Catalog",
    "Inventory",
    "Ordering",
    "Fulfillment",
    "Routing",
    "Partner",
    "Workforce",
    "Operations",
    "Compliance",
    "Platform",
]

PRIORITIES = [
    "Critical",
    "High",
    "Medium",
    "Low",
]


_DOMAIN_ALIAS: Dict[str, str] = {
    "fulfilment": "Fulfillment",
    "ops": "Operations",
}

_PRIORITY_ALIAS: Dict[str, str] = {}


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def _normalize_compact(value: str) -> str:
    cleaned = _normalize_text(value).casefold()
    cleaned = cleaned.replace("_", " ").replace("-", " ")
    cleaned = " ".join(cleaned.split())
    return cleaned.replace(" ", "")


def normalize_phase(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    text = _normalize_text(str(value))
    compact = _normalize_compact(text)

    match = re.match(r"^phase([0-4])", compact)
    if match:
        return f"PHASE {match.group(1)}"

    for canonical in PHASES:
        if canonical.casefold() == text.casefold():
            return canonical

    return None


def _build_normalized_map(values: Iterable[str]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for canonical in values:
        mapping[_normalize_compact(canonical)] = canonical
    return mapping


_DOMAIN_MAP = _build_normalized_map(DOMAINS)
_PRIORITY_MAP = _build_normalized_map(PRIORITIES)


def normalize_domain(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = _normalize_text(str(value))
    folded = text.casefold()

    if folded in _DOMAIN_ALIAS:
        return _DOMAIN_ALIAS[folded]

    compact = _normalize_compact(text)
    if compact in _DOMAIN_MAP:
        return _DOMAIN_MAP[compact]

    return None


def normalize_priority(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = _normalize_text(str(value))
    folded = text.casefold()

    if folded in _PRIORITY_ALIAS:
        return _PRIORITY_ALIAS[folded]

    compact = _normalize_compact(text)
    if compact in _PRIORITY_MAP:
        return _PRIORITY_MAP[compact]

    return None


def canonical_sets() -> Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...]]:
    return tuple(PHASES), tuple(DOMAINS), tuple(PRIORITIES)


def all_canonical_values() -> Iterable[str]:
    return list(PHASES) + list(DOMAINS) + list(PRIORITIES)
