"""Workspace-side progress tracking for cone-sweep resumability.

Records which apexes have been done in an in-progress sweep so a
killed run can resume without redoing finished work. Pipeline-
orchestration state — lives in workspace, never in substrate
(a cycle-completion or sweep-progress fact would conflate orchestrator
run state with lattice content; substrate-module §1 reserves substrate
links for facts about documents, not facts about pipeline runs).

File: `<WORKSPACE_DIR>/cone-sweep/<asn-label>/progress.json`

Schema:
    {"completed": ["NAT-addbound", "T4", ...]}    # apex labels

Behavior contract:
    - run_cone_sweep reads `completed` at start (default mode only).
    - `--all` mode unconditionally clears the file at start (fresh sweep).
    - During a sweep, an apex is added to `completed` exactly when the
      convergence predicate holds for it. The same write happens whether
      the apex was processed (cone-review run) or skipped (predicate
      already True at visit). Apexes that did NOT converge are left out,
      so subsequent visits re-process them.
    - On natural completion, the file is cleared.
    - To start a fresh sweep before completion: run with `--all`, or
      delete the file by hand.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE_DIR


def progress_path(asn_label):
    """Workspace path for a sweep's progress file."""
    return WORKSPACE_DIR / "cone-sweep" / asn_label / "progress.json"


def read_progress(asn_label):
    """Return the progress dict, or None if no file or unreadable."""
    path = progress_path(asn_label)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def write_progress(asn_label, data):
    """Atomic write — temp-file + rename so a kill mid-write doesn't
    corrupt the file."""
    path = progress_path(asn_label)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def clear_progress(asn_label):
    """Remove the progress file. Called on natural sweep completion and
    at the start of an `--all` sweep."""
    path = progress_path(asn_label)
    if path.exists():
        path.unlink()
    parent = path.parent
    if parent.exists():
        try:
            parent.rmdir()
        except OSError:
            pass
