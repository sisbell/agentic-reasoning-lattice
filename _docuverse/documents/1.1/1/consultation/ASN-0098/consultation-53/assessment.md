# Channel Assignment — ASN-0051 review-53

**Date:** 2026-05-16 07:00

## Issue 1: Citation inconsistency for L3
Reason: Pure naming/citation reconciliation between ASN-0043 (L3 = NEndsetStructure) and ASN-0047 (L3 = TripleEndsetStructure). The review itself identifies the canonical names; the fix is choosing a consistent citation, derivable from the ASN's own references.

## Issue 2: Citation inconsistency for K.δ
Reason: Naming fix — the review establishes that K.δ in ASN-0047 is "EntityCreation" with document allocation as a sub-case, not a separately-named "DocumentAllocation" transition. Other K.δ usages in the ASN already follow the correct convention. Fix is internal.

## Issue 3: SV11 multi-block attainment
Reason: The question is structural — whether the m·p bound is attainable for p ≥ 2 given D-CTG V-contiguity, span-as-interval, and the non-adjacency/non-overlap condition. The review sketches the argument; all machinery (D-CTG, S0 convexity, T1 interval structure, M11/M12 block decomposition) is already in scope from cited ASNs. Internal.

## Issue 4: SV5 locate transformation is not formally stated as an SV claim
Reason: The locate transformation `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}` is already derived in SV5's discussion. The fix is a presentation choice (extend SV5 or add SV5b) — purely internal labeling.

## Issue 5: SV6 sub-lemma proof structure — split needed
Reason: Stylistic restructuring of an already-correct proof. The review explicitly states the proof's correctness is not in question; the fix is splitting the sub-lemma into two named claims for readability. Internal.
