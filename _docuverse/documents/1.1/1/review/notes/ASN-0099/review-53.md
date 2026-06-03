# Review of ASN-0099

I checked the two-phase factoring (F12), the match predicate (F1) and its design justification (F4), the conformance contracts (F2/F3 and variants), the survivability/monotonicity chain (F8–F19), the ordering theorems (F10/F10a), and the worked example.

## REVISE

None. The proofs I spot-checked discharge their obligations explicitly rather than by assertion:

- **F9-λ** correctly splits `findlinks(I, Σ')` by domain and uses the *per-link* primitive (PerLinkInvarianceUnderValuePreservation), explicitly noting that ComprehensionInvariantUnderΣL is unavailable because `dom(Σ'.L) ⊋ dom(Σ.L)`. The disjointness of the union is justified from K.λ freshness.
- **F10a case (ii)** unfolds `d₂_{#d₁+1} ≥ 1` in four named foundation steps (M0, T4, Prefix, T0-discreteness) rather than waving at "the prefix carries over." The zero-count accounting is correct: d₁'s two separators sit at positions ≤ #d₁−1, transport to d₂ by prefix agreement, and exhaust d₂'s budget, forcing the separator-free region beyond #d₁.
- **F4** is honestly framed as *operational distinguishability under F2 ∧ F3*, not mathematical uniqueness, and the five realizability witnesses (3 strengthenings, 2 weakenings) each check *every* slot — including the L3-mandated non-empty slot 3 and the vacuous-coverage trap at empty slots, which Strengthening 1 explicitly addresses.
- Edge cases are covered: empty query, empty link store, empty/contracted arrangement, link-subspace V-positions (Query 4 via S3★ routing), `d ∉ dom(Σ.M)` (undefined, no silent fallback), and the **I-side vs. V-side persistence divergence** is correctly *not* over-claimed — Query 5 demonstrates V-side shrinkage under K.μ⁻ while I-side holds.
- The union-form recovery `findlinks(I,Σ) = ⋃_{i=1}^{N} findlinks_filtered({(i,I)},Σ)` with the per-term `i ≤ |Σ.L(a)|` guard correctly reconstructs the slot existential, and the `dom(Σ.L)=∅ ⇒ N=0` empty-union case is consistent.

All references (ASN-0034, 0036, 0043, 0047, 0093, 0098) are to foundation ASNs and are permitted; no notation is reinvented for what a foundation already defines.

## OUT_OF_SCOPE

The ASN correctly defers INSERT/DELETE/COPY mechanics, replication/partition tolerance, caching, the inverse FOLLOWLINK direction, and out-of-store query semantics to its Open Questions and "What We Have Not Specified" sections rather than defining them. No misplaced claims.

The ASN defines an operation on state with abstract completeness/soundness obligations an alternative implementation must satisfy, and explicitly disclaims implementation mechanics. It has not drifted.

VERDICT: CONVERGED
