# Review of ASN-0042

I checked the proofs in O1–O18 and the worked example. The mathematical content is sound: the longest-match construction (O2), the refinement/irrevocability arguments (O3/O8), the node-locality case split (O9), and the fork construction's Form A/Form B non-coverage analysis (O10) all hold, including the boundary cases (hwm_0 = 0 field-opening vs. sibling-advance, zeros(pfx(π)) ∈ {0,1}). The depth is genuine and the foundation citations (ASN-0034, ASN-0040) are used, not redeveloped.

The findings below are accretion/meta-prose, consistent with the `review-mode.anti-bloat` classifier — prose that restates conclusions or inventories claim provenance without advancing the argument.

## REVISE

### Issue 1: Verbatim duplicate conclusion across two sections
**ASN-0042, O1a and *Shared invariant induction***: O1a states "Its conclusion: every principal in every reachable state satisfies all three, so `ω` (O2) yields a unique principal at a valid hierarchy level with `fields(·)` well-defined (T4b UniqueParse)." The closing of *Shared invariant induction* states "Hence every principal in every reachable state satisfies all three invariants. Together they ensure `ω` (O2) yields a unique principal at a valid hierarchy level with `fields(·)` well-defined (T4b UniqueParse)."
**Problem**: Two paragraphs in different sections assert the same conclusion in near-identical words. The reader meets the proof's payload twice. This is the "two paragraphs say the same thing" accretion pattern.
**Required**: Keep the conclusion at its proof site (*Shared invariant induction*). In O1a/O1b, point to it without restating the conclusion sentence.

### Issue 2: Use-site inventory attached to the O17b axiom
**ASN-0042, O17b**: "O17b is the sole carrier of this form; delegation condition (v) gives only validity and freshness of `pfx(π')`."
**Problem**: This sentence explains *which claim is responsible for* a fact rather than stating what the axiom says — a claim-provenance inventory bolted onto an axiom. It does not advance the coupling statement; a reader following the next-reachable form must skip past it.
**Required**: Delete the sentence. The preceding clause already derives `pfx(π') = next(Σ.B, p, d)`; the division of labor between O17b and condition (v) is evident at the use sites.

### Issue 3: Freshness-(v) defined by its downstream consumers
**ASN-0042, Freshness-(v)**: "An alias for the pair `T4(pfx(π')) ∧ pfx(π') ∉ Σ.B` of condition (v), by which downstream proofs cite delegate-prefix validity and freshness."
**Problem**: The "by which downstream proofs cite..." clause is a use-site inventory — it names who consumes the alias rather than completing the alias's meaning. The alias is fully defined by the first clause.
**Required**: Stop the definition at "...of condition (v)." Drop the consumer-naming clause.

### Issue 4: State-relativization restated three times
**ASN-0042, EffectiveOwner definition, O2 Postconditions, and Properties table**: The fact that `ω_Σ` is state-indexed in both argument and value is stated in the EffectiveOwner paragraph ("state-relativizes both the address `a` (input) and the selected principal (output)"), and again in the table entry ("both input and output are state-indexed").
**Problem**: The same observation appears in a structural-definition slot and again in the summary table. One placement carries the meaning; the other is redundant.
**Required**: Retain the explanation at the definition; reduce the table entry to the signature without re-explaining state-indexing.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
**Why out of scope**: O3/O8 specify a refinement-only regime; transfer is correctly deferred to the Open Questions and depends on content-model machinery not in this ASN's state.

VERDICT: REVISE
