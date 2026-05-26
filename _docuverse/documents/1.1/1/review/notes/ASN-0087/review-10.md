# Review of ASN-0087

## REVISE

### Issue 1: L1c uniqueness argument for k₁ = 1 has incorrect reasoning

**ASN-0087, "Per-State Invariants at Σ'" — uniqueness strengthening, k₁ case**: "k₁ = 1 produces `[d, 1]` of length `#d + 1` with no zero introduced — but every subsequent step starting from this state cannot reach an `ℓ` with `zeros(ℓ) = 3` without first introducing the third zero via a `k = 2` step, and the resulting structure would have `E(·)₁ = 1 = s_C` (not `s_L`), contradicting L0."

**Problem**: The claim that the resulting structure has `E(·)₁ = 1` does not hold throughout the chain. After `k₁ = 1` then `k = 2` (possibly with intermediate `k = 0` steps), we reach a state like `[d, m, 0, 1]` (where `m ≥ 1` accumulates from any intermediate `k = 0` steps). At this state `sig = #d + 3`, and subsequent `inc(·, 0)` modifies position `#d + 3`, giving `[d, m, 0, 2]` where `E(·)₁ = 2 = s_L`. Extending with `k = 1` then gives `[d, m, 0, 2, 1]`, which is T4-valid with `zeros = 3`, `E(·)₁ = 2 = s_L`, `#E = 2`. So `E(·)₁ = s_L` is reachable in the `k₁ = 1` branch — the stated contradiction with L0 does not hold.

The argument in the parallel `k₂ = 1` case is correct (after `[d, 0, 1, 1]`, `sig = #d + 3` and position `#d + 2` is permanently fixed at 1 by fact (a)) because in that case the third zero falls at position `#d + 1` and E(·)₁ lives at position `#d + 2`. In the `k₁ = 1` case the third zero falls at position `> #d + 1`, so E(·)₁ lives at a position that *is* the `sig` target of subsequent `k = 0` steps — the "permanent fixity" reasoning does not transfer.

**Required**: Replace the `E(·)₁` argument with the correct origin-based argument: after `k₁ = 1`, position `#d + 1` of every reachable state is nonzero (`= 1` initially, possibly higher after `k = 0` steps, but never zero since `inc` never sets a nonzero to zero). Hence the third zero of any reachable address falls at position `≥ #d + 2`, so `D(·)` extends beyond position `#d` and `origin(·) ≠ d`. Since L1c requires `t₀ = origin(ℓ)` and the chain starts at `d`, no chain beginning with `k₁ = 1` can end at an `ℓ` with `origin(ℓ) = d`. The conclusion (`k₁ = 1` excluded) holds; the proof needs this redirection.

## OUT_OF_SCOPE

None — the ASN's stated open questions cleanly defer future-ASN territory (well-formedness of forward-reaching endsets, protocol-layer atomicity, deferred-consistency models, link V-position movement).

META: The ASN remains in specification territory throughout — composite identification, precondition derivation, weakest-precondition analysis, invariant preservation, and a worked example all stay at the abstract-state-machine level.

VERDICT: REVISE
