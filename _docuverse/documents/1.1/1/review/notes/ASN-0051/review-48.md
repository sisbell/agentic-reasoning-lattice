# Review of ASN-0051

## REVISE

### Issue 1: SV14 does not address K.λ
**ASN-0051, SV14 (DocumentDerivedDiscoverySurvivability)**: SV14 has clauses (a) monotonicity under K.μ⁺/K.μ⁺_L, (b) reduction under K.μ⁻, (c) cross-document isolation under K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~, and (d) witness for strict shrinkage. K.λ appears in none of them.

**Problem**: K.λ allocates a new link a_new. K.λ holds M in frame, so ran(M(d)) is unchanged, but a_new can enter discover_through_s(d) when coverage(L_new.s) ∩ ran(M(d)) ≠ ∅. The corollary `discover_through_s(d) in Σ ⊆ discover_through_s(d) in Σ'` under K.λ follows from SV9 + L-frame on M, but is not stated. SV14's framing ("inherits projection-style survivability of SV2–SV4 per-link") makes the omission natural — SV2–SV4 are M-modifying claims — but creates an apparent gap: a careful reader cataloguing transitions that can change document-derived discoverability finds SV14 silent on K.λ. SV14(c)'s cross-document isolation similarly omits K.λ, although K.λ trivially preserves isolation (M-frame across all documents).

**Required**: Either add an explicit K.λ clause (e.g., "(e) Monotonicity under link allocation: under K.λ, discover_through_s(d) may grow by absorbing new links whose endset coverage intersects the unchanged ran(M(d)); follows from SV9 with M held in K.λ's frame.") or extend SV14's preamble to cross-reference SV9 + L-frame on M as the locus of K.λ's effect on document-derived discovery.

### Issue 2: SV11 biconditional asserts m·p attainability without an attaining witness
**ASN-0051, SV11 (PartialSurvivalDecomposition), biconditional**: "The bound m · p is attained iff every (j, k) pair yields a non-empty decomposition term *and* these terms are pairwise non-adjacent and non-overlapping within each block."

**Problem**: The two-span non-injective worked example (4 non-empty terms, 2 fragments) and its three-span extension (4 non-empty terms among 6, 2 fragments) both exhibit strict inequality; neither attains the m·p bound. The biconditional asserts conditions for attainment but the worked examples — careful and concrete though they are — leave attainability ungrounded. Constructing such a witness with sibling-only allocations is in fact non-trivial: a span's coverage in any block I(β_k) is an ordinally contiguous prefix/middle/suffix (by S0 convexity on the span side); two spans hitting the *same* block in non-adjacent regions requires reach endpoints that lie at child-depth tumblers between siblings, which intersects the same-origin coverage-growth discussion later in the section.

**Required**: Either exhibit a concrete attainment witness (likely involving child-depth reach tumblers), or weaken the biconditional from "attained iff" to "achievable in principle iff, with attaining instances requiring …" and note the construction constraints, so the biconditional's right-direction reads as a structural condition rather than a routine corollary.

## OUT_OF_SCOPE

None to flag — the ASN explicitly scopes out higher-arity links (deferred to ASN-0043), broader-level span survivability with k ≤ p₃ (deferred to ASN-0034), link-subspace contributions to projection (deferred to a future Link Subspace ASN), and same-origin coverage growth (descriptive only, not SV-claimed). These deferrals are appropriate, not gaps in this ASN.

VERDICT: REVISE
