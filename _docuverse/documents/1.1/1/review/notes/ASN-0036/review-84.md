# Review of ASN-0036

## REVISE

### Issue 1: S7c postcondition (c) uses informal "ordinal-only formulation" terminology
**ASN-0036, S7c Formal Contract, postcondition (c)**: "TA7a's ordinal-only formulation can be applied to the within-subspace ordinal [E(a)₂, ..., E(a)_δ]."
**Problem**: TA7a's formal contract in ASN-0034 does not define an "ordinal-only formulation" as a named formulation. TA7a defines ⊕ and ⊖ on the subspace S = {o ∈ T : #o ≥ 1 ∧ (A i : oᵢ > 0)} with specific preconditions on operands. The phrase "ordinal-only formulation" is architectural prose; the Formal Contract should refer to TA7a's actual operations and preconditions, not to an informal usage pattern.
**Required**: Reformulate, e.g.: "When #E(a) ≥ 2, the within-subspace ordinal [E(a)₂, ..., E(a)_δ] is a non-empty tumbler that lies in S whenever all its components are positive, satisfying TA7a's operand precondition o ∈ S so that ⊕ and ⊖ are directly applicable."

### Issue 2: D-CTG-depth proof omits explicit S8a verification for the constructed intermediate w
**ASN-0036, D-CTG-depth proof, intermediate construction**: The proof constructs w with components copied from v₁, wⱼ₊₁ = n, and remaining components = 1, then shows v₁ < w < v₂ via T1(i). It does not verify that w satisfies S8a.
**Problem**: For the contradiction to land, D-CTG must force w ∈ V_1(d). But V_1(d) ⊆ dom(M(d)), and dom(M(d)) contains only S8a-conforming positions. If w fails S8a, D-CTG cannot place w in V_1(d) regardless of order-comparison properties. The argument's force depends on w satisfying S8a, but the step is implicit.
**Required**: Add explicit verification: "By construction, every component of w is at least 1 — (v₁)ᵢ ≥ 1 for i ≤ j by S8a on v₁, wⱼ₊₁ = n > (v₁)ⱼ₊₁ ≥ 1, and wᵢ = 1 for j + 2 ≤ i ≤ m. Hence zeros(w) = 0 and (A i : wᵢ > 0). Combined with #w = m ≥ 3 ≥ 2, w satisfies S8a — so the candidate w qualifies for D-CTG's consequent."

### Issue 3: S5 Depends entry conflates the two constructions' uses of T3
**ASN-0036, S5 Depends**: "T3 (CanonicalRepresentation, ASN-0034) — required to enumerate N + 1 pairwise-distinct documents dⱼ and N + 1 pairwise-distinct V-positions vⱼ from distinct component sequences"
**Problem**: The two constructions invoke T3 differently. The cross-document construction uses identical V-positions vᵢ = [1, 1] across N + 1 distinct documents — T3 is needed for document distinctness, not V-position distinctness. The within-document construction uses one document d with N + 1 pairwise-distinct V-positions [1, k] — T3 is needed for V-position distinctness, not document distinctness. The single conjunctive Depends entry mis-describes both uses.
**Required**: Distinguish the two roles: "T3 — used in the cross-document construction to establish distinctness of document tumblers dⱼ from distinct component sequences; and in the within-document construction to establish distinctness of V-positions [1, k] for k = 1, …, N + 1 from distinct last components."

### Issue 4: S8's existence proof and the k ≥ 1 subspace-preservation derivation are loosely connected
**ASN-0036, S8 proof, "The subspace-preservation postcondition" paragraph**: The proof constructs singleton runs (nⱼ = 1), for which conjunct (b) at k = 0 is the base mapping and the subspace-preservation property holds trivially via shift(a, 0) = a. The proof then derives subspace preservation for k ≥ 1 — "which arises only in coarser decompositions with run lengths exceeding 1."
**Problem**: The k ≥ 1 derivation establishes a property for runs of length > 1, but the proof does not construct any such runs. As presented, the derivation appears to be part of S8's existence argument when it is actually a generic-run property used to underwrite the Formal Contract postcondition "for each run, shift(aⱼ, k) preserves the I-address subspace." The framing conflates what is proved for the constructed singleton witness with what holds for any correspondence run satisfying S8.
**Required**: Either (a) lift the subspace-preservation property out of the existence proof and state it as a corollary of correspondence-run definitions with its own contract, or (b) reorganize the proof so the k = 0 case discharges the singleton's obligation and the k ≥ 1 derivation is explicitly tagged as an auxiliary fact about any correspondence run satisfying S8's conjunct (b) — not as a step in establishing singleton existence.

## OUT_OF_SCOPE

### Topic 1: Operation-specific preservation of D-CTG, D-MIN, S8a, and subspace alignment
**Why out of scope**: Operations are explicitly listed in the scope statement as out of scope. Per-operation preservation analyses belong in their respective ASNs; the strand model correctly defers them.

### Topic 2: Link-subspace (S = 2) contiguity semantics
**Why out of scope**: D-CTG, D-MIN, D-CTG-depth, D-SEQ are bound to S = 1; the link subspace's sparse, append-only-with-tombstones structure is acknowledged as deferred to a future ASN.

### Topic 3: Specific value of m in ValidInsertionPosition's empty case
**Why out of scope**: The strand model fixes only m ≥ 2 for the empty-case depth; the canonical choice (m = 2 vs deeper subdivisions Nelson contemplated at LM 4/31) is an operations-layer allocation convention.

### Topic 4: Operational guarantees of non-trivial correspondence runs
**Why out of scope**: S8 asserts existence of some finite decomposition. Whether coarser decompositions arise — through sequential allocations, run-coalescing operations — is operations-layer territory beyond a state-invariant specification.

VERDICT: REVISE
