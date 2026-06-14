# Review of ASN-0131

The mathematics here is sound. I checked the worked instance end-to-end (the `e₁` coverage `{a₂,a₃} ⊆ coverage(e₁)` via `a₂ ⊕ δ(2,#a₂) = shift(a₂,2) = a₄`; the `coverage(e₃) ∩ dom(Σ.C) = ∅` field-agreement argument; the `e₂` sibling-miss); the `RE-UDIST` existential factoring; the `RE-CWP` weakest precondition (including the `R = ∅` and `Δ = ∅` corners); and the `RE-RET` forward/backward split (R-Scope + flat-antichain backward direction is unconditional, forward is correctly conditioned on `coverage(Θ) ∩ dom(Σ.C) = ∅`). No correctness defect found. The cite-don't-rebuild discipline is mostly well honored — `F-IMG-MONO/CONTR/SWING`, `LP5/6/7/8/14/16`, the transition frames are cited, not reproved.

The findings below are about prose accretion, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: The existence/discovery section is interpretive meta-prose restating established claims

**ASN-0131, "Existence and discoverability: which side does this answer for?"**: "This sits in apparent tension with the designer's reading, which calls the operation a report of existence rather than discoverability. The designer and the foundation are slicing different axes."

**Problem**: The load-bearing content of this section is one paragraph — `RE-SEL` (`sel(W, d, Σ) = findlinks_V(W, d, Σ) ∩ addressable(Σ)`), which is cleanly derived and which places the operation on the discovery side, giving the present-tense/non-monotone stability that `RE-EDIT` rests on. That paragraph should stay. What surrounds it does not advance the specification:

- The opening restates ASN-0127's existence-vs-discovery taxonomy in detail ("an existence query takes a fixed `I ⊆ T` and answers a monotone, historical property … while a discovery query resolves its `I` through a document's current arrangement …"). The Scope explicitly designates the existence/discovery taxonomy as "ASN-0127's layer — cite, do not rebuild." A one-clause citation suffices to set up `RE-SEL`.
- The "designer's reading" reconciliation and the orthogonal-two-axes essay (`RE-EXST`) restate `RE-UNIT` in new vocabulary. `RE-EXST` ("by withholding identity the answer certifies the presence and shape of anchoring without making it followable") is `RE-UNIT` ("the answer's elements are `(role, endset)` pairs … never link identities … a surfaced from-endset cannot be paired with the to-endset of the same link") plus an interpretive label. To follow `RE-SEL` one must skip past the two-axis essay.

**Required**: Reduce the section to the `RE-SEL` derivation and its present-tense stability consequence, citing ASN-0127's taxonomy rather than restating it. If `RE-EXST` is retained, retain only the compressed table claim and drop the "designer's reading" / orthogonal-axes prose that re-says `RE-UNIT`.

### Issue 2: A forward reference promises an argument it does not deliver

**ASN-0131, "The unit of the answer"**: "A withdrawn link's anchoring should not be reported as live (we argue this below). So we range over the links that are present and not withdrawn — the addressable links."

**Problem**: The "below" (the retraction stability analysis, `RE-RET`) exposits *how* `RE` behaves once `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)` is adopted; it does not *argue* the design choice that withdrawn anchoring should be excluded from a live report. The promissory clause overstates what follows. This is the forward-reference-accretion pattern: a deferral whose target does not fulfill it.

**Required**: Either state the exclusion as the design decision it is (drop "we argue this below"), or deliver the justification at the cited location.

## OUT_OF_SCOPE

The Open Questions correctly defer link-subspace regions (OQ7), intersection-distributivity (OQ4, genuinely separate given the non-injective arrangement's failure to distribute the forward image over intersection, M13/M14), the whole-endset-vs-touching-spans question (OQ1), the rendered-into-V-order answer (OQ3), cross-store completeness (OQ5), and the type-slot-against-content match (OQ6). I found no claim that improperly reaches into the operations the Scope excludes (enumeration, counting, pagination, READLINK, FOLLOWLINK, creation/editing): `RE-UNIT` actively *withholds* identity and multiplicity rather than claiming them.

VERDICT: REVISE
