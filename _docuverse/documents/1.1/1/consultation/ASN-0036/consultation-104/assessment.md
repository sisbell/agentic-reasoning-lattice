# Channel Assignment — ASN-0036 review-104

**Date:** 2026-05-11 15:32

```
## Issue 1: Forward dependency of S7c Consequence (b) and `subspace_I` Postcondition (c) on S8's auxiliary lemma
Reason: This is a structural reorganization within the ASN — extracting a T4-validity-of-shift lemma or restating scope. All needed material (S7b, S7c, T10a.4, T4's field-segment constraint, TumblerAdd's prefix rule) is already present; no external evidence required.
```

```
## Issue 2: Auxiliary lemma is vacuous on the existence-proof witness
Reason: This is a proof-presentation choice — either lift the lemma to standalone status or extend S8's existence proof to exercise the k ≥ 1 cases. The operational fact (T10a + TA5(c) producing consecutive allocations) is already established in ASN-0034 and cited in the ASN itself.
```

```
## Issue 3: S6 is mathematically identical to S1
Reason: The reviewer's challenge — whether S6 represents a distinct commitment or duplicates S1 — turns on design intent. Deciding between strengthening S6 (e.g., formally excluding reference-counted GC) and merging it into prose requires knowing whether Nelson views the no-GC commitment as architecturally separate from monotonic growth.
Nelson question: Is the prohibition on garbage-collecting unreferenced Istream content (even when no arrangement references it) an architectural commitment distinct from monotonic growth of the content store, or is it the same commitment stated with different emphasis — and if distinct, what specific reclamation behavior must the formal statement explicitly forbid?
```
