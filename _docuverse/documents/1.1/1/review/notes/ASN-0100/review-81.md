# Review of ASN-0100

## REVISE

### Issue 1: Fresh-address invariant discharge is scattered across sections, each deferring to §Atomicity
**ASN-0100, §Post-state V-position well-formedness, §Permanence/P6, §Link store unchanged**: the per-address obligations on the freshly allocated `a_k` are repeatedly punted forward:
- "The freshly allocated `a_k ∈ dom(C') ∖ dom(C)` discharge S7a, S7b, C1b, and C1c in §Atomicity."
- "The freshly allocated `a_k ∈ dom(C') ∖ dom(C)` discharge P6 in §Atomicity."
- "The fresh-`a_k` discharge of L0's content clause is the one given in §Link store unchanged."

§Atomicity then performs all of them in one grouped paragraph ("S7a … S7b … C1b … C1c … P6 … L0's content clause").
**Problem**: This is the "multiple paragraphs in different sections defer to the same downstream location" pattern. The reader meets each invariant twice — once as a forward pointer, once as the actual argument — and must hold the deferrals in mind until §Atomicity. The fresh-`a_k` discharge is a single coherent argument (each holds at the K.α commit, persists by P0/L12) fragmented across four sites.
**Required**: Discharge the fresh-`a_k` per-address invariants once (the §Atomicity grouped paragraph already does this) and delete the forward-pointer sentences from §Post-state, §Permanence/P6, and §Link store.

### Issue 2: §Position Constraints restates region-emptiness already established three times over
**ASN-0100, §Position Constraints**: "What remains to be shown here is that each admissible position yields a well-typed composite — and the determining factor is which of the three post-state regions are empty," followed by the `j=0` / `j=N` / interior / empty bullet enumeration.
**Problem**: The region-emptiness case split is already given in (INS.μ⁻-fires) (the append and empty cases having `Right = ∅`), in §Effect Three, and demonstrated concretely in §A Worked Example (append case, empty-document first insertion). The section's only non-duplicative content is the one-sentence observation that empty regions are handled by vacuous satisfaction of the quantifier-bounded clauses. The surrounding re-derivation and the re-assertion that the predicates are "fixed upstream" add no reasoning.
**Required**: Reduce §Position Constraints to the vacuous-satisfaction observation (and the APPEND-is-`j=N` remark), and drop the region-emptiness re-enumeration.

### Issue 3: Pre-state composite-boundary status is an unstated precondition
**ASN-0100, §Provenance**: "for a Shifted-right address, `a` was in `d`'s content-subspace range at the pre-state composite boundary Σ, so `(a, d) ∈ Contains_C(Σ) ⊆ R` by pre-state P4★."
**Problem**: P4★, P4a, P7a are *composite-boundary* properties in ASN-0047's ExtendedReachableStateInvariants — they are not guaranteed at arbitrary elementary-reachable states. The post-state P4★ discharge for shifted-right content (and the P4a/P7a inheritances) silently assumes the pre-state Σ is a composite boundary, but INS.pre lists only `d ∈ dom(M)`, position validity, `n ≥ 1`, `v_k ∈ Val`. The boundary assumption is load-bearing (without it `(a,d) ∈ R` for shifted-right `a` is not secured) yet absent from the precondition.
**Required**: State explicitly in INS.pre (or as a standing assumption) that Σ is a composite boundary, so that pre-state P4★/P4a/P7a are available.

### Issue 4: Defensive allocation-history paragraph in the empty-document example
**ASN-0100, §A Worked Example (empty-document first insertion)**: "Arrangement emptiness alone would not suffice: by S0/P0, prior d-origin content persists in dom(C) even after removal from the arrangement, in which case K.α's subsequent-emission branch would fire … The post-state invariants hold for whichever fresh `a_k` the branch produces; only the address values depend on allocation history, not on arrangement emptiness."
**Problem**: The example already stipulates "no content has ever been allocated under `d`," which fixes the first-emission branch. This paragraph then imagines and rebuts a configuration the stipulation excludes — a defensive expansion that does not advance the example. The relevant fact (the branch keys on `dom(C)`, not arrangement) belongs to INS.alloc, not restated mid-example.
**Required**: Replace with one clause noting the first-emission branch fires under the stipulation; drop the counterfactual rebuttal.

## OUT_OF_SCOPE

### Topic 1: Failure-recovery, link-subspace insertion, INSERT self-composition, concurrency, derived document metadata
**Why out of scope**: These are correctly listed in the ASN's own §Open Questions and §Bounding the Scope. They are future ASNs (or operational-semantics concerns), not gaps in the present content-subspace INSERT specification.

The technical core is sound: INS.M-exhaustive closes the exhaustiveness gap, the three regions are shown pairwise-disjoint with the boundary arithmetic split correctly on `k=0` vs `k≥1`, the worked example's numeric INS.proj instantiation checks against the exhibited arrangement, and the wp analysis treats two genuinely non-trivial postconditions. The findings above are accreted prose and one unstated precondition, not reasoning errors.

VERDICT: REVISE
