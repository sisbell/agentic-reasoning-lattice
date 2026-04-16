## Definition (Span)

**Definition (Span).** A *span* is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length — a positive tumbler used as a displacement — denoting the contiguous range from `s` up to but not including `s ⊕ ℓ`. The set of tumblers in the span is `{t ∈ T : s ≤ t < s ⊕ ℓ}`.

*Formal Contract:*
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`, where `s ∈ T` is the start address and `ℓ ∈ T` with `Pos(ℓ)` is the displacement length
