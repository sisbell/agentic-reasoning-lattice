# Channel Assignment — ASN-0111 review-35

**Date:** 2026-06-10 21:57

## Issue 1: Definedness contract stated two incompatible ways
Reason: Choosing between a partial function and a total operation with an explicit failure outcome is a signature decision the ASN cannot settle internally — it depends on what the operation was meant to be and on how the implementation actually behaves when handed an unallocated link address. Both channels bear on the choice.
Nelson question: Was the direct read of a link by its address intended as a precondition-gated operation the caller must only invoke on existing links, or as a total request whose contract includes reporting that no link lives at the given address?
Gregory question: When the udanax-green back end receives a request to retrieve a link's endsets for an address with no allocated link, does it return a distinguished error/failure response to the front end, or does it treat the request as a protocol violation outside the operation's contract?

## Issue 2: RL6 has no formal statement; the no-flattening commitment is not checkable as written
Reason: The required formal statement (`readlink` is a function of `(a, Σ.L(a))` alone) follows immediately from the ASN's own definition `readlink(a, Σ) ≡ Σ.L(a)`; the review even supplies the formulation. No external evidence or intent is needed.

## Issue 3: Structural-screen prose duplicated, with inconsistent condition lists
Reason: This is an internal consolidation fix — the correct three-condition list (`zeros(a) = 3 ∧ subspace_I(a) = s_L ∧ #E(a) ≥ 2`) is already stated in the ASN's citation of L0/L1/L1b, and the required edit is deduplication within the note.

## Issue 4: Worked example's subtree-containment step cites the wrong T1 case
Reason: The fix is a proof-citation correction fully derivable from material the ASN already invokes (T1's cases and PrefixSpanCoverage from ASN-0043); the review lays out both the error and two valid repairs. No design intent or implementation evidence is involved.

## Issue 5: Claim labels skip RL3 and RL4 without explanation
Reason: This is a numbering hygiene fix internal to the spec corpus — whether RL3/RL4 are referenced elsewhere is checkable against the repository's own documents, and neither design intent nor implementation behavior bears on label continuity.
