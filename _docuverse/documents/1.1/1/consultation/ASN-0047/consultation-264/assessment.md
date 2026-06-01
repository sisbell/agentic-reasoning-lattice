# Channel Assignment — ASN-0047 review-264

**Date:** 2026-06-01 16:06

## Issue 1: D-CTG★/D-MIN★ adopted on the link subspace despite the ASN's own admission that they contradict the design
Reason: Choosing between (a) retaining the link-subspace exemption and (b) justifying a gap-free link arrangement requires both the design intent (whether tombstoning must surface as interior gaps in the arrangement or only in I-space) and implementation evidence (whether the POOM keeps gaps or compacts-and-renumbers survivors).
Nelson question: Does the tombstoning design require withdrawn interior links to remain at their original arrangement positions (leaving gaps), or is it satisfied by retaining the withdrawn link's permanent address while the arrangement layer is free to be gap-free?
Gregory question: When DELETEVSPAN removes an interior link, does the POOM leave a gap at that V-position or compact-and-renumber every subsequent link's V-address, and is the surviving order otherwise preserved?

## Issue 2: K.δ case (ii) freshness for k ∈ {1,2} is claimed "discharged by an axiom" when it is in fact a caller-checked guard
Reason: The fix is a reframing of the logical relationship between the `e ∉ E` precondition and T10a's per-(t,k') uniqueness, fully derivable from the ASN's own K.δ definition and T10a references.
