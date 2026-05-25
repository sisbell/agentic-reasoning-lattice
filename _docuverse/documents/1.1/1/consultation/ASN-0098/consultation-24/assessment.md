# Channel Assignment — ASN-0051 review-24

**Date:** 2026-05-15 20:59

## Issue 1: SV6 proof typo — "first four fields"
Reason: Pure internal typo. The proof itself establishes agreement on positions 1..k−1 ⊇ 1..p₃, which by the field decomposition gives the first three fields (N, U, D); the conclusion is fully self-contained in the existing proof structure.

## Issue 2: SV7 name understates the claim's scope
Reason: Naming/structural choice fully derivable from the ASN's own content. The formal statement, the proof's stated dependency on L-frame, and the explicit "same equality holds for every elementary transition that holds L in frame" remark already delimit the claim's scope; the fix is editorial.

## Issue 3: Bilateral vitality silently scoped to standard triples
Reason: The reviewer's primary recommendation — adding a scoping sentence to the standard-triple framework — is fully derivable from ASN-0043's L3 and ASN-0047's standard-triple convention, both already cited in this ASN. No design intent or implementation evidence is needed for the scoping fix.
