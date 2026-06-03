# Review of ASN-0070

This is a rigorous, well-bounded note. The inverse-image core (F0), the I/O-subspace correspondence (F-subspace), and the large canonical-uniqueness proof (F-canonical) are all carefully argued, with boundary cases (empty resolution, multiplicity, cross-subspace straddle, state-dependence) each exercised against a concrete configuration. The proofs handle the degenerate cases correctly: empty `X` yields zero maximal runs and the unique reconstruction forces `⟨⟩`; the `k < m` action-point case is excluded by an explicit infinitude argument. I found no correctness gap, no missing edge case, and no hand-waved multi-case proof.

One anti-bloat finding remains.

## REVISE

### Issue 1: Speculative concurrency claim in F-frame's slot
**ASN-0070, F-frame (Frame, INV)**: "The operation requires no write-locking and no exclusive access. Concurrent queries are admissible insofar as the underlying arrangement is accessible."
**Problem**: This sentence asserts a concurrency property the note has not established and explicitly defers — the Open Questions section asks "What concurrency semantics must `follow` guarantee when the queried document is being modified by another transition concurrently?". F-frame's actual content is the frame `Σ' = Σ`, already stated verbatim in F1's Frame clause. The added sentence is essay content in a structural slot: it neither follows from the frame (which only says `follow` writes nothing) nor addresses the harder case (concurrent writes to `M(d)`), and its hedge ("insofar as the underlying arrangement is accessible") signals that no guarantee is actually being made.
**Required**: Delete the concurrency sentence. If a concurrency consequence is wanted, it belongs to whatever future ASN resolves the deferred Open Question, not as an unsupported aside on the frame invariant. The component-level frame (`C'=C, M'=M, L'=L, E'=E, R'=R`) is the load-bearing content and may stay.

## OUT_OF_SCOPE

### Topic 1: Cross-home transclusion relationships, concurrency semantics, shared-lineage resolution
**Why out of scope**: The three Open Questions correctly identify these as future territory — they concern multi-document transclusion invariants, concurrent-modification semantics, and version-lineage correspondence, none of which the inverse-image query operation needs to define. They are appropriately deferred, not gaps in this ASN.

VERDICT: REVISE
