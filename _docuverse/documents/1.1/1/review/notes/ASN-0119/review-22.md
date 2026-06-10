# Review of ASN-0119

This is a strong, rigorous note. The worked transpositions (pivot `ABCDE → ACDEB`, swap `ABCDEF → AEFCDB`) are arithmetically correct against R-P1/R-P2/R-S1–S3; the four contiguity cases each check out under the stated π; the atomicity composite (`A C D B E` intermediate) is verified; and the genuinely hard invariant — S8★ on the content subspace — is discharged with a real argument (R-BLK + R-CANON) rather than waved through. The S3★-via-π⁻¹ derivation and the P4★ range-invariance argument are both sound. The findings below are modest.

## REVISE

### Issue 1: Phantom "no-op REARRANGE" — a case the precondition excludes
**ASN-0119, Links (RA7a derivation)**: "We derive RA7a inline from RA1 rather than cite ASN-0098's LP11 (ReorderingBijection): REARRANGE_K is not K.μ~, and **the no-op REARRANGE** lies outside LP11's non-triviality hypothesis."

**Problem**: There is no no-op REARRANGE. ASN-0084's R-PRE forces `w_α ≥ 1` and `w_β ≥ 1` on every admissible cut sequence; a pivot relocates `β` to start at `c₀ < c₁` and a swap likewise, so `π` is never the identity and `M'(d) ≠ M(d)` for *every* valid REARRANGE. The clause invokes a case the carrier's own precondition rules out. It is also a vacuous *second* justification: the preceding reason — "REARRANGE_K is not K.μ~" — already fully discharges why LP11 (a lemma about K.μ~ transitions) is not the source for RA7a; LP11 cannot apply to a non-K.μ~ transition regardless of triviality. The same phantom recurs in the intro: "even though a **non-trivial** REARRANGE realizes the same *net* arrangement change" — the qualifier "non-trivial" presupposes a trivial REARRANGE that cannot exist, so it is redundant. This is precisely the anti-bloat pattern the classifier flags (a clause imagining an excluded case; a reader must stop to ask "what no-op? — I was told `w_α, w_β ≥ 1`").

**Required**: Drop the no-op clause; "REARRANGE_K is not K.μ~" stands alone as the reason to derive inline. Drop the redundant "non-trivial" qualifier in the intro, or replace it with the substantive distinction actually intended (atomic vs. the content-removed K.μ~ intermediate).

### Issue 2: "Fully accounted for" omits P3 (ExtendedTransitionInvariants)
**ASN-0119, Links (invariant accounting)**: "The remaining ExtendedReachableStateInvariants conjuncts (P6, P7, P8, P7a, P4a, the E-family ..., the L-family, the C-family) are preserved by the C/E/R/L frame, **so the invariant package REARRANGE joins is fully accounted for.**"

**Problem**: ASN-0047 carries *two* invariant theorems: ExtendedReachableStateInvariants (per-state + composite-boundary) and **ExtendedTransitionInvariants (P3)**. The note discharges the first theorem conjunct-by-conjunct and discharges the coupling obligations J0/J1★/J1'★, but P3 is never named. Since the note is *adding* REARRANGE to ASN-0047's transition vocabulary (it explicitly is not in K.α/K.δ/K.λ/K.μ⁺/K.μ⁺_L/K.μ⁻/K.ρ/K.μ~), it inherits the obligation to show P3 holds for the new transition. The claim "fully accounted for" therefore overstates what is shown.

The fix is one sentence — every conjunct of P3 (`dom(C) ⊆ dom(C')`, `dom(L) ⊆ dom(L')`, `E ⊆ E'`, `R ⊆ R'`, value-preservation on C and L) holds with equality by RA0, RA6, and the E/R frame — but the standards require every conjunct addressed, and the note's own meticulous enumeration makes the silence on P3 conspicuous.

**Required**: Add P3 (ExtendedTransitionInvariants) to the accounting, discharged by RA0 ∧ RA6 ∧ (E, R inert), or scope the "fully accounted for" claim to the reachable-state package so it no longer asserts coverage it does not provide.

## OUT_OF_SCOPE

### Topic 1: REARRANGE at V-position depth > 2
**Why out of scope**: The note confines itself to depth 2 because ASN-0084's REARRANGE_K is defined only there (CS4 fixes `#cᵢ = 2`). Depth-`m_S > 2` rearrangement would require extending the imported operation first; it is new territory, not a defect here. The note states the restriction honestly ("We make no claim about other subspaces or other depths").

### Topic 2: The note's own Open Questions
**Why out of scope**: Cross-document boundary-hood when a cut resolves to content interior to a transcluder's arrangement, unserialized concurrent rearrangements, the content-discovery-index invariant under footprint fragmentation, prior-arrangement recoverability, and the subspace-boundary guard for a formula-based displacement layer are all correctly deferred as future-ASN material rather than gaps in this one.

VERDICT: REVISE
