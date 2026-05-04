"""Cone-scope helpers used by claim-review orchestrators.

The cone-review and full-review orchestrators (in lib/orchestrators/)
import from these helper modules:

- scope:   transitive_same_asn_deps, assemble_cone
- retry:   _retry_unresolved_revises, _declined_findings_for_cone
- select:  detect_dependency_cone (auto-detect a cone needing focus)

A dependency cone is a claim (the apex) that sits atop many stable
dependencies and can't converge under per-finding revision. See
docs/patterns/dependency-cone.md for the pattern.
"""

from .retry import _declined_findings_for_cone, _retry_unresolved_revises
from .scope import assemble_cone, transitive_same_asn_deps
from .select import detect_dependency_cone

__all__ = [
    "_declined_findings_for_cone",
    "_retry_unresolved_revises",
    "assemble_cone",
    "detect_dependency_cone",
    "transitive_same_asn_deps",
]
