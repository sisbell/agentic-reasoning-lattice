# Review of ASN-0099

## REVISE

(none)

## OUT_OF_SCOPE

(none)

VERDICT: CONVERGED

The ASN is thorough and well-structured. Notable strengths:

- The two-phase factoring (V→I via `image`, I→Link via `findlinks`) is cleanly motivated and the conformance contracts (F2/F3 and their filtered/scoped/V-side variants) pin abstract operations to implementation surfaces explicitly.
- F4's minimality argument exhibits three concrete witnesses for enumerated strengthenings and discharges the general case via a reachability argument (every F1-admitted pair is realizable as a conforming state extending some base via K.λ). The "framing of the uniqueness claim" paragraph correctly anchors the claim relative to F2 ∧ F3.
- A1 (LinkStoreInertOfNonAllocatingOperations) honestly surfaces a notational gap in ASN-0047 (frames for K.μ⁺, K.μ⁻, K.ρ omit `L' = L`), explicitly states what L12 + L12a do and do not supply, and grounds the closed-world reading of effect clauses in convergent design intent + implementation evidence. The handling is appropriate for the foundation gap and does not let the lemma slip past unchallenged.
- Boundary cases are systematically addressed: empty I-set, empty link store, empty constraint set, empty constraint target, empty scope, R disjoint from dom(M(d)), d ∉ dom(M).
- The worked example is dense but exercises F1, F2, F3, F4 (implicit), F5, F6, F7, F8, F9, F10 (including the version-extension T1 case ii), F11, F13, F14, F15, F17, F19, F20 against a small concrete configuration with cross-subspace handling (Query 9 via K.μ⁺_L) and multi-step preservation (Query 10).
- The chain index = K.λ event count identification underlying F10's within-document ordering is correctly derived via ChainMembershipForOrigin + ChainEnumerationInjectivity + K.λ's subsequent-emission precondition.
- Foundation citations are all to verified foundation ASNs (0034, 0036, 0043, 0047, 0053, 0058, 0093, 0098); no cross-references to non-foundation ASNs.
- The "What We Have Not Specified" section and "Open Questions" appropriately scope future work without smuggling claims through.
