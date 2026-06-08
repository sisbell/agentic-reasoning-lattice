# Channel Assignment — ASN-0111 review-4

**Date:** 2026-06-07 23:19

## Issue 1: Worked-example coverage of the type endset is computed as a singleton, contradicting the coverage semantics the ASN itself established
Reason: The fix is internal — PrefixSpanCoverage (L-claim of ASN-0043) is already cited in the ASN, and the correct coverage of a `δ(1, #x)` span as the subtree `{t : x ≼ t}` is fixed by the coverage definition the note already states and applies to the structurally identical from-span. No design intent or implementation evidence is in question; only the set value must be recomputed consistently.
