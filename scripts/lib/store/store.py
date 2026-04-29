"""Protocol substrate: typed, append-only link graph backed by JSONL + SQLite.

JSONL file is source of truth. SQLite index is rebuildable via `rebuild_index()`.
Single-writer assumption holds for stage 1 (orchestrator-driven topology).
Bootstrap toward Xanadu — the API mirrors Xanadu's primitives so migration
is a backend swap.

Xanadu-aligned API:
- `make_link` mirrors Xanadu's MAKELINK primitive.
- `find_links` mirrors FINDLINKSFROMTOTHREE.
- `find_num_links` mirrors FINDNUMLINKSFROMTOTHREE.

Links are permanent — there is no revocation. To express "this is no longer
effective," create a new link of an appropriate type pointing at the link
being neutralized (the protocol uses `resolution.reject` for comments;
nothing else needs neutralization at stage 1).

Stage-1 constraint: `type_set` is always a list of exactly one element.
The list shape is preserved in the API and JSONL so the migration to
multi-element type sets (Xanadu, stacked classifiers) is non-breaking.
"""

import contextlib
import functools
import json
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import DOCUVERSE_LOG, DOCUVERSE_INDEX, agent_doc_path
from lib.store.schema import (
    SCHEMA_SQL, make_link_id, validate_type, utcnow_iso,
)


AGENT_DOC_ENV_VAR = "XANADU_AGENT_DOC"


