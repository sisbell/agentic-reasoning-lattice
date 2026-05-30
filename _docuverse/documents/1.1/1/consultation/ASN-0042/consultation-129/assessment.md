# Channel Assignment — ASN-0042 review-129

**Date:** 2026-05-30 06:03

## Issue 1: Forward-reference inventory in the opening predicate section
Reason: Purely editorial—trim the guarantee inventory and Open-Questions defer while keeping the factual scope claim (`tumbleraccounteq` realizes `owns`/O1, not `ω`), which is already established in the ASN. No design intent or implementation evidence needed.

## Issue 2: O7(c)'s "entry-state-only" caveat stated three times
Reason: Pure deduplication—consolidate the identical hedge into the proof and leave bare claims in the postcondition and Formal Contract. The restriction and its reasoning are already fully present in the ASN.

## Issue 3: Dangling "first equality" reference in O3
Reason: Internal wording fix—only one equality is displayed, so drop "first." Derivable from the ASN text alone.
