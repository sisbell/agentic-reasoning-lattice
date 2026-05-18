# Channel Assignment — ASN-0047 review-88

**Date:** 2026-05-17 20:10

```
## Issue 1: K.λ missing from "Properties Introduced" table
Reason: K.λ is already fully defined in the "Link allocation" section of this ASN; adding a summary row to the table is a mechanical documentation fix derivable from existing content.
```

```
## Issue 2: L1c not explicitly verified or listed in ExtendedReachableStateInvariants
Reason: L1c is a foundation axiom from ASN-0043, and K.λ's allocation discipline (first emission via SubAllocatorAxiom, subsequent via inc(·, 0)) is already specified in this ASN. Verifying preservation is mechanical against the K.λ preconditions.
```

```
## Issue 3: "K.δ discharge table" referred to but does not exist as a table
Reason: Pure presentation fix — either render the existing per-sub-case bullet list as a table or change worked-example references to match the current structure.
```

```
## Issue 4: "Path 0/1/2" terminology used in worked examples but not defined in the K.δ definition
Reason: The three discharge paths are already described in K.δ's *Freshness discharge* paragraph; assigning explicit Path 0/1/2 labels is internal cross-referencing.
```

```
## Issue 5: P3★ entry references "ASN-0036's P0/P1/P2"
Reason: Factual attribution fix internal to this ASN — P0/P1/P2 are introduced here (P0 subsumes ASN-0036's S0/S1; P1 specialises ASN-0034's T8; P2 is fresh), as already stated in this ASN's own text.
```

```
## Issue 6: wp derivation phrasing "substituting R for R'" is non-standard
Reason: Standard wp-calculus rephrasing using the frame condition R' = R; internal style/convention fix.
```

```
## Issue 7: L14 entry claims "no L14 label in the foundation"
Reason: Factual attribution against ASN-0043, which is a sibling ASN in this project — its L14 (DualPrimitive) statement can be checked directly without expert consultation.
```
