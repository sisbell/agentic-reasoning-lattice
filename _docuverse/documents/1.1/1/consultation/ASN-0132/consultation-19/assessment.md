# Channel Assignment — ASN-0132 review-19

**Date:** 2026-06-13 11:31

## Issue 1: CN-MONO derives the ordinary-link increment in full but discharges the retraction-link increment by citation — and the two cases differ in a load-bearing way
Reason: Internal. The missing step is a pure consequence of material already in the ASN — the CN-MONO precondition ("no currently-counted link becomes nullified") fixes `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)`, and FL-WP(b) (ASN-0121) supplies `b`'s own contribution. The collateral-nullification mechanism it must address is just `L_R^{Σ'} = L_R^Σ ∪ {(b,F',G')}` (ASN-0086), already cited; no design intent or implementation evidence is in question.

## Issue 2: The worked example exercises only single-state (static) claims; CN-MONO's increment and CN-STAB's invariance are never verified against a transition
Reason: Internal. The transition examples are built by applying already-derived claims (CN-MONO, CN-STAB) to a concrete before/after using elementary steps whose effects are fixed by cited ASNs — `K.λ` link creation and freshness (ASN-0086, ASN-0093), `K.μ⁻` content deletion preserving `Σ.L` (F-PRES, ASN-0127). The example is a spec-level demonstration of the abstract operation, not a probe of the implementation.

## Issue 3 (anti-bloat): CN-MONO contains a roadmap paragraph that pre-announces and partially duplicates the derivation that immediately follows it
Reason: Internal. This is purely editorial — removing a within-document forward signpost and folding the roadmap into the derivation, plus trimming two thin implementation notes (note 1's Gregory dedup observation is explicitly retained, so no new evidence is added). No external channel bears on it.
