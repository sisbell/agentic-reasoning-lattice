# Review of ASN-0099

I traced through the abstract specification, the proofs of F1–F20, the worked example's 11 queries, and the dependency surface on foundation ASNs (0034, 0036, 0043, 0047, 0058, 0093, 0098).

## REVISE

None.

The ASN's load-bearing claims have explicit derivations: F8 chains from L6 + coverage determinism; F9 splits cleanly into A1a (published `L' = L` frames) and A1b (convention-grounded closed-world reading, explicitly grounded on Nelson and Gregory); F10 rests on F10a's case-split on T1's two cases lifted by PrefixOrderingExtension; F11 chains through LP13 + L6; F19 is a one-line lift of F11; F4's minimality covers both directions with realizability discharged universally via K.λ + L4. Boundary cases are handled comprehensively (empty I-set, empty link store, empty V-region, empty constraint set, empty constraint target, empty scope, documents not in dom(M), V-positions outside dom(M(d)), empty endsets at non-type slots, cross-subspace V-positions via Query 9). The worked example exercises F1, F2, F3, F5, F6, F7, F8, F9, F9★, F9★-cor, F10, F10a, F11, F13, F15, F17, F19, F20 against concrete spans. The two-phase factoring (F12) is correctly labeled as definition rather than derived identity. The F2-V/F3-V conformance pair is carefully articulated under both the factored-through-result and direct-V-side architectural models. A1b's convention-grounded status is transparent and the inheritance is correctly tracked across F9, F9★, F9-cor, F9★-cor, F17 — every downstream citation that depends on it is named.

## OUT_OF_SCOPE

None — the "What We Have Not Specified" and "Open Questions" sections appropriately defer the inverse direction (FOLLOWLINK), addresses outside dom(C) ∪ dom(L), distributed link stores, access control, caching, the combined filtered-scoped operation, and timing bounds to future ASNs.

VERDICT: CONVERGED
