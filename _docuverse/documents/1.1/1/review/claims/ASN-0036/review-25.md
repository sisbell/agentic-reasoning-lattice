# Formalize — ASN-0036 / subspace(v)

*2026-04-13 12:21*

**subspace(v) (SubspaceIdentifier).** The subspace identifier of a V-position v:

`subspace(v) = v₁`

We define the subspace identifier as the first component of the V-position. The well-formedness of this definition and its principal postcondition both rest on S8a (V-position well-formedness).

S8a establishes that every V-position v ∈ dom(Σ.M(d)) is an element-field tumbler satisfying `zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0`. The conjunct `v₁ ≥ 1` guarantees two things at once: the first component exists (the element field has at least one component, by T4's non-empty field constraint as invoked in S8a), and its value is a positive natural number. The extraction `v₁` is therefore total on dom(Σ.M(d)) — every V-position has a first component to extract.

The postcondition follows immediately: since S8a gives `v₁ ≥ 1` for all v ∈ dom(Σ.M(d)), and `subspace(v) = v₁` by definition, we have `subspace(v) ≥ 1` for every V-position. The value 1 identifies the text subspace and 2 the link subspace (per T4 and the shared vocabulary); the definition does not constrain v₁ to these values but inherits whatever range the document's subspace structure requires. ∎

*Formal Contract:*
- *Definition:* `subspace(v) = v₁` for v ∈ dom(Σ.M(d)).
- *Preconditions:* S8a (V-position well-formedness) — `v₁ ≥ 1` for all V-positions, guaranteeing the first component exists and is positive.
- *Postconditions:* `subspace(v) ≥ 1`.
