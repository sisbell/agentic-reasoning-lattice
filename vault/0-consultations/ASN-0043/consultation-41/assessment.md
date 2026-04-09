# Revision Categorization — ASN-0043 review-41

**Date:** 2026-04-09 15:36



## Issue 1: L9 witness construction assumes content store finiteness without justification
Category: INTERNAL
Reason: The fix is entirely derivable from the existing proof structure — the review itself identifies that the ghost address safety follows from subspace separation alone, and that address freshness follows from L-fin and T0(a), making the overly strong fresh-prefix constraint droppable without any external evidence.

## Issue 2: L11b L1c verification references wrong allocation frontier
Category: INTERNAL
Reason: The fix is a correction to the proof's internal reasoning about allocator state — replacing a specific sibling reference with the allocator's current frontier. The necessary concepts (T9 forward allocation, T10a allocator discipline) are already defined in ASN-0034 and cited in the proof body.
