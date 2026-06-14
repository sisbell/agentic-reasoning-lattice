# Review of ASN-0133

I reviewed this as the capstone of the substrate arc and checked the load-bearing chain against its foundations (ASN-0086/0126/0128/0129/0130). The proofs hold. Specifically I verified:

- **Q0 view-unification is complete.** The enumeration of view-sensitive forms is exhaustive: PC3's four view-parameterized constituents (`members`, `targets_of`, `is_K`, `M_K`) plus UV's four other rewritten collections (`succs`, `sources_to`, `chain`, `stale`), with the verdict/optional atoms (`is_in_chain`, `tip`, `age`, `targets_keyed`, `is_filtered`) and the fixed-view slices `A_K`/`L_K` correctly classified as view-stable. Each rebuild via the fixed-view bases is value-preserving and backed by V-AUD (which *defines* the audit readings) — the `chain` case correctly routed through `elems`/`is_in_chain` since PL has no sequence-to-sequence filter.
- **The Q-EXT → Q5a → H-RF → Q6 chain is sound.** Q-EXT's step-agnosticism (PD0 ⊥-stability indifferent to who issues the step) is what survives environment input; Q5a's `Σ_ρ |⋃_k [D_ρ]_{Σ_k}|` bound correctly rests on at-most-once-per-argument ⊆ ever-in-domain; both hypotheses shown load-bearing (the `cmt`-trigger-fired-by-`res` counterexample for SF-without-extinction is correct).
- **The H-W foil argument is correct** — the no-op-spam construction drives `|W(σ)| = ∞` while real fires stay finite, establishing H-W as strictly stronger than (and unsatisfiable relative to) the operative H-RF.
- **Q6's obstruction taxonomy (1)/(2)/(3) is the right partition** — bounded growth excludes (1) (unbounded fresh args, obstructs *reaching*) but not (3) (finitely-many cycled out-of-phase, also obstructs *reaching*); (2) obstructs only *holding*. The reaching/holding split across the grow-only line is consistent throughout.
- **H-SFAIR ⟹ H-FAIR scoped to infinite σ is correct**, and the finite-σ counterexample (vacuous H-SFAIR, violated H-FAIR at a trigger-true terminal state) genuinely forces that restriction. The self-aware unsatisfiability analysis (withdraw-before-every-turn) and the resulting "nearer a restatement than a disjoint route" honesty are accurate.
- **The worked composition checks out** — `T_P`/`T_R` are SF by PD0's `¬∃`-over-grow-only-audit rule; the `needs_attention`-in-domain-not-trigger move is correctly forced (∧ wouldn't preserve SF); the idem=⊤ `res` dedup caveat is correctly discharged (fire ⟹ `T_R(c)=⊤` ⟹ no audit-covering tuple ⟹ no active hit ⟹ miss); the concrete Σ₀→Σ₁→Σ₂ trace correctly evaluates `quiescent_R(Σ₂)=⊤` against the nested quantifier.

No cross-ASN references to non-foundation notes; no notation reinvented over the foundations; a concrete example is present and its postconditions are checked.

## REVISE

None. I could not find a skipped case, a hand-waved proof step, or an unstated hypothesis. The note's discipline — every termination hypothesis named, each placed on the correct side of the substrate-guarantees / registration-checkable / assumption line, with H-W demoted to a foil and the open/closed collapse made explicit — survives scrutiny. The two terminology choices most likely to draw a flag are both sound on careful reading: "reachable" denotes `→_sh*`-reachable in X-DEF/Q3 versus σ-reachable in Q5a/H-W, but the sets are nested (σ-reachable-from-Σ₀ ⊆ `→_sh*`-reachable), so X-DEF over the larger set soundly supplies what Q-EXT needs over σ-states; and "real fire" is effectively pinned by "a trigger-true fire is a real fire" (Q6) and "a no-op fire neither advances the state nor consumes the trigger" (H-FAIR), with the only ambiguous case (trigger-true empty-emission) excluded for extinction-disciplined rules and harmless to Q5/Q6 otherwise.

## OUT_OF_SCOPE

### Topic 1: Joint quiescence of co-resident registries
This note analyzes one registry R, correctly modeling all other actors — including other registries — as environment steps. It therefore says nothing about whether two co-resident registries reach *joint* quiescence: A's fires are environment input to B and B's to A, so the pair admits a cross-registry analog of Q4's intra-registry mutual re-arm, in which each perpetually re-arms the other while each in isolation satisfies its bounded-input hypothesis.

**Why out of scope**: The single-registry-with-arbitrary-environment framing is the correct foundation, and the joint case is a distinct future layer — not the within-registry per-scope-vs-global question (OQ3) nor the within-registry cross-scope re-entry question (OQ4). It is the natural composition theorem to build *on* this note, not a gap *in* it.

VERDICT: CONVERGED
