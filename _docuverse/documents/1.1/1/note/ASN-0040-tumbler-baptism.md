# ASN-0040: Tumbler Baptism

*2026-03-15*

We seek to understand what it means for a position to enter the tumbler hierarchy. The algebra (ASN-0034) gives us an infinite space of well-formed addresses — ordered by T1, structured into fields by T4, permanently allocated by T8, strictly increasing by T9. But the algebra cannot distinguish between a position that *has been assigned* and one that merely *could be*. Something marks the transition from arithmetic possibility to system fact.

Nelson calls this transition *baptism*:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers."

Three observations are compressed into that sentence. Baptism is *hierarchical* — it descends level by level through the field structure. Baptism is *sequential* — Nelson elsewhere describes creation as "successive new digits to the right," emphasizing that positions arrive in order, not arbitrarily. And baptism is *permanent* — "Any address, once assigned, remains valid forever." We defer the authorization aspect (who may baptize) to a future ASN on tumbler authorization. Here we characterize the structural mechanism: how the set of baptized positions grows, and what it preserves as it grows.

Gregory's implementation reveals the operational anatomy. Baptism is a two-phase process: first, the system queries the existing address space for the highest allocated position under a given parent prefix and increments to produce a candidate; second, it writes that candidate into the persistent store. The write — not the query — is the moment of baptism. A candidate computed but never written does not exist; if the query were repeated without an intervening write, it would return the same candidate. The address becomes real at the instant of commitment.

We formalize baptism as the growth law of the address space.


## State space and transitions

Before introducing the baptismal registry, we fix the ambient framework so that subsequent obligations of the form `(A Σ, Σ' : Σ → Σ' : …)` and "in every state reachable from Σ_init" carry precise meaning. The framework is conventional Kripke-style: a carrier of states, a vocabulary of operations, and the resulting transition relation. We will instantiate Σ.B as one component of the state and B0/B0a/B4 as constraints on the transitions.

**State space.** Let 𝒮 denote the state space of the tumbler-baptism system. A *state* Σ ∈ 𝒮 is a tuple of system data. The present ASN introduces one component — the baptismal registry Σ.B (defined below) — and makes no commitment about what other components Σ carries. Future ASNs (content storage, link structure, ownership) extend the tuple with additional components; the frame condition stated at Bop ensures those extensions remain orthogonal to Σ.B.

