# Channel Assignment — ASN-0091 review-16

**Date:** 2026-05-26 18:35

## Issue 1: K.μ~ frame "matches exactly" claim elides dom(M) preservation
Reason: The fix is derivable from the ASN's own content — the issue is acknowledging that `dom(M') = dom(M)` is implicit in K.μ~'s composite structure (K.μ⁻ + K.μ⁺, neither adding/removing documents) rather than explicit in its frame clauses. No design intent or implementation evidence is needed; the resolution is a textual qualification citing the structural composite argument already understood in the ASN.

## Issue 2: Non-uniqueness of π lacks a worked example
Reason: The fix is derivable from the ASN's own content — all the abstract machinery (pre-image partition characterization, S5/UnrestrictedSharing, RE-proj uniformity) is already developed in the ASN. Constructing a concrete trace with shared I-addresses and exhibiting two distinct valid π witnesses requires only instantiation of existing definitions.

## Issue 3: P4a preservation cites an unstated "append-only" property
Reason: The fix is derivable from cross-reference to ASN-0093's SequentialTransitionAxiom, which is part of the project's own specification corpus. The reviewer has already identified the resolution path (either cite the axiom or derive append-only as a corollary from atomicity + total order); no external design intent or implementation evidence is required.

## Issue 4: Chain-distinctness argument is repeated inline three times
Reason: The fix is purely a presentation refactor — factor the repeated TA5(c) + chain-structural-form argument into a named inline lemma. The fact itself is already derived in the ASN at each use site; no external information is needed to consolidate it.
