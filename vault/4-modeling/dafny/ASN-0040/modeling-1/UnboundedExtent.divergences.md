# Divergences — B9 (UnboundedExtent)

- **Line 24**: The ASN states UnboundedExtent over the full operational model (registries reachable by baptism sequences with B6 constraints), but the Dafny model captures only the structural core: the stream is injective (distinct indices give distinct elements), so hwm is unbounded. Operational reachability (Bop, B1) and B6 validity constraints are omitted as they are not needed for injectivity.
