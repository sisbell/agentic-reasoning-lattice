# Review of ASN-0064

## REVISE

### Issue 1: Overlap test operates on span denotations, not I-address sets

**ASN-0064, Definition — EndsetOverlap and Definition — Satisfaction**: The overlap predicate is defined for "an I-address set Q": `overlaps(e, Q) ≡ coverage(e) ∩ Q ≠ ∅`. But the satisfaction predicate passes `⟦F_Q⟧` — a span denotation — as the second argument: `overlaps(F, ⟦F_Q⟧)`.

**Problem**: Span denotation `⟦Σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}` (ASN-0053) includes *all* tumblers in the half-open interval — not just element-level I-addresses. The resolved set `resolve(d, Q_V)` is a finite set of element-level tumblers (by F0 + S7b). These sets are not equal: `⟦F_Q⟧ ⊋ resolve(d, Q_V)`.

The satisfaction predicate therefore tests `coverage(F) ∩ ⟦F_Q⟧ ≠ ∅`, which is span-level overlap, not element-level overlap. For two level-uniform spans at the same depth d, span-level overlap implies a shared depth-d tumbler (since if `s₁ < reach(σ₂) ∧ s₂ < reach(σ₁)` with `#s₁ = #s₂ = d`, then WLOG `s₂` falls in `⟦σ₁⟧`, and `s₂` is at depth d). But for non-level-uniform spans — which ASN-0043 permits in endsets — span-level overlap can occur without any shared element-level address.

Concrete scenario: an endset span `(a, ℓ)` where `a` is depth-8 element-level and `ℓ` has action point at position 3 (depth-3 width). The reach `a ⊕ ℓ` has length 3 (result-length identity), producing a span covering everything from one element address up to a node-level boundary — crossing subspace and document boundaries. This span has non-empty span-level intersection with nearly any query span, producing a false positive in the satisfaction predicate.

**Required**: Either:
(a) Define the satisfaction predicate using the resolved I-address set directly — `overlaps(F, resolve(d, Q_V))` — rather than the span denotation `⟦F_Q⟧`. This makes the definition exact. The pairwise span biconditional then becomes an optimization lemma, not part of the formal definition.
Or (b) add a level-uniformity precondition (endset spans and query spans are level-uniform at compatible depths) and prove a lemma: for level-uniform spans at depth d, `⟦σ₁⟧ ∩ ⟦σ₂⟧ ≠ ∅` implies `(E t : #t = d : t ∈ ⟦σ₁⟧ ∩ ⟦σ₂⟧)`.

This issue propagates to two other locations:

**(1a) F1 — ResolutionFragmentation**: "the set `resolve(d, {σ_V})` admits representation as a span-set of at most m spans." The proof constructs I-spans whose denotations are supersets of the resolved I-addresses. "Representation" is undefined — `⟦Σ⟧ ≠ resolve(d, {σ_V})`. The claim should either define a depth-restricted denotation (`⟦Σ⟧_d = ⟦Σ⟧ ∩ {t : #t = d}`) or state the relationship precisely (e.g., "the element-level addresses in `⟦Σ⟧` are exactly `resolve(d, {σ_V})`").

**(1b) Worked Example — V-span denotation**: "the selection is `⟦σ_V⟧ = {[1,k] : 2 ≤ k < 6}`." This is false. `⟦σ_V⟧ = {t ∈ T : [1,2] ≤ t < [1,6]}` includes infinitely many extension tumblers at depth > 2 (e.g., `[1,2,1]`, `[1,3,5]`). The correct statement: "the V-positions in `dom(M(d)) ∩ ⟦σ_V⟧` are `{[1,2], [1,3], [1,4], [1,5]}`," which follows from S8-depth (all V-positions have depth 2) and the resolution function's intersection with `dom(M(d))`.


### Issue 2: F6b prescribes implementation mechanism instead of abstract guarantee

**ASN-0064, Endset Symmetry section**: "Per-endset indexing must support sub-linear search: the cost of finding links matching a given endset constraint must not grow with the total number of non-matching links. No endset slot is privileged or degraded in discovery."

**Problem**: "Per-endset indexing" prescribes a specific implementation strategy. An alternative implementation (e.g., a multi-dimensional spatial index over all three endsets simultaneously) could satisfy the same performance guarantee without per-endset indexing. The specification should state what the system must guarantee, not how it must be built.

**Required**: Restate as the abstract performance guarantee: "The cost of evaluating a query constrained on endset slot `e` must not grow with the number of links whose slot `e` does not satisfy the constraint." This is what Nelson's quote ("THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS") actually demands — independence from non-matching links, not a specific indexing structure.


## OUT_OF_SCOPE

### Topic 1: Link creation transition and Σ.L state integration
**Why out of scope**: The ASN explicitly assumes LinkEntityCoherence pending a link-creation ASN (analogous to K.α for content). The integration of Σ.L into the formal system state (C, E, M, R) is also deferred. Both are prerequisites for proving properties about link store evolution but do not affect the query semantics defined here.

### Topic 2: Distributed completeness under network partition
**Why out of scope**: The ASN's completeness guarantee (F4) is defined over the full link store. Partial visibility under partition is a distributed systems concern — it requires a replication and consistency model that the ASN correctly defers.

### Topic 3: Information-flow guarantees for access control
**Why out of scope**: F7 establishes set-membership exclusion (inaccessible links absent from the result). The stronger property — no information leakage via timing, counts, or other side channels — is an information-flow guarantee that requires a different formal framework.

VERDICT: REVISE
