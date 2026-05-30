# Channel Assignment — ASN-0042 review-111

**Date:** 2026-05-30 04:10

## Issue 1: O5 (a necessary condition) used as a sufficient authorization grant
Reason: The fix reconstructs an authorization chain entirely from properties already in the ASN (O16 supplies an allocator, O5 makes it a most-specific cover, the non-coverage analysis + O1b pin it to `π`) — the worked example already performs this exact derivation, so no design intent or implementation evidence is needed.

## Issue 2: Forward-reference / defensive meta-prose around NestingByDelegation
Reason: Pure deletion of a defensive sentence that advances no reasoning; the `covers_Σ*` conjunct and Step 4 already stand on their own. Internal.

## Issue 3: Axiom-role annotations explain "why needed" rather than what the conditions say
Reason: Editorial relocation of rationale prose — fold role-names inline or move consequence sentences into the consuming proofs (O7/O8). The content is all already present in the ASN; no channel needed.

## Issue 4: Back-reference deferral inside a Formal Contract slot
Reason: The condition being deferred to (next-reachable single-step stream extensions, satisfiable when O15 (ii),(iv),(v) hold at the prospective state) is already stated in the proof of O7(c); the fix just inlines it into the contract slot. Internal.
