"""Lattice-level configuration access.

Reads `lattices/<name>/config.yaml` once per process and exposes its
fields as a typed dataclass. Used by call sites that need
lattice-scoped settings — currently `label_prefix` (the prefix on
human-readable document labels: "ASN" for xanadu, "MAT" for materials)
and `default_campaign`.

A separate concern from the substrate session: many code paths build
labels, paths, and prompts without holding a Session. Those use the
module-level `lattice_config()` accessor. Sessions opened via
`open_session()` carry the same config on `session.config` so
session-aware code can reach it without a second module import.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


DEFAULT_LABEL_PREFIX = "ASN"


@dataclass(frozen=True)
class LatticeConfig:
    label_prefix: str = DEFAULT_LABEL_PREFIX
    default_campaign: Optional[str] = None


def load_lattice_config(path: Path) -> LatticeConfig:
    """Read a lattice config.yaml into a LatticeConfig.

    Missing file → defaults. Missing fields → field defaults.
    """
    try:
        raw = yaml.safe_load(path.read_text()) or {}
    except FileNotFoundError:
        raw = {}
    return LatticeConfig(
        label_prefix=raw.get("label_prefix", DEFAULT_LABEL_PREFIX),
        default_campaign=raw.get("default_campaign"),
    )


@functools.lru_cache(maxsize=None)
def _cached_for(path: Path) -> LatticeConfig:
    return load_lattice_config(path)


def lattice_config() -> LatticeConfig:
    """The active lattice's config, loaded once per process.

    Resolves the active lattice via lib.shared.paths.LATTICE_CONFIG, which
    is itself driven by the LATTICE env var.
    """
    from lib.shared.paths import LATTICE_CONFIG
    return _cached_for(LATTICE_CONFIG)
