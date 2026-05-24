# Channel Assignment — ASN-0094 review-40

**Date:** 2026-05-23 21:16

```
## Issue 1: NAT-card and NAT-sub derivations are presentation overhead
Reason: Editorial restructuring — move local arithmetic derivations to appendix or upstream foundation ASN. The decision is internal to the framework's presentation and depends on how the foundation gap is to be addressed, not on design intent or implementation evidence.
```

```
## Issue 2: Elementary set-theoretic facts proved at full length
Reason: Editorial discipline about proof granularity. Treating routine finite-set/arithmetic facts as background is an internal presentation choice; neither design intent nor implementation evidence informs the cut.
```

```
## Issue 3: EffectiveWpSimplification's R-registration precondition is implicit
Reason: The R-registration precondition is already stated in Nullify Compatibility within the same ASN. Surfacing it at the corollary statement is a local editorial fix derivable from the ASN's own content.
```

```
## Issue 4: K_res registration timing in Comment walkthrough is ambiguous
Reason: The framework's lifetime-constancy commitment (TypedRelationCatalog Definition) already fixes T_cat at Σ_init; the walkthrough's prose needs to be aligned with that definition. Internal phrasing fix.
```

```
## Issue 5: Repetition of "Registered catalog for this walkthrough" paragraphs
Reason: Editorial deduplication — the convention is uniform and can be stated once at the framework level (Initial-State Baseline). Internal restructuring with no external dependency.
```

```
## Issue 6: Σ-prefix convention is inconsistent across walkthroughs
Reason: Editorial normalization — pick one convention and apply it. No design or implementation question, only consistency.
```

```
## Issue 7: Sh5 audit table presented without catalog-growth procedure
Reason: The framework's META discipline for catalog extensions is a self-contained design decision within the ASN — either declare a snapshot or specify a registration procedure. Both options are derivable from the framework's stated commitments without external input.
```

```
## Issue 8: Layer Composites section is over-engineered for one entry
Reason: Structural/editorial choice — fold into DirectedPair + FDD walkthrough or keep as section. No external dependency.
```

```
## Issue 9: Two near-duplicate paragraphs surface the same layer commitment
Reason: Editorial deduplication — the second paragraph explicitly declares itself expository and redundant. Internal cut.
```
