# Review of ASN-0099

## REVISE

### Issue 1: F6's formal statement does not capture the substantive claim
**ASN-0099, F6 (TransclusionTransparency)**: "findlinks({α}, Σ) is the same set regardless of whether α is queried via v₁ or v₂."

**Problem**: The formal claim is trivially true. `findlinks({α}, Σ)` is a function of `(I, Σ)` only — it does not consult `v₁` or `v₂`. The "regardless of how α is queried" parenthetical is operational intuition without formal content. The substantive transclusion-transparency claim — what the surrounding prose is actually arguing — is that V-side queries from different documents to the same I-address produce the same result.

**Required**: Reformulate F6 in terms of `findlinks_V`: `findlinks_V({v₁}, d₁, Σ) = findlinks_V({v₂}, d₂, Σ)` under the given preconditions. The derivation chain becomes explicit: `image({v₁}, d₁, Σ) = {α} = image({v₂}, d₂, Σ)` by direct evaluation, then F12 + functional determinism of `findlinks` close.

### Issue 2: Cross-document T1 case (ii) is non-vacuous; vacuity claim implied in derivation is wrong
**ASN-0099, F10 (OrderedResult)**, discussion of cross-document ordering: the derivation considers T1 case (ii) (`d₁ ≺ d₂`) and the surrounding prose suggests this case is exotic. But ASN-0047's K.δ k=1 case (version sub-allocator) creates versions via `inc(d, 1)`, producing documents with `d ≺ inc(d, 1)`. So `d₁ ≺ d₂` between documents is the normal version-of relationship, not a corner case.

**Problem**: The derivation handles the case correctly (anchors `b_L(d₁)` and `b_L(d₂)` diverge at position `#d₁+1` with 0 vs ≥1), but the framing obscures that this is the routine version-graph case rather than an edge case worth dispatching quickly.

**Required**: A sentence clarifying that T1 case (ii) on documents is the version-extension case (K.δ k=1 path), so the derivation is exercising the version-ordering machinery, not a vacuous branch.

### Issue 3: F4 adds no content beyond F1
**ASN-0099, F4 (PartialOverlapSuffices)**: states one direction of an implication that is the existential-introduction half of F1's definition.

**Problem**: F4's content is `(∃i : P(i)) ⟸ P(j)` for any j in range — pure existential introduction. The "we name F4 as a separate claim because the consequence is a load-bearing design choice" justification is about emphasis, not about a derivable property. A claim that is logically equivalent to a definitional step is not a claim, it is a restatement.

**Required**: Either delete F4 and move its prose into commentary on F1, or strengthen F4 to a load-bearing consequence not already captured by F1 (e.g., a biconditional with explicit refutation of any strengthened condition).

### Issue 4: A1's dependency surface is real and the remediation path should land before this ASN is built upon
**ASN-0099, A1 (EffectClauseExhaustivity)**: A meta-axiom asserting that ASN-0047's effect clauses are exhaustive. Load-bearing for F9's K.μ⁺/K.μ⁻ cases and F9-cor's K.ρ case.

**Problem**: A1 is a strong meta-claim about published specifications — it cannot itself be proved within the system. The ASN's Open Question proposes revising ASN-0047 to add `L' = L` to those frames, eliminating A1 entirely. But A1 sits in the body of this ASN as an axiom while that revision remains pending. Subsequent ASNs that consume F9 will inherit A1's load-bearing role.

**Required**: Either (a) land the ASN-0047 revision and remove A1 before this ASN is consumed downstream, or (b) elevate A1 from a casual "structural axiom" framing to an explicit invariant that ASN-0047 must satisfy — naming it as the contract between this ASN and the operation specifications it relies on.

## OUT_OF_SCOPE

### Topic 1: Inverse direction (FOLLOWLINK / endset resolution to V-positions)
**Why out of scope**: The ASN explicitly defers this to a separate operation with its own specification. Consistent with the two-phase factoring — FINDLINKS handles V→Link, the inverse handles Link→V.

### Topic 2: Pagination semantics across state transitions
**Why out of scope**: The ASN provides canonical ordering (F10) within a single state but defers cross-state pagination consistency. This is acknowledged as an Open Question.

### Topic 3: Multi-instance / replication / partition tolerance
**Why out of scope**: The ASN scopes itself to single-state semantics under SequentialTransitionAxiom. Multi-server concerns belong to BEBE.

### Topic 4: Access-control formalization
**Why out of scope**: The ASN identifies access control as composing with scope (F14) but defers its formalization.

### Topic 5: Phantom-address queries (I outside dom(C) ∪ dom(L))
**Why out of scope**: The ASN flags this as undecided. The match predicate is mechanically well-defined for any `I ⊆ T`, but the operational meaning is unsettled.

VERDICT: REVISE
