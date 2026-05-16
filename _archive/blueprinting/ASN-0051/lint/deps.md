# Dependency Lint — ASN-0051

Declared depends: [34, 36, 43, 47, 53, 58]


## Uncertain (needs LLM verification)

- UNCERTAIN ASN-0040: uses [B1]

## LLM Verification

## ASN-0040: B1

**Usage in ASN-0051:** SV11 (PartialSurvivalDecomposition) cites B1 explicitly:

> "The equality holds because B covers exactly the content-subspace V-positions (**B1 applied to the restriction**), so the I-extents of B's blocks are precisely the content-subspace I-addresses."

**Classification: COLLISION**

ASN-0058 is a declared dependency of ASN-0051, and it exports:

> **B1 — Coverage (PREDICATE)**
> `(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`
> Every text-subspace V-position in `dom(M(d))` appears in exactly one block.

This is precisely the property used in SV11 — the block decomposition coverage guarantee applied to the restriction `M(d)|_{V_{s_C}(d)}`. The scan matched the label B1 in ASN-0040, but ASN-0058 (already declared) provides the same label for the same concept. ASN-0040 is not a declared dependency and is not needed.

---

`RESULT: 0 MISSING, 1 COLLISION, 0 LOCAL, 0 CLEAN`
