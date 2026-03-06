# Divergences — SubtractionPreservesOrder (SubtractionPreservesOrder)

- **Line 212**: ASN states strict (<) unconditionally, but the foundation's TumblerSubtract can map distinct tumblers to the same result when both operands equal w after zero-padding (e.g., a=[1,0], b=[1,0,0], w=[1,0,0,0] gives a⊖w = b⊖w = [0,0,0,0]). Proved weak (≤) version.
