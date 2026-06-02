# Review of ASN-0086

I worked through every R-property proof (R0, R0a, R1–R6c, R-Scope), both wp cases, the supporting lemmas (CoverageEqualityDecidable, L-ContiguousPrefix, SliceUniqueness), and the worked sketch arithmetic. I also applied the anti-bloat classifier for forward-reference accretion and meta-prose.

## Findings

**Correctness.** The load-bearing new lemma R0a (FlatLinkDomain) is sound in both cases: the cross-home argument correctly establishes that `a ≼ a'` forces `zeros(w) = 0`, collapses `a'`'s three zeros onto `a`'s positions, and derives `home(a') = home(a)` — contradicting `d' ≠ d`, so the implication is vacuous; the same-home case closes via L-ContiguousPrefix + (UL) uniform length + T3. R-Scope's two branches (P1 owned-at-Σ, self-emit owned-at-commit) each correctly reduce `{t : a ≼ t} ∩ A_rel^{Σ'}` to `{a}` using R0a at Σ and Σ' respectively, and the arity-independence claim is justified (the argument touches only prefixes and the antichain, never `|Σ.L(a)|`). The wp derivations are honest: Case 1 coincides the weakest precondition with the operation's own `P0 ∧ P-tgt`, and Case 2 carries an explicit domain caveat restricting the formula to layer-reachable states, with the `G = ∅` escape branch shown non-redundant and instantiated concretely in Step 4. R3/R6a/R6c monotonicity and stability proofs cover all conjuncts. Emit_K faithfully discharges K.λ's L3 precondition (Value-shape consequence). I found no missing edge case across the operations (first emission, self-emit, empty endsets, retraction-of-retractor, self-nullification).

**Cross-ASN references.** All references are to provided foundations (ASN-0034/0036/0040/0043/0093). No violation.

**Anti-bloat.** The recent trim ("drop self-emit branch gloss," "trim SliceUniqueness proof tail") appears to have done its work — I did not find defensive justifications, use-site inventories, "see X below" deferral clusters, or duplicated paragraphs that obstruct the argument. The motivational intro is essay-toned but sits in the intro slot, not in a definition or claim carrier.

**Drift.** The note adds genuine abstract content (the R0a antichain invariant, the active/audit distinction, retraction-without-deletion semantics) that an alternative implementation would have to satisfy — not mere implementation mechanics. The retraction-as-convention status is correctly flagged in Open Questions rather than smuggled in as substrate. No META.

## OUT_OF_SCOPE

### Topic 1: Binary projections of higher-arity links
**Why out of scope**: Higher-arity links (`|Σ.L(a)| > 3`) correctly inhabit `A_rel` but index no `L_K`; how they map onto `L_K^{(n)}` relations is new territory, already named in Open Questions.

### Topic 2: Concurrency/consistency model for Emit vs. Observe and `A_K` transition observation
**Why out of scope**: The note specifies single-authority sequential transitions (inherited from ASN-0093's SequentialAtomicTransitions); concurrent observation semantics is future work, not an error here.

VERDICT: CONVERGED
