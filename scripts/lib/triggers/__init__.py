"""Trigger declarations — wire substrate predicates to agents.

Each trigger declares: scope query, predicate, agent. The runner
walks them. Adding a trigger means writing a new module here; it
does not change the runner.
"""

from .cone_review import apex_labels_in_topological_order, cone_review

__all__ = ["apex_labels_in_topological_order", "cone_review"]
