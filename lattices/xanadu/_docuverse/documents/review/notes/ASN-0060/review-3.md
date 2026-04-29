# Review of ASN-0060

## REVISE

### Issue 1: Missing strict-increase corollary
**ASN-0060, OrdinalShift / Statement Registry**: The text says "The shift advances the deepest component by exactly n" but no formal property states `shift(v, n) > v`.
**Problem**: This is the most basic guarantee of a shift — that it moves strictly forward. It follows immediately from TA-strict (since `δ(n, m) > 0`), yet the ASN names three properties (I6, I7, I8) while omitting this one from the formal characterization. Its absence is a gap: without it, monotonicity in the shift amount — `shift(v, n₁) < shift(v, n₂)` when `n₁ < n₂` for fixed `v` — is also unstated. That monotonicity follows from strict increase via I8 decomposition: `shift(v, n₂) = shift(shift(v, n₁), n₂ − n₁) > shift(v, n₁)`. These are derived consequences of the definitions and existing lemmas that belong in the ASN that introduces the shift.
**Required**: Add a named corollary stating `shift(v, n) > v` with one-line derivation from TA-strict. Derive monotonicity in `n` as a further corollary using I8 + strict increase. Add both to the statement registry.

## OUT_OF_SCOPE

### Topic 1: Extension to n = 0 and monoid structure
**Why out of scope**: The shift is a semigroup action of (N≥1, +) on T_m. Extending to n = 0 (identity) would give a monoid action, but δ(0, m) is a zero tumbler, violating the positivity precondition of ⊕. Whether to introduce a separate identity convention is a design choice for a future ASN.

### Topic 2: Connection between shift(v, 1) and inc(v, 0)
**Why out of scope**: When sig(v) = #v, shift(v, 1) coincides with TA5's sibling increment inc(v, 0). Unifying allocation operations with shift arithmetic is natural but belongs in a future ASN.

VERDICT: REVISE
