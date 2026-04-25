**TA7a.3 (SubspaceZeroResidue).** When the minuend and subtrahend coincide, subtraction collapses the residue to the zero tumbler: `o ⊖ o ∈ Z`.

  `(A o ∈ S : o ⊖ o ∈ Z)`

*Proof.* Let `o ∈ S`. Then `o ∈ T` and `o ≥ o` by the reflexivity of T1's ordering, so TA2 gives `r := o ⊖ o ∈ T`. NAT-order's trichotomy on `(#o, #o)` selects sub-case (α) `#o = #o` with `L = #o`; no zero-padding is required.

The zero-padded sequences of `o` and `o` agree at every position; hence `zpd(o, o)` is undefined and TumblerSub's no-divergence branch produces the zero tumbler `[0, ..., 0]` of length `L = #o`. Every component of `r` equals `0 ∈ ℕ` (NAT-zero), so the universal clause of TA-Pos's `Zero` predicate, `(A i : 1 ≤ i ≤ #r : rᵢ = 0)`, is satisfied. Therefore `Zero(r)` holds, placing `r ∈ Z` by TA-Pos's **Z** definition.

As a sentinel, `r` is not a valid address (TA6) and serves as a lower bound relative to every positive tumbler (TA-PosDom); its appearance as the self-subtraction residue marks the "no-displacement" fixed point of `⊖`. ∎

Example: `[1, 2] ⊖ [1, 2] = [0, 0] ∈ Z`.

*Formal Contract:*
- *Preconditions:* `o ∈ S`.
- *Depends:*
  - TA7a (SubspaceClosure) — parent claim defining **S** and establishing the complementary in-S branch whose precondition `o₁ > w₁` this sub-claim negates via `o = w` (which forces `o₁ = w₁`).
  - T0 (CarrierSetDefinition) — carrier `T` and length `#`.
  - T1 (LexicographicOrder) — reflexivity of `≥` delivering `o ≥ o`.
  - TA-Pos (PositiveTumbler) — `Zero` predicate and **Z** definition.
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ o ∈ T`.
  - TumblerSub (TumblerSub) — no-divergence branch producing the zero tumbler of length `L`.
  - TA6 (ZeroTumblers) — invalidity of zero tumblers as addresses.
  - TA-PosDom (PositiveDominatesZero) — lower-bound status of the zero-tumbler residue relative to every positive tumbler.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #o)` names `L = #o`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for every component of the zero tumbler.
- *Postcondition:* `o ⊖ o ∈ Z`, with every component zero.
