# Dependency Lint — ASN-0061

Declared depends: [34, 36, 43, 47, 53, 58]


## Uncertain (needs LLM verification)

- UNCERTAIN ASN-0040: uses [B1, B2, B3]

## LLM Verification

## ASN-0040 — B1, B2, B3

**B1 — COLLISION**
ASN-0061 uses B1 (Coverage) in the "Verification of B1–B3" section of D-BLK: *"Coverage (B1): B_other covers V-positions in other subspaces..."*. This is the block decomposition coverage predicate, which is defined in ASN-0058 (a declared dependency) as `(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : v ∈ V(βⱼ)))`. The scanner matched the label to ASN-0040, but ASN-0058 is the originating source actually being used.

**B2 — COLLISION**
ASN-0061 uses B2 (Disjointness) in the same D-BLK verification: *"Disjointness (B2): B_other is disjoint from the S blocks by subspace..."* and *"the original right-region blocks were pairwise disjoint (B2 on the pre-state decomposition)"*. Again, this is the block decomposition disjointness predicate from ASN-0058, not ASN-0040.

**B3 — COLLISION**
ASN-0061 uses B3 (Consistency) in D-BLK: *"Consistency (B3): for B_left, M'(d)(v + j) = M(d)(v + j) = a + j by D-LEFT and the original B3."* This is the block decomposition consistency predicate from ASN-0058, not ASN-0040.

In all three cases, the labels appear in the context of block decomposition (Definition — BlockDecomposition, ASN-0058), and ASN-0058 is an explicitly declared dependency that exports B1, B2, and B3 with exactly the meanings used here.

---

`RESULT: 0 MISSING, 3 COLLISION, 0 LOCAL, 0 CLEAN`
