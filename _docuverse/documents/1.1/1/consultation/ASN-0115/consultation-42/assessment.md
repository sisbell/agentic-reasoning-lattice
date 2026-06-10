# Channel Assignment — ASN-0115 review-42

**Date:** 2026-06-10 03:05

## Issue 1: The `act` override-branch gloss mischaracterizes its own trigger condition
Reason: Internal — the fix is a prose tightening fully supported by machinery already in the ASN: the `depthcompat` definition gives the exact trigger (`V_S(d) ≠ ∅ ∧ #s ≠ m_S(d)`, covering both `#s > m_S(d)` and `#s < m_S(d)`), the well-formedness rule already admits any `#s ≥ 2` against an empty subspace, ASN-0047 re-pinning is already cited, and the Confinement lemma already present shows the too-deep case is a vacuous no-op. No design intent or implementation evidence is needed.

## Issue 2: The V-spec definition pre-explains `act`'s fail-soft semantics via forward reference
Reason: Internal — this is a pure placement fix relocating already-present content; the operative behavior and rationale already live at the `act` definition and R6, and the only fact the reader needs at the V-spec definition (that the depth conjunct is re-evaluated at the consulting state) is itself derivable from the existing definitions. No external channel is required.
