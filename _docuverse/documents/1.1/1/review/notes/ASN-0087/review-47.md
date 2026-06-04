# Review of ASN-0087

## REVISE

### Issue 1: StandardAuthoring is unsatisfiable for any non-empty endset
**ASN-0087, Inputs (Standard authoring)**: "StandardAuthoring(e, Σ) ≡ coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)"

**Problem**: `coverage(e)` is the union of half-open T1-intervals `{t : s ≤ t < s ⊕ ℓ}` (ASN-0098/0043). For any span this interval is **infinite** — e.g. the canonical span `(s, δ(1,#s))` covers `subtree(s) = {t : s ≼ t}`, which by T0(a)/T0(b) has infinitely many members. The stores are finite (C-fin, L-fin). So `coverage(e) ⊆ dom(C) ∪ dom(L)` (infinite ⊆ finite) is false for every endset containing a span. Since L3 forces `e₃ ≠ ∅`, *no link can ever be standardly authored*. The worked example confirms this: `coverage(e₁) = {t : a₁ ≼ t}` is infinite, so even the note's own example endsets fail the predicate.

Consequently three load-bearing passages are vacuous:
- M-WP "Reduction under standard authoring" — the premise `coverage(eᵢ) ⊆ dom(Σ.C) ∪ dom(Σ.L)` never holds, so the collapse to Case-1 shape applies to no link.
- M-Reflexive's "Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive case is structurally excluded" — never triggers.
- Side Effects' "When ℓ' was authored under standard authoring … the side effect is vacuous" — the reassurance is empty.

**Required**: Restrict the predicate to substrate-emittable addresses, mirroring ASN-0098's own `tight` definition, which quantifies `(A t ∈ F : s ≤ t < s ⊕ ℓ : t ∈ dom(Σ_e.C) ∪ dom(Σ_e.L))`. Define `StandardAuthoring(e, Σ) ≡ coverage(e) ∩ F ⊆ dom(Σ.C) ∪ dom(Σ.L)` (or build directly on tightness). Then, because `ℓ ∈ F` and `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`, the inference `ℓ ∉ coverage(eᵢ)` goes through and the reductions become non-vacuous.

### Issue 2: Redundant lemma assembly (anti-bloat)
**ASN-0087, Permanence of the Recording**: the three-bullet assembly of L12, LP13, LP3★.

**Problem**: LP13 already gives `ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ)` for every reachable `Σ' →* Σ''` — exactly the conclusion. L12 (single-step) is subsumed by LP13's multi-step statement, and LP3★ (coverage invariance) follows immediately from value equality since `coverage` is a deterministic function of the endset. Two of the three cited guarantees do not advance the argument.

**Required**: State the permanence conclusion from LP13 alone; drop the L12 and LP3★ bullets (or reduce to a one-clause "coverage equality is then immediate").

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets
The first and fourth Open Questions (constraints on endsets covering not-yet-allocated addresses; discoverability once such content is created) are genuinely future territory — L4 permits forward references and LP18 resurrection sketches the dynamics, but a full discipline belongs to a later ASN.

VERDICT: REVISE
