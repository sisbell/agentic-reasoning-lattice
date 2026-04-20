**NAT-zero (NatZeroMinimum).** `0` is the minimum of ℕ: `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 ≤ n)`.

In words: `0` is itself a natural number, and every natural number is at least `0`. The minimum of a set must be both a member of that set and a lower bound of it — membership so that `0` is among the elements compared, and the inequality so that no element sits below it under `≤`. Either clause alone is strictly weaker: a non-member lower bound (e.g., `−1` bounding ℕ below in ℤ) satisfies the inequality without being an element, and a bare membership claim `0 ∈ ℕ` fixes no ordering of `0` against the other elements.

*Formal Contract:*
- *Axiom:* `0 ∈ ℕ` (zero is a natural number); `(A n ∈ ℕ :: 0 ≤ n)` (zero is a lower bound of ℕ).
