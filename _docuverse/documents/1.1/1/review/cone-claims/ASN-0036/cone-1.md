## Audit

### `subspace(·)` in D-CTG formal statement

D-CTG's inner quantifier guard reads `subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q`. S8-depth's formal statement uses `subspace(u) = subspace(w)`. Neither claim includes a Depends entry pointing to a definition of `subspace`. The foundation statements (T0, T1, T3, T4, OrdinalShift, NAT-*) do not define it. S8a's prose says "a subspace identifier followed by a within-subspace ordinal" and D-CTG-depth's proof writes `subspace(w) = w₁ = u₁ = 1`, implying `subspace(t) := t₁`, but no formal definitional site exists in the visible content and no Depends chain reaches one. A downstream prover encountering D-CTG's formal statement cannot discharge the `subspace(v) = 1` guard from any exported foundation statement.

### `shift`-preservation lemma promised and absent

S8-depth ends: "Ordinal shift `shift(v, n)` preserves a V-position's subspace identifier and its S8a well-formedness, **as the following lemma establishes**." The next section is S8-fin — no lemma appears anywhere in the provided ASN content. The two sub-claims (subspace-identifier preservation; S8a preservation) are each provable from OrdinalShift's postconditions (`#shift(v,n) = #v`, shift copies all but the last component, last component advances by `n ≥ 1 > 0`), but that proof is absent. The Depends of S8-depth lists OrdinalShift and S8a precisely for this lemma — the ingredients are marshalled, the argument is missing.

### S8-fin spuriously listed in D-CTG Depends

D-CTG's formal statement — `(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))` — contains no reference to `dom(M(d))` or finiteness. The S8-fin entry in D-CTG's Depends says it "strengthens contiguity at depth 2 to a single unbroken block of ordinals," but that strengthening is a consequence of D-CTG *together with* S8-fin, not a proof ingredient of D-CTG itself. D-CTG reads as a design axiom (no proof is given); axioms carry only the dependencies needed to interpret their symbols. S8-fin is not needed to state or interpret D-CTG. The spurious entry misrepresents D-CTG as depending on S8-fin, creating a false ordering constraint in the dependency DAG and suggesting — incorrectly — that S8-fin grounds or helps prove D-CTG.

---

### `subspace(·)` has no definitional site
**Class**: REVISE
**Foundation**: T0 (CarrierSetDefinition, ASN-0034) — component projection `t ↦ tᵢ` is defined, but no claim defines `subspace(t) := t₁` or any equivalent
**ASN**: D-CTG formal statement: `subspace(v) = 1`; S8-depth formal statement: `subspace(u) = subspace(w)`; D-CTG-depth proof: `subspace(w) = w₁ = u₁ = 1`
**Issue**: `subspace(·)` appears in the formal quantifier guards of D-CTG and S8-depth and is used mechanically in D-CTG-depth's proof, but no Depends entry in any of these claims cites a definitional site. The identification `subspace(t) = t₁` is implicit in D-CTG-depth's proof step but is never formally defined. A verifier encountering D-CTG's guard cannot discharge `subspace(v) = 1` without an exported definition.
**What needs resolving**: Add a formal definition claim for `subspace` (presumably `subspace(t) := t₁`) and add a Depends entry citing it in D-CTG and S8-depth. Alternatively, inline the definition into D-CTG's guard as `v₁ = 1` and rewrite S8-depth's statement in terms of `u₁ = w₁`.

---

### Shift-preservation lemma promised but absent
**Class**: REVISE
**Foundation**: OrdinalShift (ASN-0034) — postconditions `#shift(v,n) = #v`, `shift(v,n)ᵢ = vᵢ` for `i < #v`, `shift(v,n)_{#v} = v_{#v} + n ≥ 1`; S8a (ArrangementDomainRestriction, this ASN) — well-formedness predicate `zeros(t) = 0 ∧ #t ≥ 2`
**ASN**: S8-depth, closing paragraph: *"Ordinal shift `shift(v, n)` … preserves a V-position's subspace identifier and its S8a well-formedness, **as the following lemma establishes**."* No lemma follows; the next section is S8-fin.
**Issue**: The lemma is asserted but not present. Both sub-claims — (a) `subspace(shift(v,n)) = subspace(v)` and (b) `shift(v,n)` satisfies S8a whenever `v` does — are reachable from OrdinalShift's postconditions, but the argument does not appear anywhere in the ASN content.
**What needs resolving**: Deliver the promised lemma within S8-depth (or as a named sub-claim immediately following it), establishing both (a) and (b) from OrdinalShift's postconditions and S8a.

---

### S8-fin spuriously listed as dependency of D-CTG
**Class**: REVISE
**Foundation**: S8-fin (FiniteArrangement, this ASN) — `dom(Σ.M(d))` is finite
**ASN**: D-CTG Depends entry: *"S8-fin (FiniteArrangement) — supplies the finiteness of dom(M(d)), used to strengthen contiguity at depth 2 to a single unbroken block of ordinals"*
**Issue**: D-CTG's formal statement does not mention `dom(M(d))` or finiteness anywhere. The "single unbroken block" remark describes a corollary of D-CTG *combined with* S8-fin, not a consequence of D-CTG alone. D-CTG reads as a design axiom (no proof is given); its Depends entries should name only what is needed to state or interpret the claim. S8-fin is not needed for either purpose. The spurious entry injects a false edge into the dependency DAG, suggesting D-CTG is downstream of S8-fin when it is not.
**What needs resolving**: Remove S8-fin from D-CTG's Depends. If the "combined with S8-fin" consequence is worth recording, move it to a separate corollary or to the prose of a claim (e.g., D-SEQ) that actually uses both D-CTG and S8-fin together.

VERDICT: REVISE