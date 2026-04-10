# Revision Categorization — ASN-0081 review-4

**Date:** 2026-04-09 19:34



## Issue 1: D-CS frame condition is one-directional; invariant proofs require biconditional
Category: INTERNAL
Reason: The fix is purely a precision upgrade to the formal statement — strengthening a one-directional implication to a biconditional. The intent (non-S subspaces are unchanged) is already clear from the ASN's own prose and the analogous D-CD/D-DOM patterns.

## Issue 2: Statement registry missing key definitions
Category: INTERNAL
Reason: ThreeRegions, Q₃, and the contraction operation are all defined within the ASN's own text. Adding registry entries is a mechanical extraction task requiring no external evidence.

## Issue 3: D-BJ label/registry mismatch
Category: INTERNAL
Reason: The lemma text, proof, and label all agree on bijectivity; the registry line is simply an incomplete transcription. The fix is aligning the registry string with the already-established content.
