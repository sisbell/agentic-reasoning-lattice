**E₁(a) (ElementSubspaceProjection).** For an I-address `a` with `zeros(a) = 3`, the element subspace identifier is:

`E₁(a) = fields(a).element₁`

— the first component of the element field in T4's four-field decomposition.

The definition is well-founded. T4 (HierarchicalParsing, ASN-0034) specifies the address format `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, where zero-valued components are field separators and every field component is strictly positive. For `a` with `zeros(a) = 3`, T4b (UniqueParse, ASN-0034) establishes that `fields(a)` is well-defined: the three zero-valued components are exactly the field separators, and the decomposition into four non-empty fields is uniquely determined. The element field `fields(a).element = [E₁, ..., E_δ]` has `δ ≥ 1` — T4a's non-adjacency constraint (invoked by T4b) ensures every field segment is non-empty — so the extraction of its first component is total. T4's positive-component constraint gives `E₁(a) ≥ 1`.

For all I-addresses in `dom(Σ.C)`, S7b establishes `zeros(a) = 3`, so `E₁(a)` is well-defined throughout the content store. ∎

*Formal Contract:*
- *Definition:* `E₁(a) = fields(a).element₁` for `a ∈ T` with `zeros(a) = 3`.
- *Preconditions:* `a ∈ T` with `zeros(a) = 3` — T4b requires this for `fields(a)` to be well-defined. (Entailed by S7b for all `a ∈ dom(Σ.C)`.)
- *Postconditions:* `E₁(a) ≥ 1` (T4's positive-component constraint — every field component is strictly positive).
