**NAT-carrier (NatCarrierSet).** `ℕ` is a set, the carrier of natural numbers on which the NAT-* claims posit their operations and relations.

The declaration is irreducible at this level: `ℕ` is taken as a primitive — not constructed from a more elementary substrate, not extracted from the meta-language by ambient definability, but committed-to as a set whose elements the subsequent NAT-* axioms thereafter quantify over. Every Cartesian product `ℕ × ℕ` (NAT-order's `< ⊆ ℕ × ℕ`, NAT-closure's `+ : ℕ × ℕ → ℕ`), every membership `x ∈ ℕ` (NAT-zero's `0 ∈ ℕ`, NAT-closure's `1 ∈ ℕ`), and every set-builder `{j ∈ ℕ : ...}` (T0's index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}`) presupposes this primitive commitment.

No further structure on `ℕ` is asserted here. The strict order `<` is introduced by NAT-order, the constants `0` and `1` by NAT-zero and NAT-closure respectively, the binary operation `+` by NAT-closure, and discreteness by NAT-discrete. NAT-carrier supplies only the carrier set on which those subsequent commitments are layered.

*Formal Contract:*
- *Axiom:* `ℕ` is a set (the carrier of natural numbers).
- *Depends:* (none).
