# ASN-0040: Tumbler Baptism

*2026-03-15*

We seek to understand what it means for a position to enter the tumbler hierarchy. The algebra (ASN-0034) gives us an infinite space of well-formed addresses — ordered by T1, structured into fields by T4, permanently allocated by T8, strictly increasing by T9. But the algebra cannot distinguish between a position that *has been assigned* and one that merely *could be*. Something marks the transition from arithmetic possibility to system fact.

Nelson calls this transition *baptism*:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers."

Three observations are compressed into that sentence. Baptism is *hierarchical* — it descends level by level through the field structure. Baptism is *sequential* — Nelson elsewhere describes creation as "successive new digits to the right," emphasizing that positions arrive in order, not arbitrarily. And baptism is *permanent* — "Any address, once assigned, remains valid forever." We defer the authorization aspect (who may baptize) to a future ASN on tumbler authorization. Here we characterize the structural mechanism: how the set of baptized positions grows, and what it preserves as it grows.

Gregory's implementation reveals the operational anatomy. Baptism is a two-phase process: first, the system queries the existing address space for the highest allocated position under a given parent prefix and increments to produce a candidate; second, it writes that candidate into the persistent store. The write — not the query — is the moment of baptism. A candidate computed but never written does not exist; if the query were repeated without an intervening write, it would return the same candidate. The address becomes real at the instant of commitment.

We formalize baptism as the growth law of the address space.


## The baptismal registry

We introduce the central state component:

**Σ.B (BaptismalRegistry).** Σ.B ⊆ T — the set of baptized tumblers.

A tumbler t is *baptized* iff t ∈ Σ.B. Initially Σ.B contains some non-empty finite seed set B₀ ⊆ T of root addresses established at system genesis, subject to the conformance requirement stated at B1 below. Thereafter it grows monotonically:

*Justification.* Σ.B is introduced as a state definition — a subset of T, the set of all well-formed tumblers from the algebra (ASN-0034). This type constraint holds by construction in every reachable state. At genesis, B₀ ⊆ T holds by B₀ conf. (SeedConformance), which requires every seed element to be a well-formed tumbler satisfying T4. Thereafter, the only mechanism that enlarges Σ.B is baptism (by B0a, Baptismal Closure), and every baptismal output is an element of T: when the namespace is empty, the first child inc(p, d) is a well-formed tumbler by TA5(d); when siblings exist, the next sibling inc(cₘ, 0) is a well-formed tumbler by TA5(c). No operation removes elements from Σ.B (by B0, Irrevocability). Since the seed set lies in T, the sole growth mechanism produces elements of T, and no element is ever removed, the constraint Σ.B ⊆ T is preserved across all transitions. ∎

*Formal Contract:*
- *Definition:* Σ.B ⊆ T — the set of tumblers that have been baptized or were present in the seed set B₀.
- *Axiom:* Σ.B is a state component introduced by design. The type invariant Σ.B ⊆ T is preserved by B₀ conf. (seed validity), B0 (irrevocability), B0a (baptismal closure), TA5(c) (sibling increment well-definedness), TA5(d) (child increment well-definedness).

**B0 (Irrevocability).** `(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`.

No operation removes a tumbler from B. This is the state-level reading of T8 (AllocationPermanence). T8 says the allocator never reclaims an address; B0 says the *registry* never shrinks. The distinction matters: B0 forbids any mechanism — not just the allocator — from removing a baptized position. Administrative action, garbage collection, storage failure — none may contract B. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid."

B0 tells us baptism cannot be undone; its companion tells us what *can* add to B:

**B0a (Baptismal Closure).** The registry grows only through baptism:

  `(A Σ, Σ' : Σ → Σ' : (A t : t ∈ Σ'.B \ Σ.B : t was produced by baptism(p, d) for some (p, d) satisfying B6))`

Here "satisfying B6" means p satisfies T4, d ∈ {1, 2}, and zeros(p) + (d − 1) ≤ 3 — depth validity as defined below. Whether p must itself be baptized (p ∈ Σ.B) before children can be baptized beneath it is deliberately deferred to the Open Questions; B0a constrains only the depth arithmetic, not the authorization chain. No mechanism other than baptism — no administrative action, no side effect of content operations, no bulk initialization after genesis — may insert an address into B. B0 says nothing leaves; B0a says nothing enters except through the designated gate. Without B0a, an arbitrary operation could insert c₅ into a namespace lacking c₁ through c₄, and the contiguous prefix property (B1 below) would be violated.

The binary character of this state is fundamental. Nelson's model has no third status between baptized and unbaptized: "the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." A position is either conceptually assigned (in B) or not. Whether anything is *stored* at that position is a separate question, which we address below as the ghost validity property.


## The sibling stream

Consider a parent address p ∈ T and a baptismal depth d ≥ 1. From TA5, `inc(p, d)` produces a tumbler strictly greater than p that extends p by d components: d − 1 zero separators followed by 1. This is the *first child* of p at depth d. Repeated sibling increments yield a counting sequence:

  c₁ = inc(p, d)

  cₙ₊₁ = inc(cₙ, 0)    for n ≥ 1

**S(p,d) (SiblingStream).** We call the sequence c₁, c₂, c₃, ... the *sibling stream* of p at depth d, written S(p, d). By TA5(c), each sibling increment preserves the tumbler's length and advances only the last significant component by 1. Every element of S(p, d) has the form [p₁, ..., p_{#p}, 0, ..., 0, n] — the parent's components, then d − 1 zeros, then the ordinal n. The stream is strictly increasing:

