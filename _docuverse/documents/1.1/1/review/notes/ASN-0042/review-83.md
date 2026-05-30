# Review of ASN-0042

The formal core is sound: O1–O10 are derived at the right level of abstraction (predicates and invariants on `Π`, `pfx`, `Σ.B`, and transitions), the longest-match uniqueness argument (O2) is complete through all four steps, the `R_Σ` monotonicity defense in NestingByDelegation correctly leans on condition (vi) to forbid interposed newcomers, and the O10 non-coverage analysis covers both Form A/B and both `zeros(pfx(π)) ∈ {0,1}` branches. The boundary cases that matter for an ownership model — node vs account principal, `hwm_0 = 0` vs `hwm_0 ≥ 1`, bootstrap vs delegated principal, the `a = pfx(π)` self-ownership case, multi-node bootstrap — are all exercised. My findings are predominantly the meta-prose accretion the `review-mode.anti-bloat` classifier asks me to surface, plus one precision gap.

## REVISE

### Issue 1: Forward inventory in the `pfx(π)` definition
**ASN-0042, *Ownership as a Structural Predicate* (pfx(π) introduction)**: "The further structural constraints, injectivity (O1b) and the account-level bound `zeros(pfx(π)) ≤ 1` (O1a), are stated and proved as separate properties."
**Problem**: This sentence enumerates *where* downstream properties are proved without advancing the meaning of the `pfx` mapping — exactly the "definition's introduction enumerates downstream consumers" anti-bloat pattern. The `pfx` axiom already states its codomain constraint (`T4(pfx(π))`); the reader does not need a roster of which separate properties tighten it.
**Required**: Delete the sentence. O1a and O1b stand on their own where they appear.

### Issue 2: The "forevermore" interpretation is restated in three sections
**ASN-0042**, three sites converge on the same interpretive claim (refinement, not stasis):
- *Permanence and Refinement* intro: "But the naive reading — that `ω(a)` never changes — is too strong... The correct invariant is monotonic refinement."
- OwnershipDomainPermanence closing: "This is Nelson's 'forevermore': not that `ω` is static within `dom(π)`, but that no external act can alter it."
- O8 *Design confirmation*: "O8 instantiates the refinement-only reading of Nelson's 'forevermore' (established at OwnershipDomainPermanence)."
**Problem**: Two paragraphs in different sections saying the same thing in different words, with the third explicitly deferring back to the second. The interpretive gloss is object-level the first time; the repetitions are noise the precise reader skips past.
**Required**: State the refinement-vs-stasis reading once (at O3, where it motivates the formal statement) and let O8/ODP cite the property, not re-narrate the interpretation.

### Issue 3: Non-circularity justification prose in the `delegated_Σ*` construction
**ASN-0042, O15 *Definition (delegated)***: "The reflexive-transitive closure `delegated_Σ*` is built from a *parent relation* `R_Σ` defined purely on the single state `Σ`, with no reference to a witnessing path."
**Problem**: This is the "prose justifies the construction's freedom from circular/path dependency" pattern. The construction either is well-formed (it is — `R_Σ` is defined structurally) or it isn't; explaining that it avoids reference to a witnessing path is defensive meta-prose about the definitional choice rather than content advancing the definition.
**Required**: Give `R_Σ` and its closure directly; drop the editorial assurance about what the definition does *not* reference.

### Issue 4: O3's headline formula omits the reachability hypothesis its proof consumes
**ASN-0042, O3**: the displayed implication is `(A a ∈ Σ.B, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a) ⟹ (E π_d ..., π' ... : ...))`.
**Problem**: The proof excludes the bootstrap origin of `π'` only via `Π₀ ⊆ Π_Σ`, which requires `Σ` reachable. O3 is then invoked as a near-standalone lemma in OwnershipDomainPermanence Step 1 and in O8. The Formal Contract lists reachability, and a global convention assumes it, but the headline implication as written is not valid without it — a reader lifting the displayed formula loses the hypothesis that makes "the bootstrap case is excluded" go through.
**Required**: Carry `Σ reachable from Σ₀` into the displayed O3 formula (as the contract and proof both already rely on), so the property is self-contained rather than dependent on a convention stated pages earlier.

## OUT_OF_SCOPE

### Topic 1: Node-level sub-delegation semantics
O15 condition (iv) permits `zeros(pfx(π')) = 0`, so condition (i) admits a node principal `[1]` delegating a longer node-level prefix `[1,5]` (a "sub-node"). The formalism handles it uniformly and O9 permits the node-field extension, but the *meaning* of one node under another is never discussed. This is a question for whatever ASN treats node/server topology, not a defect here — the ownership predicate behaves correctly regardless.

### Topic 2: Ownership transfer reconciling provenance (O6) with effective owner (O2)
Already correctly deferred in the Open Questions and flagged at the O3 transfer tension. New territory, not an error.

VERDICT: REVISE
