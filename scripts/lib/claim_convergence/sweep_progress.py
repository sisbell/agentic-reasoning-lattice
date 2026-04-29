"""Workspace-side progress tracking for cone-sweep resumability.

Records the sweep's intent (params) and per-apex progress so an
interrupted sweep can resume on restart without re-doing already-
processed cones. Pipeline-orchestration state — lives in workspace,
never in substrate (a cycle-completion tag would conflate orchestrator
run state with lattice content; substrate-module §1 reserves substrate
links for facts about documents, not facts about pipeline runs).

File: `<WORKSPACE_DIR>/cone-sweep/<asn-label>/progress.json`

Schema:
    {
      "started_at":  ISO-8601 timestamp,
      "min_deps":    int,           # the sweep's threshold
      "all":         bool,          # --all override flag (force re-review)
      "completed":   [labels...]    # apexes done in this sweep
    }

The apex order itself is recomputed at sweep start (the DAG may have
shifted between runs); only the labels-completed set is replayed.
On natural completion, the file is cleared.
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
    """Remove the progress file on natural sweep completion."""
    path = progress_path(asn_label)
    if path.exists():
        path.unlink()
    parent = path.parent
    if parent.exists():
        try:
            parent.rmdir()
        except OSError:
            pass


def matches_params(saved, current):
    """Whether `saved` progress's params match `current`. Mismatched
    params (different min_deps or --all flag) means a different sweep
    intent, so saved progress isn't resumable.

    Both args are dicts (or None for `saved`).
    """
    if saved is None:
        return False
    return (saved.get("min_deps") == current.get("min_deps")
            and saved.get("all") == current.get("all"))


def make_params(*, min_deps, all_mode):
    """Build the params dict that goes into `progress.json`."""
    return {"min_deps": min_deps, "all": all_mode}
