# Review of ASN-0102

## REVISE

### Issue 1: PC3 is labeled a precondition but the text derives it as forced, and surrounds it with defensive meta-prose

**ASN-0102, Precondition (PC3)**: "The target subspace is the content (byte) subspace: `S = s_C`. … The target V-position subspace is then forced by S3★ … The reading runs from the placement obligation to the V-position subspace — a content image forces an `s_C` slot — not from the copied address's `subspace_I` (which is an image-routing fact discharged in the `wp` computation below, over distinct objects: the V-position projector `subspace(v) = v₁` ranges over `dom(M(d))`, the address projector `subspace_I` over `dom(C)`)."

**Problem**: Two defects compound here. (a) PC3 sits in the precondition list, but the body argues `S = s_C` is *forced* by X1 + C1 + store disjointness + S3★-aux — i.e. it is a consequence, not an independent assumable input. A "precondition" that the ASN proves cannot be otherwise is mislabeled. (b) The parenthetical disambiguating `subspace(v)` from `subspace_I` "over distinct objects" is meta-prose that defends against a confusion rather than advancing the derivation; it reads as a prior finding's content relocated into the precondition slot and forward-references "the `wp` computation below."

**Required**: Either state COPY's content-subspace targeting as a definitional choice (one sentence) and drop the forcing argument, or move the forcing argument out of the precondition list into the X1/S3★ derivation where it belongs. Delete the `subspace(v)` vs `subspace_I` disambiguation parenthetical.

### Issue 2: The J1'★ "Residence destroyed" sub-case is drift — it discharges by assigning blame to another operation

**ASN-0102, X14, J1'★ discharge**: "the resulting stranded pair `(a, d) ∈ R_clo ∖ R_B` … is a genuine composite-wide J1'★ violation — but the *offending step is that contraction, not COPY*. … The obligation not to strand a provenance-recorded address by contracting it away is borne by that K.μ⁻'s position in the composite — a constraint on which composites are *valid* — leaving COPY's recording blameless."

**Problem**: This paragraph is essay content reasoning about K.μ⁻'s contract, not COPY's specification. J1'★ is a property of the whole composite; if it is violated the composite is invalid regardless of which step is "to blame." Assigning blame to K.μ⁻ and asserting an obligation "borne by that K.μ⁻'s position" neither establishes that constraint anywhere nor advances what COPY guarantees. It is new prose around a coupling that explains why a downstream operation must behave, rather than what COPY does.

**Required**: Reduce the claim to what COPY actually establishes — at COPY's own post-state `Σ'` the recorded address is range-resident — and drop the K.μ⁻ blame analysis. If the "do not contract away a provenance-recorded address" constraint is real, it belongs to K.μ⁻'s contract (out of scope here), not to COPY's discharge prose.

### Issue 3: The coupling-discharge section (X14) carries two competing splits of `A` and repeated boundary deferrals

**ASN-0102, X14**: the New/Old split is "taken at `Σ`, not at the boundary `B`," while the J1'★ argument states "We split `A` *at the opening boundary `B`*," and J1★/P4★ both defer through "(SL)" and "each other step discharging its own additions."

**Problem**: Maintaining two different partitions of the same set `A` (one at `Σ`, one at `B`) across adjacent paragraphs, plus repeated deferral to the same `(SL)` fact and to "each other step," makes the reader reconstruct which split governs which coupling. This is accreted meta-structure around the couplings rather than a single clean discharge. The note's `anti-bloat` classifier targets exactly this.

**Required**: Use one split, state `(SL)` once, and discharge J0/J1★/J1'★/P4★ against it in sequence without re-deriving the partition per coupling.

### Issue 4: "COPY allocates nothing" is restated across many discharge bullets

**ASN-0102**: the same fact (`Σ'.C = Σ.C`, no allocation) grounds X1, X2, X3, X5, the S4 discharge, the J0 discharge, the P7a discharge, and several entries in the invariant list ("Preserved because COPY's frame leaves `Σ.L` and `Σ.E` untouched …").

**Problem**: Two or more discharge entries say the same thing in different words (frame-untouched ⇒ invariant preserved). The per-conjunct invariant list is largely a mechanical repetition of "this clause quantifies over a frozen component."

**Required**: Group the frame-trivial invariants (those quantifying solely over `C`, `L`, `E`, or their tumbler structure) into one statement citing the frame once, rather than restating the frame argument per clause.

## OUT_OF_SCOPE

### Topic 1: Behavior when copied content is later displaced, re-sourced, or its allocating document becomes unreachable
**Why out of scope**: These are the note's own Open Questions and concern subsequent operations (displacement, further references, reachability) — future-ASN territory, not defects in COPY's specification.

VERDICT: REVISE
