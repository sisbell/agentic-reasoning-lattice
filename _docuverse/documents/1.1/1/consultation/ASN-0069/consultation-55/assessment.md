# Channel Assignment — ASN-0069 review-55

**Date:** 2026-06-02 15:02

## Issue 1: V4 inherits content from `d_src` in the subsequent-fork case, contradicting J4's `d_op`
Reason: The fix is internal. J4's text — including the `d_op = prev_version` operand rule for the `k = 0` branch — is quoted in the review and is authoritative; the review explicitly forecloses overriding it. Reconciling V4 to inherit from `M(d_op)` is a mechanical restatement against the cited foundation, not a question of design intent or implementation evidence.

## Issue 2: §"Identity by Sub-Allocation" mischaracterizes J4
Reason: The fix is internal. J4's actual text (contemplating both `k = 1` and `k = 0` sub-cases) is quoted in the review; correcting the "extension of J4" framing is a factual reconciliation against that quoted foundation text, requiring no external channel.

## Issue 3: Downstream claims inherit the same `d_src`/`d_op` error
Reason: The fix is internal. Once V4 is reconciled to `d_op` (Issue 1), restating V10(b), the V12(d)/P4★ derivation, and the worked-example caveat is a mechanical propagation derivable from J4 and the ASN's own proof structure.
