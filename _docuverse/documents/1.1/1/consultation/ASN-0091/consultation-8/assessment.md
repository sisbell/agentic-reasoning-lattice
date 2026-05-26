# Channel Assignment — ASN-0091 review-8

**Date:** 2026-05-26 15:58

## Issue 1: Abstract definition implicitly requires d ∈ dom(Σ.M) without stating it
Reason: Pure definitional fix — adding an explicit precondition that aligns with K.μ~'s existing `d ∈ E_doc` from ASN-0047. No design intent or implementation evidence needed; derivable from the ASN's own formal scaffolding.

## Issue 2: Reverse witness coalescence requires justifying why cross-chain disjointness implies c ∉ {a-1, a+2}
Reason: The structural-form argument rests on sub-allocator chain element forms already established in foundation ASN-0093 (SC-NEQ, cross-document position-5 disagreement). Fix is internal exposition — either restate as explicit precondition or expand the chain-element form citation.

## Issue 3: Worked example admissibility section omits S2 verification
Reason: S2 is a foundation invariant from ASN-0036; verification is immediate by inspection of the displayed post-state map. Pure exposition fix, no external consultation needed.

## Issue 4: Identity case derivation compresses RA-frame's role
Reason: Pure proof exposition fix — stating the two-step composition explicitly using premises already present in the ASN (RA-π, RA-dom, RA-frame). No design intent or implementation evidence required.
