# Channel Assignment — ASN-0043 review-140

**Date:** 2026-05-30 21:59

## Issue 1: L5 carries provenance commentary explaining why the invariant is needed, not what it says
Reason: Purely editorial. The operative content (no span-positional accessor; access by membership only) is already stated in the surrounding sentences, and extensional equality follows mechanically from `Endset = 𝒫_fin(Span)`. No design intent or implementation evidence is needed to drop the inherited-equality framing.

## Issue 2: L6's "structural dual of L5" paragraph is relationship essay, not L6 content
Reason: Purely editorial. L6's teeth (slot index as primitive, positional accessor `Σ.L(a).eᵢ`, component-wise tuple equality) and the standard-triple consequence are already present; removing the dual-of-L5 framing is a prose deletion derivable from the ASN alone.
