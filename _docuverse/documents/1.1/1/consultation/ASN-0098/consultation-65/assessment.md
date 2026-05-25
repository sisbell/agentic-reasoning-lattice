# Channel Assignment — ASN-0051 review-65

**Date:** 2026-05-17 18:17

## Issue 1: Construction-pattern generalisation lacks rigor for higher (m, p)
Reason: The fix is internal — explicit induction on (m+p) or additional anchor witnesses uses only the block-decomposition machinery from ASN-0058 and tumbler arithmetic already in scope. No design intent or implementation evidence is needed.

## Issue 2: Pigeonhole sub-case analysis in SV11 disjoint-pair case (b) at m=2
Reason: Pure proof-refactoring task — consolidating three redundant sub-cases into one integrated argument. The argument structure (non-empty subsets of a 2-element set either share an element or are ordinally adjacent singletons) is derivable from the existing decomposition; no external input required.

## Issue 3: SV13(e) K.δ caveat under-covers the new-document case
Reason: The empty-locate-on-new-document claim is already established by the locate definition applied to the empty arrangement; restructuring the clause is purely editorial. Internal fix using machinery the ASN already contains.

## Issue 4: SV6 narrative gloss conflates origin-of-address with origin-of-allocator
Reason: The two notions (structural origin via T4-projection vs. allocator identity via T10a/S7d) are both already in scope from ASN-0034 and ASN-0036. The fix is to distinguish them explicitly in the prose; no new design intent or implementation evidence is needed since SV6's proof relies only on the structural reading.

## Issue 5: Prose drift in "After reordering" admissibility argument
Reason: The clarification cites ASN-0047's existential reading of K.μ~, which is already a sibling ASN in scope. The fix is a one-sentence editorial addition referring to existing ASN content — no Nelson or Gregory input required.
