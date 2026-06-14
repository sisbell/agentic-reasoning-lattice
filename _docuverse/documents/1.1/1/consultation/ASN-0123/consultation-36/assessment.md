# Channel Assignment — ASN-0123 review-36

**Date:** 2026-06-13 17:07

## Issue 1: V-WF and V9 circularly cross-cite and duplicate the cross-owner stream-form derivation
Reason: Purely expository — the fix reassigns citation ownership and drops one of two already-complete derivations. The review itself confirms neither citation is load-bearing (both facts are proven in both places: `Document(v)` from `zeros(v)=zeros(pfx(π))+1=2` and B6(a); the single K.δ from the stream form), so the math is wholly internal to the ASN. No design intent or implementation evidence is at stake.

## Issue 2: VD states the registry-decides-derivation result twice, plus a third time in the table
Reason: Pure deduplication — choosing one of two equivalent phrasings (`derives(v,d) ⟺ v ∈ E` vs. the `derives_addr` form) and removing the table echo. Nothing turns on design intent or the implementation; the redundancy is internal to the note.
