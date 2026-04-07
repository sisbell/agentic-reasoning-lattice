"""Deps refresh gate — dependency generation + commit.

Used by all formalization sub-pipelines as the entry gate before their
own work begins. Format normalization and name population have moved to
the blueprinting phase (scripts/lib/blueprinting/).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.common import find_asn, step_commit_asn


# Track ASN mtime after deps generation to skip redundant calls
_last_clean_mtime = {}


def step_refresh_deps(asn_num):
    """Run deps generation + commit. Returns True on success.

    Skips entirely if the ASN file hasn't been modified since the last
    successful run.
    """
    from lib.formalization.core.build_dependency_graph import generate_deps, write_deps_yaml

    print(f"\n  [DEPS] Refreshing dependencies", file=sys.stderr)

    # Skip entirely if ASN unchanged since last run
    asn_path, _ = find_asn(str(asn_num))
    if asn_path:
        current_mtime = asn_path.stat().st_mtime
        last_mtime = _last_clean_mtime.get(asn_num)
        if last_mtime is not None and current_mtime == last_mtime:
            print(f"  [DEPS] Unchanged — skipping", file=sys.stderr)
            return True

    # Deps generation
    deps = generate_deps(asn_num)
    if deps:
        write_deps_yaml(asn_num, deps)

    # Record mtime
    asn_path, _ = find_asn(str(asn_num))
    if asn_path:
        _last_clean_mtime[asn_num] = asn_path.stat().st_mtime

    step_commit_asn(asn_num, hint="refresh-deps")
    return True
