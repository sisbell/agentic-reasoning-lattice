"""Campaign resolver.

A campaign binds a (theory channel, evidence channel) pair to a target and a
curated bridge vocabulary. Each ASN binds to exactly one campaign via its
manifest's `campaign:` field, or inherits the lattice's `default_campaign`.

The resolver takes an ASN id and returns a CampaignContext with the campaign's
channel names, vocabulary path, and target. All pipeline stages that need
channel content or vocab route through here.
"""

import functools
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from lib.shared.paths import (
    LATTICE_CONFIG, load_manifest, load_lattice_config,
    campaign_dir, campaign_config, campaign_vocab,
)


class ConfigError(Exception):
    """Raised when campaign configuration is missing or malformed."""


@dataclass(frozen=True)
class CampaignContext:
    name: str
    theory_channel: str
    evidence_channel: str
    target: str
    vocabulary_path: Path


_ASN_ID_RE = re.compile(r"^(?:ASN-)?0*(\d+)$")


def _asn_int(asn_id):
    """Coerce 2, '2', '0002', 'ASN-0002' to int 2. Rejects anything else."""
    if isinstance(asn_id, int):
        return asn_id
    m = _ASN_ID_RE.match(str(asn_id).strip())
    if not m:
        raise ConfigError(f"Cannot parse ASN id: {asn_id!r}")
    return int(m.group(1))


def resolve_campaign(asn_id):
    """Resolve an ASN's campaign context. Cached per ASN id within a process."""
    return _resolve_cached(_asn_int(asn_id))


@functools.lru_cache(maxsize=None)
def _resolve_cached(asn_num):
    manifest = load_manifest(asn_num)
    name = manifest.get("campaign") or load_lattice_config().get("default_campaign")
    if not name:
        raise ConfigError(
            f"No campaign bound for ASN-{asn_num:04d}. "
            f"Set `campaign:` in the ASN manifest or `default_campaign:` in "
            f"{LATTICE_CONFIG}."
        )

    cdir = campaign_dir(name)
    if not cdir.exists():
        raise ConfigError(
            f"Campaign directory not found: {cdir}. "
            f"Expected config.yaml and vocabulary.md inside."
        )

    cfg_path = campaign_config(name)
    try:
        cfg = yaml.safe_load(cfg_path.read_text()) or {}
    except FileNotFoundError:
        raise ConfigError(f"Campaign config not found: {cfg_path}")

    theory = cfg.get("theory")
    evidence = cfg.get("evidence")
    if not theory or not evidence:
        raise ConfigError(
            f"Campaign {name} config must set `theory:` and `evidence:` "
            f"(got theory={theory!r}, evidence={evidence!r} from {cfg_path})."
        )

    return CampaignContext(
        name=name,
        theory_channel=theory,
        evidence_channel=evidence,
        target=cfg.get("target", ""),
        vocabulary_path=campaign_vocab(name),
    )
