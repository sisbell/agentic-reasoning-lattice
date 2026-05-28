# Channel Assignment — ASN-0101 review-19

**Date:** 2026-05-27 20:24

## Issue 1: D10's J1★ vacuity argument has a missing case (S = s_L)
Reason: The fix is mechanical — adding the missing `S = s_L` case to the enumeration. D6 (already in this ASN) and D0's effect specification provide all the content needed; the reviewer even supplies the exact wording.

## Issue 2: D8 Group (i) discharge of S8★ asserts a length-1 decomposition but doesn't address whether `M'(d)` actually admits the canonical (maximally merged) decomposition
Reason: The simplest discharge — clarifying that S8★ is existential and that the singleton decomposition suffices — is internal. The ASN already discusses non-reconciliation under "no reconciliation across the gap"; the fix is a rhetorical clarification, not a new claim.

## Issue 3: D11's `wp(DEL, ¬Q_disc) ≡ ¬wp(DEL, Q_disc)` step relies on determinism
Reason: D1 already establishes σ_d's injectivity via TS2. The fix is purely a citation addition within D11's determinism paragraph; no external evidence is required.

## Issue 4: Example coverage of D9 bullet 2 is uniformly vacuous
Reason: Either option (add a fourth example with both subspaces populated, or explicitly note the vacuous verification) can be constructed from the ASN's existing apparatus (D0, D6, D9). No external input required.

## Issue 5: Argument about why DEL ≠ K.μ⁻ + K.μ~ rests partly on external observability of `Σ_mid`
Reason: The fix is to ground "observability" in a formal predicate over SequentialAtomicTransitions' history sequence (already cited in the ASN from ASN-0093), or to cleanly separate the load-bearing sequence-length argument from the corroborative observational one. Both routes are internal rewording.
