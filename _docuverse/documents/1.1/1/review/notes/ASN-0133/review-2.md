# Review of ASN-0133

This note is carefully built — the separation of recognizability/absorption (unconditional) from termination (conditional, hypotheses named) is the right architecture, and Q5's observation that the real-fires bound does *not* depend on extinction discipline is a genuinely sharp piece of accounting. The trouble is that the very next step undoes that sharpness.

## REVISE

### Issue 1: Q5a does not discharge H-W; it establishes the strictly weaker real-fires bound

**ASN-0133, Q5a / "What this note commits" (Q5 bullet) / Q6 discussion**:
- Q5a: *"For an all-SF registry ..., **H-W reduces to bounded domain growth**: real fires number at most `Σ_ρ |⋃_k [D_ρ]_{Σ_k}|` — each argument fires each rule at most once (Q-EXT), so **the only unbounded-work route is unbounded new arguments**."*
- Commit bullet: *"extinction discipline is ... only the cheapest way to **discharge H-W**, through the SF case (Q5a), which needs only domain-growth bounds."*
- Q6 discussion: *"it is the means to **discharge the meta-level H-W by a registration-checkable bound** (at-most-once per argument, Q-EXT, plus bounded domain growth, Q5a) rather than a reachability-quantified assumption."*

**Problem**: H-W is defined as `|W(σ)| < ∞` for every σ, where `W(σ)` counts trigger-**true** `(ρ, x, k)` instances *across all steps* — not real fires. Q5a's argument bounds the number of real **fires** (correctly, via Q-EXT's at-most-once), then silently re-labels that as a bound on *work*. It isn't: a trigger can be true at unboundedly many steps without ever firing.

Counterexample, all-SF and bounded-domain-growth: one rule ρ with the fixed two-element domain `{t, u}` (union over all states is `{t, u}` — bounded trivially), `T_ρ(t) = ⊤` (SF) and `T_ρ(u) = ⊥`. An unfair scheduler fires `(ρ, u)` forever — a no-op each step, since `T_ρ(u) = ⊥` (RG's no-op clause) — and never fires `(ρ, t)`. The sequence σ is infinite, the state is constant, and `T_ρ(t) = ⊤` at every `Σ_k`, so `(ρ, t, k) ∈ W(σ)` for all k: `|W(σ)| = ∞`. Bounded domain growth holds; H-W fails. So **bounded domain growth does not imply H-W**, and Q5a's "the only unbounded-work route is unbounded new arguments" is false — eternal starvation of an SF trigger-true argument is exactly the second route.

The note concedes this scenario itself, four lines later in the Q6 discussion: *"drop H-FAIR and a trigger-true argument can be starved eternally with the system never settling."* A starved SF trigger-true argument is precisely the `|W| = ∞` witness. The note both asserts (Q5a) that bounded domain growth gives H-W and admits (Q6) the starvation that refutes it.

What Q5a *actually* establishes is Q5's conclusion — finitely many real fires — which is strictly weaker than H-W and is the only fact Q6's proof consumes (*"After Q5's bound is exhausted every fire is a no-op"*). Q6 never needs `|W| < ∞`; it needs a finite real-fire count. So the termination result survives, but the stated derivation of it for all-SF registries is broken: Q6 is stated over H-W, bounded domain growth does not entail H-W, and the note never restates Q6 over the real-fires bound — it papers the gap with "discharge H-W."

Separately, the parenthetical *"registration-checkable bound (at-most-once per argument, Q-EXT, plus bounded domain growth, Q5a)"* mislabels bounded domain growth: `|⋃_k [D_ρ]_{Σ_k}| < ∞` quantifies over all reachable states, so it is itself reachability-quantified — every bit as meta-level as H-W. Only the SF/at-most-once half is registration-checkable. The move from H-W to bounded domain growth swaps one reachability-quantified assumption for another (plus a syntactic certificate); it does not eliminate reachability-quantification.

**Required**: Make the operative hypothesis of Q6 explicit and distinct from H-W — name "finitely many real fires from Σ₀" (the conclusion of Q5) and route Q6 through it. Then exhibit two suppliers of that hypothesis: Q5 (`H-W ⟹` finite real fires) and Q5a (`all-SF + bounded domain growth ⟹` finite real fires). Drop every claim that Q5a discharges or reduces H-W, and correct Q5a's "the only unbounded-work route is unbounded new arguments" to "the only unbounded-real-fire route ...". Finally, stop attributing "registration-checkable" to bounded domain growth; only SF membership earns that word.

### Issue 2: Scope is defined over addresses, but rule domains can be tuple-valued

**ASN-0133, SC / Q7**: *"A scope is any Boolean PL predicate `S` over addresses; `quiescent_{R,S}(Σ)` restricts Q0's inner quantification to arguments satisfying S."* and Q7: *"the scope `S` adds a PC1 filter to each rule's inner quantification (`{x ∈ [D_ρ]_Σ : S(x)}`, a QD filter)."*

**Problem**: A rule's domain `D_ρ ∈ QD` may be tuple-valued. The note's own worked example sets the resolver's domain to `L_cmt` (the audit slice — a set of tuples), and RG fires `(ρ, x)` on `x ∈ [D_ρ]_Σ`, so there `x` is a tuple. The scope filter `{x ∈ [D_ρ]_Σ : S(x)}` then applies an address-predicate `S` to a tuple `x` — a sort mismatch. ASN-0129's filtering former requires `P : D × S → Bool` *at D's sort*; an address-predicate is not such a P over `dom(Tup)`. So as written, `S(x)` does not well-type for tuple-valued domains, and Q7's claim that scope quiescence "carries Q0's status exactly" is unestablished for every Binary/Multi resolver-style rule — including the worked example's `ρ_R`.

**Required**: Specify how a scope restricts a tuple-valued domain — e.g., `S(addr(x))`, or `S` over a named projection of the tuple — and confirm the result is a QD filter at the domain's sort. Then Q7's PL-membership claim holds for tuple-domained rules.

## OUT_OF_SCOPE

### Topic 1: Shipping the SF certificate (`pd_extinct`)
The note correctly identifies (Open Question 1) that Q-EXT/Q5a make SF membership the load-bearing registration check, while ASN-0130 ships only the ST⁺ certificate. Designating an SF-certification class is new substrate-content territory, not a defect here. (Note: this is the registration-checkable *half* of Issue 1's fix — it does not by itself supply the bounded-domain-growth half.)

### Topic 2: A PL-expressible runtime surrogate for the work bound
Open Question 2's hunt for a per-state PL predicate whose failure certifies unbounded work is genuinely future work, and is sharpened by Issue 1: since neither H-W nor bounded domain growth is PL-expressible, the question is which *finite-real-fire* witness, if any, admits a PL necessary condition.

### Topic 3: Scheduler construction / discharging H-FAIR
The note deliberately states H-FAIR as a hypothesis and ships no scheduler. Constructing fair disciplines and proving they satisfy the statement belongs to the operational layer, as the note says.

VERDICT: REVISE
