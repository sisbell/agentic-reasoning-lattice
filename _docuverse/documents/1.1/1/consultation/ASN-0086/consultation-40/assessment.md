# Channel Assignment — ASN-0086 review-40

**Date:** 2026-05-17 16:32

```
## Issue 1: "Enumeration index" terminology in R0 Step 2 Case A conflates two distinct concepts
Reason: Pure terminology/notational fix. The ASN defines T10a.7's enumeration-index convention; aligning prose with that convention (or adding a one-line note distinguishing "last-component value" from "enumeration index") is derivable from the ASN's own content.
```

```
## Issue 2: R0a-Cor1's induction quantifier scope should be →_D, not →
Reason: Mechanical scope fix. R0a explicitly restricts to `→_D*`-reachability, and R0a-Cor1's "Under R0a's hypothesis" qualifier means it inherits the same restriction; updating the quantifier is internal bookkeeping.
```

```
## Issue 3: SharedDepthOneAllocator is an unnumbered lemma with downstream citations
Reason: Numbering/citation-convention fix. The lemma's content, proof, and dependency relationships to R0 and R0a-Cor2 are already established in the ASN; assigning a number or documenting the convention is editorial.
```

```
## Issue 4: No explicit weakest precondition analysis
Reason: The wp computations are derivable from existing ASN content — Nullify's P0–P3 + discipline + regime (i)/(ii) analysis, Emit_K's A_K-membership remark under regimes (i)/(ii), and R6b's single-depth design are all explicit. The fix is to label and present these as wp computations.
```
