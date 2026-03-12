# Divergences — A4(b) (DeleteContentPersists)

- **Line 22**: positions in deleted range are required explicitly rather than derived from J1 + range bounds. J1 establishes TextOrdinals == RangeSet(TextCount), but the solver cannot automatically connect membership in that set comprehension back to TextPos(j) in s.vmap[d].
