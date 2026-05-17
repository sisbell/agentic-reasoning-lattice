# Channel Assignment — ASN-0086 review-6

**Date:** 2026-05-16 17:12

## Issue 1: Nullify scope covers subtree, not single tuple
Reason: The fix requires both design intent (was retraction meant to be tuple-scoped or subtree-scoped) and implementation evidence (does the link allocator actually produce flat or nested link layouts in practice).
Nelson question: Was the link retraction operation in Literary Machines intended to nullify a single link or its entire prefix-subtree, and is link-under-link nesting a designed possibility or an unintended degree of freedom?
Gregory question: In udanax-green, can a link address appear as a strict prefix of another link address (i.e., does the implementation ever spawn a link under an existing link via `inc(linkAddr, 1)`), or is `dom(L)` always flat with respect to prefix-ordering?

## Issue 2: R0 chain-witness vs. substrate-emission gap
Reason: Requires both design intent on whether allocation and deposit are decoupled (a foundational substrate question) and implementation evidence on how the green-side allocator actually couples address creation with value deposit.
Nelson question: In the EnfiladeOSMM design, is address allocation a separate transition from value emission (allowing "spawned but unfilled" addresses), or is each address materialized only when something is deposited there?
Gregory question: In udanax-green, does emitting a link at address `a` require prior or implicit emission at all intermediate L1c-chain addresses, or can the allocator deposit directly at `a` while leaving intermediate positions vacant?

## Issue 3: Emit_K frame condition asserted, not derived
Reason: The frame condition's derivability depends on Issue 2's resolution; the substrate's emission primitive determines whether Σ.C and Σ.M are touched by a link emission, so the same channels apply.
Gregory question: In udanax-green, does the act of allocating a new link address ever cause a write to the content store or to any document arrangement, or is link emission strictly confined to the link store?

## Issue 4: R6b justification conflates with R6a
Reason: The fix is internal — the distinction between logical depth (R6b) and temporal persistence (R6a) is derivable from the existing definitions of `nullified(Σ)` and `L_R^Σ`; only the prose needs reframing with a clearer illustrative example.

## Issue 5: R0 dependency table incomplete
Reason: The fix is internal bookkeeping — the proof text already cites every dependency (T10a.2, T10a.4, T10a.8, TA5, TA5a, S3, Setup), and the table simply needs to be updated to match.

## Issue 6: R7 framing implicitly excludes Observe
Reason: The fix is a one-word edit ("state-transforming") derivable from the ASN's own distinction between Emit_K/Nullify (writers) and Observe (pure read); no external information is needed.

## Issue 7: Setup hypothesis usage not consistently annotated
Reason: The fix is internal — tracing Setup-dependence through R0–R7 is a proof-analysis task derivable from the existing proofs; each claim can be inspected to see whether it invokes the global hypothesis or works under L14's scoped form.

## Issue 8: L14a verification in R0 Step 4 has implicit prior-state reliance
Reason: The fix is internal — making the prior-state inheritance of L14a explicit is a straightforward exposition correction, derivable from the existing structure of preservation lemmas in the ASN.
