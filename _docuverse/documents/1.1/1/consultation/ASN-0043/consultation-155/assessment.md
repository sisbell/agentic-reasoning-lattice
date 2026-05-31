# Channel Assignment — ASN-0043 review-155

**Date:** 2026-05-31 00:26

## Issue 1: T7 cited under a non-existent foundation name
Reason: Pure rename derivable from the ASN alone — the L9 worked example already cites the correct name "T7 (SubspaceDisjointness, ASN-0034)", so the canonical name is present internally; no design intent or implementation evidence is required.

## Issue 2: The L1c `s = home(a)` derivation rests on CPP, which provably cannot reach position `#s + 1`
Reason: The fix is a self-contained proof repair — a second CPP invocation on the post-seed sub-chain with `p = #s + 1`, using lemmas (CPP, TA5) already stated in the ASN; no external design or implementation input is needed.
