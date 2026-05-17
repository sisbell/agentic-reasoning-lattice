# Channel Assignment — ASN-0086 review-34

**Date:** 2026-05-17 06:42

```
## Issue 1: `#E(a')` count in Appendix B is wrong
Reason: The fix is derivable from the ASN's own definition and consistent prior usage of `#E` (L1b threshold, worked sketch's `#E(a₁) = 2`). The address `1.0.1.0.1.0.2.1.1` has zeros at positions 2, 4, 6, so E = positions 7..9, giving `#E = 3` mechanically.
```

```
## Issue 2: "Prefix ending at second zero" in Appendix B is wrong
Reason: The ASN contradicts itself — R0a Stage 1 already gives the correct formulation ("positions up to and including `D(·)`, which immediately precedes the third zero"). The fix is to align Appendix B with the ASN's own established formulation.
```

```
## Issue 3: "Sibling siblings" typo in Worked Sketch Step 3
Reason: Pure typo; the next sentence in the same passage uses "siblings" correctly. Internal proofreading fix, no external context required.
```
