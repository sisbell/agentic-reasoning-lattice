# Channel Assignment — ASN-0069 review-37

**Date:** 2026-05-27 15:01

```
## Issue 1: V11a — imprecise sibling-stream-index bound for subsequent forks
Reason: Pure internal-consistency fix; the tightening to m ≥ 2 follows mechanically from V1's first-fork/subsequent-fork dichotomy and the TA5(c) sibling-step arithmetic already worked through in the worked example (d_new² has value 2 at position #d_src + 1). No design intent or implementation evidence is consulted.
```
