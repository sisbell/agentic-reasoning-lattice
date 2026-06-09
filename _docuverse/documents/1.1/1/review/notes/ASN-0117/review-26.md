# Review of ASN-0117

## REVISE

### Issue 1: Per-state invariant accounting omits S8★ (and other extended-state invariants the contraction touches)
**ASN-0117, §"The document remains one coherent sequence"**: "it is exactly ASN-0082's post-contraction preservation family — D-SEQ-post/D-MIN-post/.../S2-post.../S8-fin-post.../S3-post..."
**Problem**: The note grounds DELETE in the ASN-0047 K.μ⁻ + K.μ⁺ vocabulary and then *manually* enumerates the arrangement-shape invariants it preserves, drawn from ASN-0082's family. But ASN-0082's family predates and does not include S8★ (PerSubspaceSpanDecomposition), which is a per-state invariant required by ExtendedReachableStateInvariants (ASN-0047). The content-subspace contraction *materially re-cuts* the V→I correspondence runs: after deletion the survivors' I-addresses (a₁…a_{J−1}, a_{J+c}…a_N) need not advance in lockstep across the closed gap, so the maximal-run decomposition changes. The note establishes D-SEQ-post (V-position density) but never addresses run-decomposition (S8★). Likewise S3★-aux, CL-OWN, CL-UNIQ are silently relied on but not named. The note's own move to upgrade S3→S3★ (per-subspace) puts it squarely in the extended-state regime where S8★ is mandatory, so the selective enumeration is internally inconsistent.
**Required**: Either cite ExtendedReachableStateInvariants (ASN-0047) once to cover *all* per-state invariants uniformly — DELETE being a valid composite of elementary K.μ⁻/K.μ⁺ steps — or add an explicit clause establishing S8★ (and noting the trivial preservation of S3★-aux, CL-OWN, CL-UNIQ) for the post-state. Don't enumerate part of the family and leave the run-decomposition conjunct unaddressed.

### Issue 2: Rationale-of-importance prose and repeated restatement of the non-destruction message (anti-bloat)
**ASN-0117, §"What is removed, and what must survive"**: "Why must this hold for *any* implementation? Because everything Nelson builds on top of editing... Append-only is not a performance choice; it is the foundation of every downstream guarantee."
**Problem**: This paragraph justifies *why P0 matters* rather than stating what the operation does; it is rationale-of-importance meta-prose. The non-destruction message ("the bytes endure; only placement is withdrawn") is then restated, in different words, across at least five sections — intro, §"What is removed" (prose + P0), §"What shifts" ("the exact-gap-closure happens only in the Vstream"), §"Invariants" (P0 again), and §"What we have established." This is the "two paragraphs say the same thing in different words" pattern compounded across the document.
**Required**: Keep the Gregory structural evidence (two deletion primitives — object-level) and one statement of P0's load-bearing role; consolidate the recurring motif so the same fact is asserted once where it is proved, not re-narrated per section.

## OUT_OF_SCOPE

### Topic 1: Deletion at depth m > 2
**Why out of scope**: DELETE inherits ASN-0082's contraction, which is itself proved only at #p = 2; the depth-2 restriction is correctly and honestly scoped here, and lifting it belongs with a generalized foundation contraction, not this note.

VERDICT: REVISE
