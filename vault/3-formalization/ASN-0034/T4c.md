**T4c (LevelDetermination).** Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`, the count of zero-valued components in a tumbler `t`. Under the constraints of T4, the function `zeros` determines the hierarchical level of an address tumbler, and the mapping from `{0, 1, 2, 3}` to the four hierarchical levels is a bijection.

By T4, valid address tumblers have at most three zero-valued components, so `zeros(t) ∈ {0, 1, 2, 3}`. By T4b (UniqueParse), every zero in `t` is a field separator and every separator is a zero — the positive-component constraint ensures that zeros appear in no other role. Therefore `zeros(t)` counts exactly the number of field separators, and the number of fields present equals `zeros(t) + 1`, since `k` separators delimit `k + 1` fields.

The mapping from zero count to hierarchical level is defined by the number of fields:

  - `zeros(t) = 0` → 1 field (node only) → node address,
  - `zeros(t) = 1` → 2 fields (node, user) → user address,
  - `zeros(t) = 2` → 3 fields (node, user, document) → document address,
  - `zeros(t) = 3` → 4 fields (node, user, document, element) → element address.

*Injectivity.* Distinct zero counts produce distinct field counts — `zeros(t) + 1` is injective on `{0, 1, 2, 3}` — and the field-count-to-level mapping is itself injective, since each level is defined by a specific number of fields. Therefore `zeros(a) ≠ zeros(b)` implies `a` and `b` belong to different hierarchical levels.

*Surjectivity.* Each of the four levels is realized: `zeros(t) = 0, 1, 2, 3` are all values permitted by T4, and each corresponds to exactly one level. The mapping is therefore bijective on `{0, 1, 2, 3}`.

We note the essential role of the positive-component constraint in this result. Without it, a tumbler `[1, 0, 0, 3]` would have `zeros(t) = 2`, classifying it as a document address with three fields: `[1]`, `[]`, `[3]`. But the second zero would be ambiguous — it could be a separator (giving an empty user field) or a zero-valued component within the user field (giving two fields: `[1]`, `[0, 3]`). The positive-component constraint eliminates the second interpretation: no field component can be zero, so every zero is unambiguously a separator, and the parse is unique. ∎

*Formal Contract:*
- *Preconditions:* `t` satisfies the T4 constraints (at most three zero-valued components, positive-component constraint, non-empty field constraint). `t` satisfies T4b (UniqueParse): every zero in `t` is a field separator and every separator is a zero, so the separator positions are exactly the zero-valued positions.
- *Postconditions:* `zeros(t)` counts exactly the number of field separators in `t`, and the number of fields present equals `zeros(t) + 1`. The mapping `zeros(t) → hierarchical level` is a bijection on `{0, 1, 2, 3}`: distinct zero counts imply distinct hierarchical levels (injectivity), and every level in {node, user, document, element} is realized by exactly one zero count (surjectivity).
