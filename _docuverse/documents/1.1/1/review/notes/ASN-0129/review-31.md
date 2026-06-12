# Review of ASN-0129

This ASN was checked claim-by-claim against the foundation contracts. The checks that drove the verdict, briefly:

- **Worked trace recomputed end-to-end.** Σ₀–Σ₄ were re-derived against the upstream contracts: frontier addresses `a₁ = chain_d(0)` through `a₄ = chain_d(3)` (FrontierUnification, first-emission branch at Σ₁), the I1 miss branches at Σ₂ and Σ₄, P0/P-reg/P-tgt at the Σ₃ Nullify, the C3 discharge at Σ₄ both via DR (the derivation's one `L_R`-growing step is the Nullify) and concretely (`a₂` and `a₄` are equal-length distinct siblings, so `subtree(a₂)` misses `a₄` by R0a). The active-view sequence ⊤,⊥,⊤,⊥,⊥, the default-view sequence ⊤,⊥,⊤,⊥,⊤, and the audit companion ⊥,⊥,⊤,⊤,⊤ all check out, including the default-view evaluations at Σ₁–Σ₃ where Φ's filter is empty.
- **V-IDX's vacuity argument verified.** The claim that no constructible registry attaches a behavior family universally holds against R-C1 plus S3: `[K_R]` is mandatory with `behaviors = ∅`, so every registry contains a class lacking every family, and the instance-wise rule excludes every class-indexed behavior atom from `Reg`-bodies. The surviving forms (core family, fixed-view slices, the class-unindexed `targets_keyed`, the `·[K]` lookup) are correctly enumerated.
- **QD-fin, V-STAT, WT decidability, PC5.** The link-store finiteness induction is sound (R-VAL base, one fresh key per K.λ_sh, frames elsewhere); the injection of `A_K`/`L_K` into `dom(Σ.L)` via `addr` is correctly grounded in R1 (ASN-0086). WT's well-foundedness through `Reg` expansion (finitely many instances by C0, each a substitution into a strictly smaller body) holds.
- **PD0 soundness.** Each grow-only base was checked against the step effects: `L_K` per-step by R3 carried through B2/RP-b, `L_dom` and `dom(Σ.M)` by the frame clauses, audit `M_K` as a union over a growing index set, filters by ST-body persistence, step-constant domains by L12. The polarity assignments (count ≥ in ST only, count ≤ in SF only, equality in neither, extrema excluded) are each correct, and the clauses PD0 deliberately omits (PC2-binder compositions, mixed-view terms) fail conservatively — unclassified, not misclassified — consistent with OQ5's framing.
- **PC6's converse at its one non-trivial leaf.** The `Observe_K` normalization is correct: `F̂ ⊆ coverage(F)` unfolds to the finite conjunction of V-TUP coverage tests, and the result — a tuple set outside COD — is consumed only in domain position, consistent with QD-refl's address-valued restriction. The `L_dom`-recovery claim in QD-audit is sound because P6 supplies both registered-type and arity-3 at every reachable state, so the union of audit slices over `Reg` exhausts `dom(Σ.L)`.
- **UV's fixed readings of the two ASN-0128 sentences.** The adopted readings (the walk = traversal + verdicts; "Nothing else is rewritten" scoped by its colon list) are internally consistent — `is_in_chain` evaluated against the unrewritten walk, verdicts and Booleans never rewritten, `elems` count-faithfulness preserved under deletion — and the layer-confusion argument grounds the split on ASN-0128's own presentation/state distinction.
- **FP/PD2 footprints.** Each footprint was checked against the atom definitions (active slices reading `L_K ∪ L_R` through `nullified`, BH4's home-wide chain arithmetic, `targets_keyed`'s cross-type join, the default-view increment), and PD2's exception list names exactly the three cross-type routes the footprints expose.
- **Anti-bloat scan.** The patterns flagged by the classifier were looked for specifically. The note's provenance inventory in V (the six fenced additions) is load-bearing for QD-audit's accounting; the three deferrals to Open Question 6 are each a conjecture stating its own obligation against a shared question; the V-TUP and PC6 passages on add-then-compare serve different roles (decidability of the leaf vs. the granularity boundary). No instance rises to relocated-finding prose, excluded-case speculation, or genuine duplication.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Discharging the inexpressibility conjectures (C-reach, the parity candidate, C-emit)
**Why out of scope**: The note correctly downgrades all three to conjectures with explicit proof obligations (Open Question 6) and shows why the shortcut citations are unsound; the invariance arguments themselves are a future ASN's work, not a gap in this one.

### Topic 2: Mechanical certification of the dynamics classes
**Why out of scope**: PD0–PD2 are sound syntactic classifications; a decision procedure a protocol checker could run (the note's Open Question 5) is new territory built on this foundation, not a missing piece of it.

### Topic 3: Protocol constructions over PL
**Why out of scope**: Triggers paired with writes, convergence arguments, and scheduler disciplines are application-layer machinery written in PL and typed by PD0–PD2; the note explicitly fences them, and the fence is the right one for a predicate-foundation ASN.

VERDICT: CONVERGED
