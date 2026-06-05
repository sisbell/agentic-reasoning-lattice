# Channel Assignment — ASN-0115 review-1

**Date:** 2026-06-04 23:36

## Issue 1: `act` and `deliver` are undefined when the named document is unallocated
Reason: The fix is internal — the ASN already cites the substrate pattern (`project`, ASN-0098, "defined when `d ∈ dom(Σ.M)`") and R6 already gestures at the open-document precondition. Adding `d ∈ dom(Σ.M)` as a V-spec/R0 precondition and distinguishing it from R6's unbound-position case is derivable from the ASN's own definitions.

## Issue 2: R9 claims inline origin-traceability that R1 and the Open Questions contradict
Reason: The fix is internal — R1 (`item` carries the value, not `a`) and the first Open Question already fix that inline provenance is undecided. Restating R9 as a property of the *resolution* (each active position has determinate `origin(Σ.M(d)(v))`) rather than of the delivered stream reconciles it with R1 and preserves the Open Question, all from the ASN's own content.

## Issue 3: R10's lead-in asserts single-span subspace straddling that the claim and Open Questions defer
Reason: The fix is internal — the reviewer's own tumbler-math argument (an ordinal text-rooted span has `s⊕ℓ` agreeing with `s` on position 1 = `s_C`, so every `t < s⊕ℓ` excludes `s_L`) follows from the ASN's level-uniform/ordinal span definitions (ASN-0053, S6). Confining the lead-in to the mixed-specs case R10 actually proves needs no external evidence.

## Issue 4: R8(ii) "by reference" collides with R1's value-vs-reference item kinds
Reason: The fix is internal — purely a terminological collision with R1's `item` payload kinds (`⟨content, Σ.C(a)⟩` vs `⟨ref, a⟩`). Rewording R8(ii) to say the two items are *resolved through* the one shared address (identity-preserving co-resolution), reserving "reference" for the link payload, is derivable from the ASN's own definitions.
