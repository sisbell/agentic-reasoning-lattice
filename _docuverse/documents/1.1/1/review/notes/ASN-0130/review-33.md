# Review of ASN-0130

I checked this note against its dependency tower with particular attention to the three places it could fail: the registration/typing/acyclicity dependency tangle (PR-SIG ↔ PR2 ↔ PR0), the expansion well-typing proof (PR3a), and the ST⁺ soundness lift (PR5). All three hold. I record the verification below so the convergence is auditable, then one out-of-scope observation.

## REVISE

None. The hard obligations are discharged:

- **Acyclicity (PR2) is genuinely event-wise, not definition-wise.** The note correctly notices that de-registration re-opens registration, so "registration order" must be an order on *events*. Part (a) (`e₁(r) < e₁(D)`) rests on PR0(iv) + the parse, not on `sig`, so it does not circularly depend on PR-SIG. Part (b) (self-reference) is airtight: at a miss every existing tuple denoting D's start is I0-equal to D's (PR-ENC-uniq) hence inactive, so (iv) has no witness — and the "first self-referencing deposit" minimization closes the induction. The dependency chain PR0(iii) → PR-SIG → PR2(a) → PR0(iv) terminates at distinct PR0 conjuncts; no cycle.

- **Expansion well-typing (PR3a) does the substitution work.** WT-α and WT-W are each conditioned on exactly the freshness PR3's renaming arranges; the `k`-fold PC2 discharge "last parameter first" is correct (simultaneous = sequential since no `yⱼ ∈ Eᵢ`), and the no-capture/no-interference clauses are verified against `Eⱼ`'s free variables lying in `dom(Γ)`. The parameter-and-binder co-renaming is what makes one freshness pass cover both — confirmed by the worked `chkW` contrast (host `x` would land under `quiescent_v1`'s `A_W` binder absent the rename).

- **ST⁺ soundness (PR5) survives the parametric lift.** Treating each parameter as a bound constant matches PD0's side conditions on every rule except the aggregate threshold ("ℕ literals"); the explicit extension to "ℕ literal or environment-bound parameter" is sound because the threshold is fixed across a step (same `args` both sides), so "count over a growing set never decreases" carries verbatim. The `count(L_W) ≥ x` example correctly motivates the non-redundancy. The three qualifications (purity → certify the expansion; view → certify only view-independent expansions; parameters → per-instantiation) are each load-bearing, and the worked `quiescent_v1` (refused: `A_W` not grow-only) vs `armed` (`L_Done`/`L_W` grow-only, ST⁺) exercises the gap PR5 turns on.

- **The wp analyses (PR0, PR5a) are weakest, not merely sufficient.** The two-disjunct partition is shown necessary (each negated sub-case falsifies POST-ref) as well as sufficient, and the standing-incumbent-vs-`VALID` divergence (a de-registered referent fails `VALID` while a's own registration stands) is correctly surfaced.

- **Boundaries handled:** empty `A_def` (cond. 0), `k=0`/bare references (PR-SIG, expansion), de-registered targets (PR1 conjunct-(iv) staleness, evaluation keys on ever-registration), overlapping runs at distinct starts (PR-ENC-uniq + start-anchored resolution), born-nullified deposits (C3), and the frontier-ghost adversary (cond. iv asks strictly more than residence) are each addressed.

- **PR-DISC scoping is discharged consistently with the foundation.** PR-DISC has the same status as ASN-0128's SD: it holds for derivations driven through the exposed surfaces, and PS1/PS2's entry-point seal discharges it there. A raw `K.λ_sh` could in principle deposit a `pdef` tuple, but that is off-surface exactly as a raw R-class `K.λ_sh` is off-SD — the note states the qualification ("for the shipped surfaces") honestly.

On the anti-bloat lens: the flagged patterns (ordering-justification prose, "why the axiom is needed" labels, content duplicated across sections, multiple forward-deferrals of the actual argument) are substantially absent — PR5a defers *backward* to PR0/PR1 rather than restating, and the labeled sub-paragraphs (PR5's Purity/View/Parameters) are definitional axes of ST⁺, not rationale. The remaining orienting sentences (e.g. PR3a's "this lemma supplies what PR3's evaluation clause actually consumes") and editorial phrases ("This is harmless") are brief and attached to load-bearing content — below the threshold of "noise the precise reader must work around." I am not manufacturing a REVISE from them.

## OUT_OF_SCOPE

### Topic 1: Expansion size and sharing
PR3 establishes that `expand(a)` terminates in a finite pure term, which is all PR3a/PC5 require. It says nothing about *size*: a diamond-shaped reference DAG (D references r twice, r references s twice, …) yields expansions whose size is exponential in DAG depth. This breaks no abstract claim — termination, well-typing, purity, and decidability all hold for finite terms of any size — but a builder will want a shared/memoized expansion representation or a bound.
**Why out of scope**: This is a representation/efficiency concern for the implementation or a future ASN, not a defect in any guarantee this note states. The note's "decidable" and "terminates" claims are correct as written.

VERDICT: CONVERGED