**Transition vocabulary.** Let Op denote the system's transition vocabulary. Each `op ∈ Op` is a partial function `op : 𝒮 ⇀ 𝒮`; the predicate `op(Σ) defined` abbreviates `Σ ∈ dom(op)`. A *transition* `Σ → Σ'` is the pair `(Σ, op(Σ))` with `op ∈ Op` and `Σ ∈ dom(op)`. The present ASN constrains Op's treatment of the Σ.B component (B0, B0a, B4) but does not exhaustively enumerate Op — content operations, link operations, and other future additions are admitted, subject to those constraints.

**Reachability.** Reachability is the reflexive-transitive closure of →: a state Σ' is *reachable from* Σ when there exists a finite sequence of states τ₀, τ₁, …, τₙ with τ₀ = Σ, τₙ = Σ', and `τᵢ → τᵢ₊₁` for every `0 ≤ i < n` (the case n = 0 gives reflexivity). The *initial state* Σ_init ∈ 𝒮 has Σ_init.B = B₀, the seed set established at system genesis. When we write "in every reachable state" without qualification, we mean reachable from Σ_init.

**Quantifier conventions.** `(A Σ, Σ' : Σ → Σ' : P(Σ, Σ'))` is a constraint on every admissible transition: for every `op ∈ Op` and `Σ ∈ dom(op)`, the pair `(Σ, op(Σ))` satisfies P. `(A Σ : Σ reachable from Σ_init : I(Σ))` is a state invariant: I holds in every reachable state. Bare `Σ.B` in an expression refers to the registry component of the implicit current state; bare `Σ'.B` to that of the successor state across a transition.

This is the same Kripke framework fixed by ASN-0034's AllocatedSet, re-lettered: ASN-0034's Σ (vocabulary) and s (state) are written Op and Σ here. The relationship between Σ.B and ASN-0034's `allocated(s)` is articulated below at the introduction of Σ.B.


## The baptismal registry

We introduce the central state component:

**Σ.B (BaptismalRegistry).** Σ.B ⊆ T — the set of baptized tumblers.

A tumbler t is *baptized* iff t ∈ Σ.B. Initially Σ.B contains a finite seed set B₀ ⊆ T of root addresses established at system genesis, subject to the conformance requirement stated at B₀ conf. below. Whether B₀ is empty is not a free parameter at the registry layer: the activation-discipline ASN is obligated, through Bridge2 (`allocated(Σ_init) ⊆ B₀`, stated below), to admit every initially-realized allocator address into B₀, and ASN-0034 fixes `allocated(s₀) = {t₀}` — so any activation discipline conforming to ASN-0034 forces t₀ ∈ B₀ and hence B₀ ≠ ∅. The "finite seed set" license therefore covers every conforming choice but not the empty seed; B₀ conf. below states only the structural conditions on B₀, leaving the precise composition (and, by composition with Bridge2, the non-emptiness obligation) to the activation-discipline ASN. Thereafter it grows monotonically:

The set-membership constraint `Σ.B ⊆ T` is not a free design stipulation: it is preserved by base case (B₀ conf. forces the seed into T) and by every transition class (B0a's partition). We record this preservation as a labelled invariant rather than as informal commentary, since later proofs (B10, B1, B8) appeal to `t ∈ Σ.B ⟹ t ∈ T` as a structural fact and the label makes the citation explicit:

**B_type (RegistryTyping).** `(A Σ : Σ reachable from Σ_init : Σ.B ⊆ T)` — every baptized address is a well-formed tumbler.

*Proof.* By induction on the number of state transitions from the initial state. Case 2 of the inductive step selects max(children(B, p, d)), whose existence requires children to be a finite set — supplied by B_fin (Registry Finiteness), proved independently below as a standalone induction over B0a's partition that appeals to nothing from B_type.

*Base case.* In the initial state, Σ.B = B₀. By B₀ conf. (SeedConformance), every t ∈ B₀ satisfies T4; T4 is a property of well-formed tumblers (T4 ranges over T by definition in ASN-0034), so every t ∈ B₀ inhabits T. B_type holds at genesis.

*Inductive step.* Assume B_type holds for state Σ with registry B — that is, B ⊆ T; B_fin gives B finite. Consider a transition Σ → Σ' producing registry B'. By B0a (Baptismal Closure), Op partitions into Σ.B-frame operations and baptismal operations; we treat the two transition classes in turn.

*Σ.B-frame transitions.* If the transition is induced by a Σ.B-frame operation, then Σ'.B = Σ.B — that is, B' = B. Therefore B' = B ⊆ T by the inductive hypothesis, and B_type holds at B'.

*Baptismal transitions.* Otherwise the transition is induced by a baptismal operation baptize(p, d) for some (p, d) satisfying B6, so B' = B ∪ {a} where a = next(B, p, d). For elements t ∈ B, the inductive hypothesis gives t ∈ T directly. It remains to show the new element a inhabits T. By the definition of next, a branches on whether children(B, p, d) is empty.

  - *Case 1: children(B, p, d) = ∅.* Then a = inc(p, d). By B6(i), p satisfies T4 and hence p ∈ T. By B6(ii), d ∈ {1, 2} so d ≥ 1. TA5's first postcondition (the unlabeled `t' ∈ T`, ASN-0034) gives `inc(p, d) ∈ T` for any p ∈ T and d ≥ 1. Therefore a ∈ T.

  - *Case 2: children(B, p, d) ≠ ∅.* Then a = inc(cₘ, 0) where cₘ = max(children(B, p, d)). The maximum exists because B is finite (B_fin) and children(B, p, d) ⊆ B is a non-empty finite subset of T totally ordered by T1. By the inductive hypothesis, cₘ ∈ B ⊆ T. TA5's first (unlabeled) postcondition (ASN-0034) gives `inc(cₘ, 0) ∈ T` for any cₘ ∈ T. Therefore a ∈ T.

In both cases a ∈ T, so B' = B ∪ {a} ⊆ T. B_type holds at B' under baptismal transitions, and by the frame argument above it holds at B' under Σ.B-frame transitions. By induction on the transition sequence, B_type holds in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A Σ : Σ reachable from Σ_init : Σ.B ⊆ T)`.
- *Base:* B₀ conf. — every seed element satisfies T4 and hence inhabits T.
- *Preservation:* B0a partitions Op; Σ.B-frame transitions leave Σ.B unchanged; baptismal transitions add `next(Σ.B, p, d)`, which inhabits T by TA5's first postcondition `t' ∈ T` — applied to the inc(p, d) form covered by TA5(d) on the empty-namespace branch (with B6(i) supplying p ∈ T and B6(ii) supplying d ≥ 1) and to the inc(cₘ, 0) form covered by TA5(c) on the non-empty branch (with the inductive hypothesis and B_fin supplying a T-valued cₘ).

B_type is the typing skeleton on which B10 builds: B_type says baptized addresses are *well-formed* tumblers (in T), and B10 sharpens this to say they additionally satisfy *T4* — the field-separator constraint. The two invariants are independent in principle (T is the carrier of the algebra; T4 is a structural predicate over T), but in practice every reachable registry satisfies both, established by parallel inductions citing the same base case (B₀ conf.) and the same case analysis on B0a's partition.

*Relationship to ASN-0034's allocated set.* The registry Σ.B and ASN-0034's `allocated(Σ)` denote closely related sets, viewed through two complementary lenses. ASN-0034 defines `allocated(Σ) = ⋃ { domₛ(A) : activated(A, Σ) }` — the union, over all activated allocators in Σ, of the addresses each has realized. ASN-0040 defines Σ.B as the set of addresses that have been baptized (including any present in the seed set B₀). One inclusion holds, given a bridge between the two ASNs' transition vocabularies:

  `allocated(Σ) ⊆ Σ.B`

The bridge has two parts, each an obligation across the two ASNs rather than a theorem of either alone. Both are forward requirements on the activation-discipline ASN (where allocator activation will be specified), parallel in status to B3's forward requirement on content storage: neither is a current invariant of ASN-0040 or ASN-0034 in isolation, and each is the hand-forward obligation under which the registry–allocator alignment becomes provable.

**Bridge1 (Allocator–Baptism Correspondence — forward requirement on activation discipline).** Every allocator-extension transition is realized by a *unique* baptismal operation that adds the same address to Σ.B:

  `(A Σ, Σ', A, a : Σ → Σ' ∧ a ∈ domₛ'(A) ∖ domₛ(A) : (E! (p, d) satisfying B6 : Σ' = baptize(p, d)(Σ) ∧ a = next(Σ.B, p, d)))`

— for every transition Σ → Σ' and every address a freshly added to the realized domain of some allocator A across that transition (`a ∈ domₛ'(A) ∖ domₛ(A)`, with the subscripts s and s' denoting states Σ and Σ'), there exists a *unique* (p, d) satisfying B6 such that the successor state is exactly the result of applying `baptize(p, d) ∈ Op` to Σ (`Σ' = baptize(p, d)(Σ)`) and a equals the address `next(Σ.B, p, d)` that B0a's baptismal branch adds to Σ.B. The equation `Σ' = baptize(p, d)(Σ)` discharges the *State Space and Transitions* obligation that every Σ → Σ' have a single witnessing `op ∈ Op` with Σ' = op(Σ); no informal "induced by" relation is invoked. The converse — that every baptismal operation is an allocator extension — is the reverse inclusion, conditional below and not part of Bridge1.

*Uniqueness proof.* Suppose (p, d) and (p', d') both satisfy B6 and both witness the existential — that is, a = next(Σ.B, p, d) and a = next(Σ.B, p', d'). By the definition of next (NextAddress), next(Σ.B, p, d) ∈ S(p, d) and next(Σ.B, p', d') ∈ S(p', d'), so a ∈ S(p, d) ∩ S(p', d'). By B7 (Namespace Disjointness), `(p, d) ≠ (p', d') ⟹ S(p, d) ∩ S(p', d') = ∅`. Since a sits in both streams, the intersection is non-empty, so the contrapositive of B7 gives (p, d) = (p', d'). ∎

**Bridge2 (Genesis Coverage — forward requirement on activation discipline).** Every address inhabiting an activated allocator's domain at system genesis is a seed element of the baptismal registry:

  `allocated(Σ_init) ⊆ B₀`

This is not a consequence of B₀ conf., which stipulates only finiteness, contiguity, and T4 for the seed; nor is it a consequence of ASN-0034 in isolation, which fixes `allocated(s₀)` but does not name B₀. The activation-discipline ASN must arrange the alignment by constraining which allocators are activated at genesis and how their initial domains relate to the seed set chosen for ASN-0040.

Under Bridge1 and Bridge2, the inclusion `allocated(Σ) ⊆ Σ.B` is preserved at every transition. ASN-0034's non-extending transitions leave `allocated` fixed; allocator extensions, by Bridge1, are baptismal operations that add the same element to both sets; B0a forbids any non-baptismal enlargement of Σ.B, so Σ.B never grows in a way that would let `allocated` outpace it. Iterating across a finite transition sequence from genesis, the registry side of the inclusion is non-contracting by B0★ (Multi-step Irrevocability) and the allocator side is non-contracting by T8 (AllocationPermanence) extended along the same sequence; both directions remain monotone, so the per-transition preservation argument lifts to every reachable state. By induction from genesis (with Bridge2 securing the base case `allocated(Σ_init) ⊆ Σ_init.B`, since `B₀ ⊆ Σ_init.B`), `allocated(Σ) ⊆ Σ.B` in every reachable state. Without either bridge requirement, the inclusion is unjustified.

The reverse inclusion `Σ.B ⊆ allocated(Σ)` holds only under enforcement of the parent prerequisite — whether a parent must be baptized before children — which is deferred to the Open Questions.

B0 follows from B0a: the partition forces `op(Σ).B = Σ.B ∪ {next(Σ.B, p, d)}` in the baptismal branch and `op(Σ).B = Σ.B` in the Σ.B-frame branch, so `Σ.B ⊆ op(Σ).B` in both, hence `Σ.B ⊆ Σ'.B` for every transition. We state it as a labelled primitive because it is the registry analogue of T8 (AllocationPermanence), cited as such by the inductive proofs of B1 and B10.

**B0 (Irrevocability).** `(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`.

No operation removes a tumbler from B. This is the state-level reading of T8 (AllocationPermanence). T8 says the allocator never reclaims an address; B0 says the *registry* never shrinks. The distinction matters: B0 forbids any mechanism — not just the allocator — from removing a baptized position. Administrative action, garbage collection, storage failure — none may contract B. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid."

B0 is a single-step law. We extend it to finite transition sequences:

**B0★ (Multi-step Irrevocability — corollary of B0).** `(A Σ, Σ' : Σ →* Σ' : Σ.B ⊆ Σ'.B)`, where Σ →* Σ' denotes the reflexive-transitive closure of the transition relation — that is, Σ' is reachable from Σ by a finite (possibly empty) sequence of transitions.

*Proof.* By induction on the length k of the transition sequence witnessing Σ →* Σ'. *Base case (k = 0).* Σ' = Σ, so Σ.B ⊆ Σ'.B = Σ.B by reflexivity of ⊆. *Inductive step.* Suppose Σ →* Σₖ is witnessed by a length-k sequence with Σ.B ⊆ Σₖ.B (inductive hypothesis), and Σₖ → Σₖ₊₁ extends it to a length-(k+1) sequence Σ →* Σₖ₊₁. By B0 applied to the single-step transition Σₖ → Σₖ₊₁, Σₖ.B ⊆ Σₖ₊₁.B. Transitivity of ⊆ gives Σ.B ⊆ Σₖ.B ⊆ Σₖ₊₁.B, so Σ.B ⊆ Σₖ₊₁.B. By induction, Σ.B ⊆ Σ'.B for every Σ →* Σ'. ∎

B0 tells us baptism cannot be undone; its companion tells us what *can* add to B. We state the closure law directly on the operation vocabulary Op rather than on an opaque predicate "produced by baptism":

**B0a (Baptismal Closure).** Op partitions into two classes whose treatment of the Σ.B component is fixed:

  - *Baptismal operations.* For each (p, d) satisfying B6, `baptize(p, d) ∈ Op` is the operation specified by Bop below; its action on the registry is `op(Σ).B = Σ.B ∪ {next(Σ.B, p, d)}`.
  - *Σ.B-frame operations.* Every other `op ∈ Op` preserves the registry: `(A op ∈ Op \ {baptize(p, d) : B6(p, d)}, Σ ∈ dom(op) : op(Σ).B = Σ.B)`.

The two classes are disjoint by behavioral construction: membership in each class is fixed by an explicit identity criterion on the operation symbol — the baptismal class is the named family `{baptize(p, d) : B6(p, d)}`, and the Σ.B-frame class is its complement in Op — so each `op ∈ Op` belongs to exactly one class by definition. This disjointness is logically prior to, and independent of, Bop's freshness proof: Bop establishes that `next(Σ.B, p, d) ∉ Σ.B` and hence that a baptismal operation strictly enlarges Σ.B by one element, but the partition itself stands even before that proof — by construction of the two class-defining predicates rather than by their distinct extensional effects.

Equivalently, `(A Σ, Σ' : Σ → Σ' : Σ'.B = Σ.B ∨ (E (p, d) : B6(p, d) : Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}))` — every transition either leaves the registry unchanged or extends it by exactly the address that the corresponding baptismal operation would produce. The parenthesization of the existential is load-bearing: `(p, d)` is bound by the inner quantifier ranging over the B6-valid namespace, not free in the surrounding `(A Σ, Σ' : …)`, so the equation `Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}` makes sense only inside the existential's scope. The equivalence rests on the *State Space and Transitions* section's definition of transition: every `Σ → Σ'` is of the form `(Σ, op(Σ))` for some `op ∈ Op`, so a partition of Op into baptismal and Σ.B-frame classes induces a partition of transitions over the same two alternatives.

Here "satisfying B6" means p satisfies T4, d ∈ {1, 2}, and zeros(p) + (d − 1) ≤ 3 — depth validity as defined below. Whether p must itself be baptized (p ∈ Σ.B) before children can be baptized beneath it is deliberately deferred to the Open Questions; B0a constrains only the depth arithmetic, not the authorization chain. The closure is structural: there is no operation symbol in Op outside the baptismal class that touches Σ.B. Administrative actions, content writes, link operations, ownership transfers — these are members of the Σ.B-frame class by construction and so leave the registry exactly intact. B0 says nothing leaves; B0a says nothing enters except through the designated gate. Without B0a, an arbitrary operation could insert c₅ into a namespace lacking c₁ through c₄, and the contiguous prefix property (B1 below) would be violated.

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

*Proof.* The sibling stream is an inc(·, 0)-enumeration with base c₁ = inc(p, d): writing t₀ = c₁ and tₙ₊₁ = inc(tₙ, 0), the sequence {c₁, c₂, ...} is exactly the domain enumeration {t₀, t₁, ...} that ASN-0034's allocator discipline indexes. ASN-0034's T10a.7 (EnumerationInjectivity) establishes that every such enumeration is strictly increasing under T1 — `(A m, n ≥ 0 : m < n : tₘ < tₙ)` — and its proof rests only on TA5(a) (per-step strict increase of inc(·, 0)) and T1's transitivity (c) and irreflexivity (a), none of which appeal to T4-validity of the base. Re-indexing (cᵢ = t_{i−1}), the conclusion is exactly `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`. ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, d ≥ 1. S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).
- *Postconditions:* `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — the sibling stream is strictly increasing.
- *Axiom:* ASN-0034 T10a.7 (EnumerationInjectivity) — the strict-increase conclusion for an inc(·, 0)-enumeration, which itself packages TA5(a) and T1's transitivity and irreflexivity.

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

As a consequence, since every cₙ extends p, the entire stream lies within the set {t ∈ T : p ≼ t}, which forms a contiguous interval under T1 by T5 (ContiguousSubtrees).

Nelson describes exactly this process: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." The word "successive" is precise — positions arrive in order, c₁ before c₂ before c₃. "Items 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." The stream is traversed monotonically, not sampled.

One structural identity of the stream construction will be needed in two later arguments (B1 and B6): a parent ending in a trailing zero generates the same stream at depth 1 as its truncation does at depth 2.

**S2 (Trailing-Zero Stream Identity).** Let p ∈ T with p_{#p} = 0, and let p′ be p with its final component removed (#p′ = #p − 1, p′ᵢ = pᵢ for 1 ≤ i ≤ #p − 1). Then S(p, 1) = S(p′, 2).

*Proof.* The first element of S(p, 1) is c₁ = inc(p, 1); by TA5(d) with d − 1 = 0 intermediate zeros, c₁ has length #p + 1 with positions 1 through #p preserved from p and position #p + 1 set to 1, so c₁ = [p₁, ..., p_{#p−1}, 0, 1] (using p_{#p} = 0). The first element of S(p′, 2) is c′₁ = inc(p′, 2); by TA5(d) with one intermediate zero, c′₁ has length #p′ + 2 = #p + 1 with positions 1 through #p′ = #p − 1 preserved from p′, position #p′ + 1 = #p set to 0 (the separator), and position #p′ + 2 = #p + 1 set to 1, so c′₁ = [p₁, ..., p_{#p−1}, 0, 1]. Component-by-component, c₁ = c′₁. Both streams share the deterministic recurrence cₙ₊₁ = inc(cₙ, 0), so they coincide: S(p, 1) = S(p′, 2). ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, p_{#p} = 0; p′ = [p₁, ..., p_{#p−1}].
- *Postconditions:* S(p, 1) = S(p′, 2).
- *Axiom:* TA5(d) (child structure), deterministic stream recurrence.


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

*Case 2: children(B, p, d) ≠ ∅.* The definition yields next(B, p, d) = inc(max(children(B, p, d)), 0). We must show that max(children(B, p, d)) exists and that the subsequent increment is well-defined. The set children(B, p, d) is a non-empty finite subset of T (finite because B is finite, non-empty by hypothesis). The lexicographic order T1 is a strict total order on T, so every non-empty finite subset has a unique maximum. Let t = max(children(B, p, d)). TA5's first (unlabeled) postcondition (ASN-0034) gives `inc(t, 0) ∈ T` for any t ∈ T; TA5(c) further specifies the form — length preserved, value at position sig(t) advanced by 1.

In both cases, next(B, p, d) produces an element of T. The definition is total on its domain {(B, p, d) : B ⊆ T finite, p ∈ T, d ≥ 1}. ∎

*Formal Contract:*
- *Definition:* next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0), where children(B, p, d) = B ∩ S(p, d).
- *Preconditions:* B ⊆ T finite (discharged by B_fin when B = Σ.B for a reachable Σ); p ∈ T; d ≥ 1; S(p, d) defined.
- *Postconditions:* next(B, p, d) ∈ T — the result is a valid tumbler.
- *Axiom:* TA5(c) (sibling increment well-definedness), TA5(d) (child increment well-definedness), T1 (total order guarantees max exists).

**Bop (Baptism).** The operation baptize(p, d) is defined by:

  PRE: B6(p, d) — depth validity (defined below); [parent prerequisite deferred to Open Questions]
  POST: Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}
  FRAME: Σ.B is modified as specified by POST. This ASN makes no commitment about whether or how other components Σ carries — including those introduced by future ASNs (content storage, link structures, arrangement) and those of ASN-0034 (Act, nₛ) — are modified across the same transition; their specification is left to the ASNs that introduce them.
  STRUCTURAL (on Op): B4 — each `baptize(p, d) ∈ Op` is a single atomic edge of the transition graph (defined below). B4 is an invariant of the operation vocabulary, not a caller-checked precondition: it is satisfied by construction of Op, not discharged per call.

The frame condition's scope is essential. With respect to Σ.B, baptism is precise: `Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}` and nothing more. Other state components — content storage, link structures, arrangement, and the allocator-side state of ASN-0034 — are not subjects of this ASN's specification; Bop makes no commitment about whether they are modified across the same transition. The structural assumption B4 — that each baptize(p, d) is a single edge in the transition relation — makes next(Σ.B, p, d) evaluable against the precondition state Σ of the same transition that produces Σ'; no other transition mediates between the evaluation of next and the registry update. Because B4 governs how Op is built rather than what a caller passes in, it is listed as a structural assumption on Op rather than as part of Bop's PRE.

*Proof of well-definedness and correctness.* We must show that under the stated preconditions, baptize(p, d) is well-defined, produces a fresh address, and preserves the system invariants B0, B1, B10, and B_fin. The four obligations are mutually recursive: well-definedness appeals to B1 to identify max(children(Σ.B, p, d)) as cₘ and to B_fin to ground its existence; B1's preservation in turn appeals to Bop's postcondition; B10's preservation likewise appeals to Bop's choice of next; and B_fin's preservation appeals to the singleton-extension form of that postcondition. We present the per-step arguments here as components of one joint induction over Σ_init →* Σ, whose hypothesis carries B1, B10, B_fin (and B_type via B10) at the precondition state Σ of every transition. The dedicated §B1, §B10, §B_fin, §B_type proofs below carry the respective single-step preservation arguments under the same hypothesis, with B0a's transition partition serving as the common discriminator. No step argument appeals to its own conclusion at the current state — each is conditional on the joint hypothesis at Σ, which the induction establishes state-by-state via B0a — so the cross-references between the Bop correctness proof and the §B1/§B10/§B_fin proofs are jointly inductive rather than circular.

**Well-definedness.** The postcondition invokes next(Σ.B, p, d), which branches on whether children(Σ.B, p, d) is empty. If empty, the result is inc(p, d) — well-defined for any p ∈ T and d ≥ 1 by TA5's first postcondition (the unlabeled `t' ∈ T`). If non-empty, the result is inc(max(children(Σ.B, p, d)), 0). By the joint inductive hypothesis at Σ, B1 gives children(Σ.B, p, d) = {c₁, ..., cₘ} for some m ≥ 1, a contiguous prefix, and B_fin gives this set finite; max therefore exists and equals cₘ. The joint hypothesis also gives B10 (registry-wide T4 validity), so cₘ ∈ Σ.B ⊆ T; TA5's first (unlabeled) postcondition then gives `inc(cₘ, 0) ∈ T`. In both branches, next produces an element of T.

