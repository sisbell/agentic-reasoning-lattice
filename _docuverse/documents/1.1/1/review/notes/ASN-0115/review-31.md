# Review of ASN-0115

I checked the formal spine of this note carefully — the Confinement lemma's use of T5, the totality of `item` via S3★-aux, R6's gap-location argument (the canonical-start derivation, the bound-iff-`k ≤ n_S` frontier, the `act = ∅` sub-cases), R7's reliance on `Σ →* Σ'` comparability, R8's link-vacuity via CL-OWN/CL-UNIQ, and R11's weakest-precondition decomposition. The mathematics is sound, the boundary cases (empty spec-set, empty subspace, terminal overrun, orphaned content) are handled, every "derived" claim carries its derivation, and the worked instances correctly exercise the cited claims. I found no correctness defect.

One bloat residue remains, which under this note's active anti-bloat classifier is a finding.

## REVISE

### Issue 1: Modeling-choice justification in the pure-query frame
**ASN-0115, "What a spec-set is, and what delivery is" (pure-query frame paragraph)**: "RETRIEVEV is a *pure query*. `deliver(R, Σ)` reads the state and produces no transition: no component of `Σ` is modified … it is a function of state, not a state transition. We record this as a frame rather than leave it implicit in the functional notation (cf. ASN-0086, Observe)."
**Problem**: The first three sentences fully establish the no-modification property — they name every component held fixed and state plainly that the operation is not in the transition vocabulary. The closing sentence "We record this as a frame rather than leave it implicit in the functional notation" justifies *why the frame is written* rather than asserting *what the operation does*. That is a defensive modeling-choice justification occupying a structural (frame) slot — exactly the residue the anti-bloat classifier targets. It advances no reasoning the reader needs to follow the frame.
**Required**: Drop the modeling-choice justification, leaving the substantive frame assertion. The precedent pointer "(cf. ASN-0086, Observe)" may stay as a cross-reference if wanted, but "rather than leave it implicit in the functional notation" should go.

## OUT_OF_SCOPE

None. The Open Questions appropriately defer inline content provenance, fail-outright conditions, dangling references, channel faithfulness, and subspace-straddling spans to future work, and the note defines no claims for the sibling-operation topics listed as out of scope.

VERDICT: REVISE
