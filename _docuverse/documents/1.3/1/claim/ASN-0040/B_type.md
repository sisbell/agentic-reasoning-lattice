**B_type (RegistryTyping).** `(A Σ : Σ reachable from Σ_init : Σ.B ⊆ T)` — every baptized address is a well-formed tumbler.

*Proof.* By joint induction with B_fin (Registry Finiteness, stated below) on the number of state transitions from the initial state. The two invariants are coupled by Case 2 of the inductive step: that case selects max(children(B, p, d)), whose existence requires children to be a finite set — a fact licensed by B_fin at the same precondition state. We carry B_type and B_fin together through the induction; the standalone B_fin proof presented later in the ASN records the finiteness component of this single joint induction, labelled separately for downstream citation. Forward references from B_type's case analysis to B_fin therefore refer to a hypothesis the joint inductive frame supplies at the same step, not to a separately established theorem.

*Base case.* In the initial state, Σ.B = B₀. By B₀ conf. (SeedConformance), every t ∈ B₀ satisfies T4; T4 is a property of well-formed tumblers (T4 ranges over T by definition in ASN-0034), so every t ∈ B₀ inhabits T (giving B_type at genesis), and B₀ is finite (giving B_fin at genesis). Both invariants hold at the initial state.

*Inductive step.* Assume B_type and B_fin both hold for state Σ with registry B — that is, B ⊆ T and B is finite. Consider a transition Σ → Σ' producing registry B'. By B0a (Baptismal Closure), Op partitions into Σ.B-frame operations and baptismal operations; we treat the two transition classes in turn.

*Σ.B-frame transitions.* If the transition is induced by a Σ.B-frame operation, then Σ'.B = Σ.B — that is, B' = B. Therefore B' = B ⊆ T by the inductive hypothesis, and B_type holds at B'. (Finiteness likewise transfers: B' = B is finite.)

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
