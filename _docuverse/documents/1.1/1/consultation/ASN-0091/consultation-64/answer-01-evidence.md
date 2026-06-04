## Question 1 [evidence]

> Does ASN-0047 supply any single-step (per-transition) preservation theorem for the arrangement-dependent invariants S3★, S3★-aux, CL-OWN, CL-UNIQ, S8★, or is ExtendedReachableStateInvariants — keyed to reachability from Σ₀ — the only available handle, and is that reachability relation closed under valid K.μ⁻/K.μ⁺ transitions?

## KB Synthesis

This question is not answerable from the KB.

The KB entries document *implementation findings* about udanax-green — tumbler arithmetic [SS-TUMBLER], enfilade structure [SS-ENFILADE-TREE], content identity semantics [SS-CONTENT-IDENTITY], subspace conventions [SS-SUBSPACE-CONVENTION], and so forth. None of them reference ASN-0047 or the formal specification objects it introduces: S3★, S3★-aux, CL-OWN, CL-UNIQ, S8★, ExtendedReachableStateInvariants, or the K.μ⁻/K.μ⁺ transition notation.

What the KB *can* say, as background context:

- The implementation has no single-step atomicity guarantee for cross-structure transitions — [INV-ATOMICITY] covers operation-level atomicity within the event loop, but [INV-DUAL-ENFILADE-CONSISTENCY] notes the granf/spanf update sequence in CREATELINK has no rollback. Whether ASN-0047 proves closure under such transitions is a question about the spec document, not the code.
- Several KB invariants are arrangement-dependent (e.g., [INV-ENFILADE-RELATIVE-ADDRESSING], [INV-ENFILADE-OCCUPANCY]) and their preservation proofs would need to track tree structure, which the KB describes but does not formalize.

To answer your question properly, ASN-0047 itself must be read directly. The KB is silent on it.

---

## Code Exploration

**ASN-0047 as described does not exist in this repository.**

After exhaustive search across all accessible files — `knowledge-base/kb-formal.md` (8,714 lines), `knowledge-base/analyzed/0047.md`, `findings/0047-docispan-granularity-per-span.md`, all 78 findings, and every file in the harness — none of the following appear anywhere:

- The label **ASN-0047** (as a formal specification document)
- The invariant names **S3★**, **S3★-aux**, **CL-OWN**, **CL-UNIQ**, **S8★**
- The predicate **ExtendedReachableStateInvariants**
- The state symbol **Σ₀**
- The transition notation **K.μ⁻ / K.μ⁺**

What **does** exist with the number 0047:

- `findings/0047-docispan-granularity-per-span.md` — a behavioral finding about per-span vs. per-byte DOCISPAN granularity in `spanf1.c:38-48`
- `knowledge-base/analyzed/0047.md` — the KB distillation of the same, with entries SS-DOCISPAN, ST-INSERT, ST-COPY, INV-SPANF-GROWTH

Neither uses the invariant notation in the question.

The repository's formal invariant system uses prefixes **INV-**, **SS-**, **ST-**, **FC-** (e.g., `INV-IADDR-IMMUTABILITY`, `SS-TUMBLER`, `ST-INSERT`). The notation S3★/CL-OWN/K.μ⁻ belongs to a different formal framework — one not present in any file I have access to.

**I cannot answer this question from the available source material.** If ASN-0047 is an external document (e.g., from the broader Xanadu design archives, a Dafny proof corpus, or a TLA+ specification tree outside this working directory), it is not accessible here. Per the role's own process: I will not speculate about the content of a document I cannot read.
