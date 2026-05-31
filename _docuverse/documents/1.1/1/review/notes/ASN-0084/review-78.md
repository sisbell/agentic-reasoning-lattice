# Review of ASN-0084

## REVISE

### Issue 1: Post-state S8 discharge restated in three places (forward-reference accretion)
**ASN-0084, "Invariant preservation" / "Canonical decomposition" / R-BLK closing**:
- Audit: "*Post-state S8 discharge.* Since `dom(M'(d)) = dom(M(d))` ... foundation S8 (ASN-0036) applies to M'(d) directly: it supplies the post-state maximal correspondence-run partition and its uniqueness."
- Canonical decomposition: "Its existence and uniqueness for the post-state M'(d) are the post-state S8 discharge recorded in the Invariant-preservation audit above."
- R-BLK end: "The existence and uniqueness of the post-state maximal (S8-unique canonical) correspondence-run decomposition is the post-state S8 discharge recorded in the Invariant-preservation audit above."

**Problem**: Two later paragraphs defer back to the same upstream audit in nearly identical words. This matches the flagged pattern "multiple paragraphs in different sections defer to the same downstream location" and "two paragraphs say the same thing in different words." The argument is made once in the audit; the restatements add no reasoning.

**Required**: Keep the discharge argument in the audit. Reduce the Canonical-decomposition and R-BLK references to a bare pointer (or delete the R-BLK one, since R-BLK's own conclusion is "B' is a valid run partition," and B' is explicitly *not* the maximal partition).

### Issue 2: Defensive reassurance in "Empty-exterior boundary cases"
**ASN-0084, Consequences of R-PRE, "Empty-exterior boundary cases"**: "Both boundary configurations are admissible: R-PRE(iv) covers the entire affected range, R-EXT degenerates to a vacuous quantification on the empty side, and the well-definedness arguments (R-PIV, R-SWP) — which partition V_S(d) into the affected range and the exterior — proceed unchanged when one exterior subset is empty."

**Problem**: The first two sentences of the paragraph establish concrete facts (which exterior subset is empty for which cut-ordinal values). This closing sentence only reassures that the proofs "proceed unchanged" — a defensive justification that establishes nothing new, and is redundant with the dedicated boundary worked example ("3-Cut Pivot at the Boundary") that demonstrates it concretely.

**Required**: Delete the "Both boundary configurations are admissible... proceed unchanged" sentence; retain the two sentences that pin the empty-side ord values.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: Already correctly deferred to Open Questions. This ASN's carrier (CS1: n ∈ {3,4}) deliberately confines the class; generalization is a future ASN, not a gap here.

### Topic 2: Cross-subspace and depth m₁ > 2 rearrangements
**Why out of scope**: Explicitly excluded by the State-and-Vocabulary scope restriction (text subspace, depth 2). Lifting either restriction is new territory, not an error.

The substantive content checks out: R-PIV/R-SWP tiling, R-PPERM/R-SPERM bijectivity (injection-on-finite-set ⟹ surjection via S8-fin), R-COMM's per-region same-region discharge, R-BLK's split/classify/reassemble, and all five worked examples (including the w_α=w_β fixed-μ, w_β<w_α backward-μ, empty-exterior, and non-S link cases) are internally consistent and verify their stated postconditions.

VERDICT: REVISE
