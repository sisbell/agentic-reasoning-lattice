"""Tests for the migrate-relocate-tumblers tool.

Imports the tool's helpers via importlib because the script lives at
scripts/migrate-relocate-tumblers.py (not a regular module).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


_TOOL_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "migrate-relocate-tumblers.py"
)


def _load_tool():
    spec = importlib.util.spec_from_file_location("relocate_tool", _TOOL_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def tool():
    return _load_tool()


def test_relocate_exact_prefix(tool) -> None:
    assert tool.relocate("1.1.0", "1.1.0", "1.2.0") == "1.2.0"


def test_relocate_subaddr(tool) -> None:
    assert tool.relocate("1.1.0.1.0.2", "1.1.0", "1.2.0") == "1.2.0.1.0.2"


def test_relocate_deep_subaddr(tool) -> None:
    assert (
        tool.relocate("1.1.0.1.0.1.1.0.2.21", "1.1.0", "1.2.0")
        == "1.2.0.1.0.1.1.0.2.21"
    )


def test_relocate_no_match(tool) -> None:
    # `1.10` does not start with `1.1.` — must not be rewritten
    assert tool.relocate("1.10.0.1", "1.1.0", "1.2.0") == "1.10.0.1"


def test_relocate_unrelated_prefix(tool) -> None:
    assert tool.relocate("2.1.0.1", "1.1.0", "1.2.0") == "2.1.0.1"


def test_relocate_record_rewrites_all_fields(tool) -> None:
    rec = {
        "id": "1.1.0.1.0.3.0.2.1",
        "homedoc": "1.1.0.1.0.3",
        "from_set": ["1.1.0.1.0.3"],
        "to_set": ["1.1.0.1.0.2"],
        "type_set": ["1.1.0.1.0.1.1.0.2.21"],
        "op": "create",
        "ts": "2026-05-03T03:43:04Z",
    }
    out = tool._rewrite_record(rec, "1.1.0", "1.2.0")
    assert out["id"] == "1.2.0.1.0.3.0.2.1"
    assert out["homedoc"] == "1.2.0.1.0.3"
    assert out["from_set"] == ["1.2.0.1.0.3"]
    assert out["to_set"] == ["1.2.0.1.0.2"]
    assert out["type_set"] == ["1.2.0.1.0.1.1.0.2.21"]
    assert out["op"] == "create"
    assert out["ts"] == "2026-05-03T03:43:04Z"


def test_relocate_record_no_homedoc(tool) -> None:
    rec = {
        "id": "1.1.0.1.0.3.0.2.1",
        "from_set": ["1.1.0.1.0.3"],
        "to_set": [],
        "op": "create",
        "ts": "2026-05-03T03:43:04Z",
    }
    out = tool._rewrite_record(rec, "1.1.0", "1.2.0")
    assert "homedoc" not in out
    assert out["id"] == "1.2.0.1.0.3.0.2.1"


def test_relocate_paths_json(tmp_path: Path, tool) -> None:
    p = tmp_path / "paths.json"
    p.write_text(json.dumps({
        "_meta": {"lattice_doc": "1.1.0.1.0.2", "lattice_name": "x"},
        "paths": {
            "doc/a.md": "1.1.0.1.0.5",
            "doc/b.md": "1.1.0.1.0.7",
            "doc/foreign.md": "2.1.0.1",
        },
    }))
    changed = tool.relocate_paths_json(p, "1.1.0", "1.2.0", dry_run=False)
    assert changed == 3  # lattice_doc + 2 paths (foreign untouched)
    data = json.loads(p.read_text())
    assert data["_meta"]["lattice_doc"] == "1.2.0.1.0.2"
    assert data["paths"]["doc/a.md"] == "1.2.0.1.0.5"
    assert data["paths"]["doc/b.md"] == "1.2.0.1.0.7"
    assert data["paths"]["doc/foreign.md"] == "2.1.0.1"


def test_relocate_links_jsonl(tmp_path: Path, tool) -> None:
    p = tmp_path / "links.jsonl"
    rec = {
        "id": "1.1.0.1.0.3.0.2.1",
        "from_set": ["1.1.0.1.0.3"],
        "to_set": ["1.1.0.1.0.2"],
        "type_set": ["1.1.0.1.0.1.1.0.2.21"],
        "op": "create",
        "ts": "2026-05-03T03:43:04Z",
    }
    p.write_text(json.dumps(rec) + "\n")
    records, fields_changed = tool.relocate_links_jsonl(
        p, "1.1.0", "1.2.0", dry_run=False,
    )
    assert (records, fields_changed) == (1, 1)
    out = json.loads(p.read_text().strip())
    assert out["id"] == "1.2.0.1.0.3.0.2.1"


def test_dry_run_does_not_write(tmp_path: Path, tool) -> None:
    p = tmp_path / "paths.json"
    body = json.dumps({
        "_meta": {"lattice_doc": "1.1.0.1.0.2"},
        "paths": {"doc/a.md": "1.1.0.1.0.5"},
    })
    p.write_text(body)
    changed = tool.relocate_paths_json(p, "1.1.0", "1.2.0", dry_run=True)
    assert changed == 2
    assert p.read_text() == body
