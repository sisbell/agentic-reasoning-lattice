"""Lattice-level configuration access.

Lattice config (label_prefix, default_campaign) lives in the active
lattice's substrate doc frontmatter — `_docuverse/documents/<node>/
<user>/lattice/<lattice-name>.md` carries:

    ---
    label_prefix: ASN
    default_campaign: xanadu-protocol
    ---

This module reads that frontmatter once per process. Falls back to
`lattices/<name>/config.yaml` (legacy location) if no lattice doc is
on disk.

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


def _config_from_dict(raw: dict) -> LatticeConfig:
    return LatticeConfig(
        label_prefix=raw.get("label_prefix", DEFAULT_LABEL_PREFIX),
        default_campaign=raw.get("default_campaign"),
    )


def load_lattice_config(path: Path) -> LatticeConfig:
    """Read a lattice config from disk into a LatticeConfig.

    Two sources, in order:
      1. The lattice doc at `_docuverse/documents/<node>/<user>/
         lattice/<name>.md` — prefers frontmatter when present.
      2. Legacy `lattices/<name>/config.yaml` — fallback for sites
         that haven't migrated to the substrate-doc shape yet.

    `path` is the legacy yaml path; the lattice-doc path is derived
    from it. Missing file → defaults. Missing fields → field defaults.
    """
    # 1. Try lattice doc frontmatter first.
    lattice_doc = _lattice_doc_path_for(path)
    if lattice_doc is not None and lattice_doc.exists():
        from lib.shared.frontmatter import read_doc_frontmatter
        return _config_from_dict(read_doc_frontmatter(lattice_doc))

    # 2. Legacy yaml fallback.
    try:
        raw = yaml.safe_load(path.read_text()) or {}
    except FileNotFoundError:
        raw = {}
    return _config_from_dict(raw)


def _lattice_doc_path_for(yaml_path: Path) -> Optional[Path]:
    """Derive the lattice-doc path from the legacy yaml path.

    yaml lives at `lattices/<name>/config.yaml`. Lattice doc lives at
    `_docuverse/documents/<node>/<user>/lattice/<name>.md`. Use the
    yaml's parent directory name as `<name>` and consult paths.py for
    `<node>/<user>`.
    """
    try:
        lattice_name = yaml_path.parent.name
    except (AttributeError, ValueError):
        return None
    # Lazy-import to avoid cycle with paths.py at module-load time.
    from lib.shared.paths import WORKSPACE, _NODE_USER_PREFIX
    nu = _NODE_USER_PREFIX.get(lattice_name)
    if nu is None:
        return None
    node, user = nu
    return (
        WORKSPACE / "_docuverse" / "documents" / node / user
        / "lattice" / f"{lattice_name}.md"
    )


@functools.lru_cache(maxsize=None)
def _cached_for(path: Path) -> LatticeConfig:
    return load_lattice_config(path)


def lattice_config() -> LatticeConfig:
    """The active lattice's config, loaded once per process.

    Resolves the active lattice via lib.shared.paths.LATTICE_CONFIG, which
    is itself driven by the LATTICE env var. Cached per-process.
    """
    from lib.shared.paths import LATTICE_CONFIG
    return _cached_for(LATTICE_CONFIG)
