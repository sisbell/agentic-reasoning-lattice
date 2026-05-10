# Cone Review — ASN-0034/T10a (cycle 1)

*2026-04-17 20:15*

### TA5a summary table diverges from TA5a statement on `k = 1` condition
**Foundation**: (none — internal consistency)
**ASN**: The summary table at the end of the TA5 section lists TA5a as: "`inc(t, k)` preserves T4 iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`". TA5a's own theorem statement says "preserves T4 if and only if `k ∈ {0, 1}`, or `k = 2` with `zeros(t) ≤ 2`", and TA5a's *Guarantee* clause in the Formal Contract repeats this form (no zero-count cap on `k = 1`). TA5a's Case `k = 1` proof text explicitly argues the redundancy: "`zeros(t) ≤ 3` — already supplied by the T4-validity precondition's zero-count bound on `t` — so no additional constraint on `zeros(t)` arises."
**Issue**: Three places in the document characterize the same biconditional with two different surface forms. Under T4-validity the two forms are semantically equivalent, but the table writes a conjunct that TA5a's statement and Guarantee deliberately omit. A downstream property citing "TA5a's `k = 1` condition" will read different text depending on which location it lands on.
**What needs resolving**: Pick one canonical form for TA5a's biconditional across the summary table, the theorem statement, and the Guarantee clause — either uniformly suppress the redundant `zeros(t) ≤ 3` conjunct on `k = 1`, or uniformly retain it (and then also adjust T10a's axiom text, which currently states the redundant `zeros(t) ≤ 3` precondition on `k' = 1` in parallel with the substantive `zeros(t) ≤ 2` precondition on `k' = 2`).

### "Sibling of Cₓ" overloads "sibling" in T10a.5 inductive step
**Foundation**: (none — internal consistency)
**ASN**: T10a's axiom and T10a.1 use "sibling" for outputs of a single allocator's `inc(·, 0)` chain ("all sibling outputs a satisfy #a = #b"). T10a.5's inductive step writes "every sibling of Cₓ carries `bₓ[j]` at position j. Each child inherits it via TA5(b)…" where Cₓ is an allocator, not a tumbler. The natural reading of "sibling of Cₓ" — a peer allocator under the same parent P — would make Cᵧ a sibling of Cₓ, but the argument is visibly about domain elements of Cₓ's own chain.
**Issue**: The same word denotes (a) within-chain output peers of a tumbler and (b), here, domain elements of a named allocator. Nothing in the surrounding prose marks the switch, and the reading that matches the prior uses (peer allocators) produces a false argument — Cᵧ does not carry `bₓ[j]`. A reader trying to trace the divergence-propagation inductive step can resolve the meaning only from the downstream mention of "Each child inherits it via TA5(b)".
**What needs resolving**: Disambiguate the term at each use in T10a.5's inductive step (e.g., "every element of `dom(Cₓ)`" or "every sibling output produced by Cₓ") so that the propagation argument does not rely on the reader inferring which of the two "sibling" senses is in scope.
