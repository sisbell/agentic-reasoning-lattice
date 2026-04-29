# Cone Review — ASN-0034/T4 (cycle 1)

*2026-04-25 16:02*

### T4c missing NAT-zero in Depends
**Class**: REVISE
**Foundation**: NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ`.
**ASN**: T4c (LevelDetermination), Injectivity argument: "NAT-addcompat's strict successor inequality `n < n + 1`, instantiated at `n ∈ {0, 1, 2}`, gives `0 < 1`, `1 < 2`, and `2 < 3`". Also Postcondition: `zeros(t) = 0 ↔ t is a node address`.
**Issue**: Instantiating NAT-addcompat's `n < n + 1` at `n = 0` requires `0 ∈ ℕ`, and the label-defining biconditional `zeros(t) = 0 ↔ ...` uses the literal `0`. Both come from NAT-zero, which is not in T4c's Depends list. T4 (which is in Depends) re-imports NAT-zero, but the convention elsewhere in this ASN (e.g., T4b lists NAT-zero directly even though it also depends on T4) is to declare direct uses explicitly.
**What needs resolving**: Either declare NAT-zero in T4c's Depends with a use-site citation (instantiation of `n < n+1` at `n = 0` and grounding of the literal `0` in the level labels), or restructure the injectivity chain to start from `0 < 1` cited from NAT-closure (which posits `0 < 1` and `1 ∈ ℕ` as axioms) and avoid the `n = 0` instantiation of NAT-addcompat — but the literal `0` in the definitional biconditional still needs grounding.

### Structural ordering of T4 vs. T4a/T4b/T4c
**Class**: OBSERVE
**Foundation**: n/a (internal structure)
**ASN**: T4 (HierarchicalParsing) is presented at the *end* of the document, after T4a, T4b, and T4c — yet all three depend on T4, and T4a's setup forward-references "T4's Exhaustion Consequence" before T4 has been stated.
**Issue**: A reader walking the document linearly encounters T4a's "Set `k = zeros(t)`; T4's Exhaustion Consequence … pins `k ∈ {0, 1, 2, 3}`" before seeing T4's body or its Exhaustion derivation. The dependency chain is correct (each Depends list is well-formed) and the cross-references resolve, so this is a presentation issue rather than a soundness issue.

VERDICT: REVISE
