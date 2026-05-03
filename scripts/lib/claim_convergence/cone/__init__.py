"""Cone-scope review operators.

Split into focused modules:

- scope:   transitive_same_asn_deps, assemble_cone
- retry:   _retry_unresolved_revises, _declined_findings_for_cone
- select:  detect_dependency_cone (auto-detect a cone needing focus)
- review:  run_cone_review (one cone's review/revise loop)
- sweep:   run_cone_sweep (bottom-up DAG walk across qualifying cones)

A dependency cone is a claim (the apex) that sits atop many stable
dependencies and can't converge under per-finding revision. See
docs/patterns/dependency-cone.md for the pattern.
"""

from .scope import assemble_cone, transitive_same_asn_deps
from .retry import _retry_unresolved_revises, _declined_findings_for_cone
from .select import detect_dependency_cone
from .review import run_cone_review
from .sweep import run_cone_sweep

__all__ = [
    "assemble_cone",
    "transitive_same_asn_deps",
    "_retry_unresolved_revises",
    "_declined_findings_for_cone",
    "detect_dependency_cone",
    "run_cone_review",
    "run_cone_sweep",
]
