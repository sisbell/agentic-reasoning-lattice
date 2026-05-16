**T4a (SyntacticEquivalence).** The non-empty field constraint of T4 — that each present field in an address tumbler has at least one component — is equivalent to three syntactic conditions on the raw tumbler: (i) no two zeros are adjacent, (ii) `t₁ ≠ 0`, (iii) `t_{#t} ≠ 0`. We prove both directions of this equivalence under the T4 positive-component constraint, which requires every field component to be strictly positive.

Recall the T4 address structure. An address tumbler `t` has the form `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ` (with trailing fields and their separators omitted when fewer than four fields are present). Each `Nᵢ, Uⱼ, Dₖ, Eₗ` is a field component; each intervening `0` is a field separator. The positive-component constraint requires every field component to satisfy `Nᵢ > 0`, `Uⱼ > 0`, `Dₖ > 0`, `Eₗ > 0`. The non-empty field constraint requires `α ≥ 1` (always), `β ≥ 1` when the user field is present, `γ ≥ 1` when the document field is present, `δ ≥ 1` when the element field is present.

*Forward.* Assume every present field has at least one component, and that the positive-component constraint holds. We derive each syntactic condition.

*Condition (ii): `t₁ ≠ 0`.* The first component `t₁` belongs to the node field, which is always present and has `α ≥ 1` components. Thus `t₁ = N₁`, and by the positive-component constraint `N₁ > 0`, so `t₁ ≠ 0`.

*Condition (iii): `t_{#t} ≠ 0`.* The last component `t_{#t}` belongs to the last present field — the node field when `zeros(t) = 0`, the user field when `zeros(t) = 1`, the document field when `zeros(t) = 2`, or the element field when `zeros(t) = 3`. In each case, that field has at least one component by the non-empty field constraint, and its last component is strictly positive by the positive-component constraint. Hence `t_{#t} > 0`.

*Condition (i): no adjacent zeros.* Suppose for contradiction that `tᵢ = 0` and `tᵢ₊₁ = 0` for some `i` with `1 ≤ i < #t`. Under T4, every zero-valued component is a field separator. Two consecutive separators at positions `i` and `i + 1` would bound a field segment containing zero components — an empty field. This contradicts the non-empty field constraint. Hence no two zeros are adjacent.

*Reverse.* Assume conditions (i), (ii), and (iii) hold. We must show every present field has at least one component. The field segments of `t` are the maximal contiguous sub-sequences of non-zero positions between consecutive separator zeros. The first segment runs from position 1 to one less than the first zero (or to `#t` if no zero exists); the last runs from one past the last zero to position `#t`.

By (ii), `t₁ ≠ 0`, so position 1 belongs to the first field segment — the node field is non-empty. By (iii), `t_{#t} ≠ 0`, so position `#t` belongs to the last field segment — the last present field is non-empty. For any two consecutive separator zeros at positions `j` and `j'` with `j < j'`, condition (i) forces `j' ≥ j + 2`, guaranteeing at least one position `p` with `j < p < j'`. That position `p` is a field component (not a separator, since it lies strictly between two separators and is not itself zero by the T4 constraint that non-separator components are positive). So the interior field between separators `j` and `j'` has at least one component.

All fields — first, interior, and last — have at least one component. ∎

*Formal Contract:*
- *Preconditions:* `t` is an address tumbler satisfying T4's positive-component constraint (`tᵢ > 0` for every non-separator component).
- *Postconditions:* The non-empty field constraint (each present field has `≥ 1` component) holds if and only if (i) no two zeros are adjacent in `t`, (ii) `t₁ ≠ 0`, and (iii) `t_{#t} ≠ 0`.