**Freshness.** Let a = next(Σ.B, p, d) = c_{m+1} where m = hwm(Σ.B, p, d). We show a ∉ Σ.B. By construction, a = c_{m+1} ∈ S(p, d). Since children(Σ.B, p, d) = Σ.B ∩ S(p, d) by definition, if a ∈ Σ.B then a ∈ children(Σ.B, p, d). By B1, children(Σ.B, p, d) = {c₁, ..., cₘ}. By S0 (StreamOrdering), distinct stream indices produce distinct elements: since m + 1 > i for all 1 ≤ i ≤ m, we have c_{m+1} ≠ cᵢ for each such i. Therefore a ∉ {c₁, ..., cₘ} = children(Σ.B, p, d), contradicting the supposition. We conclude a ∉ Σ.B. B4 guarantees that next(Σ.B, p, d) is evaluated against the precondition state Σ of the same transition that produces Σ', so the value of children(Σ.B, p, d) used here is exactly the value used in the postcondition of the same edge.

**Monotonicity (B0).** Σ'.B = Σ.B ∪ {a} ⊇ Σ.B directly — the registry grows by one element and no element is removed.

**B1 preservation.** In the target namespace, children(Σ'.B, p, d) = {c₁, ..., cₘ, c_{m+1}} — a contiguous prefix of length m + 1, since the new element is the immediate successor of the previous maximum. For every other B6-valid namespace (p', d'), B7 ensures a ∉ S(p', d'), so children(Σ'.B, p', d') = children(Σ.B, p', d'), and their contiguous prefix property is undisturbed. Non-B6 namespaces require additional case analysis — the complete argument, covering streams whose elements are entirely T4-invalid and the sole-defect trailing-zero case where stream identity collapses to an already-handled B6-valid namespace, is given in the B1 proof below. B0a (Baptismal Closure) guarantees no non-baptismal mechanism introduces elements that could disrupt contiguity in any namespace.

