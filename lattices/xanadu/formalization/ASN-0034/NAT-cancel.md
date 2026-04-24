**NAT-cancel (NatAdditionCancellation).** Addition on ℕ is cancellative on either side. A sum equals one of its summands only when the other summand is zero — a consequence of cancellation together with NAT-closure's two-sided additive identity.

- Left cancellation (axiom): `m + n = m + p ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Right cancellation (axiom): `n + m = p + m ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Summand absorption (consequence): `m + n = m ⟹ n = 0` for every `m, n ∈ ℕ`.

Summand absorption is recorded as a consequence rather than an axiom because both its posited form `m + n = m ⟹ n = 0` and its mirror form `n + m = m ⟹ n = 0` are derivable from the two cancellation axioms together with NAT-closure's two-sided additive identity. From the hypothesis `m + n = m` and NAT-closure's right identity `m + 0 = m` we have `m + n = m + 0`; left cancellation, instantiated at `p := 0`, then delivers `n = 0`. The mirror form admits the parallel walk: from the hypothesis `n + m = m` and NAT-closure's left identity `0 + m = m` we have `n + m = 0 + m`; right cancellation, instantiated at `p := 0`, then delivers `n = 0`.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` (left cancellation); `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` (right cancellation).
- *Consequence:* `(A m, n ∈ ℕ : m + n = m : n = 0)` (summand absorption, posited form) — derived from the left-cancellation axiom and NAT-closure's right additive identity `n + 0 = n` instantiated at `n := m`, as shown in the preceding prose; the mirror form `(A m, n ∈ ℕ : n + m = m : n = 0)` is the parallel consequence, derived from right cancellation and NAT-closure's left additive identity `0 + n = n` instantiated at `n := m`.
- *Depends:*
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the binary operation `+ : ℕ × ℕ → ℕ` used in all clauses; the right additive identity `(A n ∈ ℕ :: n + 0 = n)`, instantiated at `n := m`, used to rewrite the RHS of `m + n = m` to `m + 0` in the derivation of the posited absorption form from left cancellation; and the left additive identity `(A n ∈ ℕ :: 0 + n = n)`, instantiated at `n := m`, used to rewrite the RHS of `n + m = m` to `0 + m` in the parallel derivation of the mirror form from right cancellation.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` on the right-hand side of the absorption conclusion `m + n = m ⟹ n = 0`.
