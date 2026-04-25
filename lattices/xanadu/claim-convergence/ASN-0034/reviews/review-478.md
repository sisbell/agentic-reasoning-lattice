# Regional Review — ASN-0034/TA-Pos (cycle 5)

*2026-04-24 03:17*

### Use-site framing in NAT-closure body
**Class**: REVISE
**Foundation**: n/a (meta-prose / use-site inventory)
**ASN**: NAT-closure body: "Totality rules out partial addition and closure rules out sums that escape ℕ; together they are what lets callers chain `+` across steps without carrying a well-definedness obligation at each application."
**Issue**: The trailing "what lets callers chain `+` across steps without carrying a well-definedness obligation at each application" is a use-site justification — it anticipates what downstream consumers do with the signature and what obligation they avoid. Earlier cycles removed "the strict-above reading callers need when they use `1` as a positive reference" from this same claim; the pattern has reappeared relocated to the signature paragraph. The preceding sentence ("compositional terms like `(m + n) + p` re-enter the signature without a side condition") already states the mathematical content; the "callers… chain… obligation at each application" trailer adds no reasoning and invokes external consumers that have not been introduced.
**What needs resolving**: End the paragraph at "sums that escape ℕ." (or, if the composition point is worth keeping, stop at the earlier "re-enter the signature without a side condition" clause). Drop the "what lets callers chain… at each application" framing.

### Parenthetical aside about indiscernibility in NAT-zero body
**Class**: REVISE
**Foundation**: n/a (meta-prose / defensive justification)
**ASN**: NAT-zero body: "In the second case, `0 = n` rewrites `n < 0` to `0 < 0` by indiscernibility of `=` — a logical property of equality available throughout, not a property of `<` — again contradicting irreflexivity."
**Issue**: The em-dash aside "a logical property of equality available throughout, not a property of `<`" defends the invocation of indiscernibility by telling the reader where the principle lives (in equality reasoning, not NAT-order) and reassuring that it is in scope. This is a defensive justification of an inference step — the "essay content explaining why an axiom/step is needed rather than what it says" drift pattern — and it uses the rhetorical-negation shape ("X… not Y"). The inference `0 = n ⟹ (n < 0 ⟺ 0 < 0)` by indiscernibility of `=` stands on its own; the reader does not need to be told which theory owns the principle.
**What needs resolving**: Remove the em-dash aside. The sentence reduces to "In the second case, `0 = n` rewrites `n < 0` to `0 < 0` by indiscernibility of `=`, again contradicting irreflexivity."

### NAT-order body trails into implicational-form recovery
**Class**: REVISE
**Foundation**: n/a (use-site anticipation)
**ASN**: NAT-order body, closing sentence: "The familiar implicational form `m < n ⟹ m ≠ n` is the mutual-exclusion conjunct `¬(m < n ∧ m = n)` rewritten by the classical equivalence `¬(A ∧ B) ⟺ (A ⟹ ¬B)`."
**Issue**: "The familiar implicational form" anticipates a downstream consumer who expects `m < n ⟹ m ≠ n` and tells them how to recover it from the Consequence bullet by classical equivalence. The previous cycle flagged and removed "a consumer wanting the implicational form unfolds it from the exactly-one trichotomy bullet at the point of use"; the current sentence is the same unfolding relocated from an explicit use-site pointer into a standalone derivation of the implicational form. No new mathematical content is established — classical equivalence is a logical rewrite available to any consumer — and the sentence sits outside the exactly-one derivation it is appended to.
**What needs resolving**: Drop the closing sentence. The exactly-one trichotomy derivation is self-contained without the implicational-form trailer; a consumer who wants `m < n ⟹ m ≠ n` applies the classical equivalence without needing the claim to state it.

VERDICT: REVISE
