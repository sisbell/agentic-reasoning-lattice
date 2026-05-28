# Review of ASN-0100

I checked the three-effect decomposition, every invariant-preservation argument, the substrate-composite ordering analysis, the worked examples, the wp analysis, and all cross-ASN citations.

## REVISE

(none)

The proofs do the work that the "by similar reasoning" anti-pattern usually hides:

- **Boundary cases are all present and distinct.** First-insertion-into-empty (`ValidFirstInsertionPosition`, caller-chosen `m`), beginning (`j=0`, Left empty, `n'_{s_C}=0`), append (`j=N`, Shifted-right empty, K.μ⁻ omitted), and interior are each handled with their own composite shape. The empty-arrangement-with-prior-emissions sub-case (chain continuation vs. first emission) is separated correctly, and `n ≥ 1` is explicitly invoked to exclude the degenerate empty insertion.
- **Every invariant conjunct is addressed, including the hard ones.** S2 functionality is closed by an explicit pairwise-disjointness argument on last-component arithmetic *plus* INS.M-exhaustive (no fourth `s_C` region), with Shifted-right source uniqueness routed through TS2's equal-length precondition discharged via S8-depth. L0's two conjuncts are split (the `dom(C)`-ranging conjunct is not waved through as "unchanged"). D-SEQ★/D-MIN★/D-CTG★ are verified against the explicit `{1,…,N+n}` last-component range, with the `m_C ≥ 3` shared-prefix case implicit but correct.
- **The `shift(t,0)` convention is introduced explicitly** (not silently), and the disjointness proof correctly splits on `k` because `δ(k,m_C)` requires `k ≥ 1`.
- **INS.chain-shift is proved, not asserted** — the `inc(·,0) = shift(·,1)` identity is grounded in T4-validity → TA5-SigValid (`sig = #`) → TA5 → TA5a iteration → TS3 composition, which is exactly what S8★'s single-run collapse needs (M7 I-adjacency).
- **The I3 scope analysis is a strength, not a hand-wave.** Disclaiming I3-V/I3-CS/I3-CX (which describe ASN-0082's structurally smaller shift-only post-state) and identifying *precisely* which Insertion positions they would wrongly exclude, then verifying the Insertion region's contribution to each invariant independently, is the correct treatment.
- **The atomicity section's C/R symmetry argument is sound.** The ASN catches and rejects its own unsound "reorder K.ρ to exempt R from J1'★" justification, showing the unplaced-allocation window for C is structurally unavoidable and that composite-level atomicity (a stated precondition, not a consequence of SequentialTransitionAxiom) shields both. The forced/free ordering taxonomy is complete.
- **wp analysis is genuinely non-trivial** (tight-endset discoverability collapses to the pre-state via LP19a; the P4★/chain-membership wp is a real Boolean combination of a state predicate and a substrate-derivable property).
- **Citations are foundation-only** (ASN-0034/0036/0047/0058/0082/0093/0098); no non-foundation cross-references, no reinvented notation.

## OUT_OF_SCOPE

The scope-bounding is correct, not deficient. Link-subspace insertion, COPY/DELETE/REARRANGE, version derivation, and replication are excluded cleanly and re-surfaced as Open Questions rather than left as silent gaps. Closure-under-composition and concurrent same-position INSERTs are appropriately deferred.

VERDICT: CONVERGED
