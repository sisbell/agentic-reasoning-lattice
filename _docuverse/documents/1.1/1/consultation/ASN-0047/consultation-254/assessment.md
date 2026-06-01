# Channel Assignment — ASN-0047 review-254

**Date:** 2026-06-01 14:31

## Issue 1: The K.δ case-(ii) freshness mechanism is stated three times
Reason: Purely a deduplication/restructuring task — consolidate the FrontierEquivalence and per-`(t,k')` discharge to one location and convert the others to references. No design intent or implementation evidence is at stake; derivable from the ASN's own structure.

## Issue 2: P4 is introduced as a named property only to be declared unsatisfiable
Reason: Editorial removal of a phantom property the ASN itself proves unsatisfiable; the surviving motivation (unscoped bound fails against P7) is already stated in-text. Internal restructuring requiring no external channel.
