# Review of ASN-0040

The core development is rigorous: S(p,d) canonical form, S0, B7, B1, B8, B9, B10 all carry genuine multi-step proofs with the boundary cases (empty children m=0, first child, d=1 vs d=2, equal-length vs unequal-length parents, nesting prefixes) actually worked. The trace verifies the key postconditions against concrete addresses. My findings are confined to accreted meta-prose and redundant restatement — the patterns the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: Spurious T10a.6 dependency and provenance editorializing in B7
**ASN-0040, B7 Formal Contract Depends**: "The disjointness conclusion specializes T10a.6 (DomainDisjointness) to baptismal namespaces; the case analysis and the B6(i)/aliasing necessity argument are the ASN-local content."
**Problem**: The B7 proof is fully self-contained — it discharges disjointness through T3, B6, TA5(d), and TA5-SigValid. It never invokes T10a.6. Listing T10a.6 in *Depends* is a dependency the proof does not have, and the trailing clause ("...are the ASN-local content") is provenance commentary that explains what is novel rather than what the claim uses. This is exactly the use-site/meta-prose pattern; it also runs against the prior revision's stated intent to drop T10a cross-references.
**Required**: Remove the T10a.6 citation and the "ASN-local content" sentence from B7's Depends. The Depends slot should list what the proof consumes, nothing more.

### Issue 2: B10 corollary restates the s.B definition
**ASN-0040, B10 Formal Contract**: "*Corollary:* `s.B ⊆ T`, since T4-validity entails t ∈ T."
**Problem**: s.B is *defined* as "s.B ⊆ T — the set of baptized tumblers" (BaptismalRegistry). Re-deriving `s.B ⊆ T` from T4-validity asserts a fact already fixed by the type of the state component. Two statements saying the same thing.
**Required**: Drop the corollary; it adds nothing the definition does not already guarantee.

### Issue 3: Redundant restatement after the B6 depth table
**ASN-0040, B6**: post-table sentence "d = 2 crosses one level; the four-field cap follows from condition (iii)."
**Problem**: The preceding prose already states "Condition (iii) ensures no address exceeds the four-level hierarchy; it is binding only at d = 2," and the table's d=2 column already shows the level crossing and the invalid Element/d=2 cell. The post-table sentence repeats both points without advancing them.
**Required**: Delete the sentence; the table and the prior paragraph fully carry it.

## OUT_OF_SCOPE

### Topic 1: Cross-path / cross-replica collision in the same namespace
B8 is deliberately scoped to *co-reachable* (single-path) acts; two baptisms in one namespace on divergent branches would both emit c_{m+1}. This is correctly identified as the distributed-coordination question and already appears in Open Questions.
**Why out of scope**: Concurrency and cross-replica ordering are new territory, not a defect in the single-path uniqueness B8 actually claims.

VERDICT: REVISE