*Proof.* We must show that every element cₙ of S(p, d) has the form [p₁, ..., p_{#p}, 0, ..., 0, n] — the parent's first #p components, then d − 1 zeros, then ordinal n — with uniform length #cₙ = #p + d. The argument proceeds by induction on n.

*Base case (n = 1).* c₁ = inc(p, d) with d ≥ 1. By TA5(d) (ASN-0034), c₁ has length #p + d: the first #p components are preserved from p (TA5(b)), the next d − 1 positions #p + 1 through #p + d − 1 are zero-valued field separators, and the final position #p + d has value 1. This is exactly [p₁, ..., p_{#p}, 0, ..., 0, 1] with d − 1 zeros and ordinal 1.

*Inductive step.* Assume cₙ = [p₁, ..., p_{#p}, 0, ..., 0, n] with d − 1 zeros and #cₙ = #p + d for some n ≥ 1. Since n ≥ 1, position #p + d holds value n > 0, so sig(cₙ) = #p + d — the ordinal position is the last significant component. Consider cₙ₊₁ = inc(cₙ, 0). By TA5(c), cₙ₊₁ has the same length as cₙ (#cₙ₊₁ = #p + d) and differs from cₙ only at position sig(cₙ) = #p + d, where cₙ₊₁ at that position equals n + 1. All other positions are unchanged: the first #p components remain p₁, ..., p_{#p} (since every position i ≤ #p satisfies i < sig(cₙ) = #p + d), and the d − 1 zeros at positions #p + 1 through #p + d − 1 remain zero (since each such position j satisfies j < #p + d = sig(cₙ)). Therefore cₙ₊₁ = [p₁, ..., p_{#p}, 0, ..., 0, n + 1], the claimed form with ordinal n + 1. ∎

*Formal Contract:*
- *Definition:* S(p, d) = c₁, c₂, c₃, ... where c₁ = inc(p, d) and cₙ₊₁ = inc(cₙ, 0) for n ≥ 1.
- *Preconditions:* p ∈ T, d ≥ 1.
- *Postconditions:* `(A n ≥ 1 : cₙ = [p₁, ..., p_{#p}, 0, ..., 0, n])` with d − 1 zeros and `#cₙ = #p + d`.
- *Axiom:* TA5(b) (prefix preservation), TA5(c) (sibling structure), TA5(d) (child structure).

**S0 (StreamOrdering).** `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`.

*Proof.* We must show that for every pair of indices i, j with 1 ≤ i < j, the i-th element of the sibling stream S(p, d) is strictly less than the j-th under the lexicographic order T1. The sibling stream is defined by c₁ = inc(p, d) and cₙ₊₁ = inc(cₙ, 0) for n ≥ 1. The argument proceeds by strong induction on the gap j − i.

*Base case (j − i = 1).* Here j = i + 1, so cⱼ = c_{i+1} = inc(cᵢ, 0). By TA5(a) (ASN-0034), `inc(t, 0)` produces a tumbler strictly greater than t under T1 for any valid tumbler t. Instantiating with t := cᵢ yields cᵢ₊₁ > cᵢ, establishing cᵢ < cⱼ.

*Inductive step (gap j − i = g + 1, assuming the result holds for all gaps ≤ g).* Since g + 1 ≥ 2, the index j − 1 satisfies i ≤ i < j − 1 < j, with gap (j − 1) − i = g ≥ 1. By the inductive hypothesis applied to the pair (i, j − 1), cᵢ < c_{j−1}. By the base case applied to the pair (j − 1, j), c_{j−1} < cⱼ. The lexicographic order T1 is a strict total order and therefore transitive: from cᵢ < c_{j−1} and c_{j−1} < cⱼ we conclude cᵢ < cⱼ. ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, d ≥ 1. S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).
- *Postconditions:* `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — the sibling stream is strictly increasing.
- *Axiom:* TA5(a) (strict increase under inc), T1 (transitivity of lexicographic order).

**S1 (StreamPrefix).** `(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

*Proof.* We must show that for every n ≥ 1, the n-th element cₙ of S(p, d) satisfies p ≼ cₙ — that is, #cₙ ≥ #p and cₙᵢ = pᵢ for all 1 ≤ i ≤ #p. The argument proceeds by induction on n.

*Base case (n = 1).* c₁ = inc(p, d) with d ≥ 1. By TA5(d), c₁ has length #p + d, with the first #p components preserved from p: c₁ᵢ = pᵢ for 1 ≤ i ≤ #p. Since d ≥ 1, #c₁ = #p + d ≥ #p + 1 > #p. Both conditions of the prefix relation are satisfied: p ≼ c₁.

*Inductive step.* Assume p ≼ cₙ for some n ≥ 1. We show p ≼ cₙ₊₁ where cₙ₊₁ = inc(cₙ, 0). By TA5(c), cₙ₊₁ has the same length as cₙ (#cₙ₊₁ = #cₙ) and differs from cₙ only at position sig(cₙ), where cₙ₊₁ at sig(cₙ) equals cₙ at sig(cₙ) plus 1. The modification preserves the prefix provided sig(cₙ) > #p — we establish this now.

For c₁, the final component has value 1 (TA5(d)), so sig(c₁) = #c₁ = #p + d. Each subsequent cₙ₊₁ = inc(cₙ, 0) advances the value at position sig(cₙ) by 1 (TA5(c)), preserving its positivity, and preserves length. By induction on the stream index, sig(cₙ) = #cₙ = #p + d for all n ≥ 1. Since d ≥ 1, sig(cₙ) = #p + d > #p.

Therefore every position i with 1 ≤ i ≤ #p satisfies i < sig(cₙ), so cₙ₊₁ᵢ = cₙᵢ at these positions (TA5(c) modifies only sig(cₙ)). By the inductive hypothesis, cₙᵢ = pᵢ for 1 ≤ i ≤ #p, hence cₙ₊₁ᵢ = pᵢ. Since #cₙ₊₁ = #cₙ ≥ #p (from the hypothesis), both prefix conditions hold: p ≼ cₙ₊₁. ∎

*Formal Contract:*
- *Definition:* `p ≼ cₙ ⟺ #cₙ ≥ #p ∧ (A i : 1 ≤ i ≤ #p : cₙᵢ = pᵢ)`.
- *Preconditions:* p ∈ T, d ≥ 1. S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).
- *Postconditions:* `(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

As a consequence, since every cₙ extends p, the entire stream lies within the set {t ∈ T : p ≼ t}, which forms a contiguous interval under T1 by T5 (PrefixContiguity).

Nelson describes exactly this process: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." The word "successive" is precise — positions arrive in order, c₁ before c₂ before c₃. "Items 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." The stream is traversed monotonically, not sampled.


## The baptism operation

We define the *children* of parent p at depth d in state B:

  children(B, p, d) = B ∩ S(p, d)

— the baptized addresses that belong to the sibling stream. The next address in a namespace is determined by the current registry state:

**next(B,p,d) (NextAddress).**

  next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0)

— find the greatest baptized sibling and produce its immediate successor; if none exists, produce the first child.

*Justification of well-definedness.* We must show that next(B, p, d) is well-defined for any registry B ⊆ T, parent p ∈ T, and depth d ≥ 1 — that is, each branch of the conditional produces an element of T, and the case split is exhaustive.

The case split is exhaustive: children(B, p, d) = B ∩ S(p, d) is a set, so it is either empty or non-empty. No third possibility exists.

*Case 1: children(B, p, d) = ∅.* The definition yields next(B, p, d) = inc(p, d). By TA5(d) (ASN-0034), inc(p, d) is well-defined for any p ∈ T and d ≥ 1, producing a tumbler of length #p + d whose first #p components are preserved from p, whose next d − 1 positions are zero-valued field separators, and whose final position has value 1. The result is an element of T — specifically, c₁ of the sibling stream S(p, d).

*Case 2: children(B, p, d) ≠ ∅.* The definition yields next(B, p, d) = inc(max(children(B, p, d)), 0). We must show that max(children(B, p, d)) exists and that the subsequent increment is well-defined. The set children(B, p, d) is a non-empty finite subset of T (finite because B is finite, non-empty by hypothesis). The lexicographic order T1 is a strict total order on T, so every non-empty finite subset has a unique maximum. Let t = max(children(B, p, d)). By TA5(c), inc(t, 0) is well-defined for any t ∈ T: it preserves the length of t and advances the value at position sig(t) by 1, producing an element of T.

In both cases, next(B, p, d) produces an element of T. The definition is total on its domain {(B, p, d) : B ⊆ T finite, p ∈ T, d ≥ 1}. ∎

*Formal Contract:*
- *Definition:* next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0), where children(B, p, d) = B ∩ S(p, d).
- *Preconditions:* B ⊆ T finite; p ∈ T; d ≥ 1; S(p, d) defined.
- *Postconditions:* next(B, p, d) ∈ T — the result is a valid tumbler.
- *Axiom:* TA5(c) (sibling increment well-definedness), TA5(d) (child increment well-definedness), T1 (total order guarantees max exists).

**Bop (Baptism).** The operation baptize(p, d) is defined by:

  PRE: B6(p, d) — depth validity (defined below); B4 — serialized within namespace (p, d) (defined below); [parent prerequisite deferred to Open Questions]
  POST: Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}
  FRAME: only Σ.B is modified; all other state components are unchanged

The frame condition is essential: baptism alters the registry and nothing else. Content storage, link structures, arrangement — all are untouched. The precondition B4 ensures the operation observes a stable state: no concurrent same-namespace baptism may interleave between the read of max(children) and the commitment of the new element.

*Proof of well-definedness and correctness.* We must show that under the stated preconditions, baptize(p, d) is well-defined, produces a fresh address, and preserves the system invariants B0, B1, and B10.

**Well-definedness.** The postcondition invokes next(Σ.B, p, d), which branches on whether children(Σ.B, p, d) is empty. If empty, the result is inc(p, d) — well-defined for any p ∈ T and d ≥ 1 by TA5(d). If non-empty, the result is inc(max(children(Σ.B, p, d)), 0). By B1, children(Σ.B, p, d) = {c₁, ..., cₘ} for some m ≥ 1, a finite contiguous prefix, so max exists and equals cₘ. The sibling increment inc(cₘ, 0) is well-defined by TA5(c), since cₘ has a positive last component: for c₁ = inc(p, d), position #p + d holds value 1 (TA5(d)), and each subsequent sibling increment advances this position by 1 (TA5(c)), preserving positivity. In both branches, next produces an element of T.

**Freshness.** Let a = next(Σ.B, p, d) = c_{m+1} where m = hwm(Σ.B, p, d). We show a ∉ Σ.B by partitioning Σ.B into three classes. Within namespace (p, d): by B1, children(Σ.B, p, d) = {c₁, ..., cₘ} is a contiguous prefix of length m, so c_{m+1} is the first unbaptized sibling — it does not appear among {c₁, ..., cₘ}. In any other namespace (p', d') ≠ (p, d): by B7 (Namespace Disjointness), S(p, d) ∩ S(p', d') = ∅, and since a ∈ S(p, d) by construction, a cannot belong to children(Σ.B, p', d') ⊆ S(p', d'). For elements of Σ.B belonging to no sibling stream — root seeds such as [1], where no valid (p'', d'') yields #p'' + d'' = 1 since #p'' ≥ 1 and d'' ≥ 1 — these elements are not in S(p, d), so a ∈ S(p, d) ensures a ≠ t for each such t. The three classes exhaust Σ.B; in each, a is absent. B4 ensures the partition is stable: no concurrent same-namespace baptism modifies children(Σ.B, p, d) between the read and the commitment.

**Monotonicity (B0).** Σ'.B = Σ.B ∪ {a} ⊇ Σ.B directly — the registry grows by one element and no element is removed.

**B1 preservation.** In the target namespace, children(Σ'.B, p, d) = {c₁, ..., cₘ, c_{m+1}} — a contiguous prefix of length m + 1, since the new element is the immediate successor of the previous maximum. For every other namespace (p', d'), B7 ensures a ∉ S(p', d'), so children(Σ'.B, p', d') = children(Σ.B, p', d'), and their contiguous prefix property is undisturbed. B0a (Baptismal Closure) guarantees no non-baptismal mechanism introduces elements that could disrupt contiguity in any namespace.

**B10 preservation.** The new element a must satisfy T4 for the registry-wide validity invariant to hold. Two cases arise from the definition of next. When m = 0, a = inc(p, d) — the first child. B6 provides exactly the three conditions that the TA5a (IncrementPreservesT4, ASN-0034) requires: p satisfies T4 by B6(i), d ≤ 2 by B6(ii), and zeros(p) + (d − 1) ≤ 3 by B6(iii). Therefore a satisfies T4. When m > 0, a = inc(cₘ, 0) — a sibling increment. By B10 for the current state, cₘ satisfies T4 (it was admitted by a prior baptism or is a conforming seed). TA5a with k = 0 preserves T4 unconditionally — no zeros are added, no adjacencies are introduced. Therefore a satisfies T4. ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1; B6(p, d) holds; B4 holds for namespace (p, d); Σ.B satisfies B1 and B10.
- *Postconditions:* Σ'.B = Σ.B ∪ {next(Σ.B, p, d)} with next(Σ.B, p, d) ∉ Σ.B; Σ'.B satisfies B0, B1, and B10.
- *Frame:* Only Σ.B is modified; all other state components are unchanged.


## The contiguous prefix property

We claim that children(B, p, d) is always a *prefix* of the sibling stream: the first m elements for some m ≥ 0, with no gaps.

**B1 (Contiguous Prefix).** `(A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))`.

Equivalently: children(B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

*Proof.* We must show that in every state reachable from a conforming seed B₀, for every parent p and depth d, children(Σ.B, p, d) is a contiguous prefix of S(p, d). The argument proceeds by induction on the number of state transitions from the initial state.

*Base case.* In the initial state, Σ.B = B₀. By B₀ conf. (SeedConformance), children(B₀, p, d) is a contiguous prefix of S(p, d) for every (p, d). B1 holds at genesis.

*Inductive step.* Assume B1 holds for state Σ with registry B. Consider a transition Σ → Σ' producing registry B'. By B0a (Baptismal Closure), the only mechanism that adds elements to B is baptism: B' = B ∪ {a} where a = next(B, p₀, d₀) for some (p₀, d₀) satisfying B6. We must show that children(B', p, d) is a contiguous prefix of S(p, d) for every (p, d). Two cases exhaust the possibilities.

*Target namespace: (p, d) = (p₀, d₀).* By B4 (Namespace Serialization), this baptism observes the complete state left by any prior same-namespace baptism — no interleaving has occurred. By the inductive hypothesis, children(B, p₀, d₀) = {c₁, ..., cₘ} for some m ≥ 0. Two sub-cases arise from the definition of next (NextAddress).

When m = 0: children(B, p₀, d₀) = ∅, so a = next(B, p₀, d₀) = inc(p₀, d₀) = c₁, the first element of S(p₀, d₀) by the definition of the sibling stream. Therefore children(B', p₀, d₀) = {c₁}, a contiguous prefix of length 1.

When m ≥ 1: the maximum of children(B, p₀, d₀) is cₘ, since the prefix {c₁, ..., cₘ} is strictly ordered by S0 (StreamOrdering). The definition of next gives a = inc(cₘ, 0). By TA5(c), this sibling increment advances only the last significant component of cₘ by 1, producing exactly c_{m+1} — the immediate successor in S(p₀, d₀). No element is skipped: the definition of next always selects the immediate successor via inc(cₘ, 0), which by TA5(c) cannot leap over any stream element. By B0 (Irrevocability), B ⊆ B', so {c₁, ..., cₘ} ⊆ B'. Together with the new element c_{m+1} ∈ B', we obtain children(B', p₀, d₀) = {c₁, ..., cₘ, c_{m+1}}, a contiguous prefix of length m + 1.

*All other namespaces: (p, d) ≠ (p₀, d₀).* By construction, a ∈ S(p₀, d₀) and a satisfies T4 (by B10 preservation, established in the Bop correctness proof). We show children(B', p, d) is a contiguous prefix by case analysis on (p, d).

When (p, d) satisfies B6: both (p₀, d₀) and (p, d) meet B7's preconditions, so B7 gives S(p₀, d₀) ∩ S(p, d) = ∅, hence a ∉ S(p, d). Therefore children(B', p, d) = children(B, p, d), a contiguous prefix by the inductive hypothesis.

When (p, d) does not satisfy B6 and every element of S(p, d) violates T4: since a satisfies T4, a ∉ S(p, d). Moreover, B10 for the current state ensures every element of B satisfies T4, so children(B, p, d) = ∅. Therefore children(B', p, d) = ∅, trivially a contiguous prefix. (This covers cases where p has adjacent zeros, p starts with zero, or d ≥ 3.)

When (p, d) does not satisfy B6 but S(p, d) contains T4-valid elements: this occurs when p ends in zero (with no other T4 defect) and d = 1. (When d = 2, the trailing zero of p at position #p and the d − 1 = 1 intermediate zero from TA5(d) at position #p + 1 create adjacent zeros, so all stream elements violate T4 — this falls under the previous sub-case.) Let p' be p with its trailing zero removed, so #p' = #p − 1 and p'ᵢ = pᵢ for 1 ≤ i ≤ #p − 1, and let d' = 2. We show S(p, 1) = S(p', 2) by proving first-element equality and then applying the shared recurrence.

*First-element equality.* The first element of S(p, 1) is c₁ = inc(p, 1). By TA5(d), c₁ has length #p + 1, with the first #p components preserved from p and position #p + 1 set to 1 (d − 1 = 0 intermediate zeros). So c₁ = [p₁, ..., p_{#p−1}, 0, 1] since p_{#p} = 0. The first element of S(p', 2) is c'₁ = inc(p', 2). By TA5(d), c'₁ has length #p' + 2 = #p + 1, with the first #p' = #p − 1 components preserved from p', one intermediate zero at position #p' + 1 = #p, and position #p' + 2 = #p + 1 set to 1. So c'₁ = [p'₁, ..., p'_{#p−1}, 0, 1] = [p₁, ..., p_{#p−1}, 0, 1]. Component-by-component, c₁ = c'₁.

*Stream identity.* Both streams share the recurrence cₙ₊₁ = inc(cₙ, 0). Since c₁ = c'₁ and the recurrence is deterministic, the streams are identical: S(p, 1) = S(p', 2).

We verify that p' satisfies T4 and (p', 2) satisfies B6. For T4: p₁ > 0 (inherited from p); no adjacent zeros (the trailing zero was the sole defect — if p had adjacent zeros or a leading zero, these would be additional T4 violations, contradicting the sole-defect hypothesis); p'_{#p'} = p_{#p−1} > 0 since the trailing zero was the sole defect. For the zero count: the sole-defect hypothesis gives zeros(p) ≤ 3 (a second violation — such as zeros(p) > 3 — would contradict sole defect). Removing the trailing zero yields zeros(p') = zeros(p) − 1 ≤ 2. B6(i): p' satisfies T4 as just shown. B6(ii): d' = 2 ∈ {1, 2}. B6(iii): zeros(p') + (d' − 1) = zeros(p') + 1 ≤ 3. Therefore (p', 2) satisfies B6. Two sub-cases arise. If (p', d') ≠ (p₀, d₀), B7 gives S(p₀, d₀) ∩ S(p', d') = ∅, hence a ∉ S(p', d') = S(p, d), and children(B', p, d) = children(B, p, d). If (p', d') = (p₀, d₀), then children(B', p, d) = children(B', p₀, d₀), whose contiguous prefix property was established in the target namespace case above.

In all sub-cases, children(B', p, d) is a contiguous prefix of S(p, d).

Since B1 is preserved in the target namespace and in every other namespace, B1 holds for B'. By induction on the transition sequence, B1 holds in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A p, d, n : n ≥ 1 ∧ cₙ ∈ Σ.B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ Σ.B))` — equivalently, children(Σ.B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.
- *Base:* B₀ conf. — seed set satisfies contiguous prefix for all (p, d).
- *Preservation:* Each baptism preserves B1 in the target namespace (by Bop, B0, B4, S0, TA5(c)) and in all other namespaces (by B7 for B6-valid pairs; by B10 for non-B6 pairs whose streams are entirely T4-invalid; by stream identity S(p, 1) = S(p', 2) — proved by first-element component comparison and deterministic recurrence — for non-B6 pairs where p ends in zero as its sole defect and d = 1).

Two dependencies bear emphasis. B7 (Namespace Disjointness) ensures no operation outside a namespace inserts an element into its stream. B0a (Baptismal Closure) ensures no mechanism other than baptism adds elements to B at all — without B0a, a non-baptismal operation could insert arbitrary elements into B, and the preservation argument would be ungrounded.

The induction also requires a conforming base:

**B₀ conf. (SeedConformance).** B₀ is non-empty and finite, `(A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))`, and `(A t ∈ B₀ : t satisfies T4)`.

B₀ must be non-empty and finite, satisfy B1 for every namespace at genesis, and have every seed element be a valid address under T4. Non-emptiness is required because with B₀ = ∅ the conformance conditions hold vacuously but no parent exists to anchor any baptism — the system cannot grow. Finiteness is required because the next function's well-definedness depends on max(children(B, p, d)) existing, which requires children to be a finite set; since B starts as B₀ and grows by one element per baptism, B₀ finite implies B finite in every reachable state. Without the contiguity requirement, the seed set could contain {c₁, c₃} for some namespace — a gap that the inductive argument cannot repair, since baptism only appends the next sibling. Without the T4 requirement, a seed element could serve as a parent that violates B6(i), undermining B7's disjointness guarantee.

From B₀ conformance (T4 for seeds) and B6(i) (T4 for parents), we derive by induction on the baptism sequence that T4 validity is a registry-wide invariant:

**B10 (T4ValidityInvariant).** `(A t ∈ Σ.B : t satisfies T4)`

*Proof.* We must show that in every state reachable from a conforming seed B₀, every element of Σ.B satisfies T4 (FieldSeparatorConstraint, ASN-0034). The argument proceeds by induction on the number of state transitions from the initial state.

*Base case.* In the initial state, Σ.B = B₀. By B₀ conf. (SeedConformance), every t ∈ B₀ satisfies T4. The invariant holds at genesis.

*Inductive step.* Assume B10 holds for state Σ with registry B — that is, every t ∈ B satisfies T4. Consider a transition Σ → Σ' producing registry B'. By B0a (Baptismal Closure), the only mechanism that adds elements to B is baptism: B' = B ∪ {a} where a = next(B, p, d) for some (p, d) satisfying B6. We must show every t ∈ B' satisfies T4. For elements t ∈ B, the inductive hypothesis gives t satisfies T4 directly. It remains to show the new element a satisfies T4.

By B6, the parent p satisfies T4 (condition (i)), d ∈ {1, 2} (condition (ii)), and zeros(p) + (d − 1) ≤ 3 (condition (iii)). Let m = hwm(B, p, d). The definition of next (NextAddress) and B2 (High Water Mark Sufficiency) give a = c_{m+1}, the (m + 1)-th element of the sibling stream S(p, d). Two cases arise from the value of m.

*Case 1: m = 0.* The children set is empty, so a = c₁ = inc(p, d). The TA5a (IncrementPreservesT4, ASN-0034) states that inc(t, k) preserves T4 when t satisfies T4, k ≤ 2, and zeros(t) + (k − 1) ≤ 3. These three conditions are exactly B6(i), B6(ii), and B6(iii) with t = p and k = d. Therefore a = inc(p, d) satisfies T4.

*Case 2: m ≥ 1.* The children set is non-empty, and a = c_{m+1} = inc(cₘ, 0) — a sibling increment. By B1 (Contiguous Prefix), children(B, p, d) = {c₁, ..., cₘ}, so cₘ ∈ B. By the inductive hypothesis (B10 for the current state), cₘ satisfies T4. TA5a with k = 0 states that inc(t, 0) preserves T4 unconditionally: no zeros are added (TA5(c) modifies only position sig(t), advancing a positive value by one), no adjacent zeros are introduced, and the tumbler neither begins nor ends in zero after the increment. Therefore a = inc(cₘ, 0) satisfies T4.

In both cases, a satisfies T4. Since every element of B satisfies T4 by the inductive hypothesis and the new element a satisfies T4 by the case analysis, every element of B' = B ∪ {a} satisfies T4. By induction on the transition sequence, B10 holds in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A t ∈ Σ.B : t satisfies T4)` — every baptized address satisfies FieldSeparatorConstraint.
- *Base:* B₀ conf. — every seed element satisfies T4.
- *Preservation:* Each baptism preserves B10: when m = 0, by B6 and TA5a (IncrementPreservesT4, ASN-0034) with k = d; when m ≥ 1, by the inductive hypothesis and TA5a with k = 0. B0a ensures no non-baptismal mechanism introduces elements that might violate T4.

B1 holds for all states reachable from a conforming B₀ under operations satisfying B0a and B7.

The gap between T9 (ForwardAllocation) and B1 is the *no-skip property*: baptism always selects the immediate successor in the stream, never an arbitrary later value. T9 says addresses increase; B1 says they increase *contiguously*. The difference is the guarantee that every ordinal from 1 through m is represented, which T9 alone does not assert.


## The high water mark

B1 yields a simplification: the entire allocation state of a namespace reduces to a single natural number.

**hwm(B,p,d) (HighWaterMark).** hwm(B, p, d) = #children(B, p, d) — the *high water mark*.

*Justification.* We must establish that the cardinality of children(B, p, d) is a sufficient statistic for the allocation state of the namespace (p, d) — that is, knowing only #children(B, p, d) determines both the maximum baptized address and the next address to allocate. Let m = #children(B, p, d).

By B1 (Contiguous Prefix), children(B, p, d) = {c₁, ..., cₘ} — the first m elements of the sibling stream S(p, d) with no gaps. This contiguity is the load-bearing property: it means the set of children is determined entirely by its cardinality. Any set of m elements drawn from a contiguous prefix of a sequence is the prefix itself, so knowing m tells us children(B, p, d) = {c₁, ..., cₘ}.

Two consequences follow. First, the maximum: by S0 (StreamOrdering), the sibling stream is strictly increasing under T1, so max(children(B, p, d)) = cₘ — the last element of the prefix. Second, the next allocation target: since children occupy exactly the first m positions of S(p, d), the next unoccupied position is c_{m+1}. No scan of the children set is needed; the count alone suffices.

Without B1, the count would not determine the maximum — a set of m elements drawn non-contiguously from the stream could have its maximum anywhere. Without S0, even a contiguous prefix need not have its maximum at the last position. Both properties are required for the reduction from set to scalar. ∎

*Formal Contract:*
- *Definition:* hwm(B, p, d) = #children(B, p, d) where children(B, p, d) = {cₙ ∈ S(p, d) : cₙ ∈ B}.
- *Preconditions:* B satisfies B1 for (p, d); p ∈ T, d ≥ 1; S(p, d) defined.
- *Invariant:* hwm(B, p, d) = m implies children(B, p, d) = {c₁, ..., cₘ} and max(children) = cₘ (when m ≥ 1).
- *Axiom:* B1 (contiguous prefix), S0 (stream ordering).

Because children(B, p, d) = {c₁, ..., cₘ} is a contiguous prefix (B1), the maximum is always cₘ and the next element is always c_{m+1}. The operational definition of next — "find max, increment" — reduces to counting:

**B2 (High Water Mark Sufficiency).** `next(B, p, d) = c_{hwm(B,p,d) + 1}`.

Concretely: if hwm = 0, then next = inc(p, d) — the first child; if hwm = m > 0, then next = inc(cₘ, 0) — the next sibling. No counter distinct from the data, no free list, no reservation table. The cardinality of the existing children is a sufficient statistic for the next allocation.

*Proof.* We must show that for any registry B satisfying B1 and any valid parent-depth pair (p, d), the operationally defined next address equals the (hwm + 1)-th element of the sibling stream S(p, d). Let m = hwm(B, p, d) = #children(B, p, d). By B1 (Contiguous Prefix), children(B, p, d) = {c₁, ..., cₘ} for this m — the first m elements of S(p, d) with no gaps. The argument splits into two cases exhausting the possible values of m.

*Case 1: m = 0.* The children set is empty: children(B, p, d) = ∅. By the definition of next (NextAddress), next(B, p, d) = inc(p, d). By the definition of the sibling stream, c₁ = inc(p, d). Since hwm + 1 = 0 + 1 = 1, the claim c_{hwm+1} = c₁ = inc(p, d) = next(B, p, d) holds.

*Case 2: m ≥ 1.* The children set is non-empty: children(B, p, d) = {c₁, ..., cₘ}. We must identify max(children(B, p, d)). By S0 (StreamOrdering), the sibling stream is strictly increasing: c₁ < c₂ < ... < cₘ under the lexicographic order T1. The maximum of a finite strictly ordered set is its last element, so max(children(B, p, d)) = cₘ. By the definition of next, next(B, p, d) = inc(cₘ, 0). By the recursive clause of the sibling stream definition, c_{m+1} = inc(cₘ, 0). Since hwm + 1 = m + 1, the claim c_{hwm+1} = c_{m+1} = inc(cₘ, 0) = next(B, p, d) holds.

In both cases, next(B, p, d) = c_{hwm(B,p,d) + 1}. The proof depends on B1 to guarantee the contiguous prefix structure (without which the maximum of children need not be the m-th stream element) and on S0 to identify that maximum as cₘ (without which max could be some other element). ∎

*Formal Contract:*
- *Preconditions:* B satisfies B1 for all (p, d); p ∈ T, d ≥ 1; S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).
- *Postconditions:* `next(B, p, d) = c_{hwm(B,p,d) + 1}`.

The substantive wp question targets the invariants themselves. What must hold before a baptism for B1 to hold after? We separate three kinds of condition: the *state precondition* (what must hold of B), the *environmental assumptions* (what the system must enforce around the operation), and the *supporting lemma* (a mathematical property of the stream structure that the wp derivation depends on).

Under B4 (serialized execution within the namespace):

  wp(baptize(p, d), B1) — state precondition: B1; environmental: B0a, B4; lemma: B7.

Let B' = B ∪ {a} where a = next(B, p, d) = c_{hwm+1}. B1 for B' requires two things. First, every previously baptized cₙ in B still has predecessors c₁, ..., c_{n−1} in B' — satisfied because B ⊆ B' (by B0). Second, the new element c_{hwm+1} has predecessors c₁, ..., c_{hwm} in B' — satisfied iff children(B, p, d) = {c₁, ..., c_{hwm}}, which is exactly B1 for the current state. The second condition also requires that no non-baptismal mechanism has altered the namespace — the transition constraint B0a. B4 ensures the baptism observes the complete state left by the previous one.

The freshness derivation similarly:

  wp(baptize(p, d), a ∉ B) — state precondition: B1; environmental: B4; lemma: B7.

The new address c_{hwm+1} must not already appear in B. We partition B into three cases. Within namespace (p, d), B1 ensures children is a contiguous prefix of length hwm, so c_{hwm+1} is the first unbaptized sibling — it cannot be in B ∩ S(p, d). In any other namespace (p', d'), B7 (a mathematical property of the stream structure, not a state predicate) ensures S(p, d) ∩ S(p', d') = ∅, so c_{hwm+1} cannot be in B ∩ S(p', d') either. For elements of B not in any namespace stream — root seed elements such as [1] that have no standard parent (no tumbler p exists with #p + d = #[1] = 1 for valid d) — c_{hwm+1} ∈ S(p, d) by construction, and these elements ∉ S(p, d), so no collision. Together, B1, B7, and the stream membership of c_{hwm+1} guarantee freshness across the full partition of B, with B4 ensuring the state observation is current.

Both derivations reason about a single baptism acting on a known state B. B4 (Namespace Serialization) discharges the serialization assumption: by ensuring that same-namespace baptisms do not interleave, B4 guarantees that each baptism observes the complete state left by the previous one. Without B4, two concurrent baptisms could both read hwm = m, and both wp results would be invalidated.

The simpler observation also holds: wp(baptize(p, d), hwm = N + 1) = (hwm = N). But this merely says "to advance a counter, the counter must be at the previous value" — the definition of counting, not a substantive derivation. The invariant-targeting wp reveals the real dependencies: B1, B0a, B4, and B7 are mutually supporting properties, each required for the others' preservation.

Two systems beginning from the same B₀ and executing the same sequence of baptisms — same parents, same depths, same order — produce identical address spaces. The addresses are not identifiers assigned by fiat; they are the inevitable consequence of the baptism history.

We observe that next is *idempotent in its read*: evaluating next(B, p, d) without committing the result leaves B unchanged, and a second evaluation returns the same answer. The address is consumed by commitment, not by computation. If baptism is aborted after determination but before commitment, no harm is done — the namespace is unchanged, the high water mark is unchanged, the next invocation will compute the same address.

Gregory's implementation confirms this precisely. The query-and-increment function produces a candidate address in a local variable; the candidate exists only as bits in memory. If the function were called twice without an intervening write, both invocations would return the same address — because the persistent tree has not changed and the search would find the same maximum both times. The address enters reality only when the subsequent insertion function writes it into the tree.


## Ghost elements: baptism without content

A baptized position need not contain anything. Nelson names these *ghost elements*:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

A ghost element is "virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." The position is in Σ.B — it has been baptized, it is permanent, it anchors a namespace for children — but nothing is stored at that address.

**B3 (Ghost Validity).** Baptism and content occupation are independent predicates. For any t ∈ T:

  - t ∈ Σ.B ∧ t occupied: a populated position
  - t ∈ Σ.B ∧ t unoccupied: a ghost element (permitted)
  - t ∉ Σ.B: an unbaptized position (not addressable)
  - t ∉ Σ.B ∧ t occupied: **forbidden**

The fourth case is a *requirement on content operations*: any operation that populates a position must have t ∈ Σ.B as a precondition. We do not establish this here — content storage is beyond this ASN's scope. We record the requirement: downstream specifications of content operations must enforce `t ∈ Σ.B` before writing content at t. But the second case is explicitly permitted and common. Structural positions — nodes, users, documents — ordinarily function as ghosts. They exist to organize the namespace, not to carry payload. Their value is the subtree they anchor.

B3 separates two questions that might otherwise be conflated. "Does address t exist?" is answered by Σ.B. "Is there content at t?" is answered by a separate concern (content storage, whose structure is beyond this ASN's scope). The baptismal registry is an existence index, not a content index.


## Atomicity

The baptism process — read the high water mark, compute the next address, commit the result — must not be interleaved with another baptism in the same namespace. If two baptisms both read hwm = m before either commits, both compute c_{m+1} and both attempt to commit the same address — violating B8.

**B4 (Namespace Serialization).** For any two baptisms β₁, β₂ targeting the same namespace (p, d), the commitment of one precedes the computation of the other:

  `(A β₁, β₂ : ns(β₁) = ns(β₂) : commit(β₁) ≺ read(β₂) ∨ commit(β₂) ≺ read(β₁))`

where ≺ denotes temporal precedence.

B4's scope is *per-namespace*: baptisms under different (p, d) pairs need not be serialized with respect to each other, because B7 guarantees their outputs are disjoint. The minimum serialization grain is the namespace, not the entire system. This is precisely what enables decentralized baptism — two agents baptizing under different parents proceed independently, and their addresses are guaranteed distinct by the partition structure of the address space (T10).

Gregory's implementation achieves serialization through single-threaded dispatch — the event loop processes one request to completion before accepting another, and the entire path from query through increment to write runs without yielding control. But B4 is a specification-level requirement, not an implementation prescription. Any mechanism that serializes same-namespace baptisms — locking, transactions, hardware serialization — satisfies B4.


## Depth and field structure

Baptism interacts with the field hierarchy through the depth parameter. Recall from ASN-0034 that zeros(t) — the count of zero-valued components — determines the hierarchical level: 0 for node, 1 for user, 2 for document, 3 for element. When baptism crosses from one level to the next, it must introduce a new zero separator.

**B5 (Field Advancement).** `zeros(inc(p, d)) = zeros(p) + (d − 1)`.

For d = 1: zeros is preserved — the child is at the same hierarchical level. For d = 2: zeros advances by 1 — the child descends one level.

*Proof.* We must show that for a tumbler p and depth d ≥ 1, the zero count of inc(p, d) equals zeros(p) + (d − 1). Let t' = inc(p, d). Since d ≥ 1, TA5(d) applies: t' has length #p + d, with the first #p components preserved from p (TA5(b)), d − 1 zero-valued components at positions #p + 1 through #p + d − 1, and a final component of value 1 at position #p + d.

We partition the components of t' into three ranges and count zeros in each. Positions 1 through #p are identical to the corresponding components of p by TA5(b), contributing exactly zeros(p) zero-valued components. Positions #p + 1 through #p + d − 1 are the field separators introduced by the increment — there are d − 1 of them, each zero-valued, contributing d − 1 zeros. (When d = 1 this range is empty, contributing none; when d = 2 it contains exactly one zero.) Position #p + d holds value 1, contributing no zeros.

Since these three ranges exhaust all #p + d positions of t', the total zero count is zeros(t') = zeros(p) + (d − 1) + 0 = zeros(p) + (d − 1). ∎

*Formal Contract:*
- *Preconditions:* p ∈ T with d ≥ 1. (In the baptismal context, d ∈ {1, 2} by B6(ii).)
- *Postconditions:* `zeros(inc(p, d)) = zeros(p) + (d − 1)`.

B5 establishes the zeros count for the *first* child c₁ of a stream. The sibling stream preserves it:

**B5a (Sibling Zeros Preservation).** `(A t : t_{sig(t)} > 0 : zeros(inc(t, 0)) = zeros(t))`

*Proof.* We must show that for any tumbler t with t_{sig(t)} > 0, the zero count of inc(t, 0) equals zeros(t). Let t' = inc(t, 0). By TA5(c), t' has the same length as t (#t' = #t) and differs from t only at position sig(t), where t'_{sig(t)} = t_{sig(t)} + 1. At every other position, t'_i = t_i.

We count zeros in t' by comparing each component with the corresponding component of t. At every position i ≠ sig(t), t'_i = t_i, so position i is zero-valued in t' exactly when it is zero-valued in t — these positions contribute identically to both zeros(t') and zeros(t). At position sig(t), the precondition gives t_{sig(t)} > 0, so this position contributes no zero to zeros(t). After the increment, t'_{sig(t)} = t_{sig(t)} + 1 ≥ 2 > 0, so this position contributes no zero to zeros(t') either. Since every position contributes identically to both zero counts, zeros(t') = zeros(t). ∎

*Formal Contract:*
- *Preconditions:* t ∈ T with t_{sig(t)} > 0.
- *Postconditions:* `zeros(inc(t, 0)) = zeros(t)`.

To apply B5a inductively across the sibling stream S(p, d), we must discharge its precondition: every cₙ satisfies cₙ_{sig(cₙ)} > 0. For c₁ = inc(p, d), the final component is 1 (from TA5(d)), so sig(c₁) = #c₁ and c₁_{sig(c₁)} = 1 > 0. Each cₙ₊₁ = inc(cₙ, 0) advances the value at sig(cₙ) by 1 (TA5(c)), preserving positivity. By induction, every stream element satisfies the precondition. Combined with B5, every element of S(p, d) inherits the zeros count established at c₁:

  `(A n ≥ 1 : zeros(cₙ) = zeros(p) + (d − 1))`

The B6 validity table below depends on this uniformity — all elements in a stream share the same hierarchical level.

This deserves attention. The `.0.` that appears in addresses like `1.1.0.1.0.1` is not a syntactic convention imposed by a parser — it is a *consequence* of baptism at depth 2. When inc(p, 2) extends p by two components, the first is zero (the field separator, from TA5(d)'s d − 1 = 1 intermediate zero) and the second is 1 (the first child's ordinal). The field structure of tumblers is *produced* by baptism arithmetic.

Gregory's evidence confirms the structural necessity in three independent ways. First, the zero separator is mechanically produced by the depth parameter computed from the type hierarchy — crossing from one hierarchical level to the next always uses d = 2 and therefore always inserts exactly one zero. Second, it is semantically interpreted by the containment operation, which treats zero positions as namespace boundaries during prefix comparison. Third, it is arithmetically essential for allocation: the search-bound and truncation logic depend on measuring the parent's length against the zero boundary. An address produced without the correct zero separators corrupts containment testing and all subsequent baptisms in the affected namespace.

**B6 (Valid Depth).** Baptism at depth d from parent p is valid when:

  (i) p satisfies T4,

  (ii) d ∈ {1, 2}, and

  (iii) zeros(p) + (d − 1) ≤ 3.

Conditions (ii) and (iii) are necessary and sufficient for T4 preservation of the sibling stream, given (i). Condition (ii) follows from the ASN-0034 lemma "TA5 preserves T4": for d ≥ 3, the appended sequence contains adjacent zeros, violating T4's non-empty-field constraint. Condition (iii) ensures no address exceeds the four-level hierarchy. Condition (i) serves a dual role: when the parent has adjacent zeros, the violation propagates to the stream; when the parent ends in zero, the stream may satisfy T4 but coincides with a valid stream from a different parent, collapsing namespace disjointness (B7). All three conditions are jointly necessary for the baptism system to maintain its invariants. Together:

| Parent level | d = 1 (same level) | d = 2 (level crossing) |
|---|---|---|
| Node (zeros = 0) | node child | user child |
| User (zeros = 1) | user child | document child |
| Document (zeros = 2) | sub-document / version | element child |
| Element (zeros = 3) | sub-element | **invalid** |

At most three level crossings can occur in a valid address chain: node → user, user → document, document → element. This is the four-field structure of T4, now visible as a consequence of baptism depth arithmetic rather than an independent syntactic constraint.

*Proof.* We prove sufficiency (all three conditions imply T4 preservation) and then necessity (violating any single condition either produces a T4 violation in the stream or collapses namespace disjointness).

**(⟸) Sufficiency.** Assume (i) p satisfies T4, (ii) d ∈ {1, 2}, and (iii) zeros(p) + (d − 1) ≤ 3. We show every element of S(p, d) satisfies T4.

For the first child c₁ = inc(p, d): the "TA5 preserves T4" lemma (ASN-0034) states that inc(t, k) preserves T4 when t satisfies T4, k ≤ 2, and zeros(t) + (k − 1) ≤ 3. Our three conditions instantiate this exactly with t = p and k = d: p satisfies T4 by (i), d ≤ 2 by (ii), and zeros(p) + (d − 1) ≤ 3 by (iii). Therefore c₁ satisfies T4.

For subsequent siblings cₙ₊₁ = inc(cₙ, 0): the same lemma with k = 0 states that inc(t, 0) preserves T4 unconditionally — no zeros are added and no new adjacencies are introduced, since sibling increment modifies only position sig(t), advancing a positive value by one (TA5(c)). Since c₁ satisfies T4, and each sibling increment preserves T4, by induction every cₙ satisfies T4.

**(⟹) Necessity.** We show that violating any single condition either produces a T4 violation in the stream or collapses an essential system invariant.

*Condition (ii) is necessary for T4.* Let d ≥ 3. By TA5(d), inc(p, d) appends d − 1 ≥ 2 zeros followed by 1. Positions #p + 1 and #p + 2 are both zero — adjacent zeros that parse as two consecutive field separators enclosing an empty field, violating T4's non-empty-field constraint. No choice of p avoids this: the adjacent zeros lie in the appended suffix, independent of p's content.

*Condition (iii) is necessary for T4.* Let zeros(p) + (d − 1) > 3 with d ∈ {1, 2} and p satisfying T4. By B5, zeros(c₁) = zeros(p) + (d − 1) > 3. But T4 requires zeros(t) ≤ 3 for any valid address — at most three field separators for the four-level hierarchy. The first child already exceeds the zero budget, so c₁ violates T4.

*Condition (i) is necessary for the system.* Let p violate T4 with d ∈ {1, 2} and zeros(p) + (d − 1) ≤ 3. Two structurally distinct situations arise, depending on whether the T4 violation lies in the interior of p (positions 1 through #p − 1) or only at the trailing position #p.

*(a) Interior violation: some T4 defect in positions 1 through #p − 1.* This covers adjacent zeros anywhere in p and the leading-zero case p₁ = 0. By TA5(b), inc(p, d) preserves positions 1 through #p, so the defective positions survive into c₁. Each subsequent cₙ₊₁ = inc(cₙ, 0) modifies only position sig(cₙ) = #p + d > #p (since d ≥ 1), leaving positions 1 through #p untouched. By induction, every stream element carries the interior T4 violation. For example, with p = [0, 1, 2] (leading zero, p₁ = 0): c₁ = inc([0, 1, 2], 1) = [0, 1, 2, 1], and (cₙ)₁ = 0 for all n ≥ 1, violating T4's t₁ ≠ 0 requirement.

*(b) Trailing zero as the sole T4 defect: p_{#p} = 0 with no adjacent zeros and p₁ > 0.* The stream may satisfy T4 without condition (i). Consider p = [1, 0] with d = 1. Then c₁ = inc([1, 0], 1) = [1, 0, 1] — one zero at position 2, positive first and last components, no adjacent zeros — and every cₙ = [1, 0, n] satisfies T4. However, S([1, 0], 1) is identical to S([1], 2): both produce the sequence [1, 0, 1], [1, 0, 2], [1, 0, 3], ... (The stream identity is proved in B1's other-namespaces argument below.) In general, when p ends in zero and d = 1, the trailing zero of p merges with the stream structure to produce the same elements as S(p', d + 1) where p' is p with the trailing zero removed — a T4-valid parent at greater depth. Permitting baptism under such a malformed parent creates a namespace whose sibling stream coincides with an existing valid namespace, collapsing B7 (Namespace Disjointness). When d = 2, the trailing zero of p at position #p and the d − 1 = 1 intermediate zero from TA5(d) at position #p + 1 create adjacent zeros, so all stream elements violate T4 — this falls under sub-case (a).

Condition (i) is therefore necessary: interior violations propagate to every stream element, and trailing-zero violations either propagate (when d = 2 creates adjacent zeros) or collapse the namespace partitioning on which global uniqueness (B8) depends (when d = 1). ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1.
- *Postconditions:* (a) Sufficiency: `(p satisfies T4 ∧ d ∈ {1, 2} ∧ zeros(p) + (d − 1) ≤ 3) ⟹ (A n ≥ 1 : cₙ ∈ S(p, d) satisfies T4)`. (b) Necessity: violating (ii) or (iii) produces T4 violations in S(p, d); violating (i) either propagates interior violations (adjacent zeros, leading zero) to every stream element via TA5(b), or — when the sole defect is a trailing zero — produces adjacent zeros for d = 2 (falling under interior violation) or creates a stream identical to some valid S(p', d') for d = 1, collapsing B7.


## Namespace disjointness

Each parent-depth pair defines a namespace. Distinct namespaces must produce non-overlapping address ranges, or global uniqueness collapses.

**B7 (Namespace Disjointness).** For distinct valid pairs (p, d) ≠ (p', d'):

  S(p, d) ∩ S(p', d') = ∅

provided both parents satisfy T4 and both depths satisfy B6.

*Proof.* We must show that for distinct valid pairs (p, d) ≠ (p', d'), where both parents satisfy T4 and both depths satisfy B6, no tumbler belongs to both S(p, d) and S(p', d'). Let a ∈ S(p, d) and b ∈ S(p', d'). We show a ≠ b by exhaustive case analysis on the relationship between the two pairs.

We first establish a uniform length property. Every element of S(p, d) has length #p + d: c₁ = inc(p, d) has length #p + d by TA5(d), and each cₙ₊₁ = inc(cₙ, 0) preserves length by TA5(c). By induction, #cₙ = #p + d for all n ≥ 1. Similarly, every element of S(p', d') has length #p' + d'.

*Case 1: different element lengths.* Suppose #p + d ≠ #p' + d'. Then #a = #p + d ≠ #p' + d' = #b. By T3, tumblers of different lengths are never equal, so a ≠ b.

*Case 2: equal element lengths, non-nesting prefixes.* Suppose #p + d = #p' + d' and neither p ≼ p' nor p' ≼ p. By S1, p ≼ a and p' ≼ b. Since the prefixes are non-nesting, T10 gives a ≠ b.

*Case 3: equal element lengths, nesting prefixes.* Suppose #p + d = #p' + d' and one prefix extends the other — say p ≼ p' without loss of generality (the argument for p' ≼ p is identical with the roles exchanged). Since (p, d) ≠ (p', d') and p ≼ p', either p = p' with d ≠ d', or p is a strict prefix of p'. If p = p' then #p = #p', so #p + d = #p' + d' gives d = d', contradicting d ≠ d'. Therefore p is a strict prefix of p': #p' > #p. From #p + d = #p' + d' we obtain d − d' = #p' − #p > 0, so d > d'. Since d, d' ∈ {1, 2} by B6(ii), the constraint d > d' forces d = 2 and d' = 1, whence #p' = #p + 1.

We show the two streams disagree at position #p + 1 for every pair of elements. For an arbitrary cₙ ∈ S(p, 2): at c₁ = inc(p, 2), TA5(d) places d − 1 = 1 zero-valued component at position #p + 1, so (c₁)_{#p+1} = 0. Each subsequent cₙ₊₁ = inc(cₙ, 0) modifies only position sig(cₙ). Since sig(c₁) = #c₁ = #p + 2 (the last component has value 1, hence is the rightmost nonzero position), and each sibling increment preserves length and advances only position sig(cₙ) by TA5(c), we have sig(cₙ) = #p + 2 for all n ≥ 1. Because #p + 2 ≠ #p + 1, position #p + 1 is never modified. By induction on n, (cₙ)_{#p+1} = 0 for all n ≥ 1.

For an arbitrary c'ₘ ∈ S(p', 1): by S1, p' ≼ c'ₘ, so (c'ₘ)_i = p'_i for all 1 ≤ i ≤ #p'. In particular, (c'ₘ)_{#p+1} = p'_{#p+1}. Since #p + 1 = #p', this is the last component of p'. By T4, valid addresses do not end in zero, so p'_{#p'} > 0. Therefore (c'ₘ)_{#p+1} = p'_{#p+1} > 0 for all m ≥ 1.

At position #p + 1, every element of S(p, 2) has value 0 and every element of S(p', 1) has a value greater than 0. By T3, tumblers that differ at any position are distinct, so a ≠ b.

The three cases are exhaustive: for any two streams, the element lengths are either different (Case 1), equal with non-nesting prefixes (Case 2), or equal with nesting prefixes (Case 3). In every case a ≠ b, so S(p, d) ∩ S(p', d') = ∅. ∎

*Formal Contract:*
- *Preconditions:* (p, d) ≠ (p', d') with p, p' satisfying T4 and d, d' satisfying B6.
- *Postconditions:* `S(p, d) ∩ S(p', d') = ∅`.


## A baptism traced

We trace a concrete sequence to ground the formal development. Begin with B₀ = {[1]} — a single root node. We verify B₀ conformance. First, [1] satisfies T4: a single positive component, no zeros. Second, [1] does not belong to any sibling stream — membership in S(p, d) requires element length #p + d, and no valid parent p with d ∈ {1, 2} satisfies #p + d = 1 (since #p ≥ 1). Therefore children(B₀, p, d) = ∅ for all (p, d), which is trivially a contiguous prefix of length 0. The seed is conforming.

**Step 1: first user.** Namespace ([1], 2) — node [1], depth 2 (level crossing to user).

  next(B₀, [1], 2) = inc([1], 2) = [1, 0, 1]

TA5(d) appends d − 1 = 1 zero separator and child value 1. B5: zeros([1, 0, 1]) = 1 = 0 + (2 − 1). B6: d = 2 and zeros([1]) + 1 = 1 ≤ 3. B1: children = {[1, 0, 1]}, a prefix of length 1.

State: B₁ = {[1], [1, 0, 1]}.

**Step 2: second user.** Same namespace ([1], 2).

  next(B₁, [1], 2) = inc([1, 0, 1], 0) = [1, 0, 2]

TA5(c): sibling increment preserves length, advances position sig([1, 0, 1]) = 3, so the ordinal goes from 1 to 2. B5a: zeros([1, 0, 2]) = 1 = zeros([1, 0, 1]) — sibling preserves zeros. B1: children = {[1, 0, 1], [1, 0, 2]}, a prefix of length 2.

State: B₂ = {[1], [1, 0, 1], [1, 0, 2]}.

**Step 3: document under first user.** Namespace ([1, 0, 1], 2) — user [1, 0, 1], depth 2 (level crossing to document).

  next(B₂, [1, 0, 1], 2) = inc([1, 0, 1], 2) = [1, 0, 1, 0, 1]

B5: zeros([1, 0, 1, 0, 1]) = 2 = 1 + (2 − 1). B6: d = 2 and zeros([1, 0, 1]) + 1 = 2 ≤ 3. B1: children = {[1, 0, 1, 0, 1]}, a prefix of length 1. B7: S([1], 2) elements have length 3; S([1, 0, 1], 2) elements have length 5 — Case 1 disjointness.

State: B₃ = {[1], [1, 0, 1], [1, 0, 2], [1, 0, 1, 0, 1]}.

Nelson's "Items 2.1, 2.2, 2.3, 2.4" is exactly this mechanism — successive baptisms under parent 2 at depth 1, yielding the sibling stream 2.1, 2.2, 2.3, 2.4 by repeated application of inc(·, 0). The sequence is determined, contiguous, and the ordinals carry no semantics beyond order.

**B7 Case 3 verified.** The steps above exercise only Case 1 of B7 (different stream lengths). We now trace Case 3 — nesting prefixes with equal element lengths. Suppose node [1, 1] has been baptized via inc([1], 1) = [1, 1] (TA5(d) with k = 1: #t' = 2, zero intermediate zeros, position 2 set to 1). Consider S([1], 2) and S([1, 1], 1). Both streams have element length 3: #[1] + 2 = #[1, 1] + 1 = 3. The prefixes nest — [1] ≼ [1, 1] — so this is Case 3 with p = [1], d = 2, p' = [1, 1], d' = 1.

At position 2 of each stream: inc([1], 2) = [1, 0, 1] — the value at position 2 is 0, the zero separator produced by TA5(d) with d − 1 = 1 intermediate zero. inc([1, 1], 1) = [1, 1, 1] — the value at position 2 is p'₂ = 1 > 0 (by T4, valid addresses do not end in zero, so the last component of [1, 1] is positive). Sibling increments inc(·, 0) modify only the last component (TA5(c)), so position 2 is invariant across both streams: always 0 in S([1], 2), always 1 in S([1, 1], 1). The streams disagree at a fixed position and are therefore disjoint.


## Global uniqueness

**B8 (Global Uniqueness).** Distinct baptisms produce distinct addresses:

  `(A a, b : produced by distinct baptismal acts : a ≠ b)`.

Within the same namespace, B4 ensures each baptism observes a distinct hwm value — serialization prevents two baptisms from reading the same maximum — and B1 ensures sequential, gap-free allocation, so distinct baptisms produce distinct stream indices, which S0 maps to distinct addresses. Across namespaces, B7 ensures non-overlapping ranges. Together, no two baptisms anywhere in the system, at any time, produce the same tumbler.

ASN-0034 establishes GlobalUniqueness from the algebraic angle through T3, T9, T10, and T10a. Here we reach the same conclusion through the set-theoretic lens of baptism namespaces and the contiguous prefix property. The two derivations are complementary: the algebraic route proceeds from allocator discipline (per-stream monotonicity), while the set-theoretic route proceeds from namespace partitioning (per-stream contiguity plus cross-stream disjointness). The algebraic route answers "why is each stream collision-free?"; the set-theoretic route answers "why are different streams collision-free with each other?"

*Proof.* We must show that for any two distinct baptismal acts β₁ and β₂, the addresses they produce are distinct. Let a be the address produced by β₁ in namespace (p, d), and b the address produced by β₂ in namespace (p', d'). We proceed by case analysis on whether the two baptisms target the same or different namespaces.

*Case 1: same namespace — (p, d) = (p', d').* By B4 (Namespace Serialization), same-namespace baptisms are serialized: commit(β₁) ≺ read(β₂) or commit(β₂) ≺ read(β₁). Assume without loss of generality that commit(β₁) ≺ read(β₂) — the argument with roles exchanged is identical. Let Σ₁ be the state observed by β₁ and Σ₂ the state observed by β₂. Since β₁ commits before β₂ reads, β₁'s output a is in Σ₂.B by B0 (Irrevocability): Σ₁.B ⊆ Σ₂.B and a ∈ Σ₂.B.

Let m₁ = hwm(Σ₁.B, p, d) and m₂ = hwm(Σ₂.B, p, d). By B2 (High Water Mark Sufficiency), a = c_{m₁+1} and b = c_{m₂+1}, where cₙ denotes the n-th element of S(p, d). Since a = c_{m₁+1} ∈ Σ₂.B and B1 (Contiguous Prefix) holds for Σ₂, the children of (p, d) in Σ₂ include {c₁, ..., c_{m₁+1}}, so hwm(Σ₂.B, p, d) ≥ m₁ + 1. That is, m₂ ≥ m₁ + 1, hence m₂ + 1 ≥ m₁ + 2 > m₁ + 1. The indices m₁ + 1 and m₂ + 1 are distinct with m₁ + 1 < m₂ + 1. By S0 (StreamOrdering), c_{m₁+1} < c_{m₂+1} under the lexicographic order T1. By T1 irreflexivity, c_{m₁+1} ≠ c_{m₂+1}. Therefore a ≠ b.

*Case 2: different namespaces — (p, d) ≠ (p', d').* By construction, a ∈ S(p, d) — baptism in namespace (p, d) produces the next element of its sibling stream — and b ∈ S(p', d') by the same reasoning. By B7 (Namespace Disjointness), S(p, d) ∩ S(p', d') = ∅, so a ≠ b.

The two cases are exhaustive: two baptisms either target the same namespace or they do not. In both cases a ≠ b. No two distinct baptisms, whether in the same namespace, across sibling namespaces, or at different hierarchical levels, can produce the same address. ∎

*Formal Contract:*
- *Preconditions:* β₁, β₂ are distinct baptismal acts in a system conforming to B0, B0a, B1, B4, and B7; β₁ produces a in namespace (p, d) and β₂ produces b in namespace (p', d'), where both (p, d) and (p', d') satisfy B6.
- *Postconditions:* `a ≠ b`.


## Unbounded growth

Nelson insists that the address space imposes no capacity limits:

> "A tumbler consists of a series of integers. Each integer has no upper limit."

**B9 (Unbounded Extent).** `(A p ∈ Σ.B, d satisfying B6, M ∈ ℕ : (E B' : B' reachable from B by a finite sequence of baptisms : hwm(B', p, d) ≥ M))`.

No architectural limit constrains how many children a position may have. This follows from T0(a) (UnboundedComponents): since each tumbler component is an unbounded natural number and the child ordinal occupies a single component, the ordinal can grow without bound. Combined with B1, the children of any parent can grow to form an arbitrarily long contiguous prefix {c₁, ..., cₘ} for any m.

Nelson designed this deliberately: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — the process of baptism never exhausts any namespace. Between physical resource limits and address space design, there is a deliberate gap: the design guarantees infinite headroom, leaving capacity as a pure engineering concern.

Nelson reinforces this at every level: "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." The word "possible" does not mean "a finite number of possible" — it means the tree can always grow further. The address space is designed not for a known population but for indefinite proliferation.

*Proof.* We must show that for any baptized parent p ∈ Σ.B, depth d satisfying B6, and bound M ∈ ℕ, there exists a registry B' reachable from Σ.B by a finite sequence of baptisms such that hwm(B', p, d) ≥ M. The argument is constructive: we exhibit the required sequence of baptisms.

Let m = hwm(Σ.B, p, d) — the current count of children in namespace (p, d). If m ≥ M, set B' = Σ.B and the claim holds trivially. Otherwise m < M, and we construct a sequence of M − m baptisms, each targeting namespace (p, d). We show by induction on k that k successive baptisms produce a registry Bₖ with hwm(Bₖ, p, d) = m + k.

*Base case (k = 0).* B₀ = Σ.B with hwm(Σ.B, p, d) = m = m + 0. The claim holds.

*Inductive step.* Assume Bₖ is a registry reachable from Σ.B by k baptisms in namespace (p, d), with hwm(Bₖ, p, d) = m + k < M. We perform baptize(p, d) on state Bₖ. The preconditions of Bop are satisfied: B6(p, d) holds by hypothesis; B4 (Namespace Serialization) holds because the baptisms execute sequentially — each commitment precedes the next computation.

By Bop, the postcondition gives B_{k+1} = Bₖ ∪ {next(Bₖ, p, d)}. By B2 (High Water Mark Sufficiency), next(Bₖ, p, d) = c_{m+k+1}, the (m + k + 1)-th element of the sibling stream S(p, d). This element is well-defined: the stream S(p, d) produces cₙ for every n ≥ 1, since c₁ = inc(p, d) ∈ T by TA5(d), and each cₙ₊₁ = inc(cₙ, 0) ∈ T by TA5(c). The final component of cₙ equals n — a value that grows without bound. That no ceiling constrains this component is precisely T0(a) (UnboundedComponentValues): for any bound M' ∈ ℕ, there exists a tumbler in T whose value at that position exceeds M'. The stream never exhausts its namespace.

The new element c_{m+k+1} is fresh — by the freshness argument of Bop, it does not appear in Bₖ. The contiguous prefix property is preserved — by B1 preservation under Bop, children(B_{k+1}, p, d) = {c₁, ..., c_{m+k+1}}. Therefore hwm(B_{k+1}, p, d) = m + k + 1.

After M − m steps, hwm(B_{M−m}, p, d) = m + (M − m) = M. Setting B' = B_{M−m}, we have B' reachable from Σ.B by a finite sequence of M − m baptisms, and hwm(B', p, d) = M ≥ M. ∎

*Formal Contract:*
- *Preconditions:* p ∈ Σ.B, d satisfying B6(p, d), M ∈ ℕ.
- *Postconditions:* There exists B' reachable from Σ.B by a finite sequence of baptisms such that hwm(B', p, d) ≥ M.
- *Axiom:* T0(a) — component values in T are unbounded; ℕ is closed under successor.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.B | B ⊆ T — the set of baptized tumblers (baptismal registry) | introduced |
| S(p,d) | Sibling stream: c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0) | from TA5(b), TA5(c), TA5(d) |
| hwm(B,p,d) | High water mark: #children(B, p, d) — sufficient allocation statistic | from B1, S0 |
| next(B,p,d) | Next address: if children = ∅ then inc(p, d) else inc(max(children), 0) | from TA5(c), TA5(d), T1 |
| Bop | baptize(p, d): PRE B6, B4; POST Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}; FRAME only Σ.B | from B0, B1, B4, B6, B7, B0a, B10, TA5, TA5a |
| S0 | `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — stream strictly ordered | from TA5(a), T1 |
| S1 | `(A n : n ≥ 1 : p ≼ cₙ)` — all stream elements extend parent | from TA5(b), TA5(c), TA5(d) |
| B0 | `Σ.B ⊆ Σ'.B` for all transitions — irrevocability (extends T8) | design requirement |
| B0a | `Σ'.B \ Σ.B ⊆ {baptism(p,d) outputs for (p,d) satisfying B6}` — registry grows only through baptism | design requirement |
| B₀ conf. | B₀ is non-empty and finite, `children(B₀, p, d)` is a contiguous prefix for all (p, d), and `(A t ∈ B₀ : t satisfies T4)` — seed conformance | design requirement |
| B1 | `cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B)` — contiguous prefix (requires conforming B₀) | from B₀ conf., B0, B0a, B4, B7, B10, Bop, S0, TA5(c) |
| B2 | `next(B, p, d) = c_{hwm+1}` — high water mark sufficiency (from B1) | from B1, S0, NextAddress |
| B3 | `t ∈ Σ.B` does not imply t is occupied — ghost validity | design requirement |
| B4 | Same-namespace baptisms serialized: `commit(β₁) ≺ read(β₂) ∨ commit(β₂) ≺ read(β₁)` | design requirement |
| B5 | `zeros(inc(p, d)) = zeros(p) + (d − 1)` — field advancement | from TA5(b), TA5(d) |
| B5a | `zeros(inc(t, 0)) = zeros(t)` — sibling increment preserves zeros | from TA5(c) |
| B6 | `p satisfies T4`, `d ∈ {1, 2}`, and `zeros(p) + (d − 1) ≤ 3` — valid depth | from T4, TA5, B5 |
| B7 | `(p, d) ≠ (p', d') ⟹ S(p, d) ∩ S(p', d') = ∅` — namespace disjointness | from T3, T4, T10, S1, TA5(c), TA5(d), B6 |
| B8 | Distinct baptisms produce distinct addresses — global uniqueness | from B0, B1, B2, B4, B7, S0, T1 |
| B9 | `(A p, d, M : (E B' reachable : hwm(B', p, d) ≥ M))` — unbounded extent | from T0(a), B1, B2, B4, B6, Bop, TA5(c), TA5(d) |
| B10 | `(A t ∈ Σ.B : t satisfies T4)` — registry-wide T4 validity | from B₀ conf., B0a, B1, B2, B6, TA5(c), TA5a |


## Open Questions

- Must a parent position be baptized before children can be baptized beneath it? Nelson's ownership model implies yes; Gregory's implementation does not check at structural levels. Resolution depends on the ownership model (Tumbler Ownership).
- What concrete seed sets B₀ are valid — which root configurations satisfy B₀ conformance while providing a viable system genesis?
- Must the specification distinguish between a ghost element that could hold content and a structural position that cannot — or is this distinction derivable from the field structure alone?
- Under what conditions may bulk allocation — baptizing a contiguous range of k positions in a single operation — satisfy B4's atomicity and B1's contiguity requirements?
- What must a distributed system guarantee about cross-replica baptism ordering to maintain global address uniqueness without centralized coordination?
- Does the abstract specification require a single canonical depth d for each parent level, or may a parent simultaneously baptize children at both d = 1 and d = 2?
- What is the minimal serialization grain for baptism — must operations be serialized per-parent per-depth, or per-parent across all depths?
- What invariants must element-level subspace partitioning (T7) satisfy so that the contiguous prefix property holds independently within each subspace?
