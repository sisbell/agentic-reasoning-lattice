# Regional Review — ASN-0034/T4a (cycle 2)

*2026-04-22 01:01*

### NAT-discrete missing from T4c's Depends
**Foundation**: NAT-discrete supplies the step from `0 ≤ n ≤ k` to `n ∈ {0, 1, …, k}` in ℕ
**ASN**: T4c's Exhaustion step: "By T4, `zeros(t) ≤ 3`; NAT-zero supplies `0 ≤ zeros(t)`; so `zeros(t) ∈ {0, 1, 2, 3}` on the T4-valid subdomain." T4c's Depends lists only T0, NAT-zero, NAT-order, T4.
**Issue**: From `0 ≤ zeros(t) ≤ 3` alone, one cannot conclude `zeros(t) ∈ {0, 1, 2, 3}` — in a non-discrete ordered structure there could be intermediate values. The step requires NAT-discrete (applied to force the successor after each of 0, 1, 2 to be the next integer). NAT-order's trichotomy and irreflexivity do not supply discreteness. T4b's Depends correctly cites NAT-discrete; T4c's does not, even though the same kind of "between 0 and 3 in ℕ" reasoning is used.
**What needs resolving**: Either add NAT-discrete to T4c's Depends and cite it explicitly at the Exhaustion step, or recast Exhaustion so it does not depend on the discreteness of ℕ between 0 and 3.

### `#` symbol overloaded between tumbler length and set cardinality
**Foundation**: T0 introduces `#·` on `T` only
**ASN**: T0 axiom: "equipped with length `#· : T → ℕ`". T4 prose and T4c: "Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`." T4a proof: "The zero positions … `p₁ < … < pₖ`" where `k = zeros(t)`.
**Issue**: `#` is defined in T0 only as the length of a tumbler — a function `T → ℕ`. But `#{i : …}` applies `#` to a *set* (a subset of `{1, …, #t}`). That is set cardinality, a distinct operation with no formal contract in this ASN, and no statement that it lands in ℕ. The definition of `zeros(t)` — and every subsequent use of `zeros(t) ∈ ℕ` (for NAT-zero's lower bound, for Exhaustion, for the bijection `{0,1,2,3} → {labels}`) — relies on this unstated operator.
**What needs resolving**: Either introduce a separate cardinality operator for finite sets of indices (with its codomain ℕ) and use a distinct symbol, or rewrite `zeros(t)` in terms already in scope (e.g., as the length of the subsequence of zero-valued components, leveraging T0's `#·`).

### T4 Formal Contract has no Depends slot
**Foundation**: structural — other claims in this ASN (T4a, T4b, T4c) each carry an explicit Depends slot
**ASN**: T4's Formal Contract has *Axiom*, *Preconditions*, *Postconditions*, but no *Depends*. Its Axiom names dependencies in prose: "Positivity of non-zero components follows from T0, NAT-zero, and NAT-discrete."
**Issue**: T4 is presented in parallel with T4a, T4b, T4c as a numbered theorem with a Formal Contract, but unlike them its dependencies are only mentioned inline. A reader checking which foundations T4 leans on must infer them from the Axiom prose. The positivity clause, the field-separator role, and the `zeros(t) ≤ 3` bound all sit downstream of T0 and the NAT-* claims, yet no Depends slot acknowledges this.
**What needs resolving**: Either add a Depends slot to T4's Formal Contract listing the foundations it rests on (T0, NAT-zero, NAT-discrete; and NAT-order if trichotomy is needed), or mark T4 structurally as axiomatic (with no dependencies) and relocate the "follows from" claims into a proof or justification section.

### T4c Injectivity proof and bijection claim misaligned
**Foundation**: T4c's stated Postcondition — "The induced mapping restricted to the T4-valid subdomain is a bijection `{0, 1, 2, 3} → {node, user, document, element}`"
**ASN**: T4c's Injectivity argument: "The values `0, 1, 2, 3` are pairwise distinct in ℕ (NAT-order trichotomy), and `zeros(t)` is single-valued. So distinct zero counts yield distinct labels."
**Issue**: The mapping claimed bijective has domain `{0, 1, 2, 3}` and codomain `{node, user, document, element}` — four elements each, named. Injectivity of such a four-element function reduces to "the four label names denote distinct concepts." The proof as written instead argues that "distinct zero counts yield distinct labels," which is a statement about the label-assignment of tumblers, not about the 4-element mapping. Meanwhile "Surjectivity" exhibits witness tumblers — again a statement about which zero counts are realised on `T`, not about the 4-element mapping. The proof structure is reasoning about one thing (level-assignment on `T`) while the postcondition names another (a 4-element bijection).
**What needs resolving**: Either reframe the Postcondition so it matches what the proof actually shows (e.g., every level label is realised by some T4-valid tumbler, and the four labels are pairwise distinct), or reframe the proof so it directly establishes the 4-element bijection claimed.
