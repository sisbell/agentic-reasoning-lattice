# Review of ASN-0084

I worked the five examples, checked the well-definedness lemmas (R-PIV/R-SWP), the bijection proofs (R-PPERM/R-SPERM), the commutation lemma (R-COMM), the run-transform (R-BLK), and the canonicity argument (R-CANON). The mathematics is sound: the depth-2 scope makes `dom(M'(d)) = dom(M(d))`, so the invariant-preservation argument is correct, the width/displacement arithmetic checks against every worked example, and R-CANON's no-forward/no-backward extension argument is complete. The defects I found are foundation-citation errors inside proofs — the kind of "cite what you actually use" slip that has to be fixed before downstream ASNs lean on this.

## REVISE

### Issue 1: R-CANON cites TS2 for amount-injectivity; the correct lemma is TS5
**ASN-0084, R-CANON, "We first record facts used in both directions"**: "...and shift is strictly increasing (TS4) and injective in its amount (TS2, ASN-0034)."
**Problem**: TS2 (ShiftInjectivity) is injectivity in the *tumbler argument at fixed amount* (`shift(v₁,n) = shift(v₂,n) ⟹ v₁ = v₂`). Injectivity *in the shift amount* is TS5 (ShiftAmountMonotonicity), which gives `n₁ ≠ n₂ ⟹ shift(v,n₁) ≠ shift(v,n₂)`. The argument needs amount-injectivity (e.g. "`w = v + i` with `i < n′ = n` contradicts `w = v + n` by injectivity of shift in its amount" later in the same lemma), so the cited TS2 does not discharge the step. The ASN's own Truncated-subtraction definition cites TS5 correctly for exactly this property, so the citations are internally inconsistent.
**Required**: Replace "(TS2, ASN-0034)" with "(TS5, ASN-0034)" at this site (and confirm the later "injectivity of shift in its amount" appeals route to TS5).

### Issue 2: Run convention miscites TS3 for the depth-generality of shift
**ASN-0084, "Correspondence-Run Decomposition Transformation" preamble**: "...the same last-component ordinal increment used for V-positions, applied to a deeper tumbler (valid at any depth, TS3 ShiftComposition, ASN-0034)."
**Problem**: The claim being supported is that `shift(a_s, k)` is well-defined on a depth-≥3 I-address and increments only the last component. That is OrdinalShift's content — `shift(v,n) = v ⊕ δ(n,#v)` is defined for any `v ∈ T` with postconditions `shift(v,n)ᵢ = vᵢ` for `i < m`, `shift(v,n)_m = v_m + n`. TS3 (ShiftComposition) is about composing two shifts (`shift(shift(v,n₁),n₂) = shift(v,n₁+n₂)`) and says nothing about depth-validity or single-shift behavior. The cited lemma does not establish the asserted fact.
**Required**: Cite OrdinalShift (ASN-0034) (`shift(v,n) ∈ T` and its component postconditions) for "valid at any depth," not TS3.

## OUT_OF_SCOPE

### Topic 1: Text subspace at depth m₁ > 2
**Why out of scope**: The ASN explicitly restricts to `m₁ = 2` so that ordinals are singleton tumblers identified with naturals. Extending the width/displacement arithmetic to multi-component ordinals (using D-CTG-depth's shared-prefix reduction to the last component) is new territory, correctly deferred, not an error here.

### Topic 2: Weakest precondition for the post-state invariant suite
**Why out of scope**: The ASN establishes invariant preservation in the forward direction and poses the wp question explicitly under Open Questions; a full wp characterization is genuinely future work.

VERDICT: REVISE
