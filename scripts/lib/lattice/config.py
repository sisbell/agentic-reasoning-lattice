"""Lattice-level configuration access.

Lattice config (label_prefix, default_campaign) lives in the active
lattice's substrate doc frontmatter — `_docuverse/documents/<node>/
<user>/lattice/<lattice-name>.md` carries:

    ---
    label_prefix: ASN
    default_campaign: xanadu-protocol
    ---

A separate concern from the substrate session: many code paths build
labels, paths, and prompts without holding a Session. Those use the
module-level `lattice_config()` accessor. Sessions opened via
`open_session()` carry the same config on `session.config` so
session-aware code can reach it without a second module import.

Three primitives:

  config_from_dict(raw)        — structural dict → LatticeConfig.
                                 Pure mapping; useful for tests.
  config_from_doc(doc_path)    — read lattice doc frontmatter at the
                                 given path; raise if missing.
  lattice_config()             — accessor for the active lattice;
                                 cached per process.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


DEFAULT_LABEL_PREFIX = "ASN"


@dataclass(frozen=True)
class LatticeConfig:
    label_prefix: str = DEFAULT_LABEL_PREFIX
    default_campaign: Optional[str] = None


def config_from_dict(raw: dict) -> LatticeConfig:
    """Map a raw frontmatter dict to a LatticeConfig."""
    return LatticeConfig(
        label_prefix=raw.get("label_prefix", DEFAULT_LABEL_PREFIX),
        default_campaign=raw.get("default_campaign"),
    )


def config_from_doc(lattice_doc_path: Path) -> LatticeConfig:
    """Load a LatticeConfig from a specific lattice doc's frontmatter.

    Raises `FileNotFoundError` if the doc doesn't exist. No fallback
    — a missing lattice doc is a configuration error, not a
    "default-to-empty" state.
    """
    if not lattice_doc_path.exists():
        raise FileNotFoundError(
            f"Lattice doc not found at {lattice_doc_path}. "
            f"Required for lattice config (label_prefix, "
            f"default_campaign)."
        )
    from lib.shared.frontmatter import read_doc_frontmatter
    return config_from_dict(read_doc_frontmatter(lattice_doc_path))


def _active_lattice_doc_path() -> Path:
    """Build the path to the active lattice's substrate doc."""
    from lib.shared.paths import (
        DOCUVERSE_DIR, LATTICE_NAME, LATTICE_NODE, LATTICE_USER,
    )
    return (
        DOCUVERSE_DIR / "documents" / LATTICE_NODE / LATTICE_USER
        / "lattice" / f"{LATTICE_NAME}.md"
    )


@functools.lru_cache(maxsize=None)
def _cached_for(lattice_doc_path: Path) -> LatticeConfig:
    return config_from_doc(lattice_doc_path)


def lattice_config() -> LatticeConfig:
    """The active lattice's config, loaded once per process.

    Resolves via lib.shared.paths.LATTICE_NAME / LATTICE_NODE /
    LATTICE_USER (which are themselves driven by the --lattice CLI
    arg or LATTICE env var). Cached per-process.
    """
    return _cached_for(_active_lattice_doc_path())
