# Review of ASN-0102

## REVISE

### Issue 1: P4★ invoked at COPY's pre-state, but P4★ is a composite-boundary property
**ASN-0102, self-transclusion example**: "COPY's provenance write `Σ'.R = Σ.R ∪ {(x_3, d)}` adds nothing not already present (`R' ∖ R = ∅` since `(x_3, d) ∈ Σ.R` by P4★ at the pre-state)."

**Problem**: In ASN-0047, P4★ (`Contains_C(Σ) ⊆ R`) is a *composite-boundary property* — it is listed under "composite-boundary properties: P4★ ∧ P4a ∧ P7a", explicitly **not** among the per-state invariants. COPY is an elementary transition that "may appear in the sequence" of a composite, so its pre-state `Σ` can be an intermediate (non-boundary) state at which P4★ need not hold. The example asserts `(x_3, d) ∈ Σ.R` directly "by P4★ at the pre-state," which is unjustified at an elementary step's pre-state.

This is not merely cosmetic: COPY's effect *unconditionally* records `(a_j+i, d)` for every copied address, including ones already content-subspace-range-resident (exactly the self-transclusion case). The soundness of this against J1'★ (ProvenanceRequiresExtension: new provenance ⟹ range-new) for an already-resident copied address rests entirely on that address's provenance pair already being in `R`. That fact follows from P4★ **at the composite's initial boundary** together with P2 (provenance permanence) — not from P4★ "at the pre-state."

**Required**: Either stipulate that the example's `Σ` is a composite boundary, or correct the justification to derive `(x_3, d) ∈ Σ.R` from P4★ at the composite's initial boundary plus P2. The X14 discharge should also state explicitly that COPY's unconditional provenance write is reconciled with J1'★ for already-resident copied addresses via boundary-P4★ + P2, rather than leaving this dependency implicit in one worked example.

### Issue 2: X2's allocation-handle derivation omits the first-emission case
**ASN-0102, X2**: "X2 fixes the concrete allocation handle that K.α consults: `d`'s next content address is drawn as `inc(a_prev, 0)` off the per-document frontier `a_prev = max{a' ∈ dom(Σ.C) : origin(a') = d}`."

**Problem**: K.α (ASN-0093) has two cases. The frontier `max{a' ∈ dom(Σ.C) : origin(a') = d}` is well-defined only in the *subsequent-emission* case (`{a' : origin(a')=d} ≠ ∅`). Consider a freshly registered document `d` (empty content subspace) into which COPY places **cross-origin** content (origin ≠ d): after COPY, `{a' ∈ dom(Σ.C) : origin(a') = d}` is still `∅`, so the next K.α is *first-emission* (`a = [d.0.s_C.1]`) and the `max` X2 names is over the empty set — undefined. The intended conclusion (next allocation handle unchanged by COPY) does hold in both cases, but the derivation as written only covers the subsequent-emission regime.

**Required**: Address the first-emission case — note that when `{a' : origin(a')=d}` is empty before and after COPY (cross-origin copy into a natively-empty document), the handle is the determinate first emission `[d.0.s_C.1]`, likewise unchanged by X1. Both K.α cases must be covered for X2's "frontier is identical" claim to be discharged.

### Issue 3: Internal redundancy and repeated downstream deferral (anti-bloat)
**ASN-0102, X14 and self-transclusion example**: the phrase "the record-with-residency the composite couplings consume" appears verbatim-in-substance in X14 ("the record-with-residency pairing the composite couplings consume") and again in the example ("This is the record-with-residency the composite couplings consume, with no new range entry to ground"). Likewise the deferral "[couplings] are ValidComposite★'s obligation, evaluated only between an embedding composite's initial and final states" is restated across X14 and the example.

**Problem**: Two passages in different sections say the same thing in different words and defer to the same composite-level location — the accretion pattern this note's classifier targets.

**Required**: State the SL-feeds-couplings fact and the composite-level deferral once (in X14), and have the example simply exhibit the instance without re-deriving the deferral.

## OUT_OF_SCOPE

### Topic 1: Discoverability of displaced/copied content under later operations
The first open question (origin vs. continued discoverability after subsequent displacement) is link-projection territory (ASN-0098), correctly left as a forward question rather than a claim here.

VERDICT: REVISE