class Store:
    def __init__(self, log_path=None, index_path=None):
        self.log_path = Path(log_path) if log_path else Path(DOCUVERSE_LOG)
        self.index_path = Path(index_path) if index_path else Path(DOCUVERSE_INDEX)

        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(str(self.index_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA_SQL)
        self.conn.commit()

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def make_link(self, from_set, to_set, type_set, ts=None):
        if not isinstance(type_set, list) or len(type_set) != 1:
            raise ValueError(
                "type_set must be a list of exactly one element at stage 1"
            )
        type_str = type_set[0]
        validate_type(type_str)
        ts = ts or utcnow_iso()
        from_set = list(from_set)
        to_set = list(to_set)
        link_id = make_link_id(type_str, from_set, to_set, ts)

        row = self.conn.execute(
            "SELECT id FROM links WHERE id = ?", (link_id,)
        ).fetchone()
        if row is not None:
            raise ValueError(f"link id already exists: {link_id}")

        self._append_log({
            "op": "create",
            "id": link_id,
            "from_set": from_set,
            "to_set": to_set,
            "type_set": type_set,
            "ts": ts,
        })
        self._apply_create(link_id, type_str, from_set, to_set, ts)
        self.conn.commit()
        return link_id

    def get(self, link_id):
        row = self.conn.execute(
            "SELECT * FROM links WHERE id = ?", (link_id,)
        ).fetchone()
        if row is None:
            return None
        return self._row_to_record(row)

    def find_links(self, home_set=None, from_set=None, to_set=None, type_set=None):
        sql, params, empty = self._build_query(
            "SELECT DISTINCT links.* FROM links",
            home_set, from_set, to_set, type_set,
        )
        if empty:
            return []
        sql += " ORDER BY links.ts, links.id"
        rows = self.conn.execute(sql, params).fetchall()
        return [self._row_to_record(r) for r in rows]

    def find_num_links(self, home_set=None, from_set=None, to_set=None, type_set=None):
        sql, params, empty = self._build_query(
            "SELECT COUNT(DISTINCT links.id) AS n FROM links",
            home_set, from_set, to_set, type_set,
        )
        if empty:
            return 0
        row = self.conn.execute(sql, params).fetchone()
        return row["n"] if row else 0

    def rebuild_index(self):
        self.conn.executescript(
            "DROP TABLE IF EXISTS endpoints; DROP TABLE IF EXISTS links;"
        )
        self.conn.executescript(SCHEMA_SQL)

        if self.log_path.exists():
            with open(self.log_path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    record = json.loads(line)
                    if record.get("op") == "create":
                        type_str = record["type_set"][0]
                        self._apply_create(
                            record["id"], type_str,
                            record["from_set"], record["to_set"], record["ts"],
                        )
        self.conn.commit()

    def _append_log(self, record):
        with open(self.log_path, "a") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")

    def _apply_create(self, link_id, type_str, from_set, to_set, ts):
        self.conn.execute(
            "INSERT INTO links (id, type, from_refs, to_refs, ts) VALUES (?, ?, ?, ?, ?)",
            (
                link_id, type_str,
                json.dumps(from_set, sort_keys=True),
                json.dumps(to_set, sort_keys=True),
                ts,
            ),
        )
        endpoint_rows = [(link_id, "from", ref) for ref in from_set]
        endpoint_rows += [(link_id, "to", ref) for ref in to_set]
        if endpoint_rows:
            self.conn.executemany(
                "INSERT INTO endpoints (link_id, direction, ref) VALUES (?, ?, ?)",
                endpoint_rows,
            )

    def _build_query(self, select_clause, home_set, from_set, to_set, type_set):
        """Build the WHERE/JOIN clauses for find_links and find_num_links.

        Returns (sql, params, empty_short_circuit). If a constraint is given
        as an empty list, no link can satisfy it — return empty=True.
        `home_set` is accepted but unused at stage 1 (single-store).
        """
        for constraint in (from_set, to_set, type_set):
            if constraint is not None and len(constraint) == 0:
                return "", [], True

        sql_parts = [select_clause]
        params = []
        join_idx = 0

        if from_set is not None:
            join_idx += 1
            alias = f"ef{join_idx}"
            placeholders = ",".join(["?"] * len(from_set))
            sql_parts.append(
                f"INNER JOIN endpoints {alias} ON {alias}.link_id = links.id "
                f"AND {alias}.direction = 'from' AND {alias}.ref IN ({placeholders})"
            )
            params.extend(from_set)

        if to_set is not None:
            join_idx += 1
            alias = f"et{join_idx}"
            placeholders = ",".join(["?"] * len(to_set))
            sql_parts.append(
                f"INNER JOIN endpoints {alias} ON {alias}.link_id = links.id "
                f"AND {alias}.direction = 'to' AND {alias}.ref IN ({placeholders})"
            )
            params.extend(to_set)

        if type_set is not None:
            type_clauses = []
            for t in type_set:
                type_clauses.append("(links.type = ? OR links.type LIKE ?)")
                params.extend([t, t + ".%"])
            sql_parts.append("WHERE " + " OR ".join(type_clauses))

        return " ".join(sql_parts), params, False

    def _row_to_record(self, row):
        type_str = row["type"]
        return {
            "id": row["id"],
            "type_set": [type_str],
            "from_set": json.loads(row["from_refs"]),
            "to_set": json.loads(row["to_refs"]),
            "ts": row["ts"],
        }


_default_store = None


def _get_default():
    global _default_store
    if _default_store is None:
        _default_store = Store()
    return _default_store


def make_link(from_set, to_set, type_set, ts=None):
    return _get_default().make_link(from_set, to_set, type_set, ts)


def get(link_id):
    return _get_default().get(link_id)


def find_links(home_set=None, from_set=None, to_set=None, type_set=None):
    return _get_default().find_links(home_set, from_set, to_set, type_set)


def find_num_links(home_set=None, from_set=None, to_set=None, type_set=None):
    return _get_default().find_num_links(home_set, from_set, to_set, type_set)


def rebuild_index():
    return _get_default().rebuild_index()


def default_store(log_path=None, index_path=None):
    """Return a Store, wrapped in AgentStore if `XANADU_AGENT_DOC` is set.

    Orchestrators (cone-review, full-review) set the env var so subprocess
    tools (convergence-resolution.py, convergence-cite.py, claim-classify.py,
    link/*.py) that emit substrate links
    inherit the agent identity and attribute every operation back to it.
    Standalone CLI runs (no env var) get a plain Store — operations land
    in the substrate without `manages` attribution, which is correct since
    there's no registered agent acting on the user's behalf.
    """
    store = Store(log_path=log_path, index_path=index_path)
    agent_doc = os.environ.get(AGENT_DOC_ENV_VAR)
    if not agent_doc:
        return store
    from lib.store.agent_store import AgentStore
    return AgentStore(store, agent_doc)


@contextlib.contextmanager
def agent_context(agent_doc):
    """Bind `XANADU_AGENT_DOC` for the duration of the block.

    Use to scope agent attribution around an orchestrator block. Restores
    any prior value on exit, so nested orchestrators (e.g. full-review
    invoking cone-review on a detected dependency cone) cleanly inherit
    the outer agent and pop back when the inner block ends.
    """
    prior = os.environ.get(AGENT_DOC_ENV_VAR)
    os.environ[AGENT_DOC_ENV_VAR] = agent_doc
    try:
        yield
    finally:
        if prior is None:
            os.environ.pop(AGENT_DOC_ENV_VAR, None)
        else:
            os.environ[AGENT_DOC_ENV_VAR] = prior


def attributed_to(role):
    """Decorator: wrap an orchestrator entrypoint so its body runs inside
    `agent_context(agent_doc_path(role))`.

    Substrate writes inside the block (review/comment/resolution links)
    get a `manages` link from the agent doc, and subprocess tools
    (convergence-resolution.py, etc.) inherit `XANADU_AGENT_DOC` so their
    writes are attributed too.
    """
    agent_doc = agent_doc_path(role)

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            with agent_context(agent_doc):
                return fn(*args, **kwargs)
        return wrapper

    return decorator
