# Channel Assignment — ASN-0094 review-65

**Date:** 2026-05-24 10:50

## Issue 1: Global empty-link-store strengthening conflates framework requirement with walkthrough convenience
Reason: The technical analysis (preservation theorems require only per-K empty baselines) is internal, but whether to downgrade the global commitment or keep it as a faithful substrate property depends on whether the design treated `Σ_init` as globally empty or only per-K empty.
Nelson question: Did the design intend the substrate's `Σ_init` to have an empty link store globally (across all type indices, including unregistered ones), or only at registered types?

## Issue 2: Sh4 contract clause (i.a) interleaves correctness and tightness derivations awkwardly
Reason: Pure restructuring of clause (i.a)'s prose — the correctness derivation (forward + reverse inclusion via post-filter) and the tightness derivation (under Sh-conf clause (d)) are both already present in the ASN; the fix is to sequence them rather than commingle them.

## Issue 3: The four named layer-discipline commitments lack a consolidated reference
Reason: The four commitments are each fully defined in the ASN; adding a consolidated reference table tabulating their signatures (name, defining section, applicable K's, gate position, discharged theorem, failure mode) is a presentation task derivable from existing content.

## Issue 4: Walkthroughs are exhaustively detailed and impede framework readability
Reason: Restructuring or extracting walkthroughs is a presentation choice resolvable within the ASN; the repeated rejection patterns (e.g., G-side partition mismatch across Classifier/Tuple-Classifier/Retraction walkthroughs) are visible from the ASN's own content, and the cross-referencing fix needs no external input.

## Issue 5: Sh5(b) checklist's "decidable per row" claim conflates per-symbol decidability with end-to-end procedural assurance
Reason: The fix is a framing choice — either commit to a documented verification mechanism (e.g., separate auditor role with explicit acceptance criteria) or acknowledge contingency on author diligence — both options are resolvable within the ASN's own META discipline framing.

## Issue 6: SubstrateConsumerActiveSubsetCompatibility's "exhaustiveness proof" Path (a) cites a hypothetical layer transition vocabulary the framework doesn't model
Reason: Whether to formalize the consuming layer's transition vocabulary parametrically or acknowledge Path (a) as informal depends on whether the design treated the substrate's (C, M, L) triple as the complete state model or contemplated layer-side auxiliary state as part of the overall system.
Nelson question: Did the design treat the substrate's (C, M, L) triple as the complete state model, or did it contemplate layer-maintained state outside the substrate (timestamps, metadata, external accessors) as part of the overall system?
