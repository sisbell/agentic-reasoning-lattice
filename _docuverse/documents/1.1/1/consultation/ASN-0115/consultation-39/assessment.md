# Channel Assignment — ASN-0115 review-39

**Date:** 2026-06-10 02:02

## Issue 1: Behavior on a depth-incompatible V-spec is unspecified
Reason: Internal — the choice (reject vs. empty active set) and its justification are derivable from the ASN's own settled stance on stale references. R6 (silent filtering, "never fail the whole," already citing Nelson 4/60) and R11 (stale-but-referenced content stays deliverable) dictate admitting the spec rather than rejecting the request; R2 (faithful resolution) forbids over-capturing the subtree on a shallow start, forcing empty rather than over-broad. The depth-stale citation is the same flavour of stale reference R6/R11 already govern, so treating its active set as empty reconciles with R6 from material already present.

## Issue 2: Open Question 3 is vacuous under the standing S3★ invariant
Reason: Internal — the ASN's standing reachability precondition and imported S3★ (ASN-0047) already guarantee that every resolved reference `Σ.M(d)(v)` is bound in exactly one store, so the posited "no entity in either store" scenario cannot arise from this operation. Removing or reframing the question as a model-extension ("were S3★ relaxed…") follows directly from content already in the ASN.

## Issue 3: Roadmap / preview meta-prose (anti-bloat)
Reason: Internal — this is a pure prose-deletion task targeting navigational/meta sentences flagged by the note's anti-bloat classifier; no design intent or implementation evidence bears on which scaffolding sentences to cut.
