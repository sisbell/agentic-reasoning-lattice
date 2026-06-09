# Review of ASN-0118

I worked through the resolution/placement split, the composite decomposition, the displacement tiling, the provenance derivation, the wp analysis, and the worked example. The ASN is unusually rigorous — the no-holes tiling is derived from ordinal arithmetic rather than hand-waved, the provenance obligation is read off J1★/J1'★ with correct initial-to-final scoping, and the link-discoverability wp is genuinely non-trivial. Two gaps remain.

## REVISE

### Issue 1: Displacing-case decomposition does not discharge CP6 for the link subspace
**ASN-0118, "The COPY operation" (displacing-case composite) and CP6**: the K.μ⁻ step is described as "contracts d's text subspace to the retained prefix [min, p) — retention count n'_{s_C} = j", and CP6 asserts `(A v : subspace(v) ≠ s_C : Σ'.M(d)(v) = Σ.M(d)(v))` — the link-subspace V-positions of `d` are preserved.

**Problem**: K.μ⁻ (ASN-0047, per-subspace scope) contracts to `M'(d) = M(d) ↾ R` with `R = ⋃_S {[S,1,…,1,k] : 1 ≤ k ≤ n'_S}`. The decomposition fixes `n'_{s_C} = j` but never specifies `n'_{s_L}`. If `d` holds link-subspace V-positions, an unspecified `n'_{s_L}` leaves the contracted arrangement ambiguous and, on the natural "only one subspace named" reading, would drop `d`'s link arrangement — which K.μ⁺ then does not re-add. The composite as written therefore does not visibly establish CP6's `subspace(v) ≠ s_C` conjunct; the stated frame and the exhibited decomposition are not reconciled. This is exactly a "hard conjunct skipped" case.

**Required**: State in step (i) that K.μ⁻ retains the link subspace in full (`n'_{s_L} = n_{s_L}`, a non-strict retention permitted since the text subspace already supplies the required strict contraction `j < N`), and note that K.μ⁺ in step (ii) adds only `s_C` positions — so the link-subspace arrangement is carried through both steps unchanged, discharging CP6.

### Issue 2: Worked example does not exercise CP8, the most intricate postcondition
**ASN-0118, "A worked assembly from two sources"**: the example verifies CP1, CP2, CP3a, and CP11 numerically but omits CP8 (provenance), whose derivation (composite decomposition, J0 vacuity, J1★/J1'★, the P4★/P2 already-referenced branch) is the heaviest analytic content of the ASN.

**Problem**: Per the depth standard, the key postconditions should be checked against a concrete scenario; the postcondition with the longest proof receives no numeric instantiation. The example is the natural place to demonstrate the range-new versus already-referenced classification that the CP8 derivation hinges on.

**Required**: Extend the example to classify each resolved address against `d`'s pre-state content range `{x₁, x₂}` — all of `a₁, a₂, b₁` are range-new, so each triggers a K.ρ step yielding `(a₁,d), (a₂,d), (b₁,d) ∈ Σ'.R` — and exhibit at least one already-referenced case (e.g., re-placing `x₁`) so the P4★/P2 branch is shown to fire rather than a redundant K.ρ.

## OUT_OF_SCOPE

### Topic 1: Partial binding, overlapping/repeated spans, mixed-depth assembly, later link removal, correspondence, link-subspace transclusion
**Why out of scope**: These are the ASN's own listed Open Questions and concern operations or relations beyond COPY's placement semantics. Note that interior partial-binding is in fact precluded for text sources by D-CTG/D-SEQ (the content subspace is always a contiguous run), so the only realizable partiality is span overreach past the bound top — the ASN's `act = dom ∩ ⟦σ⟧` truncates this soundly, and the deferred question (error vs. silent truncation) is genuinely future territory.

VERDICT: REVISE
