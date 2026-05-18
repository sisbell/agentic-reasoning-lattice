# Channel Assignment — ASN-0086 review-51

**Date:** 2026-05-18 04:33

## Issue 1: SharedDepthOneAllocator step (d) carries an unused conditional-independence claim
Reason: Fix is internal — the question is whether downstream proofs consume the conditional-independence claim, which is verifiable by reading the note itself. The naming convention's consumers and the absence of joint-constraint reasoning elsewhere are both observable in the ASN text.

## Issue 2: R0 Step 4's L11b verification is defensive prose for a non-obligation
Reason: Fix is internal — L11b's classification as a permission (vs. invariant) is determined by its statement in ASN-0043, which is already referenced, and the ASN-0086 text already contains an L-permissions paragraph that demonstrates the correct treatment for permissions.

## Issue 3: Implementation hypothesis justification explains why-needed rather than what
Reason: Fix is internal — removing comparative-justification prose is a stylistic decision derivable from the note's own consumer pattern (R0 Step 2 cites the hypothesis directly without needing the T10a comparison).

## Issue 4: Nullify's "Why no content address lies under a" paragraph imagines an excluded case
Reason: Fix is internal — the Definition of `nullified(Σ')` already restricts its carrier to `A_rel^{Σ'}`, making the content-side discharge structurally redundant. The redundancy is visible by comparing the paragraph against the Definition in the same note.
