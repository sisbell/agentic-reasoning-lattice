**B5a (Sibling Zeros Preservation).** `(A t : t_{sig(t)} > 0 : zeros(inc(t, 0)) = zeros(t))`

*Proof.* We must show that for any tumbler t with t_{sig(t)} > 0, the zero count of inc(t, 0) equals zeros(t). Let t' = inc(t, 0). By TA5(c), t' has the same length as t (#t' = #t) and differs from t only at position sig(t), where t'_{sig(t)} = t_{sig(t)} + 1. At every other position, t'_i = t_i.

We count zeros in t' by comparing each component with the corresponding component of t. At every position i ≠ sig(t), t'_i = t_i, so position i is zero-valued in t' exactly when it is zero-valued in t — these positions contribute identically to both zeros(t') and zeros(t). At position sig(t), the precondition gives t_{sig(t)} > 0, so this position contributes no zero to zeros(t). After the increment, t'_{sig(t)} = t_{sig(t)} + 1 ≥ 2 > 0, so this position contributes no zero to zeros(t') either. Since every position contributes identically to both zero counts, zeros(t') = zeros(t). ∎

*Formal Contract:*
- *Preconditions:* t ∈ T with t_{sig(t)} > 0.
- *Postconditions:* `zeros(inc(t, 0)) = zeros(t)`.

To apply B5a inductively across the sibling stream S(p, d), we must discharge its precondition: every cₙ satisfies cₙ_{sig(cₙ)} > 0. For c₁ = inc(p, d), the final component is 1 (from TA5(d)), so sig(c₁) = #c₁ and c₁_{sig(c₁)} = 1 > 0. Each cₙ₊₁ = inc(cₙ, 0) advances the value at sig(cₙ) by 1 (TA5(c)), preserving positivity. By induction, every stream element satisfies the precondition. Combined with B5, every element of S(p, d) inherits the zeros count established at c₁:

  `(A n ≥ 1 : zeros(cₙ) = zeros(p) + (d − 1))`

The B6 validity table below depends on this uniformity — all elements in a stream share the same hierarchical level.

This deserves attention. The `.0.` that appears in addresses like `1.1.0.1.0.1` is not a syntactic convention imposed by a parser — it is a *consequence* of baptism at depth 2. When inc(p, 2) extends p by two components, the first is zero (the field separator, from TA5(d)'s d − 1 = 1 intermediate zero) and the second is 1 (the first child's ordinal). The field structure of tumblers is *produced* by baptism arithmetic.

Gregory's evidence confirms the structural necessity in three independent ways. First, the zero separator is mechanically produced by the depth parameter computed from the type hierarchy — crossing from one hierarchical level to the next always uses d = 2 and therefore always inserts exactly one zero. Second, it is semantically interpreted by the containment operation, which treats zero positions as namespace boundaries during prefix comparison. Third, it is arithmetically essential for allocation: the search-bound and truncation logic depend on measuring the parent's length against the zero boundary. An address produced without the correct zero separators corrupts containment testing and all subsequent baptisms in the affected namespace.
