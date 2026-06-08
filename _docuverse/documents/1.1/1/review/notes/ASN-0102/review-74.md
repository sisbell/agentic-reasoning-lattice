# Review of ASN-0102

## REVISE

### Issue 1: P4a discharged at the wrong state — "Σ' is a trace state" is unsound in the general case

**ASN-0102, X14 (P4a discharge)**: "P4a: each new pair `(a_j + i, d)` is witnessed by COPY's own post-state arrangement `Σ'.M(d)` (`a_j + i ∈ ran(Σ'.M(d))` at a content-subspace position, X14), and `Σ' is a trace state`."

**Problem**: P4a (TraceWitnessing) is a *composite-boundary* property whose witnesses `Σ_k` must be boundary states drawn from the transition history `{Σ_0, …, Σ_n}` (with `M_k` the arrangement at boundary `Σ_k`). COPY's post-state `Σ'` is an *elementary* post-state; when COPY appears mid-composite it is not a boundary, so "Σ' is a trace state" is false in general — it holds only for the standalone case where `Σ' = Σ_clo`. Note the inconsistency: the parallel P4★ and P7a discharges in the same section correctly reason at the closing boundary `Σ_clo`, while P4a reverts to `Σ'`. The conclusion does in fact hold — but for a different reason: composite-wide J1'★ forbids recording `(a, d)` unless `a` is range-new across `B →* Σ_clo`, which forces `a ∈ ran_{s_C}(Σ_clo.M(d))`, so `Σ_clo` is the genuine witness. The justification as written does not establish this.

**Required**: Discharge P4a at the composite boundary `Σ_clo`, mirroring the P4★ argument: every pair COPY contributes is either already in `R_B` (and witnessed by `B`'s pre-existing P4a) or is range-new and hence range-resident at `Σ_clo` by J1'★, which then witnesses it. Drop the claim that `Σ'` is a trace state.

### Issue 2: Trailing restatement at the end of X14 (anti-bloat)

**ASN-0102, X14, final paragraph**: "By content-containment permanence this record persists across subsequent states (the address remains discoverable as contained in `d` even if `d` later drops it from its arrangement), recorded against the *destination* document `d`, not the content's original creator."

**Problem**: This sits after the full coupling/invariant/P3 discharge and adds no new reasoning. It restates X14's own containment-recording effect (`Σ'.R = Σ.R ∪ {(a_j+i, d)}`) and re-glosses attribution already covered by X6. Essay content in a proof slot — the same trailing-sentence pattern prior cycles trimmed (cf. commit `83b2dc5f4`).

**Required**: Delete, or fold the single load-bearing fact (provenance recorded against destination `d`) into the effect Definition where `Σ'.R` is given.

### Issue 3: Repeated citation gloss for ASN-0058 C1 (anti-bloat)

**ASN-0102, X3 / wp paragraph / X5**: the parenthetical "(resolution yields only existing addresses)" attached to C1 recurs verbatim across three locations (X3 derivation, the `wp(COPY, S3★)` discharge, X5).

**Problem**: The same citation gloss restated three times is noise the reader steps over. The fact `a_j + i ∈ dom(Σ.C)` is established once in PC1/the wp computation; downstream uses need only cite it, not re-explain it.

**Required**: State the C1 consequence once (at PC1 or the wp step) and reference it thereafter without the recurring parenthetical.

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content under later displacement (Open Question 1)
**Why out of scope**: Link projection over `ran(M(d))` after subsequent shifts is link-model territory (ASN-0098 LP-series), correctly deferred as an open question rather than specified here.

### Topic 2: Provenance/containment chaining when a reference-obtained document is itself a source (Open Question 2)
**Why out of scope**: Cross-document provenance composition is new territory beyond COPY's single-operation contract.

META: not applicable — the ASN defines a state transition, its effect on all five state components, and discharges the abstract invariants, staying squarely in specification territory.

VERDICT: REVISE
