# Review of ASN-0036

## REVISE

### Issue 1: `subspace(v)` function lacks a Formal Contract entry parallel to `subspace_I(a)`
**ASN-0036, Arrangement contiguity section**: "Write `S = subspace(v) = v₁` for the subspace identifier (the first component of the element-field V-position)"
**Problem**: The function is introduced as a notational gloss inside running prose, then carries weight in S8a (subspace identifier defining V-position structure), S8-depth (quantification over `subspace(v₁) = subspace(v₂)`), D-CTG (text-subspace binding via `subspace(v) = 1`), OrdAddHom postcondition (b), and OrdShiftHom postcondition (b). Its companion `subspace_I(a) = E(a)₁` gets a Formal Contract entry under S7c with preconditions, definition, and postconditions, but `subspace(v)` is left as definitional shorthand. The asymmetry makes `subspace(v)` an unstated primitive in load-bearing claims — particularly OrdAddHom (b)'s "subspace(v ⊕ w) = subspace(v)" which is the formal statement of the architectural promise that V-position arithmetic stays within a subspace.
**Required**: Introduce a Formal Contract for `subspace(v)` near S8a (where V-position structure is first developed), parallel to `subspace_I(a)`. Preconditions (`v ∈ T`, `#v ≥ 1`), Definition (`subspace(v) = v₁`), Postconditions (`subspace(v) ∈ ℕ`; when v satisfies S8a, `subspace(v) ≥ 1`; subspace preservation under shift follows from OrdShiftHom (b)).

### Issue 2: D-SEQ Step 3 quantifies over "any integer k" but the carrier is ℕ
**ASN-0036, D-SEQ proof, Step 3**: "For any integer k with k₁ < k < k₂, the tuple w = [1, 1, …, 1, k] satisfies subspace(w) = 1, #w = m, and v₁ < w < v₂..."
**Problem**: Tumbler components live in ℕ by T0 (CarrierSetDefinition, ASN-0034) — the ASN is otherwise careful to maintain this discipline (e.g., OrdAddS8a's positivity chain explicitly cites NAT-* axioms). Quantifying over "integer" here is loose: the construction needs k ∈ ℕ to ensure w_m ∈ ℕ and hence w ∈ T. The proof's later S8a check requires k ≥ 1 (positive), which is consistent only under ℕ.
**Required**: Replace "any integer k" with "any natural number k" (or "any k ∈ ℕ") in Step 3.

## OUT_OF_SCOPE

(none — the ASN scopes its claims tightly via the explicit Scope block and Open Questions section. Deferrals to operations-layer (subspace alignment, D-CTG/D-MIN preservation by editing operations, depth-choice conventions), link-subspace semantics (V_2 sparse-with-tombstones), and document creation discipline are appropriate and clearly marked.)

VERDICT: REVISE
