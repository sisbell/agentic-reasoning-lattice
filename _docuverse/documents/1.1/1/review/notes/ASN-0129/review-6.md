# Review of ASN-0129

## REVISE

(none)

I went looking for the failure modes this note is most exposed to, and each probe came back clean:

- **V-IDX vacuity.** Checked the universal-attachment foreclosure against the foundation records directly: R-C1 makes `retired`/`supersedes`/`R` mandatory; BH1 fails at the two Binary designates (R-C0 requires Unary), BH2/BH3 fail at `retired` (require Binary), BH4 fails at all three (requires `idem = ⊥`, all designates are `idem = ⊤`). The "no constructible registry attaches any behavior family universally" claim is airtight, and the surviving `Reg`-body vocabulary (core family, fixed-view slices, the class-unindexed `targets_keyed`, the `·[K]` lookup) is enumerated correctly.
- **The worked trace.** Recomputed all three steps end-to-end: gate verdicts (Sh-conf Binary on both emits), frontier addresses (`chain_d(0..2)` via FrontierUnification), C2/C3 at each deposit, the dedup miss at Σ₁ (`A_res = ∅`), P0/P-reg/P-tgt at the Nullify, single-tuple scope leaving `a₁` active, and the slice evaluations — `OPEN(t)` = {c₁}, ∅, {c₁}; `quiescent(t)` = ⊥, ⊤, ⊥; `ever_res` = ⊥, ⊤, ⊤. All correct, including the boundary case (PC1 over the empty `M_res` at Σ₁).
- **PD0's polarity discipline.** Verified rule-by-rule: grow-only bases match the `→_sh` step effects (no contraction step exists in K.σ ∪ K.α ∪ K.λ_sh, so `C_dom`/`M_dom`/`L_K`/`L_dom` growth is exact); witness persistence rests correctly on L12/L12a carried by B2/RP-b; and the deliberate exclusions are the right ones — `count(D) = c` in neither class, `count(D) ≤ c` only in SF, T1-extrema fenced, ∀-over-growing-with-ST correctly absent.
- **PC6's converse.** The one non-trivial leaf — `Observe_K` — normalizes to exactly the V-TUP conjunction filter (ASN-0086's `F̂ ⊆ coverage(F)` unfolds to the finite per-element conjunction); `dom(Σ.L)` recovery via P6/RP-a is sound (P6 forces arity 3 and registered type at every reachable state, so the audit-slice union over the finite registry covers the store); registry lookups constant-fold by R1. The granularity and node-vocabulary restrictions are stated, priced (the `t ⊕ w` leaf, the ℕ-multiplication example, the parity example), and internally consistent — the parity example only coheres because the admitted fold forms are exactly PC1/PC2a's, which the class definition does enumerate.
- **FP/PD2 cross-check.** Footprints match UV's per-codomain rules (default increment on collection-valued atoms only), BH4's home-wide read is honestly cross-type ("the chain interleaves every type homed at d"), and PD2's exception list — retraction, same-home traffic under BH4, every BH3-attached Binary type under `targets_keyed` — is exactly the set of cross-type effects the foundations admit; I found no fourth.
- **Honesty of the fences.** H-init is correctly named as a hypothesis (no foundation claim states initial C/M cardinality — I checked); `age`'s ⊥-totalization is conservative and its load-bearing justification (definedness-stability for PC4/PC5) is right; C-reach's demotion to conjecture, with the three named defects of the FO argument (unbounded walk atoms on out-degree-≤1 graphs, counting, built-in orders), is the correct move — the out-degree-≤1 observation that `is_in_chain` *is* `reach` there checks out against BH2's walk definition.

## OUT_OF_SCOPE

### Topic 1: The C-reach proof obligation
**Why out of scope**: Proving that no PL term computes transitive closure requires an invariance argument over branchy, cardinality-balanced state families in a counting-plus-order regime — research-grade model theory. The note correctly records it as a conjecture with the proof obligation named (Open Question 6); discharging it is a dedicated future ASN, not a revision of this one.

### Topic 2: Protocol-layer convergence theory
**Why out of scope**: Fire-until-stable termination arguments, scheduler fairness, fire atomicity, and re-opening rules are constructions *over* PD0–PD2, and the note fences them explicitly. PD1's un-termination warning and the discipline-as-hypothesis pattern (DR's move) give the future note its starting obligations.

### Topic 3: Extensional equivalence and mechanical class-checking
**Why out of scope**: Deciding whether two PL terms denote the same predicate (Open Question 3) and soundly certifying ⊤-stability mechanically (Open Question 5) are what a protocol checker will need, but they are theory about the language, not gaps in its definition — well-typing and per-state decidability are already delivered here.

### Topic 4: Cross-layer predicates over PL and the arrangement-query algebra
**Why out of scope**: The note deliberately draws the structural-reads-only boundary, leaving `image`/`findlinks_V` to ASN-0127's layer. A trigger that reacts to image motion (D-NONMONO territory) would need a joint layer with its own dynamics classification — new territory, consistent with the boundary as drawn.

VERDICT: CONVERGED
