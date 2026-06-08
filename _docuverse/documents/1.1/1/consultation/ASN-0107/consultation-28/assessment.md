# Channel Assignment — ASN-0107 review-28

**Date:** 2026-06-08 12:41

## Issue 1: D3 conflates the existence count with the discovery count — as written it contradicts E1/E2
Reason: The fix is internal — scoping D3 to `num_disc` and noting the existence-count zero certifies historical absence follows directly from the note's own E1/E2 and the definitions of `num` vs `num_disc`. No design intent or implementation evidence is required.

## Issue 2: Claim label `P0a` is introduced before `P0`
Reason: Purely a labeling/ordering decision internal to the document; renumbering or relabeling needs neither design intent nor implementation evidence.
