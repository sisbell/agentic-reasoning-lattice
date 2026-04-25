# Regional Review — ASN-0034/T1 (cycle 2)

*2026-04-21 23:52*

### `min(m, n)` is used in T1's proof but no `min` operation is defined in the ASN

**Foundation**: T1 (LexicographicOrder) — proof of part (b), Case 3: "Minimality of `k` rules out any shared-position mismatch — such a mismatch would satisfy (α) at a position `j ≤ min(m, n) < k`, contradicting the minimality — so `aᵢ = bᵢ` for all `i` with `1 ≤ i ≤ m ∧ i ≤ n`."

**ASN**: T0 defines `#· : T → ℕ` and component projection only; NAT-order supplies `<` and `≤`; NAT-addcompat, NAT-cancel, NAT-discrete, NAT-wellorder supply further ℕ properties. None of these establishes a binary `min` operation on ℕ. No other claim in the ASN defines `min`. The recent commit `a5f34644` explicitly notes "drop min(S)", removing another `min` invocation elsewhere; the invocation in Case 3 was not carried along.

**Issue**: `min(m, n)` appears as a load-bearing bound inside a minimality argument, but the ASN nowhere introduces a `min` function. The surrounding statements read precisely — "`j ≤ min(m, n) < k`" is a numerical bound the reader is expected to verify — yet the operation that would make that bound meaningful is absent from the formal vocabulary. The step is rescuable without `min` (split on whether `k = m+1` so `j ≤ m < k`, or `k = n+1` so `j ≤ n < k`, each using the clause already in hand), but as written the prose leans on notation the ASN does not license, and does so right after a cycle whose commit message advertises removing the same notation from a companion argument.

**What needs resolving**: Either introduce `min : ℕ × ℕ → ℕ` (or an equivalent operation) as part of the ASN's formal vocabulary, or rewrite the Case 3 minimality sub-argument so it uses only the clauses that already define (β) and (γ), without passing through a `min` that this ASN does not supply.

---

### `≥` on ℕ is used by NAT-addcompat but NAT-order defines only `≤`

**Foundation**: NAT-order (NatStrictTotalOrder) — formal contract: "The non-strict relation `≤` on ℕ is defined by `m ≤ n ⟺ m < n ∨ m = n`." No definition of `≥` on ℕ.

**ASN**: NAT-addcompat (NatAdditionOrderAndSuccessor) — formal contract: "`(A m, n, p ∈ ℕ : n ≥ p : m + n ≥ m + p)` (left order compatibility); `(A m, n, p ∈ ℕ : n ≥ p : n + m ≥ p + m)` (right order compatibility)". T1's body separately establishes `a ≥ b` for tumblers ("`a ≥ b` abbreviates `b ≤ a`"), but no analogous definition is given for ℕ.

**Issue**: NAT-addcompat is stated in terms of `≥` on ℕ in both order-compatibility clauses, yet the only claim charged with fixing the non-strict companions on ℕ is NAT-order, and it defines only `≤`. The convention that `m ≥ n` means `n ≤ m` is universal, but the ASN is otherwise precise about naming its abbreviations — the tumbler-side `≥` is explicitly introduced at the end of T1, making the ℕ-side omission visibly asymmetric. A reader resolving NAT-addcompat's axiom statement has no in-document definition to bind `≥` against.

**What needs resolving**: Either extend NAT-order's formal contract to define `≥` on ℕ alongside `≤` (e.g., `m ≥ n ⟺ n ≤ m`), or restate NAT-addcompat's clauses using `≤` so they fit within the vocabulary NAT-order already establishes.
