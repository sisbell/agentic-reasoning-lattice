# Channel Assignment — ASN-0042 review-45

**Date:** 2026-05-14 06:53

```
## Issue 1: hwm description is technically incorrect in O10 non-coverage analysis
Reason: Fix is internal — replace the incorrect parenthetical with the correct ASN-0040 citation chain (hwm cardinality + B1 ContiguousPrefix). Both definitions are already imported facts of the ownership model and the review prescribes the exact replacement text.
```

```
## Issue 2: Worked example cites O5 for delegation authority
Reason: Fix is internal — the ASN's own Delegation section explicitly distinguishes allocation (O5) from delegation (condition (ii) of the `delegated` relation), and the review prescribes the exact citation correction.
```

```
## Issue 3: O10 proof references `S'` without formal definition
Reason: Fix is internal — `S'` is a notational gap; either define it explicitly using the existing Form B sub-delegate machinery already in the proof, or restate the bound in existing notation. The review prescribes both options.
```
