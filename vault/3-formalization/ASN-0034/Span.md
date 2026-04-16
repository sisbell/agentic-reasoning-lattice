## Definition (Span)

**Definition (Span).** A *span* is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length — a positive tumbler used as a displacement whose action point satisfies `actionPoint(ℓ) ≤ #s` — denoting the contiguous range from `s` up to but not including `s ⊕ ℓ`. The two conditions `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` are precisely TA0's preconditions for `s ⊕ ℓ ∈ T`, so under them the upper bound denotes a tumbler in `T` and the set `{t ∈ T : s ≤ t < s ⊕ ℓ}` — the span — is well-defined; pairs `(s, ℓ)` violating either condition are not spans.

*Formal Contract:*
- *Preconditions:* `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, `actionPoint(ℓ) ≤ #s`
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`
