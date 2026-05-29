# Channel Assignment — ASN-0036 review-146

**Date:** 2026-05-29 01:47

## Issue 1: S8 postcondition (b) is a tautology
Reason: The fix is editorial and internal — drop (b) or recast it as a definition of the labeled partition grounded in S2 (functionality) and S3 (referential integrity), both already proved within the ASN. No design intent or implementation evidence is required.

## Issue 2: S8a prose conflates subtree-contiguity with V-position contiguity
Reason: The correction restates T5's meaning (order-convexity of the prefix subtree, established in ASN-0034) versus V-position contiguity (D-CTG, defined in this ASN). Both facts are already present; distinguishing them is internal mathematical bookkeeping requiring no channel.

## Issue 3: S5 queryability paragraph is implementation-concern essay duplicating an Open Question
Reason: The fix reduces prose to the single derivable consequence (the sharing relation is a function of Σ) and drops the efficiency tangent and Open Question duplicate. This is editorial trimming derivable from the ASN's own content and stated anti-bloat mandate.
