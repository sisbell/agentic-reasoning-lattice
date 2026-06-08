# Review of ASN-0102

## REVISE

### Issue 1: `Contains_C ⊆ R` is used as both a non-invariant and a per-step inductive hypothesis

**ASN-0102, X14 (P4★ discharge)**: "P4★ is a composite-boundary property, not a per-state invariant, so we do not assert it at the mid-composite state Σ ... assuming the inductive hypothesis `Contains_C(Σ) ⊆ Σ.R` entering COPY, we derive `Contains_C(Σ') ⊆ Σ'.R` leaving it ... Since the inclusion holds at the initial boundary and is preserved by every elementary step, P4★ holds at every composite boundary."

**Problem**: The predicate assumed as the entering inductive hypothesis (`Contains_C ⊆ R`) is exactly P4★, which the same paragraph declares "not a per-state invariant" that does not hold at mid-composite states. The argument then claims this inclusion "is preserved by every elementary step." That is false: K.μ⁺ (content-subspace ArrangementExtension, ASN-0047) grows `Contains_C` without growing `R` (its frame is `R' = R`), so after a K.μ⁺ and before its coupled K.ρ the inclusion fails — which is precisely why J1★/P4★ are composite-boundary properties rather than per-state invariants. COPY is an elementary transition "applicable at intermediate states," so its entering state Σ may be mid-composite with `Contains_C(Σ) ⊄ Σ.R`. The discharge thus assumes the very thing it concedes can fail.

**Required**: Discharge P4★ at the composite level (initial-to-final), invoking J1★ on the prior step to guarantee recording by the closing boundary, rather than via a per-elementary-step invariant `Contains_C ⊆ R` that K.μ⁺ refutes. State the actual frame assumption COPY relies on (e.g., that the only `s_C`-range growth at COPY's own step is the addresses COPY itself records).

### Issue 2: J1'★ Old-branch discharge inherits the unsound assumption

**ASN-0102, X14 (J1'★)**: "For `a ∈ Old`... `(a, d) ∈ Contains_C(Σ)`, and the entering inductive hypothesis `Contains_C(Σ) ⊆ Σ.R` ... gives `(a, d) ∈ Σ.R`. Hence `(a, d) ∉ Σ'.R ∖ Σ.R` and the antecedent is vacuous for `a ∈ Old`."

**Problem**: This rests on the same `Contains_C(Σ) ⊆ Σ.R` assumption flagged in Issue 1. Construct the failing case: within one composite, a K.μ⁺ places content address `a` into `d`'s content subspace (so `a ∈ ran(Σ.M(d))`) but its K.ρ has not yet fired, so `(a,d) ∉ Σ.R`. A subsequent COPY in the same composite whose source resolves to `a` then has `a ∈ Old`. COPY records `(a,d)`, so `(a,d) ∈ Σ'.R ∖ Σ.R` — the J1'★ antecedent fires — yet `a` is **not** range-new (it was already in `ran(Σ.M(d))`), so J1'★'s consequent fails. The "vacuous for Old" conclusion does not hold at such an entering state.

**Required**: Either evaluate J1'★ composite-wide (where the prior step is responsible for the pair) or restrict the Old-branch to addresses provably already in `Σ.R` at COPY's entering state, with a justification that does not assume P4★ mid-composite.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by later operations
**Why out of scope**: The first open question (origin/discoverability of copied content under a later displacement) concerns subsequent operation mechanics and discoverability dynamics; it belongs to a future ASN, not to COPY's contract.

### Topic 2: Cross-time view divergence and unreachable allocating documents
**Why out of scope**: The third and fourth open questions (time-varying resolution of shared references; identity when the allocating document is unreachable) introduce temporal/reachability territory the present state model does not yet formalize.

VERDICT: REVISE
