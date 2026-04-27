"""Link store schema, DDL, type validation, and ID generation.

The link store implements the Claim Convergence Protocol's link graph as a
JSONL append-only log (source of truth) with a rebuildable SQLite index.

Xanadu-aligned: links are permanent. There is no revocation. Once a link
is made, it persists forever as part of the graph's history.
"""

import hashlib
import json
from datetime import datetime, timezone


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS links (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  from_refs TEXT NOT NULL,
  to_refs TEXT NOT NULL,
  ts TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_links_type ON links(type);

CREATE TABLE IF NOT EXISTS endpoints (
  link_id TEXT NOT NULL,
  direction TEXT NOT NULL,
  ref TEXT NOT NULL,
  FOREIGN KEY (link_id) REFERENCES links(id)
);
CREATE INDEX IF NOT EXISTS idx_endpoints_ref ON endpoints(ref);
CREATE INDEX IF NOT EXISTS idx_endpoints_link ON endpoints(link_id);
"""


VALID_TYPES = {
    # Protocol-defined
    "claim", "note", "review", "contract", "citation", "comment", "resolution",
    # Substrate-owned (general-purpose document primitives)
    "retraction", "label", "name", "description",
    # Agent module
    "agent", "manages",
}

VALID_SUBTYPES = {
    "contract": {
        "axiom", "definition", "theorem", "corollary", "lemma",
        "consequence", "design-requirement",
    },
    "comment": {"revise", "observe", "out-of-scope"},
    "resolution": {"edit", "reject"},
}


def validate_type(type_str):
    """Raise ValueError if type_str is not a known parent or parent.subtype."""
    if "." in type_str:
        parent, sub = type_str.split(".", 1)
        if parent not in VALID_TYPES:
            raise ValueError(f"unknown parent type: {parent!r}")
        valid_subs = VALID_SUBTYPES.get(parent, set())
        if sub not in valid_subs:
            raise ValueError(f"unknown subtype {sub!r} for parent {parent!r}")
    else:
        if type_str not in VALID_TYPES:
            raise ValueError(f"unknown type: {type_str!r}")


def make_link_id(type_str, from_set, to_set, ts):
    """Content-derived link ID: 'l_' + first 12 hex chars of sha256."""
    serialized = "|".join([
        type_str,
        json.dumps(list(from_set), sort_keys=True),
        json.dumps(list(to_set), sort_keys=True),
        ts,
    ])
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return "l_" + digest[:12]


def utcnow_iso():
    """ISO-8601 UTC timestamp, seconds precision, 'Z' suffix."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
