"""Citation-graph predicates.

Outgoing/incoming citation traversal over `citation.<direction>`
links. Retracted citations drop from the graph automatically.

Generated from `lib/predicates/factory.py`'s `citation_outgoing` /
`citation_incoming` templates parameterized by direction.
"""

from __future__ import annotations

from .factory import citation_incoming, citation_outgoing


depends = citation_outgoing("depends")
dependents = citation_incoming("depends")
