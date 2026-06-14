# Channel Assignment — ASN-0134 review-8

**Date:** 2026-06-13 20:53

## Issue 1: The §4 enumeration of operation-level non-confluences is incomplete
Reason: Internal. The note already states the full mechanism — M1(b)(ii) establishes that a coverage-equal `idem=⊤` emit is a zero-step hit "only while that incumbent is active" and flips to a miss (resurrection, citing ASN-0128 I1/I2) if the incumbent is nullified between/before, and §4 already commits that the hit/miss verdict reads the *global* `A_K`. The third source is just §4's *concurrency* enumeration failing to count the nullify-of-incumbent race that M1(b)(ii) already describes; that it survives emit-before-retract (B targets the long-emitted T, not A's output) and surface discipline follows from those disciplines' own definitions in the note. The fix is reconciling the enumeration/G1 row with a mechanism the note already states — no design intent or implementation evidence is required.

## Issue 2: H0's proof leaves the cross-document, cross-subspace case to lemmas that do not cover it
Reason: Internal. The repair is derivable from the note's own definition `P_S(d, Σ) = {a ∈ dom_S(Σ) : origin(a) = d}`, H0's already-asserted allocation effect (a deposit into `(d', S')` carries `origin = d'` and subspace `S'`, citing ASN-0093 K.α / ASN-0128 K.λ_sh), and store disjointness `SD`, which the note already carries as a per-state invariant. Any allocation into `(d', S') ≠ (d, S)` differs in `origin` or lands in the disjoint sibling store, hence outside `P_S(d, ·)` — settling all three sub-cases directly without invoking the lemmas H1 itself disclaims. No external channel needed.
