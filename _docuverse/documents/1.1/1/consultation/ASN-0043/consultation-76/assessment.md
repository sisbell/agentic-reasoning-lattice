# Channel Assignment — ASN-0043 review-76

**Date:** 2026-05-30 08:54

## Issue 1: Worked-example S7d derivation gives a false allocation chain for `d`
Reason: Pure tumbler-arithmetic correction — the fix (use `r = 1.0.1` user-level seed, verify `inc(r, 2) = 1.0.1.0.1 = d`) is fully determined by T10a/TA5a and `inc` semantics from ASN-0034 already cited in the ASN. No design intent or implementation evidence needed.

## Issue 2: `subspace_I` notational convention closes with a downstream use-site inventory
Reason: Editorial trim of a definition's per-consumer roll-call; the projection's meaning and well-definedness precondition are stated in the ASN itself. Internal.

## Issue 3: L11a draws a boundary it does not own and defers to L12
Reason: Editorial reduction of meta-prose; L11a's substantive claim (distinct events ⟹ distinct addresses) is already stated and the L12 relationship is internal to this ASN. Internal.

## Issue 4: L1c carries defensive prose justifying its own formulation
Reason: Straight deletion of a defensive sentence whose work is already done by the existing T4-validity postcondition. Internal.

## Issue 5: Three sections defer to a single "chain-prefix-preservation" argument
Reason: Structural refactor extracting an already-composed argument (from TA5(b)/(c), TA5-SigValid, T10a.4 — all ASN-0034) into a named local lemma cited by L1c, Home/Ownership, L9, L11b. The lemma's content is wholly internal. Internal.
