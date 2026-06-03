# Channel Assignment — ASN-0069 review-66

**Date:** 2026-06-02 22:52

## Issue 1: J4-correspondence inventory after V1 does not advance the identity argument
Reason: The fix is a pure prose collapse — the J4 clause structure and label mapping are already present in the ASN, and the required single-sentence replacement restates content V1 already established. Derivable from the ASN alone.

## Issue 2: V4's "motivation is twofold" is rationale prose in a claim slot
Reason: The fix removes justification prose and keeps V4's formula, both already in the ASN. No design-intent or implementation evidence is needed to decide what to cut.

## Issue 3: "Why I-Address Identity Suffices" is an essay that introduces no state, operation, or invariant
Reason: The section restates already-proved results (V6a/V8/V9/V11) and the disclaimers (counterpart correspondence, semantic equivalence) are already articulated in the ASN's own text and Open Questions. Deletion/folding is internal.

## Issue 4: V8b's non-monotonicity paragraph drifts into operational mechanics it disclaims as out of scope
Reason: The two retained bound claims and their derivations are already in V8b; cutting the surrounding mechanics narrative is a self-contained editorial trim. No channel needed.

## Issue 5: Multiple paragraphs defer the same verification to "The Fork Composite" below
Reason: Consolidating three deferrals into one pointer is a structural edit over material already in the ASN; the verification itself already exists in "The Fork Composite." Derivable internally.

## Issue 6: "design commitment / not derivable from J4" framing is duplicated across V4, V4b, and V4b's forward-pointer
Reason: Deduplicating the non-derivability framing and keeping V4b's domain-equality content with its existing one-line justification is purely editorial. No external evidence required.
