**NAT-addassoc (NatAdditionAssociative).** Addition on ℕ is associative: `(m + n) + p = m + (n + p)` for every `m, n, p ∈ ℕ`.

This is a standard property of ℕ, stated here as an axiom so downstream proofs can cite it directly. The ASN's convention (T0) is that each proof cites only the ℕ facts it actually uses; associativity is used in TS3 (to reconcile `(vₘ + n₁) + n₂` with `vₘ + (n₁ + n₂)` at the shared action point) and in TA-assoc (to reconcile `(aₖ + bₖ) + cₖ` with `aₖ + (bₖ + cₖ)` in the coincident-action-point case). Without an explicit axiom those citations would appeal to background arithmetic, breaking the citation policy that the other NAT-* axioms enforce.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` (associativity of addition on ℕ).
