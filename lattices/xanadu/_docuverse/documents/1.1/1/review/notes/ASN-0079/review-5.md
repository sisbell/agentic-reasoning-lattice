# Review of ASN-0079

## REVISE

### Issue 1: F19 contains implementation mechanics
**ASN-0079, Scale**: "The implementation achieves this through a spanfilade — a 2D enfilade (branching factor 4–6) indexing link endsets by I-address range. Tree traversal to the matching region is O(log n), where n is the number of spanfilade entries. Three independent index traversals (one per endset type) are intersected to produce the final result."
**Problem**: This paragraph specifies a concrete data structure (spanfilade), its branching factor, and a three-way intersection algorithm. These are implementation mechanics, not system guarantees. The preceding paragraph also mixes normative content ("Any conforming implementation must maintain index structures enabling sublinear candidate location") with implementation analysis ("Tree-based indexing achieves Θ(log |dom(Σ.L)|) traversal cost"; "Ω(log |dom(Σ.L)|) is a comparison-based lower bound for key lookup").
**Required**: The normative content of F19 is the sublinearity requirement — o(|dom(Σ.L)|) — and the architectural motivation (without it, F7's universal scope becomes impractical). Remove the spanfilade paragraph entirely. In the preceding paragraph, remove the sentences analyzing tree-based indexing complexity and the comparison-based lower bound. An alternative implementation using hash-based indexing, bloom filters, or other structures must be equally valid under the specification; prescribing tree-based analysis narrows the design space.

### Issue 2: F2 cites implementation code as evidence
**ASN-0079, Overlap Sufficiency**: "The implementation confirms this predicate at the byte level: the udanax-green spanfilade uses exactly `query_start < entry_end ∧ entry_start < query_end`, excluding the adjacent case."
**Problem**: An implementation reference is not specification evidence. The half-open interval intersection formula `s_α < reach(β) ∧ s_β < reach(α)` is derivable from the span algebra (SC classification, ASN-0053) and the definition of span denotation. The implementation happens to confirm it, but the specification should stand on its own foundations.
**Required**: Remove the sentence. The mathematical content is already established: the formula follows from the span denotation definition (⟦σ⟧ = {t : start(σ) ≤ t < reach(σ)}) and the standard characterization of non-empty intersection between half-open intervals.

## OUT_OF_SCOPE

### Topic 1: Index invariants for completeness
**Why out of scope**: F3 guarantees completeness at the specification level (FindLinks is a set comprehension — complete by construction). The question of what index invariants an *implementation* must maintain to guarantee no satisfying link is omitted is an implementation-level concern that belongs in an implementation or enfilade ASN, not in this specification of the query semantics.

### Topic 2: Concurrency and isolation model
**Why out of scope**: F6 is correctly defined for fixed state Σ. The interaction between concurrent link creation and link search — whether pagination provides snapshot isolation, read-committed semantics, or something else — is a systems-level concern acknowledged in the open questions. This is a separate ASN on transaction semantics, not a gap in the query specification.

### Topic 3: Endset projection completeness signal
**Why out of scope**: F14 correctly observes that the projection definition provides no completeness signal. Whether the system *should* signal partial coverage (and in what form) is a design decision that belongs in a future ASN on the display/rendering layer, not in the link discovery specification.

VERDICT: REVISE
