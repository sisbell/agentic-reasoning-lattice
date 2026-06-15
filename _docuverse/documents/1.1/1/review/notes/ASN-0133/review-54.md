# Review of ASN-0133

I checked the load-bearing proofs and they hold. Specifically I verified: Q0's heterogeneous-merge completeness (every view-sensitive atom class is covered, and top-level `active` is in fact a universally viable choice — active readings native, audit via the fixed-view bases `L_K`/V-AUD, default via the UV filter); Q5's per-σ injection by step index; Q5a's at-most-once bound and its closed/open asymmetry; Q-EXT's step-agnostic permanence (SF false survives environment steps because PD0 ⊥-stability quantifies the step relation); the H-SFAIR regime form and its exclusion of obstruction case (3); and the worked-composition terminal sequence (Σ₀→Σ₁→Σ₂ arithmetic and the nested-quantifier evaluation at Σ₂ both check out). No correctness defect found. The findings are one hypothesis-attribution imprecision and residual meta-prose the anti-bloat pass should remove.

## REVISE

### Issue 1: Regime (ii) attributes the structural fire bound to "all-SF," which Q5a's own text refutes

**ASN-0133, Q6 proof, regime (ii)**: "all-SF bounds the real fires structurally (Q5a ⟹ H-RF, so N exists by Q5a's structural route ... Q5a's bounded-domain-growth hypothesis still in force)"
And in the package list: "+ **Q5a's package, non-grow-only**: all-SF makes the registry's *work* finite..."

**Problem**: Q5a states the opposite in plain terms — "SF alone does not bound the count" — and exhibits the counterexample (an SF trigger emitting something other than its own falsifier fires unboundedly on a fixed argument). The bound needs the *full* Q5a package: all-SF **and** extinction discipline **and** bounded growth. The regime (ii) prose leads with "all-SF bounds" and re-mentions only bounded growth, silently leaning on extinction discipline from the bullet list. This is the precise misreading Q5a guards against, reintroduced in the proof's topic phrasing.

**Required**: Attribute the structural bound to "Q5a's package" (or "the all-SF, extinction-disciplined registry under bounded growth"), consistently, in both the package list and the regime (ii) derivation. Do not let "all-SF" stand as the subject of "bounds the real fires."

### Issue 2: Residual meta-prose — deferred-layer inventories and re-explained concepts

The anti-bloat classifier is active; these are the specific instances I had to read past:

- **(a) Scheduler inventory, H-FAIR**: "any discipline satisfying the statement (round-robin, queue-fair, priority with aging) discharges it". Schedulers are explicitly deferred ("What this note doesn't cover: A scheduler"). The reasoning needs only "any fair discipline"; the three-name list is decorative content from a deferred layer.
- **(b) Naive-merge re-explained, Q0 → worked example**: Q0 states "What that blocks is only the naive merge — the one that leaves each view-parameterized atom at its native view"; the "Heterogeneous rewrite, worked" preamble then restates it — "the naive merge — leaving each view-parameterized atom at its native view — is wrong at one conjunct or the other." Same content, different words. The example itself (R′, the value checks) is fine; cut the preamble's re-definition and let the example begin.
- **(c) Actor inventory, RG**: "other agents, other registries, and whatever feeds the docuverse its raw work all emit through the same surface" — the load-bearing point is "non-registry actors emit through the same surface"; the enumeration is decoration (weakest of the three, since it does introduce the environment).

**Required**: Delete (a) and (c)'s enumerations; remove the naive-merge restatement in (b).

## OUT_OF_SCOPE

### H-SFAIR satisfiability against an adversarial environment
Whether any scheduler can *achieve* H-SFAIR when the environment withdraws an argument before every scheduled fire (case (3)'s mechanism) is a real question, but it is correctly deferred — the note states H-SFAIR as a hypothesis and consigns "the turn/serialization model H-SFAIR's satisfiability needs" to the implementation layer. Not a defect in this note; flagging only to confirm I am not treating the deferral as a gap.

### The SF certificate (pd_extinct)
Open Question 1 correctly identifies that SF membership is the uncertified load-bearing check and that no `pd_extinct` class ships. This is genuine future catalog growth, not a revision to ASN-0133.

VERDICT: REVISE
