# Review of ASN-0071

## REVISE

### Issue 1: F-CONTENT proof routes through irrelevant premises

**ASN-0071, "The operation" / *Only content sharing can satisfy the predicate***: "By S3★ ∧ S3★-aux ... `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)`. The link-subspace portion can never contribute a match. ... the target side is its dual: the link-subspace images lie in `dom(Σ.L)`, which is disjoint from `dom(Σ.C)` (ASN-0047 L14)."

**Problem**: The stated conclusion is `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.C)`. Since *Resolution* already establishes `iaddrs(Q)(Σ) ⊆ dom(Σ.C)`, the conclusion is immediate: `ran(Σ.M(d)) ∩ iaddrs(Q) ⊆ iaddrs(Q) ⊆ dom(C)` (`A ∩ B ⊆ B`). The entire detour — characterising `ran(Σ.M(d))` via S3★-aux, splitting off the link-subspace portion, invoking L14, and the "dual" framing — proves a fact about the *target range* that the intersection makes irrelevant. The claims-table basis for F-CONTENT compounds this by listing "S3★ ∧ S3★-aux ∧ L14 ∧ the `iaddrs ⊆ dom(C)` subset claim" when only the last conjunct is load-bearing.

**Required**: Reduce the paragraph and the F-CONTENT basis to the one-line derivation from `iaddrs(Q) ⊆ dom(C)`. Drop the S3★-aux / L14 / dual-side machinery.

### Issue 2: Foundation-comparison and reuse meta-prose

**ASN-0071, "The query" and "Resolution"**: (a) "A vspec relaxes ASN-0058's `ContentReference` ... by dropping ... clause i ... the `= m_C` half of clause iii ... the full-coverage well-formedness requirement. Search must tolerate all three, since a query is posed against a source whose arrangement the requester does not control." (b) "`iaddrs_one` is the set-valued, deduplicating, coverage-tolerant counterpart of ASN-0058's `resolve` ... Where `resolve` presumes the well-formed `ContentReference` ... and yields an *ordered* sequence ... `iaddrs_one` discards V-order and run structure, deduplicates, and quietly omits ...". (c) "*Subspace confinement.* ... We reuse that result rather than re-derive it."

**Problem**: The vspec preconditions and the `iaddrs_one` definition are both stated directly and stand alone. The clause-by-clause inventory of what is dropped relative to the foundation, the justificatory "Search must tolerate all three," and the run-structure contrast with `resolve` do not advance either definition — they are exactly the over-detailed foundation comparisons trimmed in commit 0f5eaea3b, recurring. Item (c)'s "We reuse that result rather than re-derive it" is reuse-commentary; the result should simply be cited.

**Required**: Drop the relaxation inventory and its justification clause; keep the vspec preconditions. Drop the `resolve` contrast; keep the one-line statement of what `iaddrs_one` denotes. Replace "We reuse that result rather than re-derive it" with a bare citation to PC's position-1 instance.

### Issue 3: Example intros narrate the document's own coverage

**ASN-0071, "A multi-source query — cross-source deduplication"**: "Every query so far has been a singleton vspec-set, so `iaddrs`'s defining feature — the union *over several vspecs* ... — has not yet been traced."

**Problem**: This is meta-narration about what the note has and has not yet demonstrated, not reasoning. The example itself establishes cross-source dedup; the preamble about prior examples' coverage is noise the reader steps over.

**Required**: Open the example with its construction (`Q_G = {(d_A, σ_A), (d_B, σ_B)}` resolving the shared `a₁`), not with commentary on what earlier examples omitted.

## OUT_OF_SCOPE

### Topic 1: Relationship between current result and provenance relation R

The note's first Open Question (how `find`'s current-state result relates to permanent `R`) is correctly left to a future ASN; *Currency* already states `find` does not consult `R`, which suffices here.

### Topic 2: Rejecting vs. silently filtering unresolvable positions

The second Open Question (when the system must reject rather than filter via F-FILT) is a policy question for a future operation-error ASN, not a gap in this query specification.

The rigor is sound: PC's componentwise/totality/closure argument is complete, PC-RANGE covers `#v <, =, > #u` exhaustively, F-DEEP splits the empty-source and deep-anchor cases, and the worked scenario discharges single/multi-address, multi-source, cross-depth, and deep-anchor cases against concrete states. The findings are anti-bloat, not correctness.

VERDICT: REVISE
