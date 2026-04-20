# Dependency Lint — ASN-0067

Declared depends: [34, 36, 43, 47, 53, 58]


## Uncertain (needs LLM verification)

- UNCERTAIN ASN-0040: uses [B1, B2, B3]

## LLM Verification

## Classification

**ASN-0040: [B1, B2, B3]**

ASN-0067 does use B1, B2, and B3 — explicitly in the "Well-Formedness of B'" section:

- **B2 (Disjointness):** "The four groups occupy non-overlapping V-ranges..."
- **B1 (Coverage):** "Within subspace S, let N = |V_S(d)|..."
- **B3 (Consistency):** "Pre-blocks: M'(d)(p) = M(d)(p) for p < v..."

However, B1, B2, and B3 are defined in **ASN-0058** (declared dependency), not ASN-0040. ASN-0058 exports them as the block decomposition predicates (Coverage, Disjointness, Consistency). ASN-0067 depends on ASN-0058 and that is what it is referencing throughout the block decomposition machinery.

**B1 → COLLISION** — defined in declared dependency ASN-0058 (Coverage predicate).  
**B2 → COLLISION** — defined in declared dependency ASN-0058 (Disjointness predicate).  
**B3 → COLLISION** — defined in declared dependency ASN-0058 (Consistency predicate).

---

`RESULT: 0 MISSING, 3 COLLISION, 0 LOCAL, 0 CLEAN`
