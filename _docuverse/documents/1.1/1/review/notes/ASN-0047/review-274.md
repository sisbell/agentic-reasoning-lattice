# Review of ASN-0047

## REVISE

### Issue 1: "K.μ~ range-invariance" jumps from content-range equality to full-range equality without the link step
**ASN-0047, *Decomposition of K.μ~* (K.μ~ range-invariance):** "applying the bijection equation `M'(d)(π(v)) = M(d)(v)` over the content-subspace positions gives the range equality ... and hence `Contains_C(Σ') = Contains_C(Σ)`, and a fortiori `ran(M'(d)) \ ran(M(d))` is empty."

**Problem**: The inline derivation establishes equality of the *content* range only (it applies the bijection equation "over the content-subspace positions"). The conclusion `ran(M'(d)) = ran(M(d))` is a statement about the *full* range, whose link half is not closed by what precedes the "a fortiori." `ran(M'(d)) = ran_C ∪ ran_L`; equality of the content half does not entail equality of the union. J3 (reordering isolation, `Contains(Σ') = Contains(Σ)`) and the P4★ K.μ~ cell both depend on full-range invariance, so this is load-bearing, not cosmetic. The needed fact — `M'(d)|_{dom_L} = M(d)|_{dom_L}` as functions — is genuinely available (sub-step (3) of the link-subspace fixity proof), but it is not the immediately-preceding content-only derivation that "a fortiori" points back to.

**Required**: Derive full-range invariance as the union of the content half (shown here) and the link half (sub-step (3)'s functional identity `M'(d)|_{dom_L} = M(d)|_{dom_L}`), and cite both at the "a fortiori" step. Then J3 may cite the combined result.

### Issue 2: Worked-example slot carries proof-architecture essay rather than verification
**ASN-0047, *Worked example: interior content replacement*, "Intermediate-state verification at M_int"**: "Two classes of property must be distinguished. The *per-state invariants* (...) hold at every intermediate state ... The *composite-boundary properties* (...) need *not* hold at M_int as a precondition ... we verify the Class (a) per-state invariants ... P4★ at M_int is a *consequence* ... not a requirement we must establish to take the step."

**Problem**: This restates the per-state / composite-boundary distinction already established in the *Extended reachable-state invariants* preamble. In a worked-example slot — whose job is to check named invariants against concrete tumblers — this is essay content reproducing the proof framework, the "forward-reference accretion" pattern the note's `review-mode.anti-bloat` classifier directs me to flag at source. The concrete checks that follow (`D-CTG★ at M_int`, etc.) are the substance; the framing paragraph is noise the precise reader must skip past to reach them.

**Required**: Drop the classification essay; keep the concrete per-state checks and the single sentence noting P4★ is restored at the trailing K.ρ. The general statement belongs once, in the preamble where it already lives.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
The ASN models link-arrangement contraction only by suffix removal (K.μ⁻), and explicitly defers interior `DELETEVSPAN`-style compaction to a future ASN (Open Questions, *D-CTG★/D-MIN★* modeling-choice note). This is correctly left open — interior withdrawal with survivor renumbering is new territory, not an error here.

META: not applicable — the ASN defines state (C, L, E, M, R), elementary transitions, and their invariants abstractly, with implementation citations as evidence rather than specification; it has not drifted into mechanics.

VERDICT: REVISE
