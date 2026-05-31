# Channel Assignment — ASN-0043 review-137

**Date:** 2026-05-30 21:38

## Issue 1: The Link definition's prose enumerates downstream consumers instead of advancing the definition, and misattributes the `.type` accessor
Reason: Internal fix. The defect is editorial — the Link definition already carries the formal content (`N`-tuple of endsets, N ≥ 3), and the slot-3-as-type convention is already fixed at the Named accessor/StandardTriple site. Relocating the convention and stripping the L3/L8/StandardTriple inventory requires only the ASN's existing text; no design intent or implementation evidence is at stake.

## Issue 2: L5's formal statement is set-theoretic extensionality, not a model invariant; its load-bearing content is unformalized
Reason: Internal fix. L5's intended content — no span-positional accessor exists within an endset, equality inherited from `𝒫_fin(Span)` — is already stated in the ASN's own prose and is the structural dual of L6, which is also already present. Reformulating the invariant to capture that commitment is derivable from the ASN alone; it concerns how the model states its own operator set, not what Nelson intended or what udanax-green enforces.
