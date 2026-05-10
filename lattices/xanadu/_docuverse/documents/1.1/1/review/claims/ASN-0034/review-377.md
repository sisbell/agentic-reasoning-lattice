# Regional Review — ASN-0034/TA-Pos (cycle 3)

*2026-04-22 16:31*

### Successor-closure axiom is derivable from addition closure plus `1 ∈ ℕ`
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: NAT-closure formal contract: "`1 ∈ ℕ` (one is a natural number); `(A n ∈ ℕ :: n + 1 ∈ ℕ)` (successor closure); `(A m, n ∈ ℕ :: m + n ∈ ℕ)` (addition closure); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity)." Prose: "For every `n ∈ ℕ`, the successor `n + 1 ∈ ℕ`. For every `m, n ∈ ℕ`, the sum `m + n ∈ ℕ`."
**Issue**: The successor-closure clause `(A n ∈ ℕ :: n + 1 ∈ ℕ)` is an immediate instance of addition closure `(A m, n ∈ ℕ :: m + n ∈ ℕ)` combined with `1 ∈ ℕ` (set `m := n, n := 1`). There is no separate successor primitive — the notation `n + 1` refers to the same `+` that addition closure governs. Listing successor closure as a distinct axiom is redundant, and a precise specification should not axiomatize derivable clauses. The redundancy also misleads the reader into thinking successor is an independent operation on ℕ alongside addition, when here it is simply an instance of `+`.
**What needs resolving**: Either drop the successor-closure clause from the formal contract (it follows from the other two), or, if the author wishes to foreground the inductive/Peano-style structure, introduce successor as a named primitive function separate from `+` and relate it to `+` explicitly.
