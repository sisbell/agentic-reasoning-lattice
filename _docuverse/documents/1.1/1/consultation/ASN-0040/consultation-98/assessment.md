# Channel Assignment — ASN-0040 review-98

**Date:** 2026-05-29 03:37

## Issue 1: B4 carries a downstream-consumer inventory and "why-needed" prose
Reason: Pure prose-trimming — cut the consumer inventory and interleaving rationale, state the single-edge collapse. The object content is already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: B3 wraps its invariant in forward-reference essay prose
Reason: The invariant `Occupied(t, s) ⟹ t ∈ s.B` and the three-way taxonomy are already stated; the fix only strips the forward-reference framing. Fully internal.

## Issue 3: Worked-example sprawl restates the proofs it illustrates
Reason: Folding the M=5 B9 re-derivation and the equal-length B7 illustration back to a line each is a mechanical deduplication against proofs already in the note. No external channel needed.

## Issue 4: s.B-vs-allocated(s) disambiguation defers to an open question
Reason: Reducing the disambiguation to one sentence and dropping the binary-character restatement is internal editing; the open question already owns the allocated(s) ⊆ s.B linkage, so no design/implementation input is required.
