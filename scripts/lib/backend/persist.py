"""JSONL persistence for the substrate's link store.

The substrate is monotone-append (ASN-0043 L11a/L12/L12a): every fact
is a Link record; the link store is the only state that matters for
substrate-level queries. The doc-allocator's cursor, the type-registry
doc address, and the parent/kind/content caches are all *recoverable*
from the link log plus deterministic re-allocation, but for now we
only persist the link store.

Format — each record:

    {
      "op": "create",
      "id": "<link tumbler address>",
      "from_set": ["<addr>", ...],
      "to_set": ["<addr>", ...],
      "type_set": ["<type tumbler address>", ...],
      "ts": <unix epoch seconds, int>
    }

`ts` is scoped to agentic concerns per `feedback_ts_scoped_to_agentic.md`
— substrate-side structural reasoning uses tumbler-address sequence,
not ts. Stored as Unix int seconds (compact + fast comparison).

Read-time backward compat: existing JSONL records may carry `ts` as
ISO-8601 string ("2026-05-09T03:55:22Z"); load_jsonl parses either
format to int, so old data loads correctly without migration. Run
`scripts/migrate-ts-to-int.py` for a one-time cleanup pass.

Deferred (not persisted): doc body content (lives in dict cache),
allocator state (recoverable), parent/kind caches (recoverable from
classifier and lattice links plus address structure).
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional, Union

from .addressing import Address
from .links import Link, LinkStore


def _utcnow_unix() -> int:
    return int(time.time())


def _parse_ts(raw: Union[int, float, str, None]) -> Optional[int]:
    """Parse a record's ts field to Unix-int seconds.

    Accepts the canonical int, a numeric float (legacy persistence
    paths that stored decimal), or an ISO-8601 string (legacy data
    pre-migration to int). Returns None on unparseable input.
    """
    if raw is None:
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float):
        return int(raw)
    if isinstance(raw, str):
        try:
            normalized = raw.replace("Z", "+00:00")
            dt = datetime.fromisoformat(normalized)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            return None
    return None


def _link_to_record(link: Link, ts: int) -> dict:
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
    ts: int | None = None,
) -> int:
    """Write every link to `path` in append-only JSONL format.

    `ts` overrides the timestamp on every record (useful for
    reproducibility); if None, current UTC time is used.
    Returns the number of records written.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = ts if ts is not None else _utcnow_unix()
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
    objects. `ts` is parsed via `_parse_ts` (handles both int and
    legacy ISO-8601 string formats).
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
                ts=_parse_ts(record.get("ts")),
            )
    return store
