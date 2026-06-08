# Review of ASN-0111

## REVISE

### Issue 1: RL6 (nesting fidelity) is never verified against a concrete instance

**ASN-0111, "A worked read"**: The worked example states it checks "the load-bearing postconditions" and verifies RL1, RL2, RL5, RL-ARITY, and an orphaned RL8 instance. The from-set targets cross-document content and the type-set targets a ghost document — but no endset references another *link*.

**Problem**: RL6 introduces a genuinely distinct behavioral guarantee — that a link address appearing in an endset's coverage is disclosed *as an address*, unflattened and unrecursed (citing the canonical reflexive span of L13). This behavior is exercised by none of the checked instances; from→content and type→ghost-document do not touch link-subspace targets. Per the review standard ("the ASN should verify its key postconditions against at least one specific scenario"), a substantive claim with an entire dedicated section should be checked concretely, especially since link-to-link nesting (compound/faceted structures) is architecturally central.

**Required**: Extend the worked example with a to-set (or additional) span over a link address `a' ∈ dom(Σ.L)` — e.g. a unit-depth span `(a', δ(1, #a'))` — and check that `readlink` returns `a'` as the address it is, with `a' ∈ coverage(readlink(a, Σ).e₂)`, no flattening into `a'`'s (possible) content, and no silent recursion.

### Issue 2: RL2's formal statement is subsumed by RL1

**ASN-0111, RL1 and RL2**: RL1 concludes "`readlink(a, Σ) = Σ.L(a)` componentwise"; RL2 states "`(A i : 1 ≤ i ≤ |Σ.L(a)| : readlink(a, Σ).eᵢ = Σ.L(a).eᵢ)`".

**Problem**: RL1's bidirectional span-membership conjunction already yields per-slot set equality `readlink(a, Σ).eᵢ = Σ.L(a).eᵢ` for every `i` — which is exactly RL2's formal line. The two claims are formally the same proposition. The prose distinguishes them (completeness-vs-satisfaction for RL1; role grouping for RL2), but the intended additional content of RL2 — that slot indexing is a returned-value *primitive* (L6), not a reconstructable label — is not captured by a formula identical to RL1's.

**Required**: Either express RL2's independent content distinctly (e.g., that the returned value preserves arity and slot-position as a primitive, `|readlink(a,Σ)| = |Σ.L(a)|` with index-aligned access, invoking L6), or fold the role observation into RL1's prose and drop the duplicate formal claim.

## OUT_OF_SCOPE

None — the operations the ASN sets aside (follow, search, count, create, edit) are correctly excluded and only referenced to draw contrasts.

VERDICT: REVISE
