# Review of ASN-0102

## REVISE

### Issue 1: X14's "already-resident" provenance discharge assumes Σ₀-residency it has not established

**ASN-0102, X14 (provenance reconciliation)**: "For an already-resident `a` — one with `a ∈ ran_{s_C}(Σ.M(d))` already at the pre-state (the self-transclusion case) — the pair `(a, d)` is already present in `R`: at the embedding composite's initial boundary `Σ_0`, `(a, d) ∈ Contains_C(Σ_0) ⊆ R` by P4★ ... and it persists to COPY's pre-state by P2."

**Problem**: The appeal to P4★ requires `(a, d) ∈ Contains_C(Σ_0)`, i.e. `a` content-subspace-resident in `d` *at `Σ_0`*. The only premise in hand is residency at COPY's pre-state `Σ`, which the text itself flags as "possibly-mid-composite." COPY is added to `ValidComposite★`'s atomic vocabulary (the Amendment), so a prior elementary step (e.g. an earlier K.μ⁺ or COPY) within the same composite may have introduced `a` into `d`'s range *after* `Σ_0`. In that case `a ∉ ran_{s_C}(M_{Σ_0}(d))`, so `(a, d) ∉ Contains_C(Σ_0)`, the P4★ step fails, and `(a, d)` may genuinely be `R`-new at COPY's pre-state (J1★ is only guaranteed at the composite's *final* boundary). The stated chain conflates pre-state residency with `Σ_0`-residency.

**Required**: Either restrict the appeal to the case where `a` was resident at `Σ_0`, or — the clean fix — drop the "already in `R`" claim and instead observe that for mid-composite residency `(a, d)` may be `R`-new, then show J1'★ is still satisfied at the composite level because `a` is range-new *relative to `Σ_0`*. Name the premises explicitly and stop routing through P4★ at `Σ_0`.

### Issue 2: X14 carries obligation-inventory and composite-coupling rationale prose that does not advance the argument

**ASN-0102, X14**: "As an elementary transition (Definition), COPY discharges here what such a transition owes: its frame, the per-state invariants, the transition invariant P3, and the *local* recording fact below." ... "The composite-level couplings (J0, J1★, J1'★) and the composite-boundary properties (P4★, P4a, P7a) are `ValidComposite★`'s obligation, evaluated only between an embedding composite's initial and final states, not the elementary step's; COPY's whole contribution to them is (SL) together with X1 — no allocation, so J0 is vacuous."

**Problem**: This is obligation-inventory and division-of-labor rationale (what a transition "owes," whose obligation a coupling is) rather than reasoning that establishes a postcondition. The same "(SL) + X1 ⟹ couplings, J0 vacuous" content is then restated in the claims table ("composite couplings J0/J1★/J1'★ follow from (SL) + X1 ... J0 is vacuous"), so two locations carry the same deferral. The anti-bloat classifier on this note flags exactly this accretion around forward references.

**Required**: Replace the obligation-inventory framing with the minimal load-bearing statement: COPY's only coupling-relevant contribution is (SL); J0 is vacuous by X1. Remove the duplicate restatement (keep it in one place — body or table, not both).

## OUT_OF_SCOPE

### Topic 1: Discoverability and containment of copied content under *subsequent* displacement
The Open Questions (origin/discoverability after a later displacement, re-sourcing of referenced content, identity when the allocating document is unreachable) are correctly posed as future work — they concern operations and reachability properties downstream of COPY's single transition and belong in later ASNs.

**Why out of scope**: These ask about composition with future operations and link-projection dynamics (ASN-0098 territory), not about COPY's own pre/post-state contract.

VERDICT: REVISE
