# Channel Assignment — ASN-0115 review-3

**Date:** 2026-06-05 05:59

## Issue 1: Subspace-confinement step omits T5 and misstates the interval
Reason: Fully internal — T5 (ContiguousSubtrees) is already part of the cited substrate (ASN-0034); the fix is to invoke it explicitly for the endpoint-to-interior step and to restate the bound as `t ∈ ⟦σ⟧`. No design intent or implementation evidence is at issue.

## Issue 2: `#s ≥ 2` rests on S8a, which constrains only bound positions; "V-position of d" is undefined
Reason: Internal — the V-position well-formedness shape (`zeros(s) = 0`, `#s ≥ 2`, positive components) comes from the already-cited ASN-0036 substrate, so the author can define "V-position of `d`" by shape and derive `#s ≥ 2` directly, or require the start to be active; either resolution uses only definitions present in the ASN.

## Issue 3: R7's WLOG assumes comparability the theorem statement does not guarantee
Reason: Internal — the fix is to scope R7's hypothesis to states reachable from a common initial state along the sequential transition order (ASN-0047, already cited), which discharges the WLOG by the axiom rather than assuming it. No external channel is needed.