**B10 preservation.** The new element a must satisfy T4 for the registry-wide validity invariant to hold. Two cases arise from the definition of next. When m = 0, a = inc(p, d) — the first child. TA5a (IncrementPreservesT4, ASN-0034) states that for any t satisfying T4, inc(t, k) satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`. With t = p and k = d: B6(i) gives p T4-valid; B6(ii) restricts d ∈ {1, 2}. For d = 1, TA5a's `k ∈ {0, 1}` branch applies with no further obligation on zeros(p). For d = 2, TA5a's `k = 2 ∧ zeros(t) ≤ 2` branch requires zeros(p) ≤ 2, which is B6(iii) — `zeros(p) + (d − 1) ≤ 3` — specialized to d = 2. The applicable TA5a case is therefore satisfied, and a satisfies T4. When m > 0, a = inc(cₘ, 0) — a sibling increment. By B10 for the current state, cₘ satisfies T4 (it was admitted by a prior baptism or is a conforming seed). TA5a's `k = 0` case states inc(t, 0) satisfies T4 for any T4-valid t with no further constraint — no zeros are added, no adjacencies are introduced. Therefore a satisfies T4. ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1; B6(p, d) holds. (B1, B10, and B_fin are *state invariants*, not per-call obligations: they are established at genesis by B₀ conf. and preserved inductively by the proofs in §B1, §B10, and §B_fin, so they hold in every reachable state at which baptize(p, d) can be invoked. They are appealed to in the well-definedness and preservation arguments below but are not discharged by the caller.)
- *Structural assumptions on Op:* B4 (Atomic Baptism) — each `baptize(p, d) ∈ Op` is a single atomic edge of the transition graph; this is an invariant of the operation vocabulary, not a caller-checked precondition.
- *Postconditions:* Σ'.B = Σ.B ∪ {next(Σ.B, p, d)} with next(Σ.B, p, d) ∉ Σ.B; Σ'.B satisfies B0, B1, B10, and B_fin.
- *Frame:* Σ.B is modified as specified by the postcondition above. This ASN makes no commitment about whether or how other components Σ carries (content storage, link structures, arrangement, and ASN-0034's Act and nₛ) are modified across the same transition; their specification is left to the ASNs that introduce them. The full successor state Σ' = baptize(p, d)(Σ) is thereby compatible with Bridge1's joint update of Σ.B and ASN-0034's allocator-side state across one baptismal transition.


## The contiguous prefix property

We claim that children(B, p, d) is always a *prefix* of the sibling stream: the first m elements for some m ≥ 0, with no gaps.

**B1 (Contiguous Prefix).** `(A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))`.

Equivalently: children(B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

*Proof.* We must show that in every state reachable from a conforming seed B₀, for every parent p and depth d, children(Σ.B, p, d) is a contiguous prefix of S(p, d). The argument proceeds by induction on the number of state transitions from the initial state.

*Base case.* In the initial state, Σ.B = B₀. By B₀ conf. (SeedConformance), children(B₀, p, d) is a contiguous prefix of S(p, d) for every (p, d). B1 holds at genesis.

*Inductive step.* Assume B1 holds for state Σ with registry B. Consider a transition Σ → Σ' producing registry B'. By B0a (Baptismal Closure), Op partitions into Σ.B-frame operations and baptismal operations; we treat the two transition classes in turn.

*Σ.B-frame transitions.* If the transition is induced by a Σ.B-frame operation, then Σ'.B = Σ.B — that is, B' = B. For every (p, d), children(B', p, d) = B' ∩ S(p, d) = B ∩ S(p, d) = children(B, p, d), a contiguous prefix of S(p, d) by the inductive hypothesis. B1 holds at B'.

*Baptismal transitions.* Otherwise the transition is induced by a baptismal operation baptize(p₀, d₀) for some (p₀, d₀) satisfying B6, so B' = B ∪ {a} where a = next(B, p₀, d₀). We must show that children(B', p, d) is a contiguous prefix of S(p, d) for every (p, d). Two cases exhaust the possibilities.

*Target namespace: (p, d) = (p₀, d₀).* By B4 (Atomic Baptism), this baptism is a single Op-transition acting on B; the value of children(B, p₀, d₀) appearing in the postcondition is computed from the same precondition state B that licenses the transition. By the inductive hypothesis, children(B, p₀, d₀) = {c₁, ..., cₘ} for some m ≥ 0. Two sub-cases arise from the definition of next (NextAddress).

When m = 0: children(B, p₀, d₀) = ∅, so a = next(B, p₀, d₀) = inc(p₀, d₀) = c₁, the first element of S(p₀, d₀) by the definition of the sibling stream. Therefore children(B', p₀, d₀) = {c₁}, a contiguous prefix of length 1.

When m ≥ 1: the maximum of children(B, p₀, d₀) is cₘ, since the prefix {c₁, ..., cₘ} is strictly ordered by S0 (StreamOrdering). The definition of next gives a = inc(cₘ, 0). By TA5(c), this sibling increment advances only the last significant component of cₘ by 1, producing exactly c_{m+1} — the immediate successor in S(p₀, d₀). No element is skipped: the definition of next always selects the immediate successor via inc(cₘ, 0), which by TA5(c) cannot leap over any stream element. By B0 (Irrevocability), B ⊆ B', so {c₁, ..., cₘ} ⊆ B'. Together with the new element c_{m+1} ∈ B', we obtain children(B', p₀, d₀) = {c₁, ..., cₘ, c_{m+1}}, a contiguous prefix of length m + 1.

*All other namespaces: (p, d) ≠ (p₀, d₀).* By construction, a ∈ S(p₀, d₀) and a satisfies T4 (by B10 preservation, established in the Bop correctness proof). We show children(B', p, d) is a contiguous prefix by case analysis on (p, d).

The case analysis is exhaustive over arbitrary (p, d) ≠ (p₀, d₀). We split first on whether (p, d) satisfies B6, and within the non-B6 branch on whether S(p, d) contains any T4-valid element. This yields three sub-cases: (A) (p, d) satisfies B6; (B) (p, d) violates B6 and every element of S(p, d) violates T4 — covering p with a leading zero, p with interior adjacent zeros, p violating B6(iii) (zero budget), d ≥ 3, and the configuration where p is T4-valid except for a trailing zero combined with d = 2; and (C) (p, d) violates B6 but S(p, d) contains T4-valid elements — the unique configuration in which this can occur is p T4-valid except for a trailing zero (p_{#p} = 0, p₁ > 0, no other defect) with d = 1. The partition is exhaustive on its face: B6 either holds (A) or fails, and within failing-B6 the stream either has all elements violating T4 (B) or contains some T4-valid element (C); the assignment of specific configurations to (B) and (C) is justified inline below. Sub-case (B)'s propagation mechanisms differ across its configurations: when p₁ = 0 or p has interior adjacent zeros or some other interior T4 defect, TA5(b) preserves positions 1 through #p of p into c₁, and each sibling increment cₙ₊₁ = inc(cₙ, 0) modifies only sig(cₙ) = #p + d > #p, so the defect persists at the same position in every cₙ. When zeros(p) + (d − 1) > 3 with d ∈ {1, 2}, B5 gives zeros(c₁) = zeros(p) + (d − 1) > 3, exceeding T4's three-zero budget; B5a propagates the count to every cₙ. When d ≥ 3, TA5(d) appends d − 1 ≥ 2 zeros followed by 1, placing adjacent zeros at positions #p + 1 and #p + 2 of c₁; since each subsequent sibling modifies only sig(cₙ) = #p + d ≥ #p + 3, positions #p + 1 and #p + 2 are invariant across the stream and the adjacency persists. When p is T4-valid except for a trailing zero (p_{#p} = 0) and d = 2, the defect arises not from preserved-prefix propagation but from the union of p's trailing zero and TA5(d)'s separator: by TA5(b), (c₁)_{#p} = p_{#p} = 0; by TA5(d) with d = 2, (c₁)_{#p+1} = 0 (the intermediate zero); positions #p and #p + 1 are adjacent zeros in c₁, and since sig(cₙ) = #p + 2 > #p + 1 for every n, both positions are invariant across siblings, so every cₙ carries the same adjacent-zero violation. By elimination from these propagation results, the only failure mode of B6 that does *not* drive every stream element out of T4 is the sole-defect trailing-zero configuration with d = 1; this is sub-case (C).

When (p, d) satisfies B6 (sub-case A): both (p₀, d₀) and (p, d) meet B7's preconditions, so B7 gives S(p₀, d₀) ∩ S(p, d) = ∅, hence a ∉ S(p, d). Therefore children(B', p, d) = children(B, p, d), a contiguous prefix by the inductive hypothesis.

When (p, d) does not satisfy B6 and every element of S(p, d) violates T4 (sub-case B): since a satisfies T4, a ∉ S(p, d). Moreover, B10 for the current state ensures every element of B satisfies T4, so children(B, p, d) = ∅. Therefore children(B', p, d) = ∅, trivially a contiguous prefix. (The configurations covered by this sub-case — p with a leading zero, p with interior adjacent zeros or other interior defects, zeros(p) + (d − 1) > 3, d ≥ 3, and p T4-valid except for a trailing zero combined with d = 2 — were enumerated above, along with the propagation mechanism that drives every stream element out of T4 in each.)

When (p, d) does not satisfy B6 but S(p, d) contains T4-valid elements (sub-case C): by the elimination established above, this occurs exactly when p ends in zero (with no other T4 defect) and d = 1. Let p' be p with its trailing zero removed, so #p' = #p − 1 and p'ᵢ = pᵢ for 1 ≤ i ≤ #p − 1, and let d' = 2. By S2 (Trailing-Zero Stream Identity), S(p, 1) = S(p', 2).

We verify that p' satisfies T4 and (p', 2) satisfies B6. For T4: p₁ > 0 (inherited from p); no adjacent zeros (the trailing zero was the sole defect — if p had adjacent zeros or a leading zero, these would be additional T4 violations, contradicting the sole-defect hypothesis); p'_{#p'} = p_{#p−1} > 0 since the trailing zero was the sole defect. For the zero count: the sole-defect hypothesis gives zeros(p) ≤ 3 (a second violation — such as zeros(p) > 3 — would contradict sole defect). Removing the trailing zero yields zeros(p') = zeros(p) − 1 ≤ 2. B6(i): p' satisfies T4 as just shown. B6(ii): d' = 2 ∈ {1, 2}. B6(iii): zeros(p') + (d' − 1) = zeros(p') + 1 ≤ 3. Therefore (p', 2) satisfies B6. Two sub-cases arise. If (p', d') ≠ (p₀, d₀), B7 gives S(p₀, d₀) ∩ S(p', d') = ∅, hence a ∉ S(p', d') = S(p, d), and children(B', p, d) = children(B, p, d). If (p', d') = (p₀, d₀), then children(B', p, d) = children(B', p₀, d₀), whose contiguous prefix property was established in the target namespace case above. Because S(p, d) = S(p, 1) = S(p', 2) = S(p₀, d₀) by the stream-identity argument established above, a contiguous prefix of S(p₀, d₀) is the same finite sequence considered as a prefix of S(p, d) — the two namespaces share the same element set in the same order, so contiguity transfers across the rebadging.

In all sub-cases, children(B', p, d) is a contiguous prefix of S(p, d).

Since B1 is preserved in the target namespace and in every other namespace, B1 holds for B' under baptismal transitions. By the frame argument above, B1 also holds for B' under Σ.B-frame transitions. By induction on the transition sequence, B1 holds in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A p, d, n : n ≥ 1 ∧ cₙ ∈ Σ.B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ Σ.B))` — equivalently, children(Σ.B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.
- *Base:* B₀ conf. — seed set satisfies contiguous prefix for all (p, d).
- *Preservation:* Each baptism preserves B1 in the target namespace (by Bop, B0, B4, S0, TA5(c)) and in all other namespaces (by B7 for B6-valid pairs; by B10 for non-B6 pairs whose streams are entirely T4-invalid; by stream identity S(p, 1) = S(p', 2) (S2) for non-B6 pairs where p ends in zero as its sole defect and d = 1).

Two dependencies bear emphasis. B7 (Namespace Disjointness) ensures no operation outside a namespace inserts an element into its stream. B0a (Baptismal Closure) ensures no mechanism other than baptism adds elements to B at all — without B0a, a non-baptismal operation could insert arbitrary elements into B, and the preservation argument would be ungrounded.

The induction also requires a conforming base:

**B₀ conf. (SeedConformance).** B₀ is finite, `(A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))`, and `(A t ∈ B₀ : t satisfies T4)`.

B₀ must be finite, satisfy B1 for every namespace at genesis, and have every seed element be a valid address under T4. Non-emptiness is *not* a separate clause of B₀ conf.; it is forced externally by the composition of Bridge2 (`allocated(Σ_init) ⊆ B₀`) and ASN-0034's `allocated(s₀) = {t₀}`, which together require t₀ ∈ B₀ and hence B₀ ≠ ∅ in every system conforming to both ASNs. Keeping non-emptiness out of B₀ conf. preserves the layering: B₀ conf. specifies the *structural* conditions a seed must satisfy (finiteness, per-namespace contiguity, per-element T4-validity), while the *contents* of B₀ — which addresses sit alongside the algebra-mandated root, and whether the seed admits non-singleton root configurations — are settled by the activation-discipline ASN through Bridge2. The remaining structural conditions are individually necessary. Finiteness is required because the next function's well-definedness depends on max(children(B, p, d)) existing, which requires children to be a finite set; since B starts as B₀ and grows by one element per baptism, B₀ finite implies B finite in every reachable state. Without the contiguity requirement, the seed set could contain {c₁, c₃} for some namespace — a gap that the inductive argument cannot repair, since baptism only appends the next sibling. Without the T4 requirement, a seed element could serve as a parent that violates B6(i), undermining B7's disjointness guarantee.

B₀ conformance fixes the seed as a finite set; B0a constrains every transition to add at most one element. The composition yields a registry-wide finiteness invariant:

**B_fin (Registry Finiteness).** `(A Σ : Σ reachable from Σ_init : Σ.B is finite)`.

*Proof.* By induction on the number of state transitions from the initial state. The argument is self-contained — it appeals to nothing from B_type.

*Base case.* In the initial state, Σ.B = B₀. By B₀ conf. (SeedConformance), B₀ is finite. The invariant holds at genesis.

*Inductive step.* Assume Σ.B is finite for state Σ with registry B. Consider a transition Σ → Σ' producing registry B'. By B0a (Baptismal Closure), either the transition is Σ.B-frame, in which case B' = B and B' is finite by the inductive hypothesis; or the transition is baptismal, in which case B' = B ∪ {a} for a single new element a, and B' is the union of a finite set with a singleton, hence finite. In both transition classes, B' is finite. By induction, Σ.B is finite in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A Σ : Σ reachable from Σ_init : Σ.B is finite)`.
- *Base:* B₀ conf. — B₀ is finite.
- *Preservation:* B0a — every transition either leaves Σ.B unchanged or adds exactly one new element.

From B₀ conformance (T4 for seeds) and B6(i) (T4 for parents), we derive by induction on the baptism sequence that T4 validity is a registry-wide invariant:

**B10 (T4ValidityInvariant).** `(A t ∈ Σ.B : t satisfies T4)`

*Proof.* We must show that in every state reachable from a conforming seed B₀, every element of Σ.B satisfies T4 (FieldSeparatorConstraint, ASN-0034). The argument proceeds by induction on the number of state transitions from the initial state.

*Base case.* In the initial state, Σ.B = B₀. By B₀ conf. (SeedConformance), every t ∈ B₀ satisfies T4. The invariant holds at genesis.

*Inductive step.* Assume B10 holds for state Σ with registry B — that is, every t ∈ B satisfies T4. Consider a transition Σ → Σ' producing registry B'. By B0a (Baptismal Closure), Op partitions into Σ.B-frame operations and baptismal operations; we treat the two transition classes in turn.

*Σ.B-frame transitions.* If the transition is induced by a Σ.B-frame operation, then Σ'.B = Σ.B — that is, B' = B. Every t ∈ B' = B satisfies T4 by the inductive hypothesis. B10 holds at B'.

*Baptismal transitions.* Otherwise the transition is induced by a baptismal operation baptize(p, d) for some (p, d) satisfying B6, so B' = B ∪ {a} where a = next(B, p, d). We must show every t ∈ B' satisfies T4. For elements t ∈ B, the inductive hypothesis gives t satisfies T4 directly. It remains to show the new element a satisfies T4.

By B6, the parent p satisfies T4 (condition (i)), d ∈ {1, 2} (condition (ii)), and zeros(p) + (d − 1) ≤ 3 (condition (iii)). By the definition of next (NextAddress), a = next(B, p, d) branches on whether children(B, p, d) is empty. Two cases arise.

*Case 1: children(B, p, d) = ∅.* Then a = inc(p, d) by the definition of next. TA5a (IncrementPreservesT4, ASN-0034) states that for any t satisfying T4, inc(t, k) satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`. Instantiating with t = p and k = d, B6(i) provides T4-validity of p and B6(ii) restricts d to {1, 2}. For d = 1, TA5a's `k ∈ {0, 1}` branch applies directly with no further obligation on zeros(p). For d = 2, TA5a's `k = 2 ∧ zeros(t) ≤ 2` branch requires zeros(p) ≤ 2, which B6(iii) — `zeros(p) + (d − 1) ≤ 3` specialized to d = 2 — supplies. The applicable TA5a case is therefore satisfied, and a = inc(p, d) satisfies T4. (B6(iii)'s uniform form `zeros(p) + (d − 1) ≤ 3` is ASN-0040's own bridging restatement, collapsing TA5a's two d-cases into a single bound under T4-validity of p; it is not itself part of TA5a's case structure.)

*Case 2: children(B, p, d) ≠ ∅.* The set children(B, p, d) = B ∩ S(p, d) is a non-empty finite subset of T (finite because B is finite by B_fin). Let t = max(children(B, p, d)) — which exists because T1 is a total order on every non-empty finite set. By definition of children, t ∈ children(B, p, d) ⊆ B. By the inductive hypothesis (B10 for the current state), t satisfies T4. The definition of next gives a = inc(t, 0). TA5a's `k = 0` case states that inc(t, 0) satisfies T4 for any T4-valid t with no further constraint: no zeros are added (TA5(c) modifies only position sig(t), advancing a positive value by one), no adjacent zeros are introduced, and the tumbler neither begins nor ends in zero after the increment. Therefore a = inc(t, 0) satisfies T4.

In both cases, a satisfies T4. Since every element of B satisfies T4 by the inductive hypothesis and the new element a satisfies T4 by the case analysis, every element of B' = B ∪ {a} satisfies T4. B10 holds at B' under baptismal transitions, and by the frame argument above, B10 holds at B' under Σ.B-frame transitions. By induction on the transition sequence, B10 holds in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A t ∈ Σ.B : t satisfies T4)` — every baptized address satisfies FieldSeparatorConstraint.
- *Base:* B₀ conf. — every seed element satisfies T4.
- *Preservation:* Each baptism preserves B10: when children are empty, by B6 and TA5a (IncrementPreservesT4, ASN-0034) with k = d; when children are non-empty, max(children) ∈ B satisfies T4 by the inductive hypothesis, and TA5a with k = 0 preserves T4 unconditionally. B0a ensures no non-baptismal mechanism introduces elements that might violate T4.

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

Throughout these derivations, B4 (Atomic Baptism) guarantees that `children(B, p, d)` is evaluated against the precondition state B of the same transition that produces B'; we state this once here and do not repeat it per derivation.

Under B4 (serialized execution within the namespace):

  wp(baptize(p, d), B1) — state precondition: B1; environmental: B0a, B4; lemma: B7.

Let B' = B ∪ {a} where a = next(B, p, d) = c_{hwm+1}. B1 for B' requires two things. First, every previously baptized cₙ in B still has predecessors c₁, ..., c_{n−1} in B' — satisfied because B ⊆ B' (by B0). Second, the new element c_{hwm+1} has predecessors c₁, ..., c_{hwm} in B' — satisfied iff children(B, p, d) = {c₁, ..., c_{hwm}}, which is exactly B1 for the current state. The second condition also requires that no non-baptismal mechanism has altered the namespace — the transition constraint B0a.

The freshness derivation similarly:

  wp(baptize(p, d), a ∉ B) — state precondition: B1; environmental: B4; lemma: S0.

The new address c_{hwm+1} must not already appear in B. By construction, c_{hwm+1} ∈ S(p, d). Since children(B, p, d) = B ∩ S(p, d), membership of c_{hwm+1} in B would place it in children(B, p, d). By B1, children is a contiguous prefix {c₁, ..., c_{hwm}}. By S0, distinct stream indices produce distinct elements, so c_{hwm+1} ∉ {c₁, ..., c_{hwm}}. Contradiction: c_{hwm+1} ∉ B.

The T4 validity of the new element is the third wp obligation:

  wp(baptize(p, d), B10) — state precondition: B10 at Σ; environmental: B0a, B6 from Bop's precondition on (p, d); lemma: TA5a.

B10 at B' requires every t ∈ B' to satisfy T4. For elements already in B, the state precondition (B10 at Σ) gives T4 directly, and B0a's partition rules out any non-baptismal mechanism that could have introduced a T4-violating element between the wp evaluation and the transition. For the newly added element a, the obligation is more delicate. Two sub-cases mirror next's case structure. When children(B, p, d) = ∅, a = inc(p, d): B6(i) (Bop's precondition on (p, d)) gives p satisfies T4 and B6(ii) gives d ∈ {1, 2}; TA5a's `k ∈ {0, 1}` branch handles d = 1 unconditionally, and TA5a's `k = 2 ∧ zeros(t) ≤ 2` branch handles d = 2 under B6(iii). When children(B, p, d) ≠ ∅, a = inc(cₘ, 0) where cₘ = max(children(B, p, d)): the state precondition (B10 at Σ) gives cₘ satisfies T4 since cₘ ∈ B, and TA5a's `k = 0` branch preserves T4 unconditionally. The B6 precondition is essential for the first sub-case but not the second; the state precondition (B10) is essential for the second but vacuously discharged on the first. Both must hold for the joint claim to carry forward to B'.

The simpler observation also holds: wp(baptize(p, d), hwm = N + 1) = (hwm = N). But this merely says "to advance a counter, the counter must be at the previous value" — the definition of counting, not a substantive derivation. The invariant-targeting wp reveals the real dependencies: B1, B0a, B4, and B7 are mutually supporting properties, each required for the others' preservation.

The wp derivations above are single-step: each establishes that if B satisfies the precondition then B' = baptize(p, d)(B) satisfies the postcondition. The single-step B0 citation "B ⊆ B' (by B0)" inside the B1 derivation is exact for the one-transition step B → B'. The lift from per-transition preservation to the global claim "B1 holds in every reachable state Σ" is by induction over the transition sequence Σ_init →* Σ, with B0★ (Multi-step Irrevocability) underwriting the registry-side monotonicity across the entire sequence: any element baptized at any earlier step of the sequence remains in Σ.B at every later step, so the inductive hypothesis B satisfies B1 carries forward to every prefix of the sequence on which the per-transition wp argument is run.

Two systems beginning from the same B₀ and executing the same sequence of baptisms — same parents, same depths, same order — produce identical address spaces. The addresses are not identifiers assigned by fiat; they are the inevitable consequence of the baptism history.

We observe that next is *idempotent in evaluation*: as a pure function, next(B, p, d) is determined entirely by its arguments — evaluating it leaves B unchanged, and a second evaluation against the same B returns the same answer. The address enters Σ.B only through a baptize(p, d) transition whose postcondition adds it; evaluating next without taking the transition leaves the registry untouched. If a baptism is abandoned after the candidate is computed but before a transition is taken, no harm is done — the namespace is unchanged, the high water mark is unchanged, a later baptize(p, d) transition from the same precondition state returns the same address.

Gregory's implementation confirms this precisely. The query-and-increment function produces a candidate address in a local variable; the candidate exists only as bits in memory. If the function were called twice without an intervening write, both invocations would return the same address — because the persistent tree has not changed and the search would find the same maximum both times. The address enters reality only when the subsequent insertion function writes it into the tree.


## Ghost elements: baptism without content

A baptized position need not contain anything. Nelson names these *ghost elements*:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

A ghost element is "virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." The position is in Σ.B — it has been baptized, it is permanent, it anchors a namespace for children — but nothing is stored at that address.

"Occupied" is not a predicate of this ASN. Σ in our state space carries a single component — Σ.B — and no notion of content is defined here. We record the relationship between baptism and content as a *forward requirement* on whichever future ASN introduces content storage.

**B3 (Ghost Validity — forward requirement on content storage).** Let a future ASN introduce a predicate `Occupied : T × 𝒮 → {⊤, ⊥}` denoting "the address t carries content in state Σ". The present ASN does not define Occupied; the four-way classification below is therefore stated parametrically in Occupied. The forward requirement is that every future ASN introducing Occupied must arrange its operations so that

  `(A Σ : Σ reachable from Σ_init : (A t ∈ T : Occupied(t, Σ) ⟹ t ∈ Σ.B))`

— content is permitted only at baptized addresses. Under this requirement, the configurations of a tumbler t ∈ T in a reachable state Σ partition into:

  - t ∈ Σ.B ∧ Occupied(t, Σ): a populated position
  - t ∈ Σ.B ∧ ¬Occupied(t, Σ): a ghost element (permitted)
  - t ∉ Σ.B ∧ ¬Occupied(t, Σ): an unbaptized, unoccupied position (not addressable)
  - t ∉ Σ.B ∧ Occupied(t, Σ): forbidden (excluded by the forward requirement above)

The forbidden row is not a current invariant of the present ASN: the row's contrapositive (`Occupied(t, Σ) ⟹ t ∈ Σ.B`) is the obligation we hand forward. Future specifications of content storage operations must enforce `t ∈ Σ.B` as a precondition on any write that would make Occupied(t, Σ) hold. The "ghost element" row is explicitly permitted and common: structural positions — nodes, users, documents — ordinarily function as ghosts, existing to organize the namespace and anchor children rather than to carry payload.

B3 separates two questions that might otherwise be conflated. "Does address t exist?" is answered by Σ.B in the present ASN. "Is there content at t?" will be answered by Occupied, once a future ASN introduces it. The baptismal registry is an existence index; the contemplated Occupied is a content index; B3 binds them by a one-way implication and defers everything else.


## Atomicity

Informally, the baptism process — read the high water mark, compute the next address, commit the result — must not be interleaved with another baptism in the same namespace. If two baptisms both read hwm = m before either commits, both compute c_{m+1} and both attempt to commit the same address — violating B8. We state this as a constraint at the level of the transition system rather than over an undefined event vocabulary of "read" and "commit".

**B4 (Atomic Baptism).** Each baptismal operation is a single atomic transition. For every (p, d) satisfying B6:

  `(A Σ ∈ dom(baptize(p, d)) : baptize(p, d)(Σ) = Σ' with Σ'.B = Σ.B ∪ {next(Σ.B, p, d)})`

The value `next(Σ.B, p, d)` is computed against the state Σ that licenses the transition and is committed to the successor state Σ' in the same step; the transition admits no intermediate state in which `Σ.B ∩ S(p, d)` has been observed but the registry has not yet grown.

Equivalently, in the transition relation `→` of the state space 𝒮: the observation of the precondition state and the commitment of the postcondition state are not separable. There is no state Σ_mid with `Σ → Σ_mid → Σ'` representing an "intent to baptize" that some later step fulfills. Each `baptize(p, d) ∈ Op` is a single edge in the transition graph.

B0a guarantees that no other operation modifies Σ.B between any two transitions, so within a single Op-transition the read of `Σ.B ∩ S(p, d)` is exact, and across two same-namespace baptismal transitions β₁, β₂, exactly one of `β₁; β₂` or `β₂; β₁` describes their relative order in the transition sequence — there is no third option of overlap.

B4's scope is *per-namespace* in the sense that B7 guarantees baptisms under distinct (p, d) pairs produce disjoint outputs; if the system later admits a model with concurrent operations, the serialization requirement collapses to "same-namespace baptisms must reduce to a sequential order, distinct-namespace baptisms need not." The minimum serialization grain is the namespace, not the entire system. This is precisely what enables decentralized baptism — two agents baptizing under different parents proceed independently, and their addresses are guaranteed distinct by the partition structure of the address space (T10).

Gregory's implementation achieves the atomic-transition semantics through single-threaded dispatch — the event loop processes one request to completion before accepting another, and the entire path from query through increment to write runs without yielding control. But B4 is a specification-level requirement, not an implementation prescription. Any mechanism that exhibits one Op-transition per baptism — locking, transactions, hardware serialization, single-threaded dispatch — satisfies B4.


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

For the first child c₁ = inc(p, d): TA5a (IncrementPreservesT4, ASN-0034) states that for any t satisfying T4, inc(t, k) satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`. With t = p and k = d, conditions (i) and (ii) make p T4-valid and put d ∈ {1, 2}. For d = 1, TA5a's `k ∈ {0, 1}` branch applies directly with no further obligation on zeros(p). For d = 2, TA5a's `k = 2 ∧ zeros(t) ≤ 2` branch requires zeros(p) ≤ 2, which is exactly condition (iii) specialized to d = 2. The TA5a case applicable at the chosen d is therefore satisfied, so c₁ satisfies T4. (Condition (iii)'s uniform form `zeros(p) + (d − 1) ≤ 3` is ASN-0040's own bridging restatement: it collapses TA5a's two d-cases into a single bound that, combined with T4-validity of p, is equivalent to TA5a's case-based bound on d ∈ {1, 2}, but the uniform form is not itself part of TA5a.)

For subsequent siblings cₙ₊₁ = inc(cₙ, 0): TA5a's `k = 0` case states that inc(t, 0) satisfies T4 for any T4-valid t with no further constraint — sibling increment modifies only position sig(t), advancing a positive value by one (TA5(c)), so no zeros are added and no new adjacencies are introduced. Since c₁ satisfies T4, and each sibling increment preserves T4, by induction every cₙ satisfies T4.

**(⟹) Necessity.** We show that violating any single condition either produces a T4 violation in the stream or collapses an essential system invariant.

*Condition (ii) is necessary for T4.* Let d ≥ 3. By TA5(d), inc(p, d) appends d − 1 ≥ 2 zeros followed by 1. Positions #p + 1 and #p + 2 are both zero — adjacent zeros that parse as two consecutive field separators enclosing an empty field, violating T4's non-empty-field constraint. No choice of p avoids this: the adjacent zeros lie in the appended suffix, independent of p's content.

*Condition (iii) is necessary for T4.* Let zeros(p) + (d − 1) > 3 with d ∈ {1, 2} and p satisfying T4. By B5, zeros(c₁) = zeros(p) + (d − 1) > 3. But T4 requires zeros(t) ≤ 3 for any valid address — at most three field separators for the four-level hierarchy. The first child already exceeds the zero budget, so c₁ violates T4.

*Condition (i) is necessary for the system.* Let p violate T4 with d ∈ {1, 2} and zeros(p) + (d − 1) ≤ 3. Two structurally distinct situations arise, depending on whether p has a T4 defect among the positions whose values are preserved into c₁ by TA5(b) — interior positions 1 through #p − 1, or the leading position when p₁ = 0 (which coincides with the trailing position #p only in the singleton case p = [0]) — or whether p's sole defect is a clean trailing zero in a parent whose leading and interior positions are T4-valid. The two situations exhaust the configurations: if p violates T4 and the violation is not a pure trailing zero with p₁ > 0 and no other defect, then by elimination some defect lies at position 1 (leading zero) or at some interior position 1 < i < #p (adjacent zeros or other interior violation), placing p in sub-case (a) below; otherwise p falls in sub-case (b).

*(a) Defect in p's preserved prefix: some T4 defect at positions 1 through #p − 1 of p, or p₁ = 0 (the leading-zero case, including the singleton p = [0] in which leading and trailing positions coincide).* By TA5(b), inc(p, d) preserves positions 1 through #p, so each defective position of p survives unchanged into c₁ at the same index. Each subsequent cₙ₊₁ = inc(cₙ, 0) modifies only position sig(cₙ) = #p + d > #p (since d ≥ 1), leaving positions 1 through #p untouched. By induction, every stream element carries the defect. For example, with p = [0, 1, 2] (leading zero, #p = 3): c₁ = inc([0, 1, 2], 1) = [0, 1, 2, 1], and (cₙ)₁ = 0 for all n ≥ 1, violating T4's t₁ ≠ 0 requirement. For the singleton p = [0] (in which p₁ = p_{#p} = 0): with d = 1, c₁ = inc([0], 1) = [0, 1] and each cₙ = [0, n] violates t₁ ≠ 0; with d = 2, c₁ = inc([0], 2) = [0, 0, 1] preserves (cₙ)₁ = 0 from p for every n (and additionally exhibits adjacent zeros at positions 1 and 2 within c₁).

*(b) Pure trailing zero as the sole T4 defect: p_{#p} = 0, p₁ > 0, no adjacent zeros in p (which forces #p ≥ 2, since p₁ > 0 = p_{#p} requires the leading and trailing positions to be distinct).* This sub-case splits on the value of d. When d = 1, the stream may satisfy T4 without condition (i). Consider p = [1, 0] with d = 1. Then c₁ = inc([1, 0], 1) = [1, 0, 1] — one zero at position 2, positive first and last components, no adjacent zeros — and every cₙ = [1, 0, n] satisfies T4. However, S([1, 0], 1) is identical to S([1], 2): both produce the sequence [1, 0, 1], [1, 0, 2], [1, 0, 3], ... In general, let p' be p with the trailing zero removed; by S2 (Trailing-Zero Stream Identity), S(p, 1) = S(p', 2). The trailing zero of p merges with the stream structure to produce the same elements as a T4-valid namespace at greater depth. Permitting baptism under such a malformed parent creates a namespace whose sibling stream coincides with an existing valid namespace, collapsing B8 (Global Uniqueness): two distinct baptismal acts — one under invalid (p, 1), one under B6-valid (p', 2) — would produce the same stream element, giving distinct baptisms the same address. The mechanism passes through B7 — the namespace-partition premise B7 supplies is what B8's cross-namespace case relies on — but the property that actually fails is B8: the visible symptom is two baptisms with the same output, not merely two namespaces with overlapping ranges. B7's protection of B8 presupposes B6(i); without it, the partition dissolves and B8's cross-namespace branch loses its argument.

When d = 2, every stream element violates T4 — but by a propagation argument structurally distinct from sub-case (a). The defect does not preexist in p's interior; it arises within c₁ itself from the union of p's trailing zero and the separator TA5(d) inserts. By TA5(b), c₁ preserves positions 1 through #p of p, so (c₁)_{#p} = p_{#p} = 0. By TA5(d) with d = 2, c₁ has length #p + 2 and the intermediate position #p + 1 holds the field separator with value 0. Therefore (c₁)_{#p} = 0 and (c₁)_{#p+1} = 0 — adjacent zeros at positions #p and #p + 1 of c₁, violating T4's non-empty-field constraint (T4(ii) at i = #p). To propagate this to every cₙ, we show position #p + 1 is never modified by sibling increments. For c₁, position #p + 2 holds the value 1 (TA5(d)), so sig(c₁) = #p + 2; by TA5(c) each cₙ₊₁ = inc(cₙ, 0) advances the value at sig(cₙ) by 1 and preserves length, so sig(cₙ) = #p + 2 for all n ≥ 1. Position #p + 1 satisfies #p + 1 < #p + 2 = sig(cₙ), so it is invariant across the stream. By induction on n, (cₙ)_{#p} = 0 and (cₙ)_{#p+1} = 0 for every n ≥ 1, and every stream element carries the same adjacent-zero violation as c₁.

Condition (i) is therefore necessary: T4 defects in p's preserved prefix — interior, leading, or the singleton p = [0] — propagate to every stream element via TA5(b), and pure trailing-zero defects (where p's leading and interior positions are T4-valid) either propagate (when d = 2 creates adjacent zeros within c₁) or — when d = 1 — produce a stream identical to some valid S(p', 2), collapsing B8 (Global Uniqueness) by allowing two distinct baptisms (one under invalid (p, 1), one under B6-valid (p', 2)) to deliver the same address. ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1.
- *Postconditions:* (a) Sufficiency: `(p satisfies T4 ∧ d ∈ {1, 2} ∧ zeros(p) + (d − 1) ≤ 3) ⟹ (A n ≥ 1 : cₙ ∈ S(p, d) satisfies T4)`. (b) Necessity: violating (ii) or (iii) produces T4 violations in S(p, d); violating (i) either propagates defects in p's preserved prefix (interior adjacent zeros, leading zero p₁ = 0, or the singleton case p = [0] in which leading and trailing positions coincide) to every stream element via TA5(b), or — when the sole defect is a pure trailing zero with p₁ > 0 and no other T4 violation in p — produces adjacent zeros within c₁ for d = 2 (the trailing zero of p at position #p adjacent to TA5(d)'s field separator at position #p + 1, propagated to every cₙ since sig(cₙ) = #p + 2 > #p + 1 leaves the adjacent pair untouched), or creates a stream identical to some valid S(p', d') for d = 1, collapsing B8 (Global Uniqueness): distinct baptisms in the coincident namespaces produce the same stream element.


## Namespace disjointness

Each parent-depth pair defines a namespace. Distinct namespaces must produce non-overlapping address ranges, or global uniqueness collapses.

**B7 (Namespace Disjointness).** For distinct valid pairs (p, d) ≠ (p', d'):

  S(p, d) ∩ S(p', d') = ∅

provided both parents satisfy T4 and both depths satisfy B6.

*Proof.* We must show that for distinct valid pairs (p, d) ≠ (p', d'), where both parents satisfy T4 and both depths satisfy B6, no tumbler belongs to both S(p, d) and S(p', d'). Let a ∈ S(p, d) and b ∈ S(p', d'). We show a ≠ b by exhaustive case analysis on the relationship between the two pairs.

We first establish a uniform length property. The base c₁ = inc(p, d) has length #p + d by TA5(d), and the stream is an inc(·, 0)-enumeration with base c₁; ASN-0034's T10a.1 (UniformSiblingLength) gives that every sibling of such a stream shares the base length, so #cₙ = #p + d for all n ≥ 1, without re-running the length induction. Similarly, every element of S(p', d') has length #p' + d'.

*Case 1: different element lengths.* Suppose #p + d ≠ #p' + d'. Then #a = #p + d ≠ #p' + d' = #b. By T3, tumblers of different lengths are never equal, so a ≠ b.

*Case 2: equal element lengths, non-nesting prefixes.* Suppose #p + d = #p' + d' and neither p ≼ p' nor p' ≼ p. By S1, p ≼ a and p' ≼ b. Since the prefixes are non-nesting, T10 gives a ≠ b.

*Case 3: equal element lengths, nesting prefixes.* Suppose #p + d = #p' + d' and one prefix extends the other — say p ≼ p' without loss of generality (the argument for p' ≼ p is identical with the roles exchanged). Since (p, d) ≠ (p', d') and p ≼ p', either p = p' with d ≠ d', or p is a strict prefix of p'. If p = p' then #p = #p', so #p + d = #p' + d' gives d = d', contradicting d ≠ d'. Therefore p is a strict prefix of p': #p' > #p. From #p + d = #p' + d' we obtain d − d' = #p' − #p > 0, so d > d'. Since d, d' ∈ {1, 2} by B6(ii), the constraint d > d' forces d = 2 and d' = 1, whence #p' = #p + 1.

We show the two streams disagree at position #p + 1 for every pair of elements. For an arbitrary cₙ ∈ S(p, 2): at c₁ = inc(p, 2), TA5(d) places d − 1 = 1 zero-valued component at position #p + 1, so (c₁)_{#p+1} = 0. Each subsequent cₙ₊₁ = inc(cₙ, 0) modifies only position sig(cₙ). Since sig(c₁) = #c₁ = #p + 2 (the last component has value 1, hence is the rightmost nonzero position), and each sibling increment preserves length and advances only position sig(cₙ) by TA5(c), we have sig(cₙ) = #p + 2 for all n ≥ 1. Because #p + 2 ≠ #p + 1, position #p + 1 is never modified. By induction on n, (cₙ)_{#p+1} = 0 for all n ≥ 1.

For an arbitrary c'ₘ ∈ S(p', 1): by S1, p' ≼ c'ₘ, so (c'ₘ)_i = p'_i for all 1 ≤ i ≤ #p'. In particular, (c'ₘ)_{#p+1} = p'_{#p+1}. Since #p + 1 = #p', this is the last component of p'. By T4, valid addresses do not end in zero, so p'_{#p'} > 0. Therefore (c'ₘ)_{#p+1} = p'_{#p+1} > 0 for all m ≥ 1.

At position #p + 1, every element of S(p, 2) has value 0 and every element of S(p', 1) has a value greater than 0. By T3, tumblers that differ at any position are distinct, so a ≠ b.

The three cases are exhaustive: for any two streams, the element lengths are either different (Case 1), equal with non-nesting prefixes (Case 2), or equal with nesting prefixes (Case 3). In every case a ≠ b, so S(p, d) ∩ S(p', d') = ∅. ∎

*Formal Contract:*
- *Preconditions:* (p, d) and (p', d') both satisfy B6, with (p, d) ≠ (p', d').
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

**Step 4: sub-document under first document.** Namespace ([1, 0, 1, 0, 1], 1) — document [1, 0, 1, 0, 1], depth 1 (intra-level descent to sub-document, exercising d = 1).

  next(B₃, [1, 0, 1, 0, 1], 1) = inc([1, 0, 1, 0, 1], 1) = [1, 0, 1, 0, 1, 1]

TA5(d) with k = d − 1 = 0 intermediate zeros: no zero separator is inserted; the value 1 is appended at position #p + d = 6. B5: zeros([1, 0, 1, 0, 1, 1]) = 2 = zeros([1, 0, 1, 0, 1]) + (1 − 1) — d = 1 contributes no new zeros, so the parent's zero count is preserved. B6: p = [1, 0, 1, 0, 1] satisfies T4 (last component 1 is positive), d = 1 ∈ {1, 2}, and B6(iii) at d = 1 reduces to zeros(p) ≤ 3, which holds since zeros([1, 0, 1, 0, 1]) = 2 ≤ 3. B1: children(B₄, [1, 0, 1, 0, 1], 1) = {[1, 0, 1, 0, 1, 1]}, a contiguous prefix of length 1, witnessing prefix extension under a fresh namespace at d = 1.

State: B₄ = {[1], [1, 0, 1], [1, 0, 2], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 1]}.

Nelson's "Items 2.1, 2.2, 2.3, 2.4" is exactly this mechanism — successive baptisms under parent 2 at depth 1, yielding the sibling stream 2.1, 2.2, 2.3, 2.4 by repeated application of inc(·, 0). The sequence is determined, contiguous, and the ordinals carry no semantics beyond order.

**B7 Case 2 verified.** The steps above exercise only Case 1 of B7 (different stream lengths). We now trace Case 2 — non-nesting prefixes with equal element lengths. From state B₂ above, the parents [1, 0, 1] and [1, 0, 2] are both length 3, distinct, and neither is a prefix of the other (they disagree at position 3). Consider S([1, 0, 1], 1) and S([1, 0, 2], 1). Both streams have element length 4: #[1, 0, 1] + 1 = #[1, 0, 2] + 1 = 4. The prefixes are non-nesting — neither [1, 0, 1] ≼ [1, 0, 2] nor [1, 0, 2] ≼ [1, 0, 1] — so this is Case 2 with p = [1, 0, 1], d = 1, p' = [1, 0, 2], d' = 1.

At position 3 of each stream: c₁ = inc([1, 0, 1], 1) = [1, 0, 1, 1] and c'₁ = inc([1, 0, 2], 1) = [1, 0, 2, 1]. By S1, every cₙ ∈ S([1, 0, 1], 1) preserves [1, 0, 1] as prefix and hence has value 1 at position 3, and every c'ₘ ∈ S([1, 0, 2], 1) has value 2 at position 3. Sibling increments inc(·, 0) modify only position sig(·) — namely position 4 in both streams (TA5(c)) — so position 3 is invariant across both streams: always 1 in S([1, 0, 1], 1), always 2 in S([1, 0, 2], 1). By T1's lexicographic comparison resolving at the first position of disagreement, every element of S([1, 0, 1], 1) is distinct from every element of S([1, 0, 2], 1). The streams are disjoint.

**B7 Case 3 verified.** Case 3 — nesting prefixes with equal element lengths. Suppose node [1, 1] has been baptized via inc([1], 1) = [1, 1] (TA5(d) with k = 1: #t' = 2, zero intermediate zeros, position 2 set to 1). Consider S([1], 2) and S([1, 1], 1). Both streams have element length 3: #[1] + 2 = #[1, 1] + 1 = 3. The prefixes nest — [1] ≼ [1, 1] — so this is Case 3 with p = [1], d = 2, p' = [1, 1], d' = 1.

At position 2 of each stream: inc([1], 2) = [1, 0, 1] — the value at position 2 is 0, the zero separator produced by TA5(d) with d − 1 = 1 intermediate zero. inc([1, 1], 1) = [1, 1, 1] — the value at position 2 is p'₂ = 1 > 0 (by T4, valid addresses do not end in zero, so the last component of [1, 1] is positive). Sibling increments inc(·, 0) modify only the last component (TA5(c)), so position 2 is invariant across both streams: always 0 in S([1], 2), always 1 in S([1, 1], 1). The streams disagree at a fixed position and are therefore disjoint.

**B9 unbounded extent exhibited.** The trace so far stops at B₄ with hwm(B₄, [1], 2) = 2 — two children of [1] at depth 2 (the addresses [1, 0, 1] and [1, 0, 2] baptized in Steps 1 and 2; Step 4's d = 1 baptism contributed to a different namespace and left hwm at ([1], 2) unchanged). B9 (Unbounded Extent) asserts that for any target M ∈ ℕ, a finite sequence of further baptisms in this namespace reaches hwm ≥ M. We exhibit the construction concretely for M = 5: three additional baptisms suffice (since hwm currently equals 2). Each step is a single Bop transition on namespace ([1], 2); we record next(B, [1], 2), the postcondition state, the resulting children set, and the contiguous-prefix verification.

  **Step 5: third user.** Same namespace ([1], 2).

  next(B₄, [1], 2) = inc(max{[1, 0, 1], [1, 0, 2]}, 0) = inc([1, 0, 2], 0) = [1, 0, 3]

  TA5(c): sibling increment preserves length, advances position sig([1, 0, 2]) = 3, so the ordinal goes from 2 to 3. By B2, this is c_{hwm+1} = c₃. B6 holds as in Step 2 ((p, d) = ([1], 2) is unchanged). B5a: zeros([1, 0, 3]) = 1 = zeros([1, 0, 2]) — sibling preserves zeros. B1: children = {[1, 0, 1], [1, 0, 2], [1, 0, 3]} = {c₁, c₂, c₃}, contiguous prefix of length 3.

  State: B₅ = {[1], [1, 0, 1], [1, 0, 2], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 1], [1, 0, 3]}. hwm(B₅, [1], 2) = 3.

  **Step 6: fourth user.** Same namespace ([1], 2).

  next(B₅, [1], 2) = inc([1, 0, 3], 0) = [1, 0, 4]

  By B2, c_{hwm+1} = c₄. B1: children = {c₁, c₂, c₃, c₄}, contiguous prefix of length 4.

  State: B₆ = B₅ ∪ {[1, 0, 4]}. hwm(B₆, [1], 2) = 4.

  **Step 7: fifth user.** Same namespace ([1], 2).

  next(B₆, [1], 2) = inc([1, 0, 4], 0) = [1, 0, 5]

  By B2, c_{hwm+1} = c₅. B1: children = {c₁, c₂, c₃, c₄, c₅}, contiguous prefix of length 5.

  State: B₇ = B₆ ∪ {[1, 0, 5]}. hwm(B₇, [1], 2) = 5 = M.

The target hwm = 5 is reached in exactly three baptisms from B₄, witnessing B9 for the pair ((p, d), M) = (([1], 2), 5). The construction depends on no upper bound at position 3 of the stream: TA5(c) advances the ordinal value from 2 to 3 to 4 to 5 without consulting any ceiling, and the same step can be repeated indefinitely to grow the namespace through every natural number — the unbounded-component axiom T0(a). For any target M' > 5, an additional M' − 5 baptisms in ([1], 2) extend B₇ to a registry with hwm = M' along the same pattern. The trace exhibits the *bounded growth* construction of B9's proof: each individual baptism is a single Bop transition with the +1 increment that B1 preserves, and the finite sequence of such transitions reaches any prescribed M. Crucially, contiguity is maintained at every step — children(B₄, [1], 2) = {c₁, c₂}, children(B₅, [1], 2) = {c₁, c₂, c₃}, children(B₆, [1], 2) = {c₁, ..., c₄}, and children(B₇, [1], 2) = {c₁, ..., c₅} — so the trace simultaneously witnesses B9 (unboundedness) and B1 (contiguity) under iteration. The trace also illustrates that the unbounded-extent claim is structural, not an existence claim about distant or hypothetical states: each successor state Bₖ is reached by an explicit, single-step transition from the previous, and the registry remains finite at every step (B_fin), so unbounded extent does not require an infinite registry — only that no finite ceiling is imposed.


## Global uniqueness

**B8 (Global Uniqueness).** Distinct baptisms produce distinct addresses:

  `(A a, b : produced by distinct baptismal acts : a ≠ b)`.

Within the same namespace, B4 makes each baptize(p, d) a single edge of the transition graph; distinct same-namespace baptismal transitions occupy distinct edges and therefore evaluate next against distinct precondition states with distinct hwm values, and B1 ensures sequential, gap-free allocation, so distinct baptisms produce distinct stream indices, which S0 maps to distinct addresses. Across namespaces, B7 ensures non-overlapping ranges. Together, no two baptisms in any reachable state produce the same tumbler.

ASN-0034 establishes GlobalUniqueness from the algebraic angle through T3, T9, T10, and T10a. Here we reach the same conclusion through the set-theoretic lens of baptism namespaces and the contiguous prefix property. The two derivations are complementary: the algebraic route proceeds from allocator discipline (per-stream monotonicity), while the set-theoretic route proceeds from namespace partitioning (per-stream contiguity plus cross-stream disjointness). The algebraic route answers "why is each stream collision-free?"; the set-theoretic route answers "why are different streams collision-free with each other?"

*Proof.* We must show that for any two distinct baptismal acts β₁ and β₂, the addresses they produce are distinct. Let a be the address produced by β₁ in namespace (p, d), and b the address produced by β₂ in namespace (p', d'). We proceed by case analysis on whether the two baptisms target the same or different namespaces.

*Case 1: same namespace — (p, d) = (p', d').* By B4 (Atomic Baptism), each baptism is a single Op-transition, so β₁ and β₂ occupy distinct edges of the transition sequence. Without loss of generality, β₁ precedes β₂ in that sequence — the argument with roles exchanged is identical. Let Σ₁ be the state on which β₁ acts and Σ₂ the state on which β₂ acts. By the Bop postcondition, the successor state Σ₁' = β₁(Σ₁) has Σ₁'.B = Σ₁.B ∪ {a}, so a ∈ Σ₁'.B. Since β₁ precedes β₂, Σ₂ is reachable from Σ₁' through a (possibly empty) sequence of transitions — that is, Σ₁' →* Σ₂. B0★ (Multi-step Irrevocability), the labelled corollary of B0 covering finite transition sequences, gives Σ₁'.B ⊆ Σ₂.B, hence a ∈ Σ₂.B.

Let m₁ = hwm(Σ₁.B, p, d) and m₂ = hwm(Σ₂.B, p, d). By B2 (High Water Mark Sufficiency), a = c_{m₁+1} and b = c_{m₂+1}, where cₙ denotes the n-th element of S(p, d). Since a = c_{m₁+1} ∈ Σ₂.B and B1 (Contiguous Prefix) holds for Σ₂, the children of (p, d) in Σ₂ include {c₁, ..., c_{m₁+1}}, so hwm(Σ₂.B, p, d) ≥ m₁ + 1. That is, m₂ ≥ m₁ + 1, hence m₂ + 1 ≥ m₁ + 2 > m₁ + 1. The indices m₁ + 1 and m₂ + 1 are distinct with m₁ + 1 < m₂ + 1. By S0 (StreamOrdering), c_{m₁+1} < c_{m₂+1} under the lexicographic order T1. By T1 irreflexivity, c_{m₁+1} ≠ c_{m₂+1}. Therefore a ≠ b.

*Case 2: different namespaces — (p, d) ≠ (p', d').* By construction, a ∈ S(p, d) — baptism in namespace (p, d) produces the next element of its sibling stream — and b ∈ S(p', d') by the same reasoning. By B7 (Namespace Disjointness), S(p, d) ∩ S(p', d') = ∅, so a ≠ b.

The two cases are exhaustive: two baptisms either target the same namespace or they do not. In both cases a ≠ b. No two distinct baptisms, whether in the same namespace, across sibling namespaces, or at different hierarchical levels, can produce the same address. ∎

*Formal Contract:*
- *Preconditions:* β₁, β₂ are distinct baptismal acts in a system conforming to B0★ (which subsumes B0), B0a, B1, B4, and B7; β₁ produces a in namespace (p, d) and β₂ produces b in namespace (p', d'), where both (p, d) and (p', d') satisfy B6.
- *Postconditions:* `a ≠ b`.


## Unbounded growth

Nelson insists that the address space imposes no capacity limits:

> "A tumbler consists of a series of integers. Each integer has no upper limit."

**B9 (Unbounded Extent).** `(A p, d : B6(p, d) : (A M ∈ ℕ : (E Σ' : Σ →* Σ' via baptisms : hwm(Σ'.B, p, d) ≥ M)))`.

The quantifier ranges over reachable *states* rather than over abstract registries: `Σ →* Σ'` is the reflexive-transitive closure of the transition relation (introduced in *State Space and Transitions*) restricted to baptismal operations — that is, every step of the witnessing sequence is some `baptize(p_i, d_i) ∈ Op` and the registry at each intermediate state grows by exactly one element. The hwm is read off the Σ.B component of the witness state, not off a free-standing registry value. The earlier formulation "B' reachable from Σ.B by a finite sequence of baptisms" was loose in two ways: it elided the state-level transition structure on which reachability is defined (only Op induces →; registries do not transition among themselves), and it left the registry growth ungrounded in the wider state — concealing that the witness depends on a full successor state Σ' (which may also carry content, link, or ownership components) rather than a registry standing alone.

The quantifier matches Bop's precondition exactly: B9 asserts unbounded growth for every parent-depth pair that Bop admits as the target of a baptism, no more and no less. In particular, B9 does not presuppose `p ∈ Σ.B`; whether the parent must itself be baptized is the open question deferred above, and B9 should not implicitly answer it by tightening the quantifier.

No architectural limit constrains how many children a position may have. This follows from T0(a) (UnboundedComponents): since each tumbler component is an unbounded natural number and the child ordinal occupies a single component, the ordinal can grow without bound. Combined with B1, the children of any parent can grow to form an arbitrarily long contiguous prefix {c₁, ..., cₘ} for any m.

Nelson designed this deliberately: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — the process of baptism never exhausts any namespace. Between physical resource limits and address space design, there is a deliberate gap: the design guarantees infinite headroom, leaving capacity as a pure engineering concern.

Nelson reinforces this at every level: "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." The word "possible" does not mean "a finite number of possible" — it means the tree can always grow further. The address space is designed not for a known population but for indefinite proliferation.

*Proof.* We must show that for any pair (p, d) satisfying B6 and any bound M ∈ ℕ, there exists a state Σ' with Σ →* Σ' (via baptisms) such that hwm(Σ'.B, p, d) ≥ M. The argument is constructive: we exhibit the required sequence of baptismal transitions.

Let m = hwm(Σ.B, p, d) — the current count of children in namespace (p, d). If m ≥ M, set Σ' = Σ (the empty transition sequence witnesses Σ →* Σ via reflexivity) and the claim holds trivially. Otherwise m < M, and we construct a sequence of M − m baptismal transitions, each `baptize(p, d) ∈ Op` targeting namespace (p, d). We show by induction on k that k successive baptismal transitions Σ → Σ₁ → ... → Σₖ produce a state Σₖ with hwm(Σₖ.B, p, d) = m + k.

*Base case (k = 0).* Σ₀ = Σ with hwm(Σ.B, p, d) = m = m + 0. The claim holds by the reflexive case of →*.

*Inductive step.* Assume Σₖ is a state reachable from Σ by k baptismal transitions in namespace (p, d), with hwm(Σₖ.B, p, d) = m + k < M. We perform the transition `Σₖ → Σₖ₊₁` induced by `baptize(p, d) ∈ Op` — that is, Σₖ₊₁ = baptize(p, d)(Σₖ). The preconditions of Bop are satisfied: B6(p, d) holds by hypothesis; B4 (Atomic Baptism) is an invariant of the operation vocabulary — each `baptize(p, d) ∈ Op` is a single edge of the transition graph, so the constructed sequence is a chain of M − m successive edges with no shared structure.

By Bop, the postcondition gives Σₖ₊₁.B = Σₖ.B ∪ {next(Σₖ.B, p, d)}. By B2 (High Water Mark Sufficiency), next(Σₖ.B, p, d) = c_{m+k+1}, the (m + k + 1)-th element of the sibling stream S(p, d). This element is well-defined: the stream S(p, d) produces cₙ for every n ≥ 1, since c₁ = inc(p, d) ∈ T by TA5(d), and each cₙ₊₁ = inc(cₙ, 0) ∈ T by TA5(c). The final component of cₙ equals n — a value that grows without bound. That no ceiling constrains this component is precisely T0(a) (UnboundedComponentValues): for any bound M' ∈ ℕ, there exists a tumbler in T whose value at that position exceeds M'. The stream never exhausts its namespace.

The new element c_{m+k+1} is fresh — by the freshness argument of Bop, it does not appear in Σₖ.B. The contiguous prefix property is preserved — by B1 preservation under Bop, children(Σₖ₊₁.B, p, d) = {c₁, ..., c_{m+k+1}}. Therefore hwm(Σₖ₊₁.B, p, d) = m + k + 1. The B0a frame on the other components of Σₖ — content, links, ownership, ASN-0034's Act and nₛ — is left unconstrained by the present claim; Σₖ₊₁ may differ from Σₖ in those components however the corresponding ASNs' specifications permit, since B9 ranges over witness states that need only satisfy the Σ.B-component bound.

After M − m steps, hwm(Σ_{M−m}.B, p, d) = m + (M − m) = M. Setting Σ' = Σ_{M−m}, we have Σ →* Σ' via the M − m baptismal transitions, and hwm(Σ'.B, p, d) = M ≥ M. ∎

*Formal Contract:*
- *Preconditions:* (p, d) satisfying B6(p, d); M ∈ ℕ; current state Σ reachable from Σ_init.
- *Postconditions:* There exists Σ' with Σ →* Σ' via a finite sequence of baptismal transitions such that hwm(Σ'.B, p, d) ≥ M.
- *Axiom:* T0(a) — component values in T are unbounded; ℕ is closed under successor.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.B | B ⊆ T — the set of baptized tumblers (baptismal registry) | introduced |
| S(p,d) | Sibling stream: c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0) | from TA5(b), TA5(c), TA5(d) |
| hwm(B,p,d) | High water mark: #children(B, p, d) — sufficient allocation statistic | from B1, S0 |
| next(B,p,d) | Next address: if children = ∅ then inc(p, d) else inc(max(children), 0) | from TA5(c), TA5(d), T1 |
| Bop | baptize(p, d): PRE B6; STRUCT B4 (invariant of Op, not per-call); POST Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}; FRAME constrains Σ.B only, silent on other components (incl. ASN-0034's Act, nₛ) | from B0, B1, B4, B6, B7, B0a, B10, TA5, TA5a |
| S0 | `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — stream strictly ordered | from ASN-0034 T10a.7 (EnumerationInjectivity) |
| S1 | `(A n : n ≥ 1 : p ≼ cₙ)` — all stream elements extend parent | from TA5(b), TA5(c), TA5(d) |
| S2 | `p_{#p} = 0 ⟹ S(p, 1) = S(p′, 2)` (p′ = p without trailing zero) — trailing-zero stream identity | from TA5(d) |
| B0 | `Σ.B ⊆ Σ'.B` for all transitions — irrevocability (extends T8) | primitive label (B0a-derivation is given as commentary preceding the B0 statement, not as a labelled corollary; cited by B1, B10) |
| B0★ | `Σ.B ⊆ Σ'.B` for all Σ →* Σ' (reflexive-transitive closure of transitions) — multi-step irrevocability | labelled corollary of B0; cited by B8 (Case 1) and by the Bridge1 commentary and wp-analysis lift |
| B0a | Op partitions into baptismal operations (the `baptize(p, d)` for B6-valid (p, d), each acting on Σ.B as in Bop) and Σ.B-frame operations (every other op satisfies `op(Σ).B = Σ.B`) — registry grows only through baptism | design requirement |
| B₀ conf. | B₀ is finite, `children(B₀, p, d)` is a contiguous prefix for all (p, d), and `(A t ∈ B₀ : t satisfies T4)` — seed conformance | design requirement |
| B_fin | `(A Σ reachable : Σ.B is finite)` — registry finiteness | from B₀ conf., B0a |
| B_type | `(A Σ reachable : Σ.B ⊆ T)` — registry typing (every baptized address is a well-formed tumbler) | from B₀ conf., B0a, B6, TA5(c), TA5(d), B_fin |
| B1 | `cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B)` — contiguous prefix (requires conforming B₀) | from B₀ conf., B0, B0a, B4, B6, B7, B10, next def., S0, TA5(c); Bop correctness follows as corollary |
| B2 | `next(B, p, d) = c_{hwm+1}` — high water mark sufficiency (from B1) | from B1, S0, NextAddress |
| B3 | Forward requirement on a future predicate `Occupied : T × 𝒮 → {⊤, ⊥}`: `(A Σ reachable, t ∈ T : Occupied(t, Σ) ⟹ t ∈ Σ.B)` — content permitted only at baptized addresses; ghost elements (`t ∈ Σ.B ∧ ¬Occupied(t, Σ)`) explicitly allowed | forward requirement on future ASN |
| Bridge1 | `(A Σ, Σ', A, a : Σ → Σ' ∧ a ∈ domₛ'(A) ∖ domₛ(A) : (E! (p, d) satisfying B6 : Σ' = baptize(p, d)(Σ) ∧ a = next(Σ.B, p, d)))` — allocator-extension transitions are *uniquely* realized by baptismal operations adding the same address to Σ.B (uniqueness from B7) | forward requirement on activation-discipline ASN |
| Bridge2 | `allocated(Σ_init) ⊆ B₀` — every address in an allocator's initial realized domain is a seed element | forward requirement on activation-discipline ASN |
| B4 | Each `baptize(p, d) ∈ Op` is a single atomic transition: `baptize(p, d)(Σ).B = Σ.B ∪ {next(Σ.B, p, d)}` is computed and committed in one step, with no intermediate observable state | design requirement |
| B5 | `zeros(inc(p, d)) = zeros(p) + (d − 1)` — field advancement | from TA5(b), TA5(d) |
| B5a | `zeros(inc(t, 0)) = zeros(t)` — sibling increment preserves zeros | from TA5(c) |
| B6 | `p satisfies T4`, `d ∈ {1, 2}`, and `zeros(p) + (d − 1) ≤ 3` — valid depth | from T4, TA5, B5 |
| B7 | `(p, d) ≠ (p', d') ⟹ S(p, d) ∩ S(p', d') = ∅` — namespace disjointness | from T3, T4, T10, S1, TA5(d), T10a.1 (uniform length), B6 |
| B8 | Distinct baptisms produce distinct addresses — global uniqueness | from B0★, B1, B2, B4, B7, S0, T1 |
| B9 | `(A p, d : B6(p, d) : (A M ∈ ℕ : (E Σ' : Σ →* Σ' via baptisms : hwm(Σ'.B, p, d) ≥ M)))` — unbounded extent | from T0(a), B1, B2, B4, B6, Bop, TA5(c), TA5(d) |
| B10 | `(A t ∈ Σ.B : t satisfies T4)` — registry-wide T4 validity | from B₀ conf., B0a, B6, TA5(c), TA5a |


## Open Questions

- Must a parent position be baptized before children can be baptized beneath it? Nelson's ownership model implies yes; Gregory's implementation does not check at structural levels. Resolution depends on the ownership model (Tumbler Ownership).
- What concrete seed sets B₀ are valid — which root configurations satisfy B₀ conformance while providing a viable system genesis?
- Must the specification distinguish between a ghost element that could hold content and a structural position that cannot — or is this distinction derivable from the field structure alone?
- Under what conditions may bulk allocation — baptizing a contiguous range of k positions in a single operation — satisfy B4's atomicity and B1's contiguity requirements?
- What must a distributed system guarantee about cross-replica baptism ordering to maintain global address uniqueness without centralized coordination?
- Does the abstract specification require a single canonical depth d for each parent level, or may a parent simultaneously baptize children at both d = 1 and d = 2?
- What is the minimal serialization grain for baptism — must operations be serialized per-parent per-depth, or per-parent across all depths?
- What invariants must element-level subspace partitioning (T7) satisfy so that the contiguous prefix property holds independently within each subspace?
