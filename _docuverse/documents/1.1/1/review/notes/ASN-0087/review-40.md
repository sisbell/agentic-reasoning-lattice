# Review of ASN-0087

## REVISE

### Issue 1: Spurious L14 in the `ℓ ∉ ran(Σ_mid.M(d))` derivation chain
**ASN-0087, Preconditions**: "it must be derived through the S3★ + S3★-aux + L14 chain."

**Problem**: The derivation that follows uses only S3★-aux (every active V-position has `subspace(v) ∈ {s_C, s_L}`), S3★ (image lands in `dom(C)` resp. `dom(L)`), and K.λ's freshness (`ℓ ∉ dom(C) ∪ dom(L)`). The conclusion `Σ.M(d)(v) ≠ ℓ` follows because the image lies *inside* `dom(C) ∪ dom(L)` while `ℓ` lies *outside* it. The store-disjointness fact L14 (`dom(C) ∩ dom(L) = ∅`) is never invoked — disjointness of the two stores plays no role in separating an in-union image from an out-of-union address. The cited chain names a premise the proof does not use.

**Required**: Either drop L14 from the named chain (the chain is "S3★ + S3★-aux + K.λ freshness"), or, if L14 was intended to discharge some step, make that step explicit. As written the citation overstates the dependency set.

### Issue 2: Reflexive-route material scattered with repeated downstream deferrals (anti-bloat)
**ASN-0087, *What Is Indexed?*, *Weakest Precondition* Case 2, claims table (M-Reflexive)**:
- *What Is Indexed?*: "the home document alone gains a *reflexive route* ... (M-Reflexive, derived in *Weakest Precondition for Discoverability*, Case 2), a capability no `d_target ≠ d` can have."
- M-Reflexive table row: "(derivation in *Weakest Precondition for Discoverability*, Case 2)."
- WP Case 2: "Because `ℓ` enters only `d`'s arrangement, this route is available to the home document alone — Case 1 already shows other documents gain nothing from the allocation of `ℓ`."

**Problem**: The single fact "the reflexive route is the home document's alone" is asserted in *What Is Indexed?* and restated in WP Case 2, and two separate sites forward-defer their derivation to "WP, Case 2." This is the accretion pattern flagged for this note: multiple paragraphs in different sections deferring to the same downstream location, plus two paragraphs stating the same conclusion in different words. The reader must hold the deferral and then re-encounter the same claim at the deferral target.

**Required**: State the reflexive-route-is-home-only conclusion once, at its point of derivation (WP Case 2), and let *What Is Indexed?* cite M-Reflexive without re-asserting the home-only qualification in its own words. Remove the redundant forward pointer from the *What Is Indexed?* prose (the claims-table row already locates the derivation).

## OUT_OF_SCOPE

### Topic 1: Discoverability of endsets reaching not-yet-allocated addresses
The Open Questions correctly defer the well-formedness and discoverability semantics of forward-reaching endsets (spans over addresses not in `dom(C) ∪ dom(L)`) to future work. The current ASN bounds its discoverability claims to the post-state and handles the born-orphaned case via LP17/LP18 references; the forward-creation discoverability guarantee is genuinely new territory, not a gap in this ASN.

VERDICT: REVISE
