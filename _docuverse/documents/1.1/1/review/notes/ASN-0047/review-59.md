# Review of ASN-0047

## REVISE

### Issue 1: Prefix-incomparability preservation under suffix extension is asserted without proof
**ASN-0047, Cross-document disjointness chain (Lemma)**: "Prefix-incomparability is preserved under suffix extension: from `d₁ ⋠ d₂` we have `[d₁.0.s_L] ⋠ [d₂.0.s_L]` (a strictly-extending suffix on an already-divergent stem cannot bridge the divergence point), and symmetrically `p₂ ⋠ p₁`, so `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`."
**Problem**: This is a parenthetical hand-wave for a load-bearing step. `d₁ ⋠ d₂` decomposes into two cases via Prefix (ASN-0034): either `#d₁ > #d₂`, or there exists `k ≤ #d₁` with `d₁ₖ ≠ d₂ₖ`. The two cases need separate treatment showing that extending by `.0.s_L` preserves the non-prefix relation. The lemma underwrites K.λ's cross-document allocation uniqueness and feeds T10 directly — a structural fact this central deserves explicit derivation.
**Required**: Show the two-case proof inline, or cite a named foundation property (none currently exists in ASN-0034 for this).

### Issue 2: K.μ~ contract is defined in two locations with overlapping content
**ASN-0047, "Elementary transitions" section and "Decomposition of K.μ~" section**: K.μ~ appears in the elementary-transitions enumeration with bijection equation, admissibility constraints, and frame; the same content is restated in the dedicated Decomposition section.
**Problem**: The "Elementary transitions" bullet for K.μ~ visually presents it alongside elementary transitions despite the explicit disclaimer that K.μ~ is not elementary. The dual statement creates maintenance risk (future revisions touching one site but not the other) and reader confusion ("which is the authoritative definition?"). Throughout the document, references to "the K.μ~ contract" or "K.μ~'s preconditions" could point to either site.
**Required**: Move the K.μ~ contract entirely out of the elementary-transitions list into a dedicated subsection (or its own section adjacent to the Decomposition material); leave a brief pointer in the elementary-transitions list noting that K.μ~ is a named composite handled separately.

### Issue 3: K.μ⁻ amendment cites D-SEQ★ before its formal definition
**ASN-0047, K.μ⁻ section under "Elementary transitions"**: "*Admissible removal pattern (per-subspace suffix or full clearance).* For each subspace S, the removed positions in `V_S(d)` form either a suffix of `V_S(d)` under the D-SEQ★-shaped enumeration or all of `V_S(d)`. The shape D-SEQ★ — stated inline here for self-contained reading and elevated to a system-wide per-state invariant below..."
**Problem**: K.μ⁻'s precondition depends on D-SEQ★, but D-SEQ★ is formally defined in the "Amendments to existing transitions" section that comes *after* the elementary transitions section. The author acknowledges this with the parenthetical "stated inline here for self-contained reading," but readers verifying K.μ⁻'s precondition must scroll forward to find the formal D-SEQ★ definition. The forward dependency is structural (D-SEQ★ is derived from D-CTG★ + D-MIN★ + S8-fin + S8-depth + S8a), so reorganizing the section order would resolve it cleanly.
**Required**: Either define D-SEQ★ before K.μ⁻ (e.g., move the foundation-state derivation of D-SEQ from ASN-0036 to a "Per-state arrangement shape" preamble before the elementary transitions), or restructure so K.μ⁻'s amendment appears after D-SEQ★ is formally derived. The current placement makes the K.μ⁻ precondition unverifiable in document-reading order.

### Issue 4: "Arrangement invariants from elementary preservation" lemma hand-waves the S8 derivation
**ASN-0047, lemma after the elementary transitions enumeration**: "Each elementary transition preserves these per-state properties: ... S8 follows from S8-fin, S8a, S2, S8-depth, T5, TA5(c), TA7a via the derivation chain in ASN-0036."
**Problem**: This is the canonical "follows from ... via the derivation chain in ASN-0036" hand-wave the standards explicitly forbid. The same phrasing recurs in the ExtendedReachableStateInvariants proof. Either the chain transfers automatically (in which case the conjuncts S8-fin, S8a, S2, S8-depth should suffice without re-deriving T5/TA5(c)/TA7a) or it requires explicit restatement at this scope. The reader has no way to verify the chain without leaving the document.
**Required**: Either show the chain in one explicit derivation (it would be short), or cite the specific named lemma in ASN-0036 that packages the result.

VERDICT: REVISE
