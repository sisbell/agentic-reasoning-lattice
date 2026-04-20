# Dependency Lint — ASN-0058

Declared depends: [34, 36, 53]


## Uncertain (needs LLM verification)

- UNCERTAIN ASN-0040: uses [B1, B2, B3]

## LLM Verification

## Analysis

**FLAGGED ASN-0040: uses [B1, B2, B3]**

Checking ASN-0058's properties table:

| Label | Status in ASN-0058 |
|-------|-------------------|
| B1 | **introduced** — Coverage: blocks partition the text-subspace V-positions of `dom(M(d))` |
| B2 | **introduced** — Disjointness: no two blocks share a V-position |
| B3 | **introduced** — Consistency: each block correctly describes `M(d)` |

All three labels are defined locally in ASN-0058's "Block Decomposition" section and listed with status "introduced" in its properties table. They are structural conditions on block decompositions — a concept ASN-0058 introduces from scratch, elevating ASN-0036's correspondence runs (S8) to first-class algebraic objects. ASN-0040 is not a declared dependency and the scanner matched the label strings, but there is no cross-ASN reference here.

---

- **B1** — LOCAL. Defined in ASN-0058's "Block Decomposition" definition block under condition (B1), introduced locally.
- **B2** — LOCAL. Defined in ASN-0058's "Block Decomposition" definition block under condition (B2), introduced locally.
- **B3** — LOCAL. Defined in ASN-0058's "Block Decomposition" definition block under condition (B3), introduced locally.

`RESULT: 0 MISSING, 0 COLLISION, 3 LOCAL, 0 CLEAN`
