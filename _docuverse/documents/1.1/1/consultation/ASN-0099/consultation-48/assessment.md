# Channel Assignment — ASN-0099 review-48

**Date:** 2026-06-03 08:44

## Issue 1: F9 and A1a treat K.μ~ as a single-step / atomic operation, contradicting its definition as a non-atomic composite
Reason: The fix is internal — the ASN already carries every needed piece: ASN-0047's "K.μ~ is not atomic" definition is cited in the foundation deps, A1b already supplies the closed-world commitment for K.μ⁻/K.μ⁺, and F9★ already establishes the transitivity-over-atomic-steps pattern. Reclassifying K.μ~ under A1b and composing its (derived) L'=L over the two atomic steps is a formal rerouting derivable from the ASN's own machinery; the conclusion is unchanged and no design-intent or implementation evidence is at stake.
