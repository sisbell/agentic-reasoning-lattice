# Dependency Lint — ASN-0059

Declared depends: [34, 36, 47, 53, 58]


## Uncertain (needs LLM verification)

- UNCERTAIN ASN-0040: uses [B1, B2, B3]

## LLM Verification

## ASN-0040: [B1, B2, B3]

**B1 — Coverage**: COLLISION. ASN-0059 uses B1 in the "Block Decomposition Effect" section: *"Verification of B1–B3. Coverage (B1): B_other covers V-positions in subspaces S' ≠ S..."*. The property being used is the block decomposition coverage predicate, which is defined in ASN-0058 (a declared dependency) as `B1 — Coverage (PREDICATE)`. ASN-0040 also happens to define a label B1, but ASN-0058 is the originating source for the block decomposition predicates that ASN-0059 depends on.

**B2 — Disjointness**: COLLISION. ASN-0059 uses B2 in the verification of I10: *"Disjointness (B2): B_other is disjoint from the subspace-S blocks by subspace..."* and also cites it directly as *"B2 (Disjointness, ASN-0058)"* in the straddling block argument. This is explicitly sourced to ASN-0058, a declared dependency, which defines `B2 — Disjointness (PREDICATE)`.

**B3 — Consistency**: COLLISION. ASN-0059 uses B3 in the I10 verification: *"Consistency (B3): for B_other, M'(d)(v + j) = M(d)(v + j) = a + j by I4 and original B3..."*. This is the block consistency predicate from ASN-0058 (a declared dependency), which defines `B3 — Consistency (PREDICATE)`.

---

`RESULT: 0 MISSING, 3 COLLISION, 0 LOCAL, 0 CLEAN`
