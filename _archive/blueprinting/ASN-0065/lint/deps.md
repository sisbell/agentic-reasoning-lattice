# Dependency Lint — ASN-0065

Declared depends: [34, 36, 47, 53, 58]


## Uncertain (needs LLM verification)

- UNCERTAIN ASN-0040: uses [B1, B2, B3]

## LLM Verification

## ASN-0040: uses [B1, B2, B3]

**B1 — COLLISION**
**B2 — COLLISION**
**B3 — COLLISION**

ASN-0065 uses B1, B2, and B3 in the R-BLK (BlockDecompositionTransformation) lemma. The text explicitly cites ASN-0058 each time:

- "Let B = {β₁, ..., βₘ} be a block decomposition of M(d) satisfying **B1–B3 (ASN-0058)**."
- "The resulting blocks satisfy **B3** (Consistency):"
- "**Coverage (B1) and disjointness (B2)** follow from π being a bijection"

These are the Coverage, Disjointness, and Consistency predicates for mapping block decompositions defined in ASN-0058 (a declared dependency). The scanner matched these labels against ASN-0040, which apparently also defines properties with the same labels, but ASN-0065 is not using ASN-0040's versions — it is using ASN-0058's.

---

`RESULT: 0 MISSING, 3 COLLISION, 0 LOCAL, 0 CLEAN`
