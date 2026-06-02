# Channel Assignment — ASN-0047 review-292

**Date:** 2026-06-01 21:47

## Issue 1: P4a's "trace property" classification is restated in four locations
Reason: Purely editorial deduplication — consolidate the trace-property classification and discharge to the definition box and reduce the other three to pointers. No design intent or implementation evidence is needed; the fix is derivable from the ASN's own structure.

## Issue 2: K.μ~ clause-(v) "forced, not a guarantee" is restated four times with bidirectional cross-references
Reason: Editorial consolidation of a repeated observation and removal of bidirectional cross-references; the underlying fixity derivation (LRP + CL-UNIQ) is already present, so this is an internal restructuring with no channel input required.

## Issue 3: GlobalLineage is a derived corollary with no consumer in this ASN
Reason: Whether any precondition, invariant discharge, or downstream lemma in this ASN consumes GlobalLineage is checkable from the ASN text alone (it is not), so the keep-with-cited-consumer-or-drop decision is internal.
