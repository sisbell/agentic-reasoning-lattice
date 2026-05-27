# Review of ASN-0101

## REVISE

### Issue 1: D8 omits S4 from invariant preservation

**ASN-0101, D8 Group (ii)**: Lists "S7a, S7b, S7c, S7d, L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, C-fin, NodeLineage" as "Allocation and store invariants."

**Problem**: ASN-0047's `ExtendedReachableStateInvariants` Class (a) lists S4 (OriginBasedIdentity) among the per-state invariants every reachable state must satisfy. D8 claims to cover every foundation invariant but omits S4 from Group (ii) (and from Groups (i) and (iii)). S4 says distinct allocation events produce distinct addresses — preserved trivially since DEL adds no allocation events and `dom(C') = dom(C)` — but the omission breaks D8's claim of complete coverage.

**Required**: Add S4 to Group (ii)'s enumeration with a one-line justification: dom(C) is unchanged by D2, and S4 is a structural predicate over allocation events that are unchanged across DEL.

### Issue 2: D8 Group (iii) mislabels per-state invariants as cross-transition

**ASN-0101, D8**: Group (iii) is titled "Cross-transition invariants" and includes P6, P7, P8.

**Problem**: ASN-0047 classifies P6 ("existential coherence"), P7 ("provenance grounding"), and P8 ("entity hierarchy") as per-state invariants in Class (a) of `ExtendedReachableStateInvariants` — they predicate over a single state, not over the relationship between Σ and Σ'. Putting them under "Cross-transition invariants" is a categorical error that conflates the per-state vs transition distinction the foundation deliberately maintains.

**Required**: Either move P6, P7, P8 into Group (ii) alongside the other per-state allocation/store invariants, or rename Group (iii) to "Transition and per-state invariants discharged by frame" so the title doesn't misrepresent what's in the group.

### Issue 3: Composite-substitute argument elides a precondition obstacle

**ASN-0101, §"The operation"**: "The post-state of DEL on an interior span can in principle be matched by a `K.μ~ ∘ K.μ⁻` composite... The composite is well-formed."

**Problem**: K.μ~ requires `|dom_C(M(d))| ≥ 2` (its formal precondition in ASN-0047). When DEL operates on a content subspace with `n_S = 1` (single-position subspace, full deletion), the K.μ~ step has no admissible permutation and the composite cannot be constructed at all. The atomicity argument is sound, but it doesn't address that the composite is also *unavailable* in some cases — strengthening the case for DEL as a primitive on precondition grounds, not only on observability grounds.

**Required**: Either acknowledge that the composite-substitute is well-formed only when `|dom_S(M(d))| ≥ 2`, or restructure the argument to lean only on atomicity (and note that even when the composite exists, the intermediate state is observable).

## OUT_OF_SCOPE

None. The ASN scopes itself tightly to DEL's specification, frame, and invariant preservation. Cross-references stay within foundation ASNs. The Open Questions section appropriately defers extensions (recovery, idempotence of DEL-then-INSERT, causal ordering across documents).

VERDICT: REVISE
