# Review of ASN-0111

## REVISE

### Issue 1: RL-HOME paragraph justifies the claim instead of stating its content
**ASN-0111, "Ownership lives in the read key" (RL-HOME)**: "Nelson's ownership model depends on this recoverability being a guarantee rather than an accident — so we state it as a claim, even though the home is not part of what readlink returns."
**Problem**: This is the anti-bloat pattern "new prose around an axiom explains why the axiom is needed rather than what it says." The sentence argues *why* RL-HOME is included and concedes it falls outside what the operation returns, rather than advancing the guarantee. RL-HOME is a property of the address/key (L2), not of the value `readlink` produces; the surrounding motivation does not change that.
**Required**: State the reader-facing guarantee directly — `home(a)` is recoverable from the key `a` the reader already holds, by T4 projection (L2) — and drop the Nelson-motivation / "even though the home is not part of what readlink returns" framing.

### Issue 2: Determinacy section closes with design-commitment essay that does not advance the claim
**ASN-0111, "Determinacy and the immutability of the recorded relationship"**: "This is the counterpart, at the read interface, of the design commitment that to record a different relationship one must make a different link: there is no operation that re-types or re-aims an existing link in place, so the structure the read returns today is the structure it will return forever."
**Problem**: RL7's support is already complete and explicit (L12 immutability lifted by LP13). This trailing paragraph is rationale/essay in a structural slot — it restates "the value never changes" as a design philosophy without contributing to the determinacy derivation.
**Required**: Remove the design-commitment paragraph; the LP13/L12 derivation already establishes RL7.

### Issue 3: RL-REP duplicates RL5's equal-coverage claim
**ASN-0111, RL-REP**: "Two recorded endsets with equal coverage record the same relationship and are interchangeable for every coverage-based use (the type relation of L8; projection independence, LP21 of ASN-0098)." vs. **RL5**: "Two links share a type exactly when their type endsets have equal coverage (L8, ASN-0043)."
**Problem**: Two paragraphs in different sections assert the same equal-coverage-means-same-relationship fact, both leaning on L8. RL-REP is the general form of RL5's type-specific instance; the L8 citation is repeated. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: Consolidate — either fold the type instance into RL-REP (cite L8 once there) and have RL5 reference it, or scope RL5 strictly to type-by-address and RL-REP strictly to decomposition-independence without re-deriving the L8 type relation.

### Issue 4: RL-GEN adds no read-specific guarantee beyond RL1 + L4
**ASN-0111, RL-GEN**: "The spans the read returns may point anywhere: across documents, within the link's own home document, or into the link subspace at other links (L4, ASN-0043). The read imposes no confinement on coverage beyond well-formedness; whatever the link recorded, the read returns."
**Problem**: "Whatever the link recorded, the read returns" is exactly RL1 (completeness). Where spans may point is an input-side fact about endsets (L4), not a guarantee the read interface adds. Stated as a read invariant it is RL1 re-expressed plus a verbatim L4 restatement.
**Required**: Either drop RL-GEN (subsumed by RL1) or restate it as a one-line corollary — "by RL1 the read returns the L4-general spans unmodified" — rather than as an independent invariant.

## OUT_OF_SCOPE

### Topic 1: Reader-facing validity/continued-discoverability conclusions
The first Open Question (what a reader may conclude about a relationship's continued validity from a read alone) is correctly posed as future work — it depends on arrangement/discoverability semantics owned by FOLLOWLINK. Listing it as an open question is appropriate; no claim is made here.

VERDICT: REVISE
