"""Campaign resolver.

A campaign binds a (theory channel, evidence channel) pair to a target and a
curated bridge vocabulary. Each ASN binds to exactly one campaign via its
manifest's `campaign:` field, or inherits the lattice's `default_campaign`.

The resolver takes an ASN id and returns the campaign's channel names,
vocabulary path, and target. All pipeline stages that need channel content or
vocab route through here.
"""

import yaml

from lib.shared.paths import (
    LATTICE_CONFIG, load_manifest, load_lattice_config,
    campaign_dir, campaign_config, campaign_vocab,
)


class ConfigError(Exception):
    """Raised when campaign configuration is missing or malformed."""


def resolve_campaign(asn_id):
    """Resolve an ASN's campaign context.

    Returns dict with keys:
      name:             campaign name (str)
      theory_channel:   channel name bound to the theory role (str)
      evidence_channel: channel name bound to the evidence role (str)
      target:           campaign target description (str, may be empty)
      vocabulary_path:  path to the campaign's vocabulary.md (Path)

    Raises ConfigError if no campaign is bound (no `campaign:` in the ASN
    manifest and no `default_campaign` in the lattice config) or if the
    named campaign's directory/config is missing.
    """
    manifest = load_manifest(asn_id)
    name = manifest.get("campaign") or load_lattice_config().get("default_campaign")
    if not name:
        raise ConfigError(
            f"No campaign bound for ASN-{int(asn_id):04d}. "
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

    return {
        "name": name,
        "theory_channel": theory,
        "evidence_channel": evidence,
        "target": cfg.get("target", ""),
        "vocabulary_path": campaign_vocab(name),
    }
