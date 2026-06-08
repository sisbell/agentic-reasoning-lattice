# Review of ASN-0102

## REVISE

### Issue 1: J1'★ embedded discharge conflates the New/Old split (at COPY's pre-state) with the branch split (at the composite boundary)

**ASN-0102, X14 ("Setup for the J1★/J1'★ discharges" and the J1'★ bullet, branch (a))**: "In the embedded reading COPY's own step makes the genuine *step-local* extension `a ∈ ran(Σ_{i+1}.M(d)) ∖ ran(Σ_i.M(d))` and records `(a, d)`."

**Problem**: The `New`/`Old` partition is defined against COPY's *own* pre-state (`Old = A ∩ ran(Σ.M(d))`, `Σ = Σ_i` in the embedded reading), but the J1'★ branch (a)/(b) split is taken against the *composite boundary* `B = Σ_0`. In the embedded reading these two reference points differ, and the prose silently imports the `New`-style "genuine step-local extension" claim into branch (a) (defined at `Σ_0`).

Counterexample: let an earlier step of the composite (`Σ_0 →* Σ_i`) add content address `a` to `d`'s content-subspace range — e.g. a prior COPY, or a self-transclusion source already laid down — so `a ∉ ran_{s_C}(Σ_0.M(d))` but `a ∈ ran_{s_C}(Σ_i.M(d))`. If COPY then re-copies `a` (so `a ∈ A`), it falls in branch (a) at the boundary, yet COPY's mapping of `a` at a fresh copied position creates **no** step-local range extension (`a` is already in `ran(Σ_i.M(d))`). The asserted equality `a ∈ ran(Σ_{i+1}.M(d)) ∖ ran(Σ_i.M(d))` is therefore false for this `a`. The final validity is unaffected (the boundary obligation is correctly deferred to `ValidComposite★`), but the stated derivation overclaims.

**Required**: Separate the two splits explicitly — argue the step-local contribution against `Σ_i` (using `New`/`Old`) and the boundary obligation against `Σ_0` (using branch (a)/(b)) — or weaken the embedded branch-(a) sentence so it no longer asserts a step-local extension for every boundary-new address.

### Issue 2: Forward-reference / deferral accretion in the Amendment and X14

**ASN-0102, Amendment to ValidComposite★**: "The coupling discharge itself — and the standalone/embedded boundary reading it turns on — is carried out once, in X14."
**ASN-0102, X14, J1'★ bullet**: "a later step — e.g. a `K.μ⁻` removing exactly the copied content — could retract the range witness while the recorded pair persists by P2, leaving `(a, d) ∈ R_n ∖ R_0` with no boundary-level content-range extension."

**Problem**: The coupling discharge runs through a deferral chain — the Amendment points forward to X14, and X14's J1'★ in turn defers the boundary obligation to `ValidComposite★` — and X14 then imagines a downstream `K.μ⁻` step to motivate that deferral. The standalone-vs-embedded apparatus is carried twice (the `B = Σ` / `B = Σ_0` bifurcation is re-derived for J1★, J1'★, P4★, and P7a). This is meta-prose about *where* and *why* the discharge happens rather than argument that advances it; a precise reader must navigate the pointers to reconstruct a discharge that is, at its core, "COPY adds provenance for exactly the containment it creates and removes none."

**Required**: State the step-local discharge once, factor the standalone/embedded boundary reading into a single named lemma rather than re-running it per clause, and drop the imagined-`K.μ⁻` narration in favor of a one-line statement that the composite-boundary J1'★ is `ValidComposite★`'s clause-2 obligation.

## OUT_OF_SCOPE

(none — the four Open Questions are correctly posed as future work, not as claims of this ASN.)

VERDICT: REVISE
