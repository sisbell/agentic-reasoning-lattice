**D-CTG** — The formal statement is well-formed given its dependencies and the betweenness structure is clear. The inner guard correctly gates on `subspace(v) = 1`, `#v = #u`, `zeros(v) = 0`, and `u < v < q`. One structural gap (below).

**subspace** — Definitionally sound. T0's nonemptiness `1 ≤ #a` ensures `v₁` is always well-defined.

**S8a** — The two-step rewrite `zeros(t) = 0 ⟺ (A i : 1 ≤ i ≤ #t : tᵢ > 0)` is correctly derived: NAT-card's `|S| = 0 ⟺ S = ∅` gives "no component zero"; NAT-zero's `0 < n ∨ 0 = n` rewrites each `tᵢ ≠ 0` as `tᵢ > 0` via disjunctive syllogism. The dependency chain is sound.

**S8-fin** — Declared as a design requirement; status is clear.

**S8-depth** — The formal claim is: equal-subspace pairs in `dom(Σ.M(d))` share depth. The dependency on `subspace` is correct. Issues noted below.

**D-CTG-depth** — The main proof is structurally sound. The construction of w is valid: T0's comprehension licenses `w ∈ T` from an explicit length and component map; S8a applied to `u` grounds `wᵢ = uᵢ ≥ 1` for `i ≤ j` and `uⱼ₊₁ ≥ 1`, so `n > uⱼ₊₁ ≥ 1` gives `wⱼ₊₁ ≥ 2 > 0`; the `wᵢ = 1` fill ensures zeros(w) = 0 for the remaining positions; T1's definition case (i) correctly grounds both `u < w` and `w < x`; T3 correctly distinguishes distinct `n`-values as distinct tumblers; S8-fin is correctly contradicted via the `V_1(d) ⊆ dom(M(d))` precondition. The case `j = m−1` (where the fill range is empty) is handled correctly — the argument degenerates cleanly. The iterative use of T0(a) to generate the sequence `n₁ < n₂ < …` is mathematically valid (standard inductive argument on ℕ); the proof writes "continuing" without naming the induction principle, but this is a minor informality.

Four issues require resolution.

---

### D-CTG and D-CTG-depth reference V_1(d), which is not defined in any shown claim
**Class**: REVISE
**Foundation**: None — the symbol has no grounding
**ASN**: D-CTG formal statement: `u ∈ V_1(d) ∧ q ∈ V_1(d)` and consequent `v ∈ V_1(d)`; D-CTG-depth preconditions and postconditions likewise
**Issue**: `V_1(d)` appears throughout D-CTG and D-CTG-depth but is defined nowhere in the shown ASN content or in the listed foundation statements. The narrative calls it "the text subspace" but no formal definition appears — no claim states `V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = 1}` or any equivalent. Without this, D-CTG's consequent `v ∈ V_1(d)` is uninterpretable, and D-CTG-depth's precondition `V_1(d) ⊆ dom(M(d))` is unverifiable. Every downstream claim that builds on D-CTG inherits the gap.
**What needs resolving**: A claim must formally define `V_1(d)` and that claim must be in D-CTG's and D-CTG-depth's Depends lists. Until then, the formal statements of both claims contain an ungrounded symbol.

---

### D-CTG's inner quantifier has no domain for v
**Class**: REVISE
**Foundation**: T0 (CarrierSetDefinition) — component projection and length are only defined on `T`; T1 (LexicographicOrder) — `<` is only defined on `T`
**ASN**: D-CTG formal statement, inner quantifier: `(A v : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d))`
**Issue**: The expression `subspace(v) = v₁` requires `v ∈ T` (T0's component projection is only defined on T); `#v` likewise requires `v ∈ T`; `u < v < q` uses T1's strict order, which is defined only on T. The quantifier binds `v` without specifying its domain, leaving every guard term in the inner quantifier formally ill-typed.
**What needs resolving**: The inner quantifier must be `(A v ∈ T : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d))`.

---

### S8-depth announces a shift-preservation lemma that is never stated
**Class**: REVISE
**Foundation**: OrdinalShift (ASN-0034); S8a (ArrangementDomainRestriction)
**ASN**: S8-depth, "Shift preservation for V-positions" section: *"Ordinal shift shift(v, n) … preserves a V-position's subspace identifier and its S8a well-formedness, as the following lemma establishes."* followed immediately by the Depends list and nothing else.
**Issue**: The phrase "as the following lemma establishes" is a structural promise: a formal statement and proof follow. Neither appears. The Depends entries (OrdinalShift, S8a) name what the lemma would consume but do not constitute a lemma — they supply no claim about what shift preserves. If OrdShiftHom (visible as a separate claim file in the repository) is the intended referent, then the text is pointing to the wrong scope: S8-depth's body cannot "establish" what a separate claim file says. The shift-preservation result is consumed by D-CTG-depth's S8a verification step (showing `zeros(w) = 0` after construction), and its absence leaves that step without a cited basis.
**What needs resolving**: Either state and prove the shift-preservation lemma inside S8-depth's body (formal statement: shift preserves `subspace` and satisfies S8a's predicate), or cite OrdShiftHom by name in S8-depth's Depends and replace "the following lemma establishes" with a citation.

---

### D-CTG-depth's second postcondition is not derived in the proof body
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder) — component-comparison clause of the definition
**ASN**: D-CTG-depth Postconditions, second bullet: *"Contiguity of V_1(d) is determined by component m alone, structurally identical to the depth-2 case."*
**Issue**: The proof body establishes the first postcondition (all pairs in V_1(d) agree on components 2 through m−1). From this, the reduction to single-component betweenness requires an additional step: any intermediate `v` satisfying `u < v < x` with `#v = m` must itself agree with u and x on every component where they agree (positions 1 through m−1). This follows from T1's definition — if v differs from u and x at some position j < m, then v is either less than u or greater than x (the standard "interval" argument in a total order), contradicting `u < v < x` — but this argument is not given. Without it, the claim that D-CTG's multi-component betweenness guard reduces to checking component m alone is asserted, not proved. Any downstream claim (including D-SEQ) that inherits this reduction without the missing argument is exposed to the gap.
**What needs resolving**: The proof must derive, from T1's definition, that any `v ∈ T` satisfying `u < v < x` and `#v = m` must agree with u and x on all positions where u and x agree (positions 1 through m−1), completing the reduction. Alternatively, if this intermediate result is already established in another cited claim, cite it explicitly.

---

### S8a formal body contains extended motivational prose
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S8a body: paragraphs beginning *"A conventional system merges these…"* through *"The remainder of this ASN derives the invariants that govern a strand."*
**Issue**: Three paragraphs — the Nelson quotation, the comparison with conventional file-save semantics, and the definition of "strand" — are rationale and context, not formal content about the domain-restriction predicate. The claim's formal argument (zeros-to-empty-set via NAT-card, empty-set-to-positivity via NAT-zero) is sound; the surrounding prose does not affect it. But the precise reader must skip multiple paragraphs to locate the formal chain. The strand definition in particular belongs in a dedicated claim or note that other claims can cite, not embedded in a domain-restriction invariant.
**What needs resolving**: Move the motivational paragraphs and strand definition to a rationale or note; retain only what grounds the formal statement of S8a.

---

VERDICT: REVISE