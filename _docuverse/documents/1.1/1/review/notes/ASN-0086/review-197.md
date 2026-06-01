# Review of ASN-0086

## REVISE

### Issue 1: "Reachable case" in L-ContiguousPrefix is subsumed by the "Extension" induction

**ASN-0086, L-ContiguousPrefix proof**: The proof splits into "*Reachable case (= ChainMembershipForOrigin).* For every →*-reachable Σ, the statement is exactly ChainMembershipForOrigin…" followed by "*Extension to substrate-conforming states.* … induct on the conformance-witnessing transition sequence Σ_init = Σ_0, …, Σ_N = Σ."

**Problem**: The induction in the second part is general — its base is Σ_init (empty link store, by EmptyInitialLinkStore) and its step handles any conformance-preserving transition via clauses (b)/(c). Every →*-reachable state is reached by K-op →-steps, which K-Step Conformance Preservation declares conformance-preserving; so →*-reachable states are a subset of substrate-conforming states and are already covered by the induction. The induction's contiguous-prefix form `{incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J}` is built directly from clause (c) (empty homed-set → `[d.0.s_L.1]`; non-empty → `inc(ℓ_prev,0)`), which are exactly A_L(d)'s anchor and recurrence — so the reachable case is not needed to ground the index identity either. The two paragraphs prove overlapping coverage.

**Required**: Either delete the standalone "Reachable case" and fold its single load-bearing fact (origin/home coincidence on link addresses) into the induction, or state explicitly what the induction *cannot* establish on its own that the reachable case supplies. As written it is redundant proof coverage.

### Issue 2: R0's per-invariant enumeration is a use-site inventory the conformance lemma already discharges wholesale

**ASN-0086, R0 proof, "*L-invariant preservation across the K.λ-step*"**: "By K-Step Conformance Preservation, Σ' is therefore substrate-conforming, which discharges the full state-local L/S/M/C invariant catalog at the fresh key a in one stroke: the frame-fixed S/M/C-invariants, L-fin, L12/L12a, and the L14/L14a fresh-key obligation … the address-structural L0/L1/L1a/L1b … the per-address chain L1c, the standard-triple value-shape L3, and the set/slot invariants L5/L6 are likewise conjuncts of that catalog, discharged at a by the same conformance step. The value-shape conjuncts are additionally underwritten by…"

**Problem**: Substrate-conformance clause (a) *is* "preserve the full L/S/M/C invariant catalog." Once the conformance lemma yields a substrate-conforming Σ', every catalog invariant holds at `a` by definition. The subsequent invariant-by-invariant roll-call (L-fin, L12/L12a, L14/L14a, L0/L1/L1a/L1b, L1c, L3, L5/L6) and the appended "additionally underwritten by the Link type" remark add no proof content — they re-enumerate a catalog the single lemma invocation already closed. This is exactly the use-site-inventory pattern the anti-bloat charge targets.

**Required**: Reduce to the lemma invocation plus the one genuinely non-redundant clause (the L3/N≥3 match between the emitted triple and K.λ's `N=3, e₃≠∅` precondition). Drop the per-invariant recitation.

### Issue 3: "Consequence — A_K is not monotone" forward-references and pre-stages the Worked Sketch

**ASN-0086, after R6c**: "*Consequence — A_K is not monotone…* Worked Sketch Steps 1 and 2 exhibit the witnesses: Step 1 (Nullify a₁) shrinks `A_K^{Σ_0} = {(a₁, F₁, G₁)}` to `A_K^{Σ_1} = ∅`… Step 2 (re-emission) grows `A_K^{Σ_1} = ∅` to `A_K^{Σ_2} = {(a₂, F₁, G₁)}`…"

**Problem**: The consequence both names concrete Worked-Sketch states (Σ_0, Σ_1, Σ_2, a₁, a₂) that are not defined until the much-later Worked Sketch and reproduces the very witnesses the Worked Sketch then develops in full. This is the "defer to a downstream location while also restating its content here" pattern — the non-monotonicity point is made twice, once abstractly with imported concrete labels and once in the Worked Sketch.

**Required**: State the non-monotonicity consequence abstractly (a retraction shrinks `A_K`, a later re-emission grows it at a fresh address — failure of both `⊆` and `⊇`) without importing forward-defined Σ_i/a_i labels; let the Worked Sketch carry the concrete witnesses.

## OUT_OF_SCOPE

### Topic 1: Multi-arity typed relations `L_K^{(n)}`
The note restricts to standard-triple links and defers higher-arity relations (`|Σ.L(a)| > 3`) to the Open Questions. Defining the n-ary typed-relation algebra is genuinely new territory, correctly deferred — not a defect here.

### Topic 2: Concurrency/atomicity of Emit vs Observe
The consistency model under concurrent Emit/Observe (Open Questions) is downstream protocol work, not a gap in this ASN's sequential `→`/`↝` model.

VERDICT: REVISE
