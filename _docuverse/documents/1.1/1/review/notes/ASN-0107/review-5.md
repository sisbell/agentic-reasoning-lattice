# Review of ASN-0107

## REVISE

### Issue 1: R1's case analysis silently assumes the deleted entry's I-address is consulted in only one slot
**ASN-0107, R1 (MinimalDecrementNoStoreRetraction)**: "Consider the *minimal contraction*: a `K.μ⁻` step removing a single consulted entry... (P-sole) *Sole matching link.* `a` is reached, in the relevant slot `i`, by exactly one matching link `ℓ`... Under (P-last) and (P-sole)... `Δnum_disc ∈ {−1, 0}`."
**Problem**: The query regions `W = (W₁, W₂, W₃)` are arbitrary subsets of `T` with no disjointness requirement, so a single V-position `v` may lie in two regions (e.g. `v ∈ W₁ ∩ W₂`). Removing `v ↦ a` then evicts `a` from both `Q₁(Σ')` and `Q₂(Σ')`. (P-sole) constrains only slot `i`; a *different* matching link `ℓ'` that reached `a` through slot `j ≠ i` can also drop, giving `Δnum_disc ≤ −2` from a single-entry removal. The conclusion `Δnum_disc ∈ {−1, 0}` is therefore not established for the stated preconditions.
**Required**: Add an explicit precondition that `a` is consulted in a single slot (or that the query regions are pairwise disjoint), or extend the case analysis to account for `a` leaving multiple `Qⱼ`.

### Issue 2: No weakest-precondition analysis; the change-laws give sufficient, not weakest, conditions
**ASN-0107, R1–R5 / Open Questions**: The R-laws derive *sufficient* conditions for the discovery count to fall (e.g. "(P-last) and (P-sole) ... ⟹ `Δ = −1`"), and the final open question defers idempotence/wp to the query layer.
**Problem**: The review standard requires at least one non-trivial weakest-precondition derivation, and the foundation ASNs (ASN-0086, ASN-0098) set this precedent with explicit `wp` claims. ASN-0107 performs wp-flavoured reasoning but never characterizes a *weakest* precondition for any non-trivial postcondition — e.g. "wp under `K.μ⁻` for a given counted link to remain counted," or "wp for `num_disc` to be preserved across a transition." R1 states sufficient conditions without arguing minimality.
**Required**: Add at least one explicit weakest-precondition derivation for a non-trivial postcondition (e.g. preservation of a counted link's discoverability, or `Δnum_disc = 0` across `K.μ⁻`), naming the postcondition and showing the precondition is weakest.

### Issue 3: R1's "floor" claim contradicts its own bound and R3
**ASN-0107, R1**: "The decrement of one is the *floor* on a contraction's effect, the `k = 1` case of R2 below."
**Problem**: This sentence is internally inconsistent. R1 itself concludes `Δnum_disc ∈ {−1, 0}`, and R3 establishes `Δ = 0` (partial survival) — a smaller-magnitude effect than `−1`. R2 establishes `Δ = −k` for shared endpoints — a larger-magnitude effect. So `−1` is neither a lower nor an upper bound on a contraction's effect; calling it "the floor" misdescribes the result.
**Required**: Reword to state that `−1` is the minimal *non-trivial single-link* decrement (the `k = 1` case), not a floor on contraction effects in general.

## OUT_OF_SCOPE

### Topic 1: Independent per-slot anchoring to separately-evolving documents
**Why out of scope**: The first open question (three parts anchored to different evolving arrangements) is genuinely new territory — the ASN fixes a single resolution document `d_q` for the discovery count, and multi-document anchoring is a distinct specification, not a defect in this one.

### Topic 2: Relationship between the count and the retrieval operation's returned set
**Why out of scope**: The staleness/coincidence guarantee between `num` and the cardinality of what FINDLINKS would return belongs with the retrieval operation (ASN-0099), explicitly excluded by scope.

VERDICT: REVISE
