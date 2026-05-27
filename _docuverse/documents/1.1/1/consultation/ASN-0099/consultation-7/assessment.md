# Channel Assignment — ASN-0099 review-7

**Date:** 2026-05-26 18:19

## Issue 1: F2/F3 conflation in worked example
Reason: Pure editorial fix. F2 and F3 are defined distinctly within this ASN; the conflation is just sloppy parenthetical phrasing. The fix is derivable from the ASN's own definitions.

## Issue 2: A1 introduced as "convention" but used as load-bearing axiom
Reason: This is a structural decision about how this ASN handles its own meta-axiom — choosing between (a) stating A1 as an axiom, (b) deferring to an ASN-0047 revision, or (c) marking F9's case conditional. All three options are internal editorial/structural choices about the spec's own framing; no design-intent or implementation evidence is needed to make the choice.

## Issue 3: Determinism and survivability for filtered/scoped forms not stated as explicit claims
Reason: The derivations are already sketched in prose and follow mechanically from F8/F9 plus the filtered/scoped definitions. Naming the claims and writing the one-line derivations is internal formalization work.

## Issue 4: Set-level monotonicity across reachable sequences not stated as a claim
Reason: The monotonicity claim follows in one line from F11 (which is already stated and derived). Lifting the buried prose to a named claim is internal editorial work.

## Issue 5: Implementation section drifts toward implementation specifics
Reason: This is a scope/style decision about what belongs in the abstract spec versus implementation notes. The author can decide to remove, relocate, or retain the content based on the spec's own framing principles. No external input needed.

## Issue 6: Image function not given a named property claim
Reason: Image-additivity follows directly from set theory (image of union under a partial function is union of images, with `R ∩ dom(Σ.M(d))` distributing over union). The V-side additivity for `findlinks_V` then composes with F13. Internal formalization.
