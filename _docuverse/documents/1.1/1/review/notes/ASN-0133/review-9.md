# Review of ASN-0133

## REVISE

### Issue 1: Closed-case claim in RG contradicts Q5a and misuses QD-fin

**ASN-0133, "The rule model" (RG)**: "The *closed* special case, in which no environment step ever fires and the registry alone moves the state, collapses that hypothesis to a restatement of its own conclusion (Q5a): the registry's reachable work is already pinned finite by QD-fin, leaving nothing to assume."

**Problem**: This claims the closed case auto-terminates ("reachable work is already pinned finite"), justified by QD-fin. Both halves are wrong, and the conclusion contradicts Q5a's own closed-case statement.

- QD-fin (ASN-0129) gives `[D]_Σ` finite *at each reachable Σ*. It says nothing about `⋃_k [D_ρ]_{Σ_k}` over the (generally infinite) sequence σ. Per-state finiteness is not cumulative finiteness, which is the quantity Q5a's bound and H-RF turn on.
- Q5a says the *opposite* about the closed case: "with the registry the only depositor, unbounded `⋃_k [D_ρ]` needs unboundedly many deposits, hence unboundedly many real fires, so there the implication reverses (bounded-domain-growth ⟺ H-RF)." That is an *equivalence*, which explicitly admits unbounded closed work (when the domain grows unbounded), not automatic finiteness.

Concretely, a closed registry can diverge while satisfying every Q5a hypothesis: one rule ρ, domain `M_K`, trigger `T_ρ(x) ≡ ¬(∃ m ∈ L_mark :: x ∈ coverage_G(m))` (SF), contract emitting *one* mark covering `x` (extinction-disciplined) *and* one fresh K-tuple. Each fire extinguishes its own argument yet deposits a new K-member that is itself trigger-true; `M_K` grows without bound, real fires are unbounded — all-SF, extinction-disciplined, closed, divergent. QD-fin bounds each `[D_ρ]_{Σ_k}` and not the union, exactly as Q5a's equivalence predicts and RG denies.

**Required**: Replace the QD-fin justification. The correct closed-case statement (matching Q5a) is that bounded-domain-growth becomes *equivalent* to H-RF, so the Q5a route carries no content beyond directly assuming H-RF — not that termination is free. State that a closed registry growing its own domain still diverges, so "leaving nothing to assume" must be read as "no assumption beyond H-RF," not "no assumption."

### Issue 2: Q6 asserts trigger-true arguments past N are "created" by the environment without deriving it

**ASN-0133, Q6 (TerminationUnderFairness)**: "Any `(ρ,x)` trigger-true at some `Σ_m`, m ≥ N … is … removed; … so it comes from an environment step. **Thus past N every trigger-true argument is both created and removed by the environment.**"

**Problem**: The preceding sentences establish only *removal* by the environment (no real fire past N can retract). The "created … by the environment" half is asserted, not derived, and is false for arguments that straddle N. An argument trigger-true at `Σ_N` was made trigger-true at some step `≤ N` — which can be a *registry* real fire re-arming it (in the non-SF case), not an environment step. The "Thus" presents a conclusion the argument does not yield. (It is non-load-bearing — regimes (i)/(ii) use removal and firing respectively — but it is stated as a derived fact.)

**Required**: Split the claim by epoch: any argument that *newly arises* trigger-true past N does so via an environment step (no-ops cannot change state, real fires are gone); any trigger-true argument is *removed* by an environment step. Drop the blanket "created … by the environment," which fails for arguments created at or before N.

### Issue 3: "Strong fairness" is relied on as a hypothesis but never stated as one

**ASN-0133, Q6 / Worked composition**: "… or a strong fairness fires every infinitely-recurring argument," and "the producer (non-grow-only domain) holding once the environment stops re-flagging uncommented targets, or under a strong fairness (Q6)."

**Problem**: The note's stated virtue is "termination as a conditional theorem with every hypothesis named," and H-FAIR is given a precise definition ("trigger-true at some `Σ_k` ⟹ eventually fired or removed"). Held quiescence over a non-grow-only domain — a stated outcome, including the worked example's producer — rests instead on a strictly stronger fairness that is only described in passing, never stated with H-FAIR's rigor as a peer hypothesis. A reader cannot pin its exact content (infinitely-often-enabled ⟹ eventually fired) from the inline phrase alone, and an honest conditional theorem should expose it.

**Required**: State strong fairness as a named hypothesis alongside H-FAIR (e.g., "H-SFAIR: every `(ρ,x)` trigger-true at infinitely many `Σ_k` is eventually fired"), and cite it by name where Q6 and the worked example invoke it.

## OUT_OF_SCOPE

### Topic 1: SF-certificate class (`pd_extinct`) and a PL surrogate for H-W
**Why out of scope**: These are correctly raised as the note's own Open Questions 1–2. Shipping a designated SF-certification class and a runtime-checkable necessary condition for bounded work are catalog/expressiveness additions that build on this note rather than corrections to it.

### Topic 2: Scheduler construction and the environment workload model
**Why out of scope**: H-FAIR and the environment steps are admitted abstractly, and the note's "What this note doesn't cover" deliberately leaves scheduler disciplines, fairness proofs, and which workloads supply bounded input to the protocol/implementation layer. That is a genuine boundary, not a gap — the substrate constrains neither.

VERDICT: REVISE
