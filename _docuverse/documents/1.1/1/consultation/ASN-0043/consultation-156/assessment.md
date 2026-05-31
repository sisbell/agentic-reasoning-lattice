# Channel Assignment — ASN-0043 review-156

**Date:** 2026-05-31 00:38

## Issue 1: FSE under-justifies `home(a') = home(a)` — the exact inference L1c declares insufficient
Reason: The fix is internal — the required observation (each `inc(·, 0)` modifies only the terminal position `#a`, and `#home(a) + 1 < #a` by L1b's `#E(a) ≥ 2`, so the separator zero is untouched) is fully derivable from TA5(c), TA5-SigValid, L1b, and L1c already present in the ASN. No design intent or implementation evidence is needed.

## Issue 2: L9 Case A re-derives L1c's two-CPP home-pinning argument instead of citing the L1c postcondition
Reason: The fix is internal — Case A's constructed chain is an explicit L1c-form chain seeded at `d`, so replacing the duplicated two-CPP block with a citation to L1c's `s = home(a)` postcondition is purely a restructuring of reasoning already in the ASN. No external channel is required.
