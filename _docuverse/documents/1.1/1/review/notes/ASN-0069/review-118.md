# Review of ASN-0069

## REVISE

### Issue 1: V11a relies on `≼`-transitivity, which the foundation does not publish — yet it is derivable inline from the published Prefix definition
**ASN-0069, §"Composability" V11a and §"Open Questions" (Foundation gap)**: "The prefix relation `≼` is transitive — a generic property of the foundation Prefix relation (ASN-0034), which we cite here rather than re-prove (see foundation-gap note below)." and "V11a's prefix-chain derivation requires transitivity of the foundation prefix relation `≼`, but ASN-0034's Prefix contract exposes only the definition and the derived `p ≺ q ⟹ #p < #q` postcondition — transitivity is not a published postcondition."

**Problem**: V11a's entire prefix-chain conclusion (`d_src ≼ d¹_new ≼ … ≼ d^k_new`, and the length/recovery argument that depends on `dⁱ_new ≼ d^k_new`) rests on transitivity of `≼`. The ASN cites this as a foundation property and parks the gap in Open Questions. But the citation is to a postcondition ASN-0034 does **not** establish — so V11a's proof has an undischarged step. Crucially, the property is *not* a genuine foundation gap: ASN-0034's published Prefix **definition** (`p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`) yields transitivity in two lines (`#p ≤ #q ≤ #r` gives `#p ≤ #r`; for `1 ≤ i ≤ #p`, `pᵢ = qᵢ = rᵢ` since `i ≤ #p ≤ #q ≤ #r`). The ASN cannot cite a property the foundation contract does not contain, and labeling a "derivation" whose load-bearing step is uncited is exactly a claim-without-proof. The gap is also discussed in two places (V11a body deferring "see foundation-gap note below," and the Open Questions restatement), the duplicate-deferral pattern.

**Required**: Derive `≼`-transitivity inline in V11a from ASN-0034's published Prefix definition (three lines), then proceed. Remove the "Foundation gap" entry from Open Questions — it is a fixable proof omission, not a future-ASN topic — and delete the "see foundation-gap note below" forward pointer. If the author prefers an upstream lemma, that is a request on ASN-0034, but it must not leave V11a's proof depending on a non-existent foundation postcondition in the interim.

## OUT_OF_SCOPE

### Topic 1: Transitive identity along *edited* or *subsequent-fork* chains
**Why out of scope**: V11 deliberately restricts to first-fork, per-step-unedited chains and explicitly excludes the edited-intermediate case (last Open Question). Correspondence under intervening edits and under subsequent-fork chains is new territory for a future ASN, not a defect here.

### Topic 2: Concurrency, descendant discoverability, snapshot-vs-living forks, transcludent sources
**Why out of scope**: The Open Questions enumerate these as guarantees beyond the sequential atomic model; they are genuinely future work and correctly not claimed.

META: not needed — the ASN defines the fork as an abstract state transition with implementation-independent invariants, squarely within spec territory.

VERDICT: REVISE
