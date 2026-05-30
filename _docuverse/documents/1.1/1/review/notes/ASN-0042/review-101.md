# Review of ASN-0042

This ASN is technically sound — the longest-match `ω`/`owns` split correctly resolves the nested-prefix tension, the bootstrap/delegation invariants chain cleanly, and the worked example is internally consistent (I traced the seed table, the `hwm=5` document stream, and the three fork branches). My findings are confined to the accumulated meta-prose the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: Repeated back-reference to "the single allocation point corroborated at O17b"

**ASN-0042, O17b / O18 / DelegatorAllocatesPrefix / O10**:
- O17b (origin): "every registry write in udanax-green funnels through a single allocation point — `findisatoinsertgr`… `findpreviousisagr`… advancing unilaterally past existing (and delegated) slots…"
- O18: "The single allocation point corroborated at O17b never re-purposes a previously baptized tumbler as a new principal's prefix…"
- DelegatorAllocatesPrefix (closing): "The single allocation point corroborated at O17b runs under the session's own account-tumbler authority…"
- O10 (closing): "This is exactly the abstract image of the single allocation point corroborated at O17b, which advances unilaterally past delegated slots."

**Problem**: This is the listed pattern "multiple paragraphs in different sections defer to the same downstream/upstream location." The corroboration is established once at O17b; the three later back-references re-assert the same implementation fact as design-justification and advance no reasoning in their host claims (O18's freshness conjunct, DelegatorAllocatesPrefix's identification, O10's construction are all discharged by the abstract argument, not by re-citing the udanax-green allocation point).

**Required**: Keep the corroboration at O17b only. Delete the three back-references, or reduce each to nothing — none is load-bearing for its host proof.

### Issue 2: Covering-chain comparability re-derived inline where parallel proofs cite the lemma

**ASN-0042, OwnershipDomainPermanence, Steps 2 and 3**: "Both `pfx(π)` and `pfx(π')` are prefixes of `a`. From the definition of the prefix relation… Taking WLOG the shorter… `pfx(π) ≼ pfx(π')`." and Step 3's analogous "Both `pfx(π)` and `pfx(π_d)` are prefixes of `pfx(π')`… gives `pfx(π) ≼ pfx(π_d)`."

**Problem**: The covering-chain lemma (PrefixesOfCommonAddressAreComparable) was introduced precisely to factor out "two prefixes of a common address are `≼`-comparable." O7(a), O10's non-coverage analysis, and DelegatorAllocatesPrefix all cite it for the identical step; OwnershipDomainPermanence instead re-unfolds it from the Prefix definition twice. Same content, different words, in the same document.

**Required**: In Steps 2–3, cite the covering-chain lemma (applied to the common tumbler, with the strict length inequality fixing the direction) rather than re-deriving componentwise.

## OUT_OF_SCOPE

None. The ASN's Scope fence and Open Questions are well-drawn; O10's "requires modification of content" is used only as the trigger for the ownership-side fork response, not a modification-semantics claim, so it stays within ownership.

VERDICT: REVISE
