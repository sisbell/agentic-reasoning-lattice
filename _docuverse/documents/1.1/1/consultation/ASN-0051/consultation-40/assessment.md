# Channel Assignment — ASN-0051 review-40

**Date:** 2026-05-16 03:04

## Issue 1: Forward reference — Maximal Endset Fragment uses π_text before SV11 defines it
Reason: Purely structural reorganization within the ASN. The π_text definition already exists in SV11; lifting it earlier requires no design intent or implementation evidence.

## Issue 2: "Full projection" wording contradicts the formal definition
Reason: Wording fix to align prose with the formal predicate already stated in the ASN. Internal.

## Issue 3: Bilateral vitality defined but never used in any SV claim
Reason: The ASN already documents Nelson's "anything left at each end" quote (LM 4/43) and explicitly frames bilateral vitality as the literal Nelson reading versus slotwise as the proof-usable weakening. The decision (add a load-bearing SV claim vs. mark as expository for downstream consumers) is derivable from the existing exposition.

## Issue 4: "Discovery through a document" is informal in SV8 caveat
Reason: The address set `A_Σ(d) = ran(Σ.M(d))` is already formalized in the TransclusionCouplingAbsence corollary. Promoting it to a top-level definition is a reorganization, not new content.

## Issue 5: SV5 worked-example explanation conflates two distinct preservation claims
Reason: The SV5 witness exhibiting the set-change behaviour already exists in the SV5 discussion. The fix is either to substitute that witness into the worked example or add a cross-reference; both options are derivable from the ASN.

## Issue 6: SV13(e) bullet on K.μ~ omits the locate-set transformation formula
Reason: The transformation rule `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}` is already established in SV5. Restating it in SV13(e) is a cross-reference fix.
