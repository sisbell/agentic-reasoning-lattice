"""JSONL persistence for the substrate's link store.

The substrate is monotone-append (ASN-0043 L11a/L12/L12a): every fact
is a Link record; the link store is the only state that matters for
substrate-level queries. The doc-allocator's cursor, the type-registry
doc address, and the parent/kind/content caches are all *recoverable*
from the link log plus deterministic re-allocation, but for now we
only persist the link store.

Format matches `scripts/lib/store/store.py` (the legacy substrate's
JSONL schema), so the file is cross-readable in either direction —
each record:

    {
      "op": "create",
      "id": "<link tumbler address>",
      "from_set": ["<addr>", ...],
      "to_set": ["<addr>", ...],
      "type_set": ["<type tumbler address>", ...],
      "ts": "<ISO-8601 UTC>"
    }

Deferred (not persisted): doc body content (lives in dict cache),
allocator state (recoverable), parent/kind caches (recoverable from
classifier and lattice links plus address structure).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .addressing import Address
from .links import Link, LinkStore


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _link_to_record(link: Link, ts: str) -> dict:
    return {
        "op": "create",
        "id": str(link.addr),
        "from_set": [str(a) for a in link.from_set],
        "to_set": [str(a) for a in link.to_set],
        "type_set": [str(a) for a in link.type_set],
        "ts": ts,
    }


def persist_jsonl(
    links: LinkStore | Iterable[Link],
    path: str | Path,
    *,
    ts: str | None = None,
) -> int:
    """Write every link to `path` in append-only JSONL format.

    `ts` overrides the timestamp on every record (useful for
    reproducibility); if None, current UTC time is used.
    Returns the number of records written.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = ts or _utcnow()
    count = 0
    with open(path, "w") as f:
        for link in links:
            record = _link_to_record(link, timestamp)
            f.write(json.dumps(record, sort_keys=True) + "\n")
            count += 1
    return count


def load_jsonl(path: str | Path) -> LinkStore:
    """Replay a JSONL file into a fresh LinkStore.

    The store is rebuilt purely from the log. Type addresses, link
    addresses, and endset addresses are all parsed back to Address
    objects.
    """
    store = LinkStore()
    path = Path(path)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if record.get("op") != "create":
                continue
            store.emit(
                addr=Address(record["id"]),
                from_set=[Address(s) for s in record["from_set"]],
                to_set=[Address(s) for s in record["to_set"]],
                type_set=[Address(s) for s in record["type_set"]],
            )
    return store
