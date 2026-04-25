"""
Finding dataclass — standard format for pipeline findings.

Used across rebase, dependency-check, and discovery pipelines.
"""

from dataclasses import dataclass


@dataclass
class Finding:
    category: str   # "stale-label", "missing-dep", "undeclared-asn", "prose-only", etc.
    label: str
    source_asn: int | None
    location: str   # e.g., "deps:GlobalUniqueness" or "prose"
    detail: str
