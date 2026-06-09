# Review of ASN-0116

The technical core is sound. I checked the valid-composite decomposition (`K.α`×n → `K.μ⁻` → `K.μ⁺` → `K.ρ`×n), the per-step precondition discharge, the coupling constraints J0/J1★/J1'★, the contiguity argument over the three index intervals, and all four named boundary cases (append, empty subspace with both content-region sub-cases, front insertion at `J=1` with `n'_{s_C}=0`). The interval/disjointness reasoning, the block-position attribution split between I3-V and I3-CS, the non-circular use of ExtendedReachableStateInvariants, and the WP analysis (containment vs. emptiness, with the LP19a tight-endset corollary) all hold. No technical REVISE items.

The remaining findings are duplication/meta-prose, which the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Duplicated RAN-coupling reasoning across two sections
**ASN-0116, valid-composite clause 2 vs. coherence-section provenance paragraph**:

Clause 2 states: "all three are driven by the range identity RAN (Effect), by which the I-addresses *new to the content-subspace range* of M'(d) are exactly A_new = {shift(a, k) : 0 ≤ k < n}, the shifted-suffix addresses being range-old."

The coherence section then says: "(The three couplings J0, J1★, J1'★ are discharged with the valid composite above, all driven by the range identity RAN — the I-addresses *new to the content-subspace range* of M'(d) are precisely A_new = {shift(a, k) : 0 ≤ k < n}, the shifted-suffix addresses being range-old, which is why I-PROV records *only* A_new ...)."

**Problem**: This is the "defer to downstream location" and "two paragraphs say the same thing in different words" patterns combined. The second passage *both* defers to the valid-composite section ("discharged with the valid composite above") *and* re-derives the identical RAN→A_new/range-old reasoning. A reader following the provenance argument must recognize this as a verbatim repeat of clause 2.
**Required**: Pick one site for the RAN-driven coupling reasoning. The coherence-section parenthetical should defer only (e.g., "J0/J1★/J1'★ are discharged with the valid composite above"); drop the re-derivation, keeping there only the genuinely new content (the P7a/P7 proofs).

### Issue 2: Anticipatory use-site justifications in the precondition slot
**ASN-0116, INSERT Precondition**: "`Σ` is reachable from `Σ₀` … — so the per-state invariants together with the composite-boundary properties …, in particular P7a (ProvenanceCoverage), hold at the pre-state"; and "`(A k : 0 ≤ k < n : w_k ∈ Val)` — each inserted unit is a well-formed content value, the typing obligation the K.α step below carries (ASN-0093: K.α commits `a ↦ v` only for `v ∈ Val`)".

**Problem**: Both clauses name a downstream consumer rather than advancing the precondition — "in particular P7a" anticipates the coherence-section coverage proof, and "the typing obligation the K.α step below carries" explains *why* the `w_k ∈ Val` clause appears rather than stating it. This is the "definition's introduction enumerates downstream consumers" pattern in a structural slot.
**Required**: State the precondition (reachable, hence composite boundary; `w_k ∈ Val`) and invoke P7a / the K.α typing obligation at their points of use.

## OUT_OF_SCOPE

(none — the Open Questions correctly route transclusion-at-shared-position, concurrent-insert freshness, transclusion provenance, and post-edit fragmentation to future ASNs rather than claiming them here.)

VERDICT: REVISE
