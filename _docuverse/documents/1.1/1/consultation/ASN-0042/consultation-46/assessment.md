# Channel Assignment — ASN-0042 review-46

**Date:** 2026-05-14 07:09

```
## Issue 1: T8 is misattributed for Σ.B monotonicity
Reason: Pure citation fix internal to the formal framework — replace T8 (allocator-domain) with ASN-0040's B0/B0★ (baptismal-registry) at the sites that need registry monotonicity. The correct property already exists in the foundation; no design intent or implementation evidence is required.
```

```
## Issue 2: Worked example invokes B1 to force ancestor baptisms it does not actually force
Reason: The simplest remedies — restructure the example so its hwm values follow from explicitly listed baptisms (option a), or attribute the intermediate document baptisms to explicit Bop calls (option b) — are entirely internal. B1's actual scope (intra-stream) and Bop's precondition (B6 only, no parent-in-Σ.B requirement) are stated in the ASN; the reviser can rewrite the example consistent with what those properties say.
```
