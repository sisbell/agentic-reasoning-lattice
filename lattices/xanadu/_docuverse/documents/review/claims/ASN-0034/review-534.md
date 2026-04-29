# Regional Review — ASN-0034/TA5-SIG (cycle 1)

*2026-04-24 14:01*

### Missing discharge of `i + 1 ≥ 1` in TA5-SIG's strict-monotonicity invocation
**Class**: REVISE
**Foundation**: NAT-sub strict monotonicity (Consequence) — requires both `m ≥ p` and `n ≥ p` as preconditions at `p = 1`.
**ASN**: TA5-SIG, contradiction branch: "`i + 1 < m` (then NAT-sub's strict monotonicity at `p = 1`, with both `i + 1 ≥ 1` and `m ≥ 1`, gives `(i + 1) − 1 < m − 1`, i.e., `i < m − 1`)".
**Issue**: `m ≥ 1` is derived via the `1 ≤ i₀ < i₀ + 1 ≤ m` chain, but `i + 1 ≥ 1` is asserted without justification. Obtaining it requires either (a) NAT-addbound's right-dominance `i + 1 ≥ 1` at `(i, 1)`, or (b) chaining `1 ≤ i` (from `i ∈ S ⊆ {1..#t}`) with NAT-addcompat's `i < i + 1` and a weak-bound case-split — neither of which the prose performs. NAT-addbound is not in TA5-SIG's Depends.
**What needs resolving**: Either (i) include an explicit derivation of `i + 1 ≥ 1` for every `i ∈ S` (using `1 ≤ i` together with a cited fact) and list the supporting ASN in Depends, or (ii) restructure the argument so strict monotonicity's second precondition is discharged by facts already in the Depends set.

### TA5-SIG depends on NAT-closure/NAT-zero but does not declare them
**Class**: REVISE
**Foundation**: NAT-sub right-inverse (at `(m, 1)` requires `1 ∈ ℕ`); arithmetic `i + 1`, `m − 1`, and the literal `1` used throughout the proof.
**ASN**: TA5-SIG *Depends:* lists T0, NAT-wellorder, NAT-order, NAT-discrete, NAT-sub, NAT-addcompat — but not NAT-closure or NAT-zero.
**Issue**: TA5-SIG directly uses `1 ∈ ℕ` (to form `m − 1` and as the boundary `1 ≤ i`) and the `+` operator on ℕ (for `i + 1`, `(m − 1) + 1`). These are NAT-closure's commitments; NAT-closure is cited only transitively through NAT-sub and NAT-addcompat. Foundation ASNs typically declare every directly-cited primitive. NAT-zero is similarly used implicitly (the lower bound `1` in `1 ≤ i` for indices derives from T0, but `0 ∈ ℕ` is nowhere needed here — the NAT-zero concern is weaker and may not apply).
**What needs resolving**: Decide whether the Depends slot should list all ASNs whose *symbols* (not just theorems) are used, and add NAT-closure (and possibly NAT-zero) accordingly; or document the convention that transitive supply is sufficient. Whichever convention is adopted must be applied consistently.

### `m ≥ 1` derivation compresses a four-subcase split into one line
**Class**: OBSERVE
**Foundation**: NAT-order `≤`-definition and transitivity of `<`.
**ASN**: TA5-SIG: "the chain `1 ≤ i₀ < i₀ + 1 ≤ m` — with the weak bounds dispatched into `<`-or-`=` cases by NAT-order's `≤`-defining clause and the strict segments composed by NAT-order's transitivity of `<` — yields `1 < m`".
**Issue**: The chain contains two `≤` links and one `<` link. Case-splitting each `≤` via `<` or `=` yields four subcases that each terminate in `1 < m`, but the prose collapses them into a single clause. The argument is correct, but a precise reader must reconstruct the subcases.

### `max(S)` construction is heavy for a bounded-above ℕ-subset
**Class**: OBSERVE
**Foundation**: NAT-wellorder (least-element principle).
**ASN**: TA5-SIG: "The maximum of a bounded nonempty ℕ-subset is not delivered directly by NAT-wellorder... We derive `max(S)` from the least-element principle with `#t` as the explicit boundedness witness."
**Issue**: Deriving `max(S)` inline — via the upper-bound set `U`, least element `m`, contradiction to produce `m − 1`, and subtraction-heavy machinery — embeds a general "bounded-above ℕ-subsets have a maximum" lemma inside TA5-SIG's definition. A reusable `NAT-maxbounded` claim would let multiple downstream ASNs cite a one-line fact instead of re-running this argument. Not a correctness defect; a modularity observation about foundation granularity.

VERDICT: REVISE
