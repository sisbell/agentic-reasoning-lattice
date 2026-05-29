# Channel Assignment — ASN-0036 review-123

**Date:** 2026-05-28 22:03

## Issue 1: "Why the axiom is needed" scaffolding around the S7 sub-axioms
Reason: Purely editorial restructuring — the fix restates S7a/S7c/S7d as design requirements in dependency order and deletes the meta-narrative connective prose. The axiom content and dependencies are already present in the ASN; no design-intent or implementation evidence is needed.

## Issue 2: Defensive "non-canonicality" paragraph in the S8 proof
Reason: The fix is to delete the paragraph (or fold a one-clause non-minimality note into the Existence step). The minimality question is already owned by an existing Open Question in the ASN; nothing external is required.

## Issue 3: S8-depth axiom justified by implementation mechanics
Reason: The fix deletes the two-blade-knife sentence, leaving the already-cited Gregory `s.x` address-form evidence to ground the design requirement. Removal is internal; the supporting evidence is already present in the ASN, so no new consultation is needed.

## Issue 4: Trailing standalone remark after the S8 section
Reason: The fix removes the orphaned sentence; the S1-monotonicity half is already stated and proved within S1, and the run-count half is explicitly deferred to a future ASN. Entirely internal disposition.

## Issue 5: S8a's `zeros(v) = 0` labeled "derived" when it is a definitional unfolding
Reason: The fix corrects the proof's own definitional-vs-derived bookkeeping — `zeros(v) = 0` follows by unfolding the posited "isolated element field" commitment, while only positivity is genuinely derived. This is internal logical hygiene derivable from the ASN's own definitions.
