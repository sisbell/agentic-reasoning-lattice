# Review of ASN-0086

## REVISE

### Issue 1: R0's freshness conclusion is invoked over the full state space but proven only for →*-reachable states

**ASN-0086, Definition — Emit_K / Definition — Nullify**: "Σ ranges over the substrate's full state space — every state `↝*`-reachable from `Σ_init`" and "The underlying `Emit_R` runs whenever its K.λ home-precondition P0 holds; it inspects neither conformance nor `a`'s store membership, so the bare operation can execute from a non-conforming pre-state."

**Problem**: The ASN deliberately ranges the bare operations and the wp computations over the *full* (`↝*`-reachable) state space, which it states "is what makes conformance conjuncts such as P2c genuinely dischargeable rather than vacuous." For `Emit_K`/`Emit_R`/`Nullify` to *execute* at a non-conforming state, K.λ must deposit an emitter address that is fresh against `dom(Σ.L) ∪ dom(Σ.C)`. But the only freshness argument supplied is R0, whose proof discharges the subsequent-emission branch entirely by citing **SubsequentEmissionFreshness** and **ChainMembershipForOrigin** (ASN-0093) — lemmas ASN-0093 establishes "at every reachable state," where *reachable* means `→*`-reachable through K-ops only. A non-conforming `↝*`-reachable state is, by construction (Definition — Categorical reachability), *not* `→*`-reachable; ASN-0093's chain-contiguity and freshness lemmas do not apply there, and R0's subsequent branch explicitly leans on "the contiguous prefix of `A_L(d)`'s realized chain" — a property that fails at exactly the non-conforming states the ASN admits.

The Emit_K function-ness Lemma notices the issue for *uniqueness* ("the max is well-defined at every state... contiguity notwithstanding") but establishes only that the chosen address is single-valued — **not** that it is fresh. Freshness at non-conforming states is left unproven, yet R0 is stated unconditionally (`(A Σ : dom(Σ.M) ≠ ∅ :: ...)`) and the necessity argument for P2c (wp Case 1) depends on Nullify actually producing a Σ' from a non-conforming pre-state.

**Required**: Either (a) restrict R0 (and "the bare operation can execute from a non-conforming pre-state") to substrate-conforming states, OR (b) supply a conformance-free freshness derivation for the subsequent-emission address `a = inc(ℓ_prev, 0)`: `ℓ_prev = max{ℓ' ∈ dom(Σ.L) : home(ℓ') = d}` gives `a > ℓ_prev ≥` every same-home address by T1 + TA5(a); `ℓ_prev` is T4-valid because L1c is preserved even at non-conforming states (→ T10a.4), so `sig(ℓ_prev) = #ℓ_prev` and `inc(ℓ_prev, 0)` keeps `home = d`; cross-home and cross-subspace freshness then close by T10 and SC-NEQ — none of which needs ChainMembershipForOrigin. Make that argument explicit rather than citing reachability-bound lemmas.

### Issue 2: wp Case 1 necessity for P1 asserts "b ≠ a" without justification

**ASN-0086, Weakest-Precondition Analysis, Case 1**: "dropping P1 admits `a ∉ A_rel^Σ`; the only new key at Σ' is the fresh emitter `b ≠ a`, so by L12a's pointwise agreement `a ∉ dom(Σ'.L) = A_rel^{Σ'}`..."

**Problem**: When P1 is dropped, `a` is an arbitrary tumbler (the target of Nullify's to-span), not constrained to lie outside `dom(Σ.L)`. The fresh emitter `b` is K.λ's chosen address at `d_retr`, selected independently of `a`. Nothing rules out `a = b` (i.e., `a` happens to be the next chain address at `d_retr`); in that sub-case `a ∈ dom(Σ'.L)` and `a ∈ coverage({(a, δ(1,#a))})`, so `a ∈ nullified(Σ')` and single-tuple scope can hold *despite* P1 being dropped. The necessity claim is therefore not universal as written.

**Required**: Necessity only needs one counterexample, so rephrase: "choose `a ∉ A_rel^Σ` distinct from the fresh emitter `a_emit(Σ, d_retr)`; then `a ∉ dom(Σ'.L)`..." Do not assert `b ≠ a` as a generic fact.

### Issue 3: Meta-prose duplication of the non-conforming-state construction and the "full state space" deferral

**ASN-0086, Definition — Categorical reachability vs. WP Case 1 (P2c necessity)**: The Categorical-reachability paragraph constructs "a higher layer may... emit `a'' = inc(a, 1)` at the same home as an existing link address `a`... yielding a nested pair `a ≼ a''`... jointly violating R0a's antichain." WP Case 1 P2c necessity then re-states the identical construction: "admits a non-conforming pre-state with `a, a'' ∈ dom(Σ.L)`, `a ≼ a''`, `a'' ≠ a` — a nested link pair excluded by R0a."

**Problem**: The same non-conforming-state witness appears in two sections in different words (the anti-bloat classifier's "two paragraphs in the same document say the same thing"). Separately, the justification "the wp is computed over the full state space... the same scope the Emit_K function-ness Lemma works over" recurs across the Emit_K Definition, the function-ness Lemma, the WP Case 1 *Domain of quantification* paragraph, and the WP Case 1 necessity paragraph — multiple paragraphs deferring to the same point. A reader must skip past the restatements to follow the actual necessity argument.

**Required**: State the non-conforming witness once (in the Categorical-reachability definition) and have WP Case 1 cite it rather than rebuild it. Collapse the repeated "full state space / same scope as the function-ness Lemma" deferrals into a single statement at the Emit_K Definition.

## OUT_OF_SCOPE

### Topic 1: Cardinality/ratio bound on `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Raised as an open question; a structural bound on retraction density is new territory requiring its own state-quantitative axioms, not a defect in the present invariants.

### Topic 2: Multi-arity typed relations `L_K^{(n)}` and binary projections
**Why out of scope**: This note explicitly restricts to standard-triple links; higher-arity relational structure is a deliberate deferral, not a gap in the arity-3 development.

### Topic 3: Atomicity/consistency model for concurrent Observe vs. Emit
**Why out of scope**: Concurrency semantics are not state, operations-on-state, or invariants of the single-authority substrate modeled here; they belong to a future concurrency ASN.

VERDICT: REVISE
