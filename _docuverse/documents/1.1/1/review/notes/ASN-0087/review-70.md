# Review of ASN-0087

This is a strong, careful note: the J0/J1★/J1'★ coupling constraints are discharged for *structurally distinct* reasons rather than by "similarly," the boundary case-splits (empty/non-empty link subspace) are carried through D-MIN★, D-SEQ★, and D-CTG★ individually, the worked example checks discoverability concretely, and the wp analysis finds the non-trivial reflexive case. The rigor bar is met. The findings below are anti-bloat accretion, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: `dom(Σ'.M) = dom(Σ.M)` equality re-derived in four places
**ASN-0087, "Inputs" / "Weakest Precondition" / "Invariant Preservation"**: The fact that MAKELINK does not extend the document set is asserted and/or re-derived repeatedly:
- the `dom(M)` notational note — "the inclusion clause `dom(Σ.M) ⊆ dom(Σ'.M)` is the part M1 shares with ASN-0093";
- the wp membership paragraph — "M1 supplies only the inclusion …; equality `dom(Σ'.M) = dom(Σ.M)` … comes from the K.λ frame and K.μ⁺_L's effect …";
- the M-Inv-State frame note — "`dom(Σ'.M) = dom(Σ.M)`, since MAKELINK allocates no new document";
- the M1 transition-invariant bullet — "Trivially holds with equality — MAKELINK does not extend `dom(M)`."

**Problem**: The same inclusion-vs-equality reconciliation is restated four times. The notational aside in particular ("the part M1 shares with ASN-0093") is cross-foundation provenance bookkeeping that does not advance MAKELINK's reasoning — it disambiguates which foundation's M1 is meant, a disambiguation the wp paragraph then performs again in full. This is the "multiple paragraphs say the same thing in different words" pattern.

**Required**: Derive the equality `dom(Σ'.M) = dom(Σ.M)` once (the wp membership paragraph is the natural site, since it is load-bearing there) and have the other three sites cite it. Drop the "part M1 shares with ASN-0093" provenance clause from the notational note; `dom(M) = E_doc` alone suffices for notation.

## OUT_OF_SCOPE

### Topic 1: well-formedness of forward-reaching endsets
The first Open Question (constraints on endsets whose spans reference not-yet-allocated I-addresses) is correctly deferred — `StandardAuthoring` characterizes the discipline without mandating it, and the general constraint belongs to a future endset-discipline ASN, not here.

VERDICT: REVISE
