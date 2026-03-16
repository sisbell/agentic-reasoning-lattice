# Divergences — O6 (StructuralProvenance)

- **Line 92**: The ASN states O6 over ω (effective owner) and Σ.alloc. The Dafny model captures the structural core: same account field implies identical covering sets for all O1a-compliant prefixes (zeros ≤ 1). Since ω is defined as the most-specific covering prefix, identical covering sets give identical ω. Modeling ω directly would require the full principal set as a parameter.
