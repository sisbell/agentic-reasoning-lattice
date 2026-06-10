# Review of ASN-0118

The core operation is sound. I checked the resolution/placement decomposition, the K.μ⁻+K.μ⁺+K.ρ composite, the displacement tiling, and the provenance branch analysis, and found no correctness error of consequence. The boundary cases are genuinely covered: empty destination (ValidFirstInsertionPosition), append (`p = max+1`, `j = N`), front-insert (`j = 0`), self-transclusion (CP9), and zero-width (`W = 0` excluded by the `W ≥ 1` precondition). The worked two-source example checks out numerically (`[1,1]↦x₁, [1,2]↦a₁, [1,3]↦a₂, [1,4]↦b₁, [1,5]↦x₂`, origins `{d_A, d_A, d_B}`), and the CP7b link-discoverability wp is a real non-trivial analysis. The depth requirements (concrete example, non-trivial wp, derived consequences) are met.

The findings below are prose-economy (the `review-mode.anti-bloat` patterns the note carries) plus one completeness asymmetry. They are surgical.

## REVISE

### Issue 1: CP3c and CP6 carry parallel necessity-justification paragraphs that make the same point twice
**ASN-0118, operation section (CP3c effect clause and CP6 frame clause)**: CP3c — "CP3c is load-bearing: without it the effect clauses CP2/CP3a/CP3b *underdetermine* the post-state … a reader could admit a post-state in which `p` is bound both to `c₀` (CP2) and to the un-vacated `Σ.M(d)(p)` — a double binding that falsifies S2 … so … S2 is dischargeable *from the postconditions alone* … in exact step with that composite." CP6 — "the first is load-bearing for the same reason CP3c is … without the domain-equality conjunct, `Σ'.M(d)` is left underdetermined on subspaces ≠ s_C … The domain-equality conjunct is the non-text analogue of CP3c's text-domain closure … in exact step with the exhibited composite."

**Problem**: The two paragraphs argue the identical principle — *a domain-closure conjunct is needed because the other postconditions underdetermine the state, and closure makes the per-state invariant (S2 / S3★) dischargeable from postconditions alone* — and CP6 announces the duplication itself ("for the same reason CP3c is," "the non-text analogue"). Both also append the same "in exact step with the composite" remark. This is the flagged pattern (two paragraphs saying the same thing; defensive prose explaining *why a clause is needed* rather than what it says). A reader following the argument must absorb the same justification twice.

**Required**: State the closure principle once (the postconditions must pin the per-document domain so S2/S3★ are dischargeable without appeal to the exhibited composite), then let CP3c (text domain) and CP6's domain-equality conjunct (non-text domain) carry their formal content with at most a one-clause pointer. Drop the duplicated failure-mode narration and the repeated "in exact step with the composite."

### Issue 2: The "S3★-over-bound-positions, not ASN-0058 C1; ordinal-level not required" design-choice justification is repeated across three sites
**ASN-0118, V-spec section, resolution-restriction paragraph, and CP0(a)**: V-spec section — "so resolution integrity (CP0(a)) rests on S3★ over the bound positions, and the run-decomposition (CP0(c)) on the single-subspace premise so obtained — neither on `actionPoint(ℓ)`." Resolution-restriction paragraph — "grounds resolution integrity in S3★ over exactly the bound positions … rather than in ASN-0058's C1, whose stated precondition is the full binding we drop. As already argued, these arrangement-side facts … are the only premises … the span's ordinal-level form is not among them." CP0(a) — "we derive it from S3★ over the bound subset rather than cite C1, whose stated precondition is the full binding COPY discards."

**Problem**: The same two points — (i) resolution rests on S3★ over bound positions rather than ASN-0058's C1/full-binding, and (ii) ordinal-level form is not needed — are made at all three locations. The phrase "As already argued" is the author signalling the recurrence. This is forward/back-reference accretion: the design rationale is distributed and restated instead of placed once.

**Required**: Establish the "single-subspace + S3★ over bound positions, C1's full-binding dropped, depth-parametric" basis once (the resolution section is the natural home), and reduce the V-spec and CP0(a) instances to a bare statement of what each claim uses, without re-litigating the choice.

### Issue 3: The composite-validity argument discharges K.μ⁻ and K.μ⁺ elementary preconditions explicitly but leaves K.ρ's unstated
**ASN-0118, CP8 / operation section**: "To these arrangement steps the composite appends one K.ρ provenance step per range-new address." The surrounding text then argues only the couplings J0, J1★, J1'★ (ValidComposite clause 2).

**Problem**: ValidComposite clause 1 requires *each* step's elementary precondition at its intermediate state. The ASN spends a paragraph each discharging K.μ⁻'s retention-count and K.μ⁺'s S8a/depth/D-CTG★/referential-integrity preconditions, but never states that K.ρ's elementary precondition (ASN-0047, K.ρ: `a ∈ dom(C) ∧ d ∈ E_doc`) holds at the steps that fire. It is discharged — `cᵢ ∈ dom(C)` by CP0(a) with `dom(C)` framed across the composite (no K.α), and `d ∈ dom(M) = E_doc` by hypothesis; equivalently the J1'★ range-new condition forces `cᵢ` into the post-state content-range, which S3★ places in `dom(C)`. But the linchpin invariant-inheritance rests on COPY being a *valid* composite, and a reader checking clause 1 must self-supply the K.ρ discharge that the μ⁻/μ⁺ discharges are given for. The asymmetry is the finding.

**Required**: Add one line in the composite construction noting the K.ρ steps' elementary precondition (`cᵢ ∈ dom(C)` by CP0(a) + the content frame CP1; `d ∈ E_doc` by hypothesis), so clause 1 is discharged uniformly across all three step kinds.

## OUT_OF_SCOPE

### The Open Questions are correctly deferred
The width-shortfall under partial binding (ASN-0058 C2 unused, and verified unused — no COPY claim references nominal extent; CP3a shifts by the actual `W`), differing element-field depth across assembled sources, transclusion *into* the link subspace, and the correspondence relation across appearances are all genuinely new territory rather than gaps in COPY's definition. The operation is fully specified for the actual resolved `W` in each case. No action needed; flagging only to record that I checked these do not hide a present inconsistency.

VERDICT: REVISE
