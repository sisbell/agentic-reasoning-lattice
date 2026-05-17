# Channel Assignment — ASN-0047 review-69

**Date:** 2026-05-17 02:49

## Issue 1: K.δ case (ii) k = 1 with live operand — operational T10a allocator unnamed
Reason: Resolving the naming question requires understanding whether versioning was designed as a sub-allocator parallel to content/link (Nelson) and whether the implementation tracks versions as a separately-managed allocator record or dispatches through general allocator machinery (Gregory).
Nelson question: Did the Xanadu design intend each document to host a distinct "version sub-allocator" analogous to its content and link sub-allocators, or is version allocation simply a tumbler-level inc-extension of the document address with no separate allocator namespace?
Gregory question: Does udanax-green's docreatenewversion (do1.c:271) operate via a separately-tracked version-allocator record (analogous to granf for content and spanf for links), or does it dispatch through the same granfilade machinery as ordinary document allocation under the parent account?

## Issue 2: Worked Example 4 (ghost-base versioning) under-enumerates per-invariant verifications
Reason: This is purely an editorial restructuring task — enumerating each invariant at each step at the level of detail used in Example 2. The verification content is already implicit in the ASN's invariant set and K.δ's frame; no external knowledge is needed.

## Issue 3: K.μ⁻ admissibility precondition — joint role of two clauses obscured
Reason: This is a structural/presentational restructuring of an existing precondition list. The content (per-subspace admissibility plus strict-contraction witness) and its joint necessity are already established in the ASN; the fix is reorganizing how it is presented.
