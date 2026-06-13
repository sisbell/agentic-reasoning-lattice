# Channel Assignment — ASN-0132 review-22

**Date:** 2026-06-13 12:25

## Issue 1: CN-MONO carries proof-narration that explains its own hypothesis rather than executing the derivation
Reason: Purely editorial tightening — both wp cases are kept and the math is correct; the fix deletes redundant forward/backward narration and consolidates it into one sentence the reviewer already drafts. No design intent or implementation evidence is at stake; the vacuous-vs-load-bearing distinction is already established by the surrounding `L_R^{Σ'} = L_R^Σ` vs. `L_R^{Σ'} ⊋ L_R^Σ` math present in the ASN.

## Issue 2: CN-OBT restates CN-DEF plus a delivery-scope disclaimer, promoted to theorem status
Reason: Both repair paths are internal. The demotion path is editorial; the strengthening path draws only on material already in the ASN — the obtainable-in-principle vs. on-demand distinction grounded in permanence (ASN-0093, already cited) — and the existence-vs-retrieval boundary is already settled as out-of-scope by the Scope section, so no live Nelson intent question or Gregory implementation evidence is required.
