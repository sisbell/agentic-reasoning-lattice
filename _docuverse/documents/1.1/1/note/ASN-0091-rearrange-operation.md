# ASN-0091: REARRANGE Operation
*2026-05-26*

We seek a precise account of rearrangement — the operation by which segments of a document's content stream are reordered without altering the content itself. The naive picture — that moving text "creates new positions" and "destroys old ones" — implies catastrophic consequences: every link attached to the moved content would break, every cross-document transclusion would dangle, and the historical record of what was contained where would dissolve. None of these failures may occur. Our task is to derive precisely why, and to identify what does change and what cannot.

Our starting commitment is the separation of two streams. The content store `Σ.C : T ⇀ Val` is permanent and append-only: once an address `a` enters `dom(Σ.C)`, it remains there bound forever to its initial value (foundation invariant C0/S0). The arrangement `Σ.M(d) : T ⇀ T` for each document `d ∈ dom(Σ.M)` is a partial function from V-positions to I-addresses recording how the document currently presents its contents in linear order. The arrangement is mutable; the content store is not. The link store `Σ.L : T ⇀ EndsetSequence` is also append-only and immutable on existing keys (foundation invariant L12). Rearrangement, by its name, can affect only the arrangement — the entire question is what this restriction lets us prove.

## REARRANGE as Vstream-Only Operation

Let us define the class of transitions REARRANGE belongs to. Its structural core is supplied by the foundation: ASN-0084's **ArrangementRearrangement** is a transition `Σ → Σ'` on a document `d` for which `dom(Σ'.M(d)) = dom(Σ.M(d))`, `Σ'.C = Σ.C`, `Σ'.M(d') = Σ.M(d')` for every `d' ≠ d`, and there exists a bijection `π : dom(Σ.M(d)) → dom(Σ'.M(d))` satisfying `Σ'.M(d)(π(v)) = Σ.M(d)(v)` for every `v ∈ dom(Σ.M(d))`. We adopt this definition rather than reprove it, and extend it.

A transition `Σ → Σ'` is *Vstream-only on `d`* when it is an ArrangementRearrangement on `d` (ASN-0084) — additionally registered, framed on the components ASN-0084 leaves unconstrained, and admissible. The ArrangementRearrangement core supplies the domain clause
```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RA-dom)
```
the rearrangement equation under the bijection `π : dom(Σ.M(d)) → dom(Σ'.M(d))`
```
(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))                                    (RA-π)
```
and the content and other-document frame conjuncts `Σ'.C = Σ.C` and `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`. The Vstream-only class adds the registration precondition
```
d ∈ dom(Σ.M)                                                                            (RA-reg)
```
and the full frame, fixing the content store `C`, the link store `L`, the entity set `E`, the provenance relation `R`, the document registry, and every other document's arrangement
```
Σ'.C = Σ.C  ∧  Σ'.L = Σ.L  ∧  Σ'.E = Σ.E  ∧  Σ'.R = Σ.R                                 (RA-frame)
  ∧  dom(Σ'.M) = dom(Σ.M)
  ∧  (A d' ∈ dom(Σ.M) : d' ≠ d : Σ'.M(d') = Σ.M(d'))
```
and the admissibility constraint
```
every per-state foundation invariant satisfied by Σ is satisfied by Σ'                  (RA-adm)
```

The bijection π is the *rearrangement permutation*. It is not in general unique: when `Σ.M(d)` has shared I-addresses (allowed by foundation S5/UnrestrictedSharing), any witness π must biject each I-address's pre-state pre-image set onto its post-state pre-image set, but the assignment within each such block is free, so distinct bijections can witness a single transition `Σ → Σ'`.

The abstract class admits two degenerate cases. The *empty case* `dom(Σ.M(d)) = ∅` is admitted: π is the empty bijection and every claim holds vacuously. REARRANGE_K excludes it via R-PRE(iv) (the affected range `{v : c₀ ≤ v < c_{n−1}}` must lie in `V_S(d)`) together with CS2's strict cut ordering, so `V_S(d) ≠ ∅` is a precondition of every REARRANGE_K invocation. The *identity case* π = id is admitted, with `Σ' = Σ` derived in two steps: first, RA-π under π = id reads `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ.M(d))`, and combined with RA-dom (`dom(Σ'.M(d)) = dom(Σ.M(d))`) this gives `Σ'.M(d) = Σ.M(d)` as partial functions; second, RA-frame preserves every other state component verbatim — `Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, `dom(Σ'.M) = dom(Σ.M)`, and `Σ'.M(d') = Σ.M(d')` for every `d' ≠ d` — so the only component left to pin is `Σ.M(d)` itself, which step one supplies. Together these force `Σ' = Σ`, after which RA-adm is trivially satisfied.

## REARRANGE_K Realises the Abstract Class

REARRANGE_K (the cut-sequence operation of ASN-0084) is one concrete realisation of the abstract Vstream-only class. The clause-by-clause argument below establishes that its π is an admissible K.μ~ bijection.

### Clause Correspondences and Per-Invariant Discharges

ASN-0047's K.μ~ precondition `d ∈ E_doc` discharges RA-reg directly: ASN-0047's M1 (ArrangementMonotonicity) records the identification `dom(M) = E_doc`, so `d ∈ E_doc ⟺ d ∈ dom(M)` and RA-reg holds at the pre-state.

*Net-effect split.* REARRANGE_K's cut-sequence construction makes π non-identity automatically: by CS2 the cuts satisfy `c₀ < c₁ < ...`, so the region widths `w_α`, `w_β` (and `w_μ` for 4-cut) are each `≥ 1`, giving `π(c₀) > c₀` (R-PPERM for 3-cut, R-SPERM for 4-cut). But `π ≠ id` as a permutation of V-positions is strictly weaker than ASN-0047's K.μ~ admissibility clause (ii), the non-trivial *net effect* `M'(d) ≠ M(d)`. The two come apart precisely under shared I-addresses: when the affected range carries a repeating I-address pattern whose period matches the permutation's displacement, R-P1/R-P2 may yield `M'(d) = M(d)` although π is the non-identity rotation. Such an arrangement is permitted because S2 (ArrangementFunctionality) imposes *only* functionality on `M(d)` — at most one image per V-position — and never a single-image (injectivity) constraint, so the same I-address may sit at several V-positions; a permutation that maps each shared-image V-position to another V-position carrying the same image leaves the map pointwise unchanged. The realisation therefore splits on net effect, with a realiser in each case. In the *non-trivial case* (`M'(d) ≠ M(d)`) the realiser is the named composite K.μ~. In the *collapse case* (`M'(d) = M(d)` with π ≠ id) the transition is the identity `Σ' = Σ`, so RA-adm holds and every RE-* claim below is an identity of `Σ` with itself.

*K.μ~ admissibility clause (i)–(v) ← discharge.*

| Clause | Discharge |
|--------|-----------|
| (i) induced post-state satisfies the shape package (S8a, S8-depth, D-CTG★, D-MIN★) | split by predicate kind. (a) S8a (`zeros(v) = 0`, `#v ≥ 2`, positive components) is a *per-position* predicate: by RA-dom the domain is unchanged (`dom(Σ'.M(d)) = dom(Σ.M(d))`), so each surviving position satisfies S8a at Σ' exactly as it did at Σ. (b) D-CTG★, D-MIN★, and S8-depth are *set-level* predicates of `V_S(d)`; since `subspace(v)` is a function of `v` alone, RA-dom forces `V_S(Σ'.M(d)) = V_S(Σ.M(d))` for every subspace S, so each set-level predicate carries over verbatim. The bijection π reshuffles images but leaves the populated V-position set fixed, so it is irrelevant to (b) |
| (ii) non-trivial net effect `M'(d) ≠ M(d)` | holds by hypothesis in the non-trivial case of the net-effect split established above |
| (iii) length-preserving `#π(v) = #v` | from the construction: each affected source position `v = cᵢ + j` and its image are ordinal shifts of a depth-2 cut, so by CS4 (`#cᵢ = 2`) and ASN-0034's OrdinalShift length identity `#shift(t, n) = #t`, `#π(v) = #v = 2`; exterior and non-S positions are fixed pointwise by R-PPERM/R-SPERM |
| (iv) subspace-preserving `subspace(π(v)) = subspace(v)` | Directly from the R-PPERM/R-SPERM branch structure: non-S and in-S-exterior positions are fixed (`π(v) = v`), so subspace is trivially preserved; every affected-range position `v` has the cut subspace S (by CS3), and R-PPERM/R-SPERM map it to a position of the form `c₀ + (offset)`, which shares c₀'s subspace S, so `subspace(π(v)) = S = subspace(v)` (ASN-0036's OrdShiftHom(a)). Discharged from the cut-sequence construction alone |
| (v) link-subspace fixing `π(v) = v` on the link subspace | RE-sub: by CS3 the cut subspace is `S = s_C`, so every `subspace(v) = s_L` V-position lies on R-PPERM/R-SPERM's non-S branch, which sets `π(v) = v` pointwise |

RA-adm requires that every per-state foundation invariant holding at Σ hold at Σ'. A per-state invariant holds at every reachable state — ASN-0047's ExtendedReachableStateInvariants gives the per-state foundation invariants at any reachable state — so it suffices to establish Σ' reachable, which we now do.

*Standing premise of the REARRANGE_K realisation.* Σ is reachable from Σ₀ by a finite sequence of elementary transitions drawn from valid composites. Under this premise we extend reachability across the REARRANGE_K step.

In the non-trivial case, K.μ~'s admissibility clauses (i)–(v) are closed above; this is only the first clause of ValidComposite★ (ASN-0047), the intra-composite sequencing condition. Its second clause — the initial-to-final coupling constraints J0, J1★, J1'★ — is discharged by J3 (ReorderingIsolation, ASN-0047): J3 gives `C' = C ∧ L' = L ∧ E' = E ∧ R' = R` across the composite, so J0 holds vacuously (no content is allocated) and J1★ is vacuous (no range-new content arises), with J1'★ vacuous for the same reason. Both clauses thus met, K.μ~ is a valid composite. Its K.μ⁻ + K.μ⁺ elementary decomposition (ASN-0047) is then a finite sequence of elementary transitions drawn from a valid composite; appending it to any trace witnessing reachability of Σ yields a trace witnessing reachability of Σ', which sits at the resulting composite boundary. In the collapse case `M'(d) = M(d)`, the REARRANGE_K transition is the identity `Σ' = Σ`; clause (ii) excludes `M'(d) = M(d)`, so K.μ~ is unavailable and none is owed. The realiser is the *empty* sequence of elementary transitions — admitted by ASN-0047's SequentialTransitionAxiom, whose reflexive-transitive closure `Σ →* Σ'` ranges over finite, possibly empty, sequences — which satisfies every elementary precondition vacuously and carries `Σ' = Σ`, so reachability of Σ' is immediate from reachability of Σ. In both cases Σ' is reachable; since the per-state foundation invariants hold at every reachable state, RA-adm holds for the REARRANGE_K realiser. The binary transition invariants fall outside the per-state list ("State-Component-Only Invariants" below).

### State-Component-Only Invariants

The binary transition invariants — those of the form `(A Σ → Σ' :: …)`, relations on the *pair* of states rather than per-state predicates, and so outside the per-state foundation list RA-adm discharges above — are discharged by **transition-satisfaction**: the REARRANGE transition `Σ → Σ'` satisfies each because the components it constrains are pinned by RA-frame, making every conjunct trivially true. This class comprises ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity) — both satisfied by `Σ'.C = Σ.C`, which simultaneously gives `dom(C) ⊆ dom(C')` and value preservation — ASN-0093's M1 (ArrangementMonotonicity, `dom(M) ⊆ dom(M')` from `dom(Σ'.M) = dom(Σ.M)`), the permanence invariants P0, P1, P2, P3 (each a `component(Σ) ⊆ component(Σ')` plus value-preservation conjunction, satisfied by the matching frame clause: P0 by `Σ'.C = Σ.C`, P1 by `Σ'.E = Σ.E`, P2 by `Σ'.R = Σ.R`, and P3 — the synthesis P0 ∧ P1 ∧ P2 ∧ L12 — by all four together), L12 (LinkImmutability, by `Σ'.L = Σ.L`), and ASN-0093's C0 (ContentImmutability, by `Σ'.C = Σ.C`).

(S5/UnrestrictedSharing is an existential theorem over the model class, not a per-state invariant, so RA-adm does not range over it.)

## What the Content Store Sees: Nothing

The first consequence of RA-frame is immediate. **Content-Store Invariance**:
```
Σ'.C = Σ.C                                                                              (RE-C)
```
No content is allocated, freed, or modified by rearrangement. Every I-address in `dom(Σ.C)` retains its bound value; no new I-address enters `dom(Σ.C)`; the function `Σ.C` is literally unchanged. This is the architectural reason rearrangement cannot disturb content identity: the layer where identity lives is untouched.

The same observation applies symmetrically to the link store via RA-frame.

## Domain Stability and Range Invariance

RA-dom asserts `dom(Σ'.M(d)) = dom(Σ.M(d))` directly. Every V-position that was populated in d remains populated; every V-position that was unpopulated remains unpopulated. For REARRANGE_K specifically, this equality is the domain clause of ASN-0084's PivotPostcondition/SwapPostcondition.

**Domain Stability**:
```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RE-dom)
```

This distinguishes rearrangement from contraction (which removes V-positions) and from extension (which adds them). Rearrangement is the unique transition class that touches the arrangement's *structure* without changing its *support*.

The bijection further makes the range — viewed as a set or as a multiset — a permutation of itself. We derive the conclusion uniformly across every registered document via a two-case argument: the target document `d` via the π-bijection, and every other registered document via RA-frame's other-document clause. For the target document `d`, compute:
```
ran(Σ'.M(d)) = {Σ'.M(d)(v') : v' ∈ dom(Σ'.M(d))}
             = {Σ'.M(d)(π(v)) : v ∈ dom(Σ.M(d))}        [π bijects dom onto itself]
             = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}             [RA-π]
             = ran(Σ.M(d))
```
For every other registered document `d' ∈ dom(Σ.M)` with `d' ≠ d`, RA-frame's other-document clause `Σ'.M(d') = Σ.M(d')` forces `ran(Σ'.M(d')) = ran(Σ.M(d'))` trivially, since identical partial functions have identical ranges. Combining the two cases delivers range invariance uniformly across every registered document.

**Range Invariance**:
```
(A d' ∈ dom(Σ.M) :: ran(Σ'.M(d')) = ran(Σ.M(d')))                                      (RE-ran)
```

Lifting to multisets: for each I-address `a` and each registered document `d'`, define `μ_a(M(d')) = |{v : v ∈ dom(M(d')) ∧ M(d')(v) = a}|`. The same two-case argument applies. For the target document `d`, by injectivity of π on a finite set (dom(M(d)) is finite by S8-fin):
```
μ_a(Σ'.M(d)) = |{v' : v' ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v') = a}|
             = |{π(v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|       [substitute v' = π(v)]
             = |{v : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|           [π injective]
             = μ_a(Σ.M(d))
```
For every other registered document `d' ∈ dom(Σ.M)` with `d' ≠ d`, RA-frame's other-document clause gives `Σ'.M(d') = Σ.M(d')`, whence `μ_a(Σ'.M(d')) = μ_a(Σ.M(d'))` trivially — the multiplicity of `a` is a function of the arrangement alone, which is fixed.

**Per-Address Multiplicity Invariance**:
```
(A a ∈ T, d' ∈ dom(Σ.M) :: μ_a(Σ'.M(d')) = μ_a(Σ.M(d')))                              (RE-μ)
```

Together, RE-ran and RE-μ are the formal content of Nelson's "the document afterward contains exactly the same set of content as before — no additions, no losses, no duplications." Range invariance says the set is identical. Multiplicity invariance says each I-address appears the same number of times. The arrangement is a permutation, not a transformation.

## Where Position Lives After Rearrangement

Every (V, I) pair in the pre-state has an image (V, I) pair in the post-state: the pre-state pair `(v, M(d)(v))` corresponds to the post-state pair `(π(v), M(d)(v))`. The I-address is the same; the V-position has moved. This is the precise sense in which "every byte retains its identity": the byte associated with I-address `M(d)(v)` is still in d, now at V-position `π(v)`.

Conversely, for each post-state V-position `v'`, the pre-image `π⁻¹(v')` is the V-position that previously held the I-address now at `v'`. The map π⁻¹ recovers, for each post-state V-position, the V-position it migrated from.

What changed is not which I-addresses are in d, nor which V-positions are populated, but which V-position holds which I-address. Any valid bijection π witnessing the transition is the entire content of the rearrangement.

## Links Persist; Their Coverage Cannot Move

The link store is fixed by RA-frame:
```
dom(Σ'.L) = dom(Σ.L)  ∧  (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))                          (RE-L)
```

Every link persists across rearrangement with its full endset sequence intact. No link is added, removed, or modified.

Coverage of an endset is a function of the endset's span representation alone (ASN-0098). Since RE-L preserves every endset verbatim, coverage is preserved — RE-cov is ASN-0098's LP3 (CoverageInvariance) instantiated at a REARRANGE step:
```
(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| :: coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))   (RE-cov)
```

This is the formal precipitate of Nelson's "links between bytes can survive rearrangements." A link's reference structure is keyed to I-addresses (via spans on the I-address space). The I-addresses are unchanged. So the reference structure is unchanged.

## Discoverability Is Preserved

A link is *discoverable from* document `d` at state `Σ` when some endset's coverage intersects the document's I-address range — when there exists a slot `i` with `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅` (the characterisation supplied by foundation lemma LP12 of ASN-0098). The claim below quantifies `d` over every registered document — the rearrangement target *and* every non-target. Each citation below applies at any such `d`: RE-cov is uniform over all links and slots and is independent of `d`, and RE-ran is uniform over all `d ∈ dom(Σ.M)`. Combining them:
```
discoverable_from(a, d, Σ')
  ⟺ (E i :: coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
  ⟺ (E i :: coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
  ⟺ discoverable_from(a, d, Σ)
```

**Discoverability Invariance**:
```
(A a ∈ dom(Σ.L), d ∈ dom(Σ.M) :: discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ))    (RE-disc)
```

The set of links that can be found from d is exactly the same before and after rearrangement. This is the strong sense of link survivability: not merely that links persist as objects, but that their *relationships* to documents — the answer to "is this link reachable from here?" — are unchanged.

## Projection Transports Along π

Where a link's coverage strikes the arrangement is the set `project(e, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`. We derive its transport across REARRANGE in two cases: at the rearrangement target `d_tgt`, where the bijection π acts non-trivially; and at any non-target document `d ≠ d_tgt`, where RA-frame's other-document clause forces stability directly. The two cases combine under a uniform formulation below.

*Target case.* For `d = d_tgt`, the bijection π carries the projection set faithfully to the post-state:
```
project(e, d_tgt, Σ') = π(project(e, d_tgt, Σ))
```
We prove this abstractly, from RA-π and the state-independence of coverage alone. For any `v ∈ dom(Σ.M(d_tgt))`:
```
v ∈ project(e, d_tgt, Σ)
  ⟺ Σ.M(d_tgt)(v) ∈ coverage(e)              [definition of project]
  ⟺ Σ'.M(d_tgt)(π(v)) ∈ coverage(e)          [RA-π: Σ'.M(d_tgt)(π(v)) = Σ.M(d_tgt)(v)]
  ⟺ π(v) ∈ project(e, d_tgt, Σ')             [definition; π(v) ∈ dom(Σ'.M(d_tgt)) by RA-π's codomain]
```
The middle step uses that `coverage(e)` is a fixed function of the endset's spans, identical at Σ and Σ', so the membership test consults the same set on both lines. Since π bijects `dom(Σ.M(d_tgt))` onto `dom(Σ'.M(d_tgt))` (RA-π), this pointwise biconditional lifts to the set equality. The derivation rests only on RA-π and coverage state-independence, so it holds for every Vstream-only realiser. For the REARRANGE_K realiser specifically, this set equality is exactly ASN-0098's LP11 (ReorderingBijection) instantiated at `Σ' = K.μ~(Σ)`.

*Non-target case.* For any `d ≠ d_tgt`, RE-other gives `Σ'.M(d) = Σ.M(d)` entirely, so the projection is identical at both states: `project(e, d, Σ') = project(e, d, Σ)`. The bijection π (which acts on `dom(Σ.M(d_tgt))`, not on `dom(Σ.M(d))`) plays no role.

*Uniform formulation.* Define the *projection transport* `π̂_d`: `π̂_d := π` when `d = d_tgt` and `π̂_d := id_{dom(Σ.M(d))}` when `d ≠ d_tgt`. The identity case is well-typed because RE-other forces `dom(Σ'.M(d)) = dom(Σ.M(d))` for `d ≠ d_tgt`, so `π̂_d` is in every case a bijection between `dom(Σ.M(d))` and `dom(Σ'.M(d))`. The two cases combine as
```
project(e, d, Σ') = π̂_d(project(e, d, Σ))      for every d ∈ dom(Σ.M)                  (RE-proj)
```

A reader who follows the link arrives at the same I-address it always identified — but its V-position in d's current arrangement may have changed. This is Nelson's "arrive at the same content, regardless of its new position": the link follows content identity, not arrangement.

## Run Decomposition Is Not Invariant

Up to now every property has been preserved. The bijection's effect lies elsewhere: the *structure* of the (V, I) mapping — the way contiguous V-intervals correspond to contiguous I-intervals — can change.

A maximal run in `M(d)` is a triple `(v, a, n)` with `M(d)(v + k) = a + k` for `0 ≤ k < n`, maximal in the sense that it cannot be extended at either end. The canonical maximal-run decomposition is unique (per the foundation's bundle algebra in ASN-0058). Its cardinality measures how "structured" the arrangement is — fewer runs means longer contiguous mappings.

Rearrangement can fragment runs. Take a maximal run `(v, a, n)` with `n ≥ 2` in `Σ.M(d)`, and suppose π displaces position `v` to a location not adjacent to π(v + 1). Then the post-state arrangement no longer has a contiguous V-interval mapping to the I-interval `[a, a + n)`. The single pre-state run resolves into multiple post-state runs.

Symmetrically, rearrangement can coalesce runs. Take two singleton runs `([v₁], a₁, 1)` and `([v₂], a₂, 1)` in `Σ.M(d)` with `a₂ = a₁ + 1` but `v₂ ≠ v₁ + 1` (the I-addresses are chain-consecutive but the V-positions are not contiguous), and suppose π brings them V-adjacent in the post-state (i.e., π(v₁) and π(v₂) satisfy π(v₂) = π(v₁) + 1). Then the post-state has a 2-run `([π(v₁)], a₁, 2)` where the pre-state had two singletons.

> **Fragmentation Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly greater than that of `Σ.M(d)`. (RE-frag)

> **Coalescence Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly less than that of `Σ.M(d)`. (RE-coal)

> **Cardinality Invariance Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` equals that of `Σ.M(d)`. (RE-eq)

Together, RE-frag, RE-coal, and RE-eq record that the maximal-run-decomposition cardinality is *neither monotonically non-decreasing nor monotonically non-increasing nor invariant* under REARRANGE — every relation between pre- and post-state cardinality (strict increase, strict decrease, equality) is realizable.

**Direct witness (fragmentation).** Take pre-state `Σ.M(d)` populated only on the content subspace with V-positions `[1, 1], [1, 2], [1, 3]` mapping to a single maximal run `([1, 1], a, 3)` — that is, `Σ.M(d)([1, k]) = a + (k − 1)` for `k ∈ {1, 2, 3}` — and with the link subspace empty (`V_{s_L}(d) = ∅`). The total canonical maximal-run cardinality therefore equals the content-subspace cardinality. Pre-state total run cardinality: 1.

Apply REARRANGE_K with cut sequence `(c₀, c₁, c₂) = ([1, 1], [1, 2], [1, 4])`, a 3-cut pivot with `w_α = ord(c₁) − ord(c₀) = 1` and `w_β = ord(c₂) − ord(c₁) = 2`. R-PRE(iv) is discharged because every depth-2 position `v` with `[1, 1] ≤ v < [1, 4]` — namely `[1, 1], [1, 2], [1, 3]` — lies in `V_S(d)`. By ASN-0084's R-P1 (`Σ'.M(d)(c₀ + j) = Σ.M(d)(c₁ + j)` for `0 ≤ j < w_β`): `Σ'.M(d)([1, 1]) = Σ.M(d)([1, 2]) = a + 1` and `Σ'.M(d)([1, 2]) = Σ.M(d)([1, 3]) = a + 2`. By R-P2 (`Σ'.M(d)(c₀ + w_β + j) = Σ.M(d)(c₀ + j)` for `0 ≤ j < w_α`): `Σ'.M(d)([1, 3]) = Σ.M(d)([1, 1]) = a`.

Post-state arrangement: `[1, 1] ↦ a + 1`, `[1, 2] ↦ a + 2`, `[1, 3] ↦ a`. The maximal runs of `Σ'.M(d)` are `([1, 1], a + 1, 2)` (since `(a + 1) + 1 = a + 2 = Σ'.M(d)([1, 2])`, but `(a + 2) + 1 ≠ a = Σ'.M(d)([1, 3])`) and `([1, 3], a, 1)` (no extension possible). Post-state run cardinality: 2 — strictly greater than the pre-state cardinality 1.

A consequence for endset projection: if a pre-state contiguous V-interval `[v, v + n)` is in `project(e, d, Σ)`, the post-state image `π([v, v + n))` may consist of multiple disjoint V-intervals. The projection transports faithfully via π (RE-proj) — preserving cardinality (π is a bijection on a finite set) and the underlying I-addresses that the projection identifies (RA-π pins each `Σ'.M(d)(π(v)) = Σ.M(d)(v)`) — but the V-positions themselves are permuted, and the V-geometry — the decomposition of the projection into contiguous V-runs — is not preserved. This is the formal account of Nelson's "the endset becomes a discontiguous set of bytes" when a linked span is split.

**Reverse witness (coalescence).** Take pre-state `Σ.M(d)` with V-positions `[1, 1] ↦ a + 1`, `[1, 2] ↦ c`, `[1, 3] ↦ a`, where `a + 1` and `a` are consecutive content addresses (both produced by the same sub-allocator chain `A_X` of some document `d_X` in subspace `s_X`) and `c` is an I-address allocated from a different sub-allocator chain `A_Y` of some `(d_Y, s_Y) ≠ (d_X, s_X)`. The two singletons at `[1, 2]` and `[1, 3]` could merge into a single run only if `c + 1 = a` (the chain-adjacency condition under which `a` is the chain successor of `c` within a single chain); symmetrically, the singletons at `[1, 1]` and `[1, 2]` could merge only if `c = (a + 1) + 1 = a + 2` (the chain-adjacency condition under which `c` is the chain successor of `a + 1`). Both chain-adjacency conditions fail by the following inline lemma, used repeatedly below.

> **Inline lemma (ChainDisjointAdjacency).** For chain elements `x ∈ A_{s_X}(d_X)` and `y ∈ A_{s_Y}(d_Y)` with `(d_X, s_X) ≠ (d_Y, s_Y)` — i.e., the two sub-allocator chains differ in either their home document or their subspace — neither `x + 1 = y` nor `y + 1 = x` can hold. *Precondition fixing the successor identification.* Sub-allocator chain elements are T4-valid (ChainElementT4Validity, ASN-0093), so for every chain element `x` we have `sig(x) = #x` (TA5-SigValid, ASN-0034), and hence the ordinal successor `x + 1 = shift(x, 1)` (OrdinalShiftBase, ASN-0058) coincides with `inc(x, 0)` (which increments position `sig(x)`). *Justification.* The chain-adjacency successor `x + 1 = inc(x, 0)` preserves sub-allocator chain membership (TA5(c), ASN-0034), so `x + 1 ∈ dom(A_{s_X}(d_X))`; symmetrically `y + 1 ∈ dom(A_{s_Y}(d_Y))`. Distinct sub-allocator chains have disjoint domains — cross-subspace by ASN-0093's DisjointSubAllocatorChains and cross-document by its CrossDocumentDisjointness, both instances of T10a.6 (DomainDisjointness, ASN-0034). Hence `x + 1 ∈ dom(A_{s_X}(d_X))` and `y ∈ dom(A_{s_Y}(d_Y))` lie in disjoint domains, forcing `x + 1 ≠ y`; the symmetric placement of `y + 1` and `x` forces `y + 1 ≠ x`.

Applying ChainDisjointAdjacency with `x = c` and `y ∈ {a, a + 1}` (both in `A_X(d_X)`, while `c ∈ A_Y(d_Y)` with `(d_X, s_X) ≠ (d_Y, s_Y)`) excludes both `c + 1 = a` and `(a + 1) + 1 = c`. The pre-state maximal runs are `([1, 1], a + 1, 1)`, `([1, 2], c, 1)`, `([1, 3], a, 1)` — three singletons, since `(a + 1) + 1 = a + 2 ≠ c` (excluding the right-extension of the first run) and `c + 1 ≠ a` (excluding the right-extension of the second run). Pre-state run cardinality: 3.

Apply REARRANGE_K with cut sequence `([1, 1], [1, 3], [1, 4])`, a 3-cut pivot with `w_α = 2` and `w_β = 1`. R-PRE(iv) is discharged as above. By R-P1 (`0 ≤ j < 1`): `Σ'.M(d)([1, 1]) = Σ.M(d)([1, 3]) = a`. By R-P2 (`0 ≤ j < 2`): `Σ'.M(d)([1, 2]) = Σ.M(d)([1, 1]) = a + 1` and `Σ'.M(d)([1, 3]) = Σ.M(d)([1, 2]) = c`.

Post-state arrangement: `[1, 1] ↦ a`, `[1, 2] ↦ a + 1`, `[1, 3] ↦ c`. The maximal runs are `([1, 1], a, 2)` (since `a + 1 = Σ'.M(d)([1, 2])`) and `([1, 3], c, 1)`. Post-state run cardinality: 2 — strictly less than the pre-state cardinality 3.

**Equality witness.** Take pre-state `Σ.M(d)` populated only on the content subspace with V-positions `[1, 1] ↦ a` and `[1, 2] ↦ c`, where `a` and `c` are I-addresses from different sub-allocator chains — concretely, `a ∈ A_C(d_X)` and `c ∈ A_C(d_Y)` with `d_X ≠ d_Y`. By ChainDisjointAdjacency (inline lemma above) applied with `(d_X, s_C) ≠ (d_Y, s_C)`, neither `a + 1 = c` nor `c + 1 = a` can hold. The pre-state maximal runs are the two singletons `([1, 1], a, 1)` and `([1, 2], c, 1)`, since `a + 1 ≠ c` rules out the right-extension of the first run. Pre-state run cardinality: 2.

Apply REARRANGE_K with cut sequence `([1, 1], [1, 2], [1, 3])`, a 3-cut pivot with `w_α = 1` and `w_β = 1`. R-PRE(iv) is discharged because every depth-2 position `v` with `[1, 1] ≤ v < [1, 3]` — namely `[1, 1]` and `[1, 2]` — lies in `V_S(d)`. By R-P1 (`j = 0`, `w_β = 1`): `Σ'.M(d)([1, 1]) = Σ.M(d)([1, 2]) = c`. By R-P2 (`j = 0`, `w_α = 1`): `Σ'.M(d)([1, 2]) = Σ.M(d)([1, 1]) = a`.

Post-state arrangement: `[1, 1] ↦ c`, `[1, 2] ↦ a`. The maximal runs are `([1, 1], c, 1)` and `([1, 2], a, 1)` — again two singletons, since `c + 1 ≠ a` (the structural fact `c + 1 ≠ a` established above is state-independent — a property of `c` and `a` as chain elements — and carries directly into the post-state context). Post-state run cardinality: 2 — equal to the pre-state. The bijection π swaps the two V-positions (`π([1, 1]) = [1, 2]`, `π([1, 2]) = [1, 1]`), so π is non-identity, yet the run-decomposition cardinality is preserved exactly.

Run-decomposition cardinality is neither monotone nor invariant under rearrangement — it tracks the *visible structure* of the arrangement, which is exactly what rearrangement reshapes.

## Cross-Document Independence

Among d's siblings, nothing happens. RA-frame guarantees `Σ'.M(d') = Σ.M(d')` for every `d' ≠ d`:
```
(A d' ∈ dom(Σ.M) : d' ≠ d :: Σ'.M(d') = Σ.M(d'))                                       (RE-other)
```

This is the formal precipitate of Nelson's "REARRANGE is document-scoped — the cuts are V-addresses within the target document." Rearrangement cannot move content between documents, cannot deplete or extend any other document's arrangement, and cannot affect any projection evaluated against any other document. The operation's scope is fully named by the document parameter `d`.

## Cross-Document Transclusion Preserved

When `a ∈ ran(Σ.M(d))` with `origin(a) ≠ d`, the I-address `a` is foreign content displayed in d — a transclusion from d's perspective. The transclusion relationship has three components: (a) `a` is in d's arrangement; (b) `a`'s home document `origin(a)` is present and undisturbed; (c) the origin function — which document allocated `a` — is unchanged.

The claim ranges over every (a, d) pair with `a ∈ ran(Σ.M(d))` and `origin(a) ≠ d` — `d` here (the *transclusion target*) can be the rearrangement target `d_tgt` or any other registered document, both of which are admitted. We must distinguish `d` (the transclusion target) from `d_tgt` (the document REARRANGE acts on), since the relationship `origin(a) ≠ d` does *not* imply `origin(a) ≠ d_tgt`. The argument splits into two conclusions whose scopes differ on this point. *Conclusion (i)* — `a ∈ ran(Σ'.M(d))` — and *conclusion (ii)* — `a` appears in d's arrangement at Σ' with the same multiplicity as at Σ — hold unconditionally for every admissible `d`. By RE-ran applied at d, the *set* of foreign addresses `{a ∈ ran(Σ.M(d)) : origin(a) ≠ d}` is preserved; by RE-μ applied at d (likewise uniform, with the non-target case again trivial under `Σ'.M(d) = Σ.M(d)`), each such address appears in d's arrangement with the same multiplicity at Σ' as at Σ — so the multiset of foreign addresses is preserved. This delivers (i) `a ∈ ran(Σ'.M(d))` and (ii) the unchanged multiplicity directly, with no further routing. Origin itself is a function of the address (per S7 of ASN-0036) — not of state — so it is invariant unconditionally.

*Conclusion (iii)* — `origin(a)`'s arrangement is unchanged — holds exactly when `origin(a) ≠ d_tgt` (the rearrangement target): by C2 (ASN-0093) `origin(a) ∈ dom(Σ.M)`, so RE-other applies at `d' = origin(a)` whenever `origin(a) ≠ d_tgt`, while if `origin(a) = d_tgt` the rearrangement permutes `origin(a)`'s own arrangement and (iii) fails — leaving (i) and (ii) at d intact regardless.

> **Transclusion Preservation.** For every transclusion relationship at Σ — every pair (a, d) with `a ∈ ran(Σ.M(d))` and `origin(a) ≠ d` — the foreign relationship at d is preserved: (i) `a ∈ ran(Σ'.M(d))` and (ii) the multiplicity of `a` at d is unchanged — both unconditional in `d`. Additionally (iii) `origin(a)`'s arrangement is unchanged when `origin(a) ≠ d_tgt` (the rearrangement target). (RE-trans)

Even when REARRANGE fragments d's view of the transcluded span (RE-frag), each piece independently carries its foreign origin: every I-address in the fragmented view retains its `origin(·)` (RE-origin), so splitting at a cut point does not change where any byte came from. The transcluding document still finds its borrowed content; the home document is undisturbed; and the function answering "where did this byte come from?" is invariant. Whether the two fragments *jointly reconstitute* the original source span — as opposed to merely each carrying the right origin — is not established here.

## Subspace Frame (REARRANGE_K-specific)

REARRANGE_K's cut-sequence structure delivers strict pointwise fixity on the complement of the cut subspace S: non-S V-positions are not permuted at all (`π(v) = v`), not merely kept within their subspace. This is RE-sub, derived directly from the R-PPERM/R-SPERM construction below.

ASN-0084's R-PPERM and R-SPERM define π directly as the identity on non-S V-positions: both constructions list a non-S branch that writes `π(v) = v` for every `v ∈ dom(Σ.M(d))` with `subspace(v) ≠ S`. ASN-0084's R-FRAME-P/S(a) records the resulting arrangement preservation `Σ'.M(d)(v) = Σ.M(d)(v)` for the same V-positions. Together these supply RE-sub in its full pointwise form — both clauses:
```
(A v : v ∈ dom(Σ.M(d)) ∧ subspace(v) ≠ S :: π(v) = v ∧ Σ'.M(d)(v) = Σ.M(d)(v))           (RE-sub)
```

When the cut subspace is the content subspace, the link subspace is wholly preserved — both its set of populated V-positions, its V→I mapping, *and* the pointwise behaviour of π on those V-positions. Rearrangement of content does not perturb the link arrangement and does not relabel any link-subspace V-position.

## In-Subspace Exterior Frame (REARRANGE_K-specific)

A second pointwise-fixity property complements RE-sub on the cut subspace itself. RE-sub covers V-positions in subspaces other than the cut subspace; RE-ext (below) covers V-positions *within* the cut subspace S that lie *outside* the affected range `[c₀, c_{n−1})`. REARRANGE_K's cut-sequence structure delivers strict pointwise fixity for in-subspace V-positions outside the affected range.

ASN-0084's R-PPERM and R-SPERM construct π as the identity on V-positions in the cut subspace S that lie outside the affected range: both constructions list exterior branches that write `π(v) = v` for every `v ∈ V_S(d)` with `v < c₀` or `v ≥ c_{n−1}`. ASN-0084's R-EXT records the resulting arrangement preservation `Σ'.M(d)(v) = Σ.M(d)(v)` for the same V-positions. Together these supply RE-ext in its full pointwise form:
```
(A v : v ∈ V_S(d) ∧ (v < c₀ ∨ v ≥ c_{n−1}) :: π(v) = v ∧ Σ'.M(d)(v) = Σ.M(d)(v))    (RE-ext)
```

## Origin and Provenance Invariance

The function `origin(a) = N(a).0.U(a).0.D(a)` (S7 of ASN-0036) projects an I-address to the document-level prefix encoding its allocator. Origin consults only the address `a`. It is a structural projection on T, independent of any state component. Therefore origin is invariant across every state transition, including REARRANGE:
```
(A a ∈ T :: origin(a) at Σ' = origin(a) at Σ)                                           (RE-origin)
```

The provenance relation `Σ.R ⊆ T × E_doc` records which documents have, at some point in their history, contained which I-addresses. RA-frame includes `Σ'.R = Σ.R` directly, so:
```
Σ'.R = Σ.R                                                                              (RE-R)
```

The historical record is intact across rearrangement. The bytes that have ever lived in d are exactly the bytes that live in d after the rearrangement (since REARRANGE adds and removes nothing — RE-ran), and the records of their past containments in other documents are unchanged.

## Worked Example

We trace a small concrete state through a single REARRANGE_K invocation and verify each RE-* claim at the level of actual values.

*Setup.* Fix documents `d = [1, 0, 1, 0, 1]` and `d' = [1, 0, 1, 0, 2]`, both T4-valid with `zeros(·) = 2`. By the sub-allocator chain discipline (ASN-0093), let `b₁ := [d.0.1.1] = [1, 0, 1, 0, 1, 0, 1, 1]` be the first emission of `A_C(d)`, and let `a₁ := [d'.0.1.1] = [1, 0, 1, 0, 2, 0, 1, 1]` and `a₂ := inc(a₁, 0) = [1, 0, 1, 0, 2, 0, 1, 2]` be the first two emissions of `A_C(d')`, so `a₂ = a₁ + 1` within the chain. Let `a_link := [d.0.2.1]` be the first emission of `A_L(d)`.

*Pre-state.* `Σ.C` contains `b₁, a₁, a₂` (and possibly more); `Σ.L` contains `a_link` with endset sequence `(e₁, e₂, e₃)`, where `e₁ = ⟨(b₁, δ(1, 8))⟩` is a canonical single-span endset with `coverage(e₁) = {t ∈ T : b₁ ≤ t < b₁ ⊕ δ(1, 8)}` (the tumbler interval under T1), and `e₃` is the non-empty type endset. Note that the interval contains many tumblers that are not I-addresses (e.g., longer tumblers extending `b₁` at lower hierarchical levels lie between `b₁` and `b₁ ⊕ δ(1, 8)` by T1 case (ii) and case (i)); what we need below is the intersection of `coverage(e₁)` with the address stores. Every address in `dom(Σ.C) ∪ dom(Σ.L)` lies in the substrate-emittable set `F` of ASN-0098: K.α and K.λ emit only sub-allocator chain elements, each of structural form `[d, 0, s, k]` with `s ∈ {s_C, s_L}` and `k ≥ 1`, the defining shape of `F`. Consequently `coverage(e₁) ∩ (dom(Σ.C) ∪ dom(Σ.L)) = coverage(e₁) ∩ F ∩ (dom(Σ.C) ∪ dom(Σ.L))`, after which LP-Fin Corollary (ASN-0098) identifies the F-side intersection. By LP-Fin Corollary, `coverage(e₁) ∩ (dom(Σ.C) ∪ dom(Σ.L)) = {b₁}` — the single first emission of `A_C(d)` is the only F-candidate the canonical span admits in the interval. In particular this intersection is disjoint from `{a₁, a₂}` (since `a₁, a₂` agree with `b₁` only on positions 1–4 and diverge at position 5, placing them outside the interval). `Σ.M(d)` populates both subspaces at their respective common depths — the content subspace at depth 2 with three positions, and the link subspace at depth 2 with one populated V-position pointing at the link in `dom(Σ.L)`:
```
Σ.M(d) = { [1, 1] ↦ a₁,    [1, 2] ↦ a₂,    [1, 3] ↦ b₁,    [2, 1] ↦ a_link }
```
The link-subspace entry `[2, 1] ↦ a_link` is well-typed under S3★: a link-subspace V-position whose image lies in `dom(Σ.L)`. `Σ.M(d')` populates its own content subspace (concrete details immaterial here), and `Σ.M(d''')` for any other `d''' ∈ dom(Σ.M)` is whatever it is.

*Operation.* Apply REARRANGE_K to `d` with cut sequence `(c₀, c₁, c₂) = ([1, 1], [1, 2], [1, 4])`, a 3-cut pivot with cut subspace S = s_C, `w_α = 1`, `w_β = 2`. The permutation π (R-PPERM, ASN-0084) acts on content-subspace V-positions as `π([1, 1]) = c₀ + w_β = [1, 3]` (α-region: c₀ + j ↦ c₀ + w_β + j), `π([1, 2]) = c₀ = [1, 1]` (β-region: c₁ + j ↦ c₀ + j with j = 0), `π([1, 3]) = c₀ + 1 = [1, 2]` (β-region with j = 1); on non-S V-positions π acts as identity (R-PPERM, non-S branch), so `π([2, 1]) = [2, 1]`.

*Post-state.* By R-P1 and R-P2 for content-subspace positions, and R-FRAME-P(a) for the link-subspace position:
```
Σ'.M(d) = { [1, 1] ↦ a₂,    [1, 2] ↦ b₁,    [1, 3] ↦ a₁,    [2, 1] ↦ a_link }
```

*Verification.* For each derived claim, we exhibit the concrete witness:

- **RE-C.** `Σ'.C = Σ.C` by RA-frame (no content allocation, no content modification).
- **RE-L.** `dom(Σ'.L) = dom(Σ.L) = {a_link}` and `Σ'.L(a_link) = Σ.L(a_link) = (e₁, e₂, e₃)` by RA-frame.
- **RE-dom.** `dom(Σ'.M(d)) = {[1, 1], [1, 2], [1, 3], [2, 1]} = dom(Σ.M(d))` by direct inspection.
- **RE-ran.** `ran(Σ'.M(d)) = {a₂, b₁, a₁, a_link} = {a₁, a₂, b₁, a_link} = ran(Σ.M(d))` as sets.
- **RE-μ.** `μ_{a₁}(Σ.M(d)) = μ_{a₂}(Σ.M(d)) = μ_{b₁}(Σ.M(d)) = μ_{a_link}(Σ.M(d)) = 1`, and identically for `Σ'.M(d)`; multiplicities of all other I-addresses are zero in both.
- **RE-cov.** `coverage(Σ'.L(a_link).eᵢ) = coverage(Σ.L(a_link).eᵢ)` for `i ∈ {1, 2, 3}`, since the endset sequence itself is preserved (RE-L) and coverage depends only on the endset.
- **RE-disc.** `coverage(e₁) ∩ ran(Σ.M(d)) ⊇ {b₁} ≠ ∅`, so `discoverable_from(a_link, d, Σ)` holds (LP12, ASN-0098). The same intersection `coverage(e₁) ∩ ran(Σ'.M(d)) ⊇ {b₁} ≠ ∅` holds at the post-state, so `discoverable_from(a_link, d, Σ')` holds too. The biconditional is satisfied.
- **RE-proj.** `project(e₁, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e₁)} = {[1, 3]}` (only `b₁`'s V-position; `[2, 1] ↦ a_link` is excluded since `a_link ∉ coverage(e₁)` — `a_link = [d.0.2.1]` agrees with `b₁ = [d.0.1.1]` on positions 1–6 but has component `2` at position 7 while `b₁` has component `1`, so by T1 case (i) at position 7 `b₁ < a_link` and `b₁ ⊕ δ(1, 8) < a_link`, placing `a_link` strictly above the interval). `project(e₁, d, Σ') = {[1, 2]}` (where `b₁` lives now). The image `π({[1, 3]}) = {[1, 2]}` matches.
- **RE-frag.** Pre-state runs on the content subspace: `([1, 1], a₁, 2)` (since `a₂ = a₁ + 1`) and `([1, 3], b₁, 1)` — cardinality 2. Post-state runs on the content subspace: `([1, 1], a₂, 1)`, `([1, 2], b₁, 1)`, `([1, 3], a₁, 1)` — cardinality 3, since no two consecutive post-state I-addresses extend each other (`a₂ + 1 ≠ b₁`; `b₁ + 1 ≠ a₁`). The link-subspace run `([2, 1], a_link, 1)` is shared between both states. The content-subspace cardinality strictly increased — a fragmentation witness. The transclusion in this arrangement is incidental: the same fragmentation occurs whenever chain-adjacent I-addresses are rearranged to V-non-adjacent positions, regardless of origin (e.g., a pre-state with `a₁, a₂, b₁` all owned by `d` would fragment identically under the same cut sequence).
- **RE-other.** `Σ'.M(d') = Σ.M(d')` by RA-frame; the foreign document's arrangement is untouched.
- **RE-trans.** Both `a₁` and `a₂` have `origin(·) = d' ≠ d`, so each is a transclusion in `d`. `{a₁, a₂} ⊆ ran(Σ.M(d))` and `{a₁, a₂} ⊆ ran(Σ'.M(d))`. `origin(a₁) = origin(a₂) = d'` is unchanged (RE-origin). `Σ'.M(d') = Σ.M(d')` by RE-other.
- **RE-sub.** The link-subspace position `[2, 1] ∈ dom(Σ.M(d))` has `subspace([2, 1]) = 2 ≠ s_C = S`. R-PPERM's non-S branch gives `π([2, 1]) = [2, 1]` (the π-fixity conjunct), and R-FRAME-P(a) gives `Σ'.M(d)([2, 1]) = Σ.M(d)([2, 1]) = a_link` (the arrangement-preservation conjunct), matching the post-state arrangement exhibited above. The cut-subspace restriction is exercised concretely: REARRANGE_K's content-subspace cuts leave the link-subspace entry verbatim and the link-subspace V-position unpermuted, despite the bijection π acting non-trivially on content-subspace V-positions.
- **RE-origin.** `origin(a₁) = origin(a₂) = d'` (extracted from positions 1–5 of `a₁` and `a₂`); `origin(b₁) = d` (extracted from positions 1–5 of `b₁`). Origin is a structural projection on the address; it does not depend on state and is unchanged.
- **RE-R.** `Σ'.R = Σ.R` by RA-frame directly.
- **Admissibility (RA-adm).** The post-state foundation invariants hold concretely against `Σ'.M(d) = {[1, 1] ↦ a₂, [1, 2] ↦ b₁, [1, 3] ↦ a₁, [2, 1] ↦ a_link}`. *S2 (functionality):* each of the four listed V-positions appears exactly once on the left-hand side of the displayed map, so `Σ'.M(d)` assigns at most one I-address per V-position. *S8a:* every V-position has `zeros = 0`, depth 2, and all positive components. *S8-depth:* the content subspace `V_{s_C}(d) = {[1, 1], [1, 2], [1, 3]}` has common depth 2; the link subspace `V_{s_L}(d) = {[2, 1]}` has common depth 2. *S3★:* the three content-subspace positions map to `{a₂, b₁, a₁} ⊆ dom(Σ.C) = dom(Σ'.C)` (RE-C), and the link-subspace position maps to `a_link ∈ dom(Σ.L) = dom(Σ'.L)` (RE-L). *D-CTG★:* `V_{s_C}(d) = {[1, 1], [1, 2], [1, 3]}` is contiguous; `V_{s_L}(d) = {[2, 1]}` is trivially contiguous. *D-MIN★:* `min(V_{s_C}(d)) = [1, 1]` and `min(V_{s_L}(d)) = [2, 1]`, each of the form `[S, 1, ..., 1]`. *D-SEQ★* follows from D-CTG★ ∧ D-MIN★ ∧ S8-depth. *S3★-aux:* every V-position has first component in `{1, 2} = {s_C, s_L}`, so the subspace-exhaustiveness condition holds. *CL-OWN:* the single link-subspace position `[2, 1]` maps to `a_link`, and `origin(a_link) = d` (extracted from positions 1–5 of `a_link = [d.0.2.1]`), so every link-subspace mapping at d has home document d. *CL-UNIQ:* `Σ'.M(d)|_{V_{s_L}(d)} = {[2, 1] ↦ a_link}` has a singleton domain, so the partial-injection property holds trivially. *S8★:* the post-state content subspace `V_{s_C}(d) = {[1, 1], [1, 2], [1, 3]}` with `Σ'.M(d)|_{V_{s_C}(d)} = {[1, 1] ↦ a₂, [1, 2] ↦ b₁, [1, 3] ↦ a₁}` decomposes into three length-1 correspondence runs `([1, 1], a₂, 1), ([1, 2], b₁, 1), ([1, 3], a₁, 1)` (the post-state runs identified under RE-frag above), discharging S8★'s content-subspace clause by direct application of ASN-0036's S8 — the restricted arrangement is a finite partial function at uniform depth 2 satisfying S3 with target `dom(Σ'.C)`. The link-subspace clause `M'(d)|_{V_{s_L}(d)} = {[2, 1] ↦ a_link}` carries over verbatim from Σ via RE-sub, with trivial length-1 decomposition `{([2, 1], a_link, 1)}`. All remaining foundation invariants hold at Σ' on the same footing as in the abstract discharge: the per-state predicates hold by RA-adm, and the binary transition invariants discharge by RA-frame's verbatim preservation of Σ.C, Σ.L, Σ.E, Σ.R, and dom(Σ.M) ("State-Component-Only Invariants" above).
- **Composite-boundary properties (P4★, P4a).** These are not per-state invariants and so fall outside RA-adm; they are discharged by their own composite-boundary arguments. *P4★:* `Contains_C(Σ') = {(a₂, d), (b₁, d), (a₁, d)} = {(a₁, d), (a₂, d), (b₁, d)} = Contains_C(Σ)` as a set of pairs (π restricted to `V_{s_C}(d)` preserves the content-subspace range, so the set of (a, d) pairs Contains_C is preserved), and `Σ'.R = Σ.R` (RE-R) preserves the right-hand side, so the pre-state inclusion `Contains_C(Σ) ⊆ Σ.R` carries over to `Contains_C(Σ') ⊆ Σ'.R`. *P4a* (TraceWitnessing) is delivered at the K.μ~ composite boundary by ASN-0047's ExtendedReachableStateInvariants.

Every derived claim holds at the concrete level; no two derived claims conflict at any point of the trace.

## Worked Example — 4-cut Swap (μ-region delta)

The 4-cut swap differs from the 3-cut pivot in exactly one structural respect: it has a middle region μ that undergoes a non-zero net displacement when `w_α ≠ w_β`. We exhibit only that delta; every other RE-* claim and every RA-adm clause discharge as in the first Worked Example, with R-SPERM in place of R-PPERM.

Reuse `d = [1, 0, 1, 0, 1]` and `d' = [1, 0, 1, 0, 2]`, with `a₁, a₂, a₃, a₄` the first four emissions of `A_C(d')` (so `a_{i+1} = a_i + 1`) and `a_link := [d.0.2.1]`. Pre-state `Σ.M(d) = { [1, 1] ↦ a₁, [1, 2] ↦ a₂, [1, 3] ↦ a₃, [1, 4] ↦ a₄, [2, 1] ↦ a_link }`. Apply REARRANGE_K with 4-cut sequence `([1, 1], [1, 2], [1, 3], [1, 5])`: cut subspace s_C, `w_α = 1`, `w_μ = 1`, `w_β = 2`, so `w_α ≠ w_β`. By R-S1/R-S2/R-S3 (ASN-0084) the post-state is `Σ'.M(d) = { [1, 1] ↦ a₃, [1, 2] ↦ a₄, [1, 3] ↦ a₂, [1, 4] ↦ a₁, [2, 1] ↦ a_link }`.

The distinguishing fact is the μ-region displacement. R-S2 maps `c₁ + j ↦ c₀ + w_β + j`, giving net displacement `Δ(μ) = w_β − w_α = +1`: the μ-content `a₂` at `[1, 2]` migrates to `[1, 3]` — a position *between* the β image (`[1, 1]`–`[1, 2]`) and the α image (`[1, 4]`) — with its transclusion relationship to `d'` intact across the displacement. This +1 μ-displacement is not realisable under any 3-cut pivot, yet it violates no RE-* invariant: RE-proj transports `project(e₁, d, Σ)` along π through R-SPERM's μ- and β-branches, and RE-frag, RE-trans, and RA-adm hold for the five-position arrangement by the first Worked Example's pattern.

## Worked Example — Interior Cuts (R-EXT on a non-empty exterior)

The first two traces place `c₀ = min(V_S(d))` and `c_{n−1}` just past `max(V_S(d))`, so the affected range covers all of `V_S(d)` and R-EXT fires on the empty set. The single new fact this trace adds is R-EXT firing on a *non-empty* in-subspace exterior — the pointwise fixity of content-subspace V-positions outside the affected range, which the abstract class alone would permit a bijection to move.

Reuse `d`, `d'`. Let `b₁, b₂` be the first two emissions of `A_C(d)` (so `b₂ = b₁ + 1`) and `a₁, a₂, a₃` the first three of `A_C(d')`; `bᵢ` and `aⱼ` are non-chain-adjacent by ChainDisjointAdjacency. Pre-state `Σ.M(d) = { [1, 1] ↦ b₁, [1, 2] ↦ a₁, [1, 3] ↦ a₂, [1, 4] ↦ a₃, [1, 5] ↦ b₂ }` — own content at the extremes, a contiguous transclusion from `d'` in the middle. Apply REARRANGE_K with cut sequence `([1, 2], [1, 3], [1, 5])`: `w_α = 1`, `w_β = 2`, affected range `{[1, 2], [1, 3], [1, 4]}` strictly interior to `V_S(d)`, leaving left exterior `{[1, 1]}` and right exterior `{[1, 5]}` non-empty. The post-state is `Σ'.M(d) = { [1, 1] ↦ b₁, [1, 2] ↦ a₂, [1, 3] ↦ a₃, [1, 4] ↦ a₁, [1, 5] ↦ b₂ }`.

The delta: `[1, 1] < c₀` and `[1, 5] ≥ c_{n−1}` are both *in* the cut subspace S = s_C yet outside the affected range, so R-EXT — not non-cut-subspace frame inheritance — fixes them pointwise: `Σ'.M(d)([1, 1]) = b₁` and `Σ'.M(d)([1, 5]) = b₂`, with `π([1, 1]) = [1, 1]`, `π([1, 5]) = [1, 5]` from R-PPERM's exterior branches. This holds even though π is non-identity on the three interior positions and the run cardinality strictly increases (pre-state 3 runs — `b₁`, the 3-run `a₁a₂a₃`, `b₂`; post-state 4 runs — `b₁`, the 2-run `a₂a₃`, `a₁`, `b₂` — confirming RE-frag). The abstract class — RA-dom, RA-π, RA-frame, RA-adm — would permit a bijection that moved `[1, 1]` and `[1, 5]`; R-EXT is what pins them.

## Worked Example — Bijection Non-Uniqueness Under Shared I-Addresses

The three preceding traces exercise RE-proj with distinct I-addresses at every V-position, so the bijection π is uniquely determined by the transition — RA-π pins each `π(v)` to the single V-position `v'` with `Σ'.M(d)(v') = Σ.M(d)(v)`. When `Σ.M(d)` instead shares I-addresses across V-positions (allowed by foundation S5/UnrestrictedSharing of ASN-0036), the abstract class admits multiple bijections satisfying RA-π for a single transition `Σ → Σ'`. A fourth trace exhibits two distinct valid witnesses for the same REARRANGE_K transition and verifies that RE-proj's set image is uniform across both — the abstract uniformity claim made in the "REARRANGE as Vstream-Only Operation" section concretely realised.

*Setup.* Reuse `d = [1, 0, 1, 0, 1]` and `d' = [1, 0, 1, 0, 2]`. Let `a := [d'.0.1.1]` be the first emission of `A_C(d')` and let `b := [d.0.1.1]` be the first emission of `A_C(d)`. By ChainDisjointAdjacency (inline lemma above) applied with `(d', s_C) ≠ (d, s_C)`, neither `a + 1 = b` nor `b + 1 = a` holds.

*Pre-state.* `Σ.C` contains `a` and `b`; `Σ.L` and other state components are immaterial here (any specific contents preserved by RA-frame). `Σ.M(d)` populates three content-subspace V-positions, with the shared I-address `a` at two of them:
```
Σ.M(d) = { [1, 1] ↦ a,    [1, 2] ↦ a,    [1, 3] ↦ b }
```
The pre-state pre-image sets are `Σ.M(d)⁻¹(a) = {[1, 1], [1, 2]}` and `Σ.M(d)⁻¹(b) = {[1, 3]}` — the multiset shape is `(a → 2, b → 1)`. Sharing is permitted by S5 (UnrestrictedSharing): the same I-address may sit at multiple V-positions within a single arrangement.

*Operation.* Apply REARRANGE_K to `d` with cut sequence `(c₀, c₁, c₂) = ([1, 1], [1, 3], [1, 4])`, a 3-cut pivot with cut subspace S = s_C, `w_α = ord(c₁) − ord(c₀) = 2`, `w_β = ord(c₂) − ord(c₁) = 1`. R-PRE(iv) is discharged because every depth-2 position `v` with `[1, 1] ≤ v < [1, 4]` — namely `[1, 1], [1, 2], [1, 3]` — lies in `V_S(d)`. By R-P1 (`Σ'.M(d)(c₀ + j) = Σ.M(d)(c₁ + j)` for `0 ≤ j < w_β`): `Σ'.M(d)([1, 1]) = Σ.M(d)([1, 3]) = b`. By R-P2 (`Σ'.M(d)(c₀ + w_β + j) = Σ.M(d)(c₀ + j)` for `0 ≤ j < w_α`): `Σ'.M(d)([1, 2]) = Σ.M(d)([1, 1]) = a` and `Σ'.M(d)([1, 3]) = Σ.M(d)([1, 2]) = a`.

*Post-state.*
```
Σ'.M(d) = { [1, 1] ↦ b,    [1, 2] ↦ a,    [1, 3] ↦ a }
```
The post-state pre-image sets are `Σ'.M(d)⁻¹(a) = {[1, 2], [1, 3]}` and `Σ'.M(d)⁻¹(b) = {[1, 1]}` — the same multiset shape `(a → 2, b → 1)` as the pre-state (forced by RE-μ), with the pre-image blocks shifted.

*Witness 1 — R-PPERM construction.* ASN-0084's R-PPERM constructs π₁ explicitly. On the α-region `c₀ + j ↦ c₀ + w_β + j` for `j ∈ {0, 1}` (since `w_α = 2`): `π₁([1, 1]) = c₀ + w_β = [1, 2]` (j = 0); `π₁([1, 2]) = c₀ + w_β + 1 = [1, 3]` (j = 1). On the β-region `c₁ + j ↦ c₀ + j` for `j = 0` (since `w_β = 1`): `π₁([1, 3]) = c₀ = [1, 1]`. So π₁ is the 3-cycle `([1, 1] ↦ [1, 2], [1, 2] ↦ [1, 3], [1, 3] ↦ [1, 1])`.

Verify RA-π under π₁:
- `v = [1, 1]`: `Σ'.M(d)(π₁([1, 1])) = Σ'.M(d)([1, 2]) = a = Σ.M(d)([1, 1])` ✓
- `v = [1, 2]`: `Σ'.M(d)(π₁([1, 2])) = Σ'.M(d)([1, 3]) = a = Σ.M(d)([1, 2])` ✓
- `v = [1, 3]`: `Σ'.M(d)(π₁([1, 3])) = Σ'.M(d)([1, 1]) = b = Σ.M(d)([1, 3])` ✓

*Witness 2 — an alternative bijection.* Construct π₂ by swapping the assignments within the `a`-block. The shared pre-image set `Σ.M(d)⁻¹(a) = {[1, 1], [1, 2]}` must be bijected onto the post-state pre-image set `Σ'.M(d)⁻¹(a) = {[1, 2], [1, 3]}` (per the bijection-class characterisation in the abstract section above), and there are exactly two ways to do so; π₁ chose one, π₂ chooses the other:
- `π₂([1, 1]) = [1, 3]`  (instead of `[1, 2]` under π₁)
- `π₂([1, 2]) = [1, 2]`  (instead of `[1, 3]` under π₁)
- `π₂([1, 3]) = [1, 1]`  (same as π₁; the `b`-block is a singleton with a forced mapping)

Verify RA-π under π₂:
- `v = [1, 1]`: `Σ'.M(d)(π₂([1, 1])) = Σ'.M(d)([1, 3]) = a = Σ.M(d)([1, 1])` ✓
- `v = [1, 2]`: `Σ'.M(d)(π₂([1, 2])) = Σ'.M(d)([1, 2]) = a = Σ.M(d)([1, 2])` ✓
- `v = [1, 3]`: `Σ'.M(d)(π₂([1, 3])) = Σ'.M(d)([1, 1]) = b = Σ.M(d)([1, 3])` ✓

Both π₁ and π₂ are bijections of `dom(Σ.M(d)) = {[1, 1], [1, 2], [1, 3]}` onto itself that satisfy RA-π for the same Σ → Σ'. They disagree pointwise — `π₁([1, 1]) = [1, 2]` but `π₂([1, 1]) = [1, 3]`; `π₁([1, 2]) = [1, 3]` but `π₂([1, 2]) = [1, 2]` — yet both witness the same transition. This is the bijection-non-uniqueness phenomenon described abstractly in the opening section: when shared I-addresses produce a non-singleton pre-image block, the within-block bijection is free.

*Uniformity of RE-proj across witnesses.* Construct a single-span endset `e_a := ⟨(a, δ(1, #a))⟩` — a canonical width-1 span starting at `a`. By the same LP-Fin Corollary computation pattern established in the first Worked Example (every stored address lies in the substrate-emittable set `F`, and the canonical width-1 span admits exactly its start), `coverage(e_a) ∩ (dom(Σ.C) ∪ dom(Σ.L)) = {a}`. (Note `b ∉ coverage(e_a)`: by ChainDisjointAdjacency, `b` belongs to `A_C(d) ≠ A_C(d')`, so `b` is not a chain-successor of `a` and lies outside the width-1 interval.)

Compute the projection at each state:
- `project(e_a, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e_a)} = {v : Σ.M(d)(v) = a} = {[1, 1], [1, 2]}`
- `project(e_a, d, Σ') = {v : Σ'.M(d)(v) = a} = {[1, 2], [1, 3]}`

Apply RE-proj under each witness:
- Under π₁: `π₁(project(e_a, d, Σ)) = π₁({[1, 1], [1, 2]}) = {π₁([1, 1]), π₁([1, 2])} = {[1, 2], [1, 3]}`
- Under π₂: `π₂(project(e_a, d, Σ)) = π₂({[1, 1], [1, 2]}) = {π₂([1, 1]), π₂([1, 2])} = {[1, 3], [1, 2]} = {[1, 2], [1, 3]}`

Both set images equal `project(e_a, d, Σ') = {[1, 2], [1, 3]}`. RE-proj's equation holds under either choice of witness — the set image is invariant under the within-block freedom, even though the individual pointwise assignments disagree. The state-determined RHS `project(e_a, d, Σ')` is the same regardless of which valid π is used to compute the LHS, which is exactly the uniformity property: the set image `π(project(e_a, d, Σ))` is a state-determined object, not a witness-dependent one.

The phenomenon is general: every endset `e` whose coverage intersects only the shared-block I-address `a` yields a projection `project(e, d, Σ)` that is the entire shared block, and the set image under either witness is the entire shared post-state block — the within-block freedom acts trivially at the set level. When coverage instead distinguishes V-positions within the shared block (impossible here, since the block's members all map to the same I-address and coverage is keyed to I-addresses, not V-positions), the bijection's freedom would be confined to the V-positions outside the block. This trace concretely realises the abstract argument that RE-proj is well-defined across witnesses.

*Admissibility (RA-adm).* The only distinction from the first Worked Example's RA-adm sweep is the shared I-address `a` at `[1, 2]` and `[1, 3]`: this is admitted by S5 (UnrestrictedSharing) while S2 (functionality) still holds, since each of `[1, 1], [1, 2], [1, 3]` appears once on the left of the map (distinct V-positions may share an image). Every other clause discharges by the first Worked Example's pattern.

Beyond exhibiting bijection non-uniqueness, this trace is also a richer RE-eq witness than the two-singleton case in "Run Decomposition Is Not Invariant": both states decompose into three singleton runs — no two adjacent V-positions are chain-adjacent (`a` repeats at `[1, 1], [1, 2]`, and `b ≠ a + 1` by ChainDisjointAdjacency) — so run cardinality is preserved at 3 even though π is non-trivial under either witness and shared I-addresses make it non-unique. RE-eq thus does not require a sparse arrangement; it persists under S5/UnrestrictedSharing.

## Worked Example — Net-Effect Collapse (non-identity π, `Σ' = Σ`)

The net-effect split of "REARRANGE_K Realises the Abstract Class" distinguishes one branch the preceding traces never instantiate: an arrangement on which the non-identity pivot π yields `M'(d) = M(d)`, so the realiser is not the K.μ~ composite but the *empty* sequence with `Σ' = Σ`. Because this branch determines which realiser discharges RA-adm, we exhibit it concretely.

*Setup.* Reuse `d = [1, 0, 1, 0, 1]` and `d' = [1, 0, 1, 0, 2]`, both T4-valid with `zeros(·) = 2`. Let `a := [d'.0.1.1]` be the first emission of `A_C(d')`, a single transcluded content address. The collapse mechanism needs only that one I-address repeat across the affected range; no second address and no chain-adjacency fact is required.

*Pre-state.* `Σ.C` contains `a` (and possibly more); other state components are immaterial here (any specific contents preserved by RA-frame). `Σ.M(d)` populates three content-subspace V-positions, all carrying the shared I-address `a`:
```
Σ.M(d) = { [1, 1] ↦ a,    [1, 2] ↦ a,    [1, 3] ↦ a }
```
The shared image is permitted because S2 (ArrangementFunctionality) imposes only functionality — each of `[1, 1], [1, 2], [1, 3]` appears once on the left of the map — and never single-image injectivity; the pre-image set `Σ.M(d)⁻¹(a) = {[1, 1], [1, 2], [1, 3]}` is therefore admissible.

*Operation.* Apply REARRANGE_K to `d` with cut sequence `(c₀, c₁, c₂) = ([1, 1], [1, 2], [1, 4])`, a 3-cut pivot with cut subspace S = s_C, `w_α = ord(c₁) − ord(c₀) = 1`, `w_β = ord(c₂) − ord(c₁) = 2`. R-PRE is met: CS1–CS5 hold (n = 3; `[1,1] < [1,2] < [1,4]`; subspace 1; depth 2; positive ordinals), and R-PRE(iv) holds because every depth-2 position `v` with `[1, 1] ≤ v < [1, 4]` — namely `[1, 1], [1, 2], [1, 3]` — lies in `V_S(d)`.

The permutation π (R-PPERM, ASN-0084) is the non-identity 3-cycle: on the α-region `c₀ + j ↦ c₀ + w_β + j` (`0 ≤ j < w_α = 1`) gives `π([1, 1]) = c₀ + 2 = [1, 3]`; on the β-region `c₁ + j ↦ c₀ + j` (`0 ≤ j < w_β = 2`) gives `π([1, 2]) = c₀ = [1, 1]` (j = 0) and `π([1, 3]) = c₀ + 1 = [1, 2]` (j = 1). So π = `([1, 1] ↦ [1, 3], [1, 3] ↦ [1, 2], [1, 2] ↦ [1, 1])`, manifestly `≠ id` (e.g. `π([1, 1]) = [1, 3] ≠ [1, 1]`).

*R-P1/R-P2 reproduce `M(d)`.* By R-P1 (`Σ'.M(d)(c₀ + j) = Σ.M(d)(c₁ + j)` for `0 ≤ j < w_β = 2`):
- j = 0: `Σ'.M(d)([1, 1]) = Σ.M(d)([1, 2]) = a`
- j = 1: `Σ'.M(d)([1, 2]) = Σ.M(d)([1, 3]) = a`

By R-P2 (`Σ'.M(d)(c₀ + w_β + j) = Σ.M(d)(c₀ + j)` for `0 ≤ j < w_α = 1`):
- j = 0: `Σ'.M(d)([1, 3]) = Σ.M(d)([1, 1]) = a`

Every right-hand side is `a` because `Σ.M(d)` is constant `= a` on the affected range. Hence
```
Σ'.M(d) = { [1, 1] ↦ a,    [1, 2] ↦ a,    [1, 3] ↦ a } = Σ.M(d)
```
This is the collapse: π is the non-identity pivot, yet R-P1/R-P2 leave the arrangement pointwise unchanged. K.μ~ admissibility clause (ii) — non-trivial net effect `M'(d) ≠ M(d)` — fails, so the named composite K.μ~ is unavailable and none is owed.

*Empty-sequence realiser delivers `Σ' = Σ`.* With `Σ'.M(d) = Σ.M(d)` and RA-frame fixing every other component (`Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, and `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`), the REARRANGE_K transition is the identity `Σ' = Σ`. The realiser is the empty sequence of elementary transitions — admitted by ASN-0047's SequentialTransitionAxiom, whose `Σ →* Σ'` ranges over finite, possibly empty, sequences — which satisfies every elementary precondition vacuously and carries `Σ' = Σ`. Reachability of Σ' is then immediate from reachability of Σ.

*Admissibility (RA-adm).* Since `Σ' = Σ`, every per-state foundation invariant that holds at the reachable pre-state Σ holds at Σ' trivially: *S2* holds as exhibited (each V-position appears once on the left, sharing notwithstanding); *S8a*, *S8-depth*, *D-CTG★*, *D-MIN★*, *S3★*, and the remaining per-state invariants hold at Σ' because they held at Σ and Σ' is the same state. Every RE-* claim of this trace is an identity of Σ with itself — `project(e, d, Σ') = project(e, d, Σ)`, `ran(Σ'.M(d)) = ran(Σ.M(d))`, run cardinality unchanged (no run extends, since a run from `[1, 1]` would need `Σ.M(d)([1, 2]) = a + 1` but `Σ.M(d)([1, 2]) = a ≠ a + 1`, so each of the three positions is its own length-1 run — three runs at both states). The collapse branch is thus a witnessed instance, not an unexhibited appeal.

## Composition Across Multi-Step REARRANGE Sequences

Each RE-* claim is a single-step property of `Σ → Σ'`. Write `Σ →_R Σ'` for a single REARRANGE step — a transition satisfying RA-dom, RA-π, RA-frame, RA-adm for some document `d` (REARRANGE_K is one realisation). For a finite sequence `Σ₀ →_R Σ₁ →_R ⋯ →_R Σ_n`, the multi-step (★) forms follow from the single-step claims.

**Document-parameterised chaining lemma.** Let `X(Σ, d)` be any quantity that is a function of `Σ.M(d)` alone (a domain, range, multiset, or subspace frame at `d`), and suppose each REARRANGE step targeting `d` preserves `X(·, d)`. Then `X(Σ_n, d) = X(Σ_0, d)`: at each step `Σᵢ₋₁ →_R Σᵢ` targeting `dᵢ`, either `dᵢ = d` (the per-step claim preserves `X`) or `dᵢ ≠ d` (RE-other gives `Σᵢ.M(d) = Σᵢ₋₁.M(d)`, so any function of `Σ.M(d)` is preserved).

The lemma's hypothesis — `X(·, d)` a function of `Σ.M(d)` alone, preserved per step — is met by the M(d)-function bare-equality claims **RE-dom★, RE-ran★, RE-μ★, and RE-sub★**, which follow by induction. The component-global and state-independent claims (RE-C★, RE-L★, RE-R★, RE-cov★, RE-origin★) chain by the trivial induction that RA-frame fixes their underlying component at every step (RE-origin★ by state-independence); RE-disc★ and RE-proj★ chain through their per-step provenance — RE-cov★ + RE-ran★ via LP12 for the biconditional, and composition of the per-step RE-proj transports for the projection. Four ★ forms are not bare equalities and need separate treatment: three carry substantive side conditions, and one is an existence claim.

**RE-other★ (fixed `d'`).** Holds only when no step targets `d'`. Then every step has `dᵢ ≠ d'`, RE-other applies at each, and the equality chains to `Σ_n.M(d') = Σ₀.M(d')`. A step targeting `d'` changes `Σ.M(d')` by construction, breaking the chain.

**RE-ext★ (fixed `d`, fixed V-position `v`).** Unlike RE-sub★ (whose non-S condition depends only on `v`'s structural subspace identifier), RE-ext's exterior condition is cut-sequence-specific: `v` may be exterior to one step's cut sequence and interior to another's. The ★ form therefore requires, at every step targeting `d` with cut sequence `Kᵢ` of cut subspace `Sᵢ`, either `v ∉ V_{Sᵢ}(Σᵢ₋₁.M(d))` (RE-ext vacuous) or `v ∈ V_{Sᵢ}(Σᵢ₋₁.M(d))` with `v < c₀,ᵢ` or `v ≥ c_{n−1},ᵢ` (RE-ext fires); steps with `dᵢ ≠ d` fix `v` by RE-other. Under that restriction the pointwise fixity chains. When some step both targets `d` and places `v` in its affected range, the ★ form is silent at that pair.

**RE-trans★.** Conclusions (i) `a ∈ ran(Σ_n.M(d))` and (ii) unchanged multiplicity compose unconditionally via the chaining lemma on `ran(M(d))` and `μ_a(M(d))`. Conclusion (iii) — `origin(a)`'s arrangement unchanged — restricts to sequences where no step targets `origin(a)` (then RE-other chains); a step targeting `origin(a)` permutes its arrangement, leaving (i)+(ii) at `d` intact but breaking (iii).

**RE-frag★ / RE-coal★ / RE-eq★ (arbitrary per-step direction).** An existence claim, not a chained invariant. For every `n ≥ 1` and every direction sequence `(s_1, …, s_n) ∈ {+, −, =}^n` (strict increase / strict decrease / exact preservation of run-decomposition cardinality), there is a sequence `Σ_0 →_R ⋯ →_R Σ_n` targeting a single `d` in which step `i` realises `s_i`. Construction by spatial partitioning: choose `n` pairwise-disjoint content-subspace sub-ranges (D-SEQ★'s contiguous-prefix characterisation of `V_{s_C}(d)` admits arbitrary finite `n`); populate the i-th with the single-step witness pattern for `s_i` (fragmentation, coalescence, or equality from "Run Decomposition Is Not Invariant"); at step `i` apply REARRANGE_K confined to the i-th sub-range. RE-ext preserves every other sub-range pointwise across step `i`, so the patterns staged for later steps survive intact and the directions realise independently. No uniform per-step monotonicity, and no claim about net cardinality change, is asserted.

For mixed sequences interleaving REARRANGE with other transitions, each non-REARRANGE step is governed by its ASN-0098 projection lemma — LP6 (K.α), LP7 (K.λ), LP9 (K.μ⁺ / K.μ⁺_L), LP10 (K.μ⁻), LP14 (K.ρ), LP8 (registration) — and each REARRANGE step by LP11 (ReorderingBijection). The closure properties above apply only to pure REARRANGE sub-sequences; coverage- and arrangement-tied properties (RE-cov, RE-disc, RE-proj) require care across mixed sequences, since intervening steps can shift coverage relationships even while leaving individual endsets verbatim (LP3, ASN-0098).

## Claims Introduced

The *Provenance* column records each claim's premises — abstract, REARRANGE_K, or structural.

| Label | Statement | Provenance | Status |
|-------|-----------|-----------|--------|
| RA-reg | Rearrangement registration precondition: d ∈ dom(Σ.M) | abstract (definition) | introduced |
| RA-dom | Rearrangement domain stability: dom(Σ'.M(d)) = dom(Σ.M(d)) | abstract (definition); REARRANGE_K realisation: ASN-0084's PivotPostcondition / SwapPostcondition domain clause dom(M'(d)) = dom(M(d)) | introduced |
| RA-π | Rearrangement equation: π : dom(Σ.M(d)) → dom(Σ'.M(d)) is a bijection with Σ'.M(d)(π(v)) = Σ.M(d)(v) for every v ∈ dom(Σ.M(d)) | abstract (definition); REARRANGE_K realisation: ASN-0084's R-PPERM (3-cut) / R-SPERM (4-cut), each a bijection of dom(Σ.M(d)) onto dom(Σ'.M(d)) with Σ'.M(d)(π(v)) = Σ.M(d)(v) | introduced |
| RA-frame | Rearrangement frame: Σ'.C = Σ.C, Σ'.L = Σ.L, Σ'.E = Σ.E, Σ'.R = Σ.R, dom(Σ'.M) = dom(Σ.M), and Σ'.M(d') = Σ.M(d') for every d' ∈ dom(Σ.M) with d' ≠ d | abstract (definition); REARRANGE_K realisation: K.μ~'s ASN-0047 frame (C' = C; E' = E; R' = R; L' = L; M'(d') = M(d') for d' ≠ d) matches each conjunct explicitly except dom(Σ'.M) = dom(Σ.M), which follows structurally since neither K.μ⁻ nor K.μ⁺ touches the document registry (registration is the exclusive province of K.σ and K.δ Document case) | introduced |
| RA-adm | Rearrangement admissibility: every per-state foundation invariant satisfied by Σ is satisfied by Σ' | abstract (definition); REARRANGE_K realisation: the K.μ~-validity / empty-composite argument makes Σ' reachable, whence the per-state foundation invariants follow at Σ' | introduced |
| RE-C | Content-store invariance: Σ'.C = Σ.C under REARRANGE | abstract (from RA-frame) | introduced |
| RE-dom | Domain stability: dom(Σ'.M(d)) = dom(Σ.M(d)) | abstract (from RA-dom) | introduced |
| RE-ran | Range invariance: ran(Σ'.M(d')) = ran(Σ.M(d')) for every d' ∈ dom(Σ.M) | abstract (target case from RA-π; non-target case from RA-frame's other-document clause) | introduced |
| RE-μ | Per-address multiplicity invariance: μ_a(Σ'.M(d')) = μ_a(Σ.M(d')) for every I-address a and every d' ∈ dom(Σ.M) | abstract (target case from RA-π; non-target case from RA-frame's other-document clause) | introduced |
| RE-L | Link store invariance: dom(Σ'.L) = dom(Σ.L) and Σ'.L(a) = Σ.L(a) for every a ∈ dom(Σ.L) | abstract (from RA-frame) | introduced |
| RE-cov | Coverage invariance: coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ) for every link a and slot i | abstract (from RE-L) | introduced |
| RE-disc | Discoverability invariance: discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ) for every link a and document d | abstract (from RE-cov + RE-ran via LP12) | introduced |
| RE-proj | Projection transport: project(e, d, Σ') = π̂_d(project(e, d, Σ)) for every endset e and every d ∈ dom(Σ.M), where π̂_d := π at the rearrangement target d_tgt and π̂_d := id_{dom(Σ.M(d))} for d ≠ d_tgt. Equivalently at d_tgt: project(e, d_tgt, Σ') = π(project(e, d_tgt, Σ)) | abstract (target case from RA-π + coverage state-independence (ASN-0098); non-target case from RE-other) | introduced |
| RE-frag | Fragmentation possibility: there exist REARRANGE instances where the maximal-run-decomposition cardinality of M(d) strictly increases | abstract (existential; witnesses are REARRANGE_K) | introduced |
| RE-coal | Coalescence possibility: there exist REARRANGE instances where the maximal-run-decomposition cardinality of M(d) strictly decreases | abstract (existential; witnesses are REARRANGE_K) | introduced |
| RE-eq | Cardinality invariance possibility: there exist REARRANGE instances where the maximal-run-decomposition cardinality of M(d) is exactly preserved | abstract (existential; witnesses are REARRANGE_K) | introduced |
| RE-other | Other-document invariance: Σ'.M(d') = Σ.M(d') for every d' ≠ d | abstract (from RA-frame) | introduced |
| RE-trans | Transclusion preservation: for every (a, d) with a ∈ ran(Σ.M(d)) and origin(a) ≠ d, (i) a ∈ ran(Σ'.M(d)) and (ii) the multiplicity of a at d is preserved — both unconditional in d; (iii) origin(a)'s arrangement is unchanged when origin(a) ≠ d_tgt (the rearrangement target) | abstract: (i)+(ii) from RE-ran + RE-μ; (iii) from RE-other applied at d' = origin(a), requiring origin(a) ≠ d_tgt | introduced |
| RE-sub | Subspace frame: for every v ∈ dom(M(d)) with subspace(v) ≠ S, π(v) = v and Σ'.M(d)(v) = Σ.M(d)(v) | REARRANGE_K (π-fixity from R-PPERM/R-SPERM non-S branch; arrangement preservation from R-FRAME-P/S(a)) | introduced |
| RE-ext | In-subspace exterior frame: for every v ∈ V_S(d) with v < c₀ or v ≥ c_{n−1}, π(v) = v and Σ'.M(d)(v) = Σ.M(d)(v) | REARRANGE_K (π-fixity from R-PPERM/R-SPERM exterior branch; arrangement preservation from R-EXT) | introduced |
| RE-origin | Origin invariance: origin(a) is unchanged across REARRANGE for every a | structural (state-independent) | introduced |
| RE-R | Provenance invariance: Σ'.R = Σ.R under REARRANGE | abstract (from RA-frame; equivalently, J3 for REARRANGE_K) | introduced |

The ★ forms catalog the multi-step composed claims derived in the "Composition Across Multi-Step REARRANGE Sequences" section, for a finite sequence of REARRANGE-only transitions `Σ_0 →_R Σ_1 →_R ⋯ →_R Σ_n`. The *Composition Conditions* column records the restriction (if any) under which each ★ form holds.

| Label | Statement | Composition Conditions | Provenance | Status |
|-------|-----------|------------------------|-----------|--------|
| RE-C★ | Multi-step content-store invariance: Σ_n.C = Σ_0.C | none | abstract (from RE-C) | introduced |
| RE-L★ | Multi-step link-store invariance: dom(Σ_n.L) = dom(Σ_0.L) and Σ_n.L(a) = Σ_0.L(a) for every a ∈ dom(Σ_0.L) | none | abstract (from RE-L) | introduced |
| RE-R★ | Multi-step provenance invariance: Σ_n.R = Σ_0.R | none | abstract (from RE-R) | introduced |
| RE-dom★ | Multi-step domain stability at fixed d: dom(Σ_n.M(d)) = dom(Σ_0.M(d)) | none | abstract (from RE-dom + RE-other case split) | introduced |
| RE-ran★ | Multi-step range invariance at fixed d: ran(Σ_n.M(d)) = ran(Σ_0.M(d)) | none | abstract (from RE-ran + RE-other case split) | introduced |
| RE-μ★ | Multi-step per-address multiplicity invariance: μ_a(Σ_n.M(d)) = μ_a(Σ_0.M(d)) for every I-address a and document d | none | abstract (from RE-μ + RE-other case split) | introduced |
| RE-cov★ | Multi-step coverage invariance: coverage(Σ_n.L(a).eᵢ) = coverage(Σ_0.L(a).eᵢ) for every link a and slot i | none | abstract (from RE-cov) | introduced |
| RE-disc★ | Multi-step discoverability invariance: discoverable_from(a, d, Σ_n) ⟺ discoverable_from(a, d, Σ_0) for every link a and document d | none | abstract (from RE-disc) | introduced |
| RE-proj★ | Multi-step projection transport: project(e, d, Σ_n) = (π̂_n ∘ ⋯ ∘ π̂_1)(project(e, d, Σ_0)), where π̂_i = π_i on steps targeting d and π̂_i = id otherwise | none | abstract (from RE-proj + RE-other) | introduced |
| RE-other★ | Multi-step other-document invariance at fixed d': Σ_n.M(d') = Σ_0.M(d') | no step in the sequence targets d' | abstract (from RE-other) | introduced |
| RE-sub★ | Multi-step subspace frame at fixed d: for every v ∈ dom(Σ_0.M(d)) with subspace(v) ≠ S, the V-position remains pointwise fixed and its image is preserved across all steps targeting d | none (per-step RE-sub chains through identity on non-targeting steps) | REARRANGE_K (inherits RE-sub's pointwise-fixity premise) | introduced |
| RE-ext★ | Multi-step in-subspace exterior frame at fixed d: for every v that lies in the in-S exterior of every targeted step (i.e., for every step `Σᵢ₋₁ →_R Σᵢ` targeting d with cut sequence Kᵢ and cut subspace Sᵢ, v ∈ V_{Sᵢ}(Σᵢ₋₁.M(d)) ∧ (v < c₀,ᵢ ∨ v ≥ c_{n−1},ᵢ), or the step does not target d), the V-position remains pointwise fixed and its image is preserved across all such steps | the v in question must lie in the in-S exterior of every step in the sequence that targets d; for steps not targeting d, RE-other applies and v is fixed unconditionally | REARRANGE_K (inherits RE-ext's pointwise-fixity premise) | introduced |
| RE-trans★ | Multi-step transclusion preservation: (i) (a, d) transclusion persists and (ii) multiplicity is preserved unconditionally; (iii) origin(a)'s arrangement is unchanged | (iii) requires no step in the sequence targets origin(a); (i)+(ii) require no restriction | abstract (from RE-trans + RE-other case split) | introduced |
| RE-frag★ / RE-coal★ / RE-eq★ | Arbitrary per-step direction: for every n ≥ 1 and every finite direction sequence (s_1, ..., s_n) ∈ {+, −, =}^n, there exists a multi-step REARRANGE sequence Σ_0 →_R ⋯ →_R Σ_n targeting a single document d such that step i realises direction s_i (+ = strict increase, − = strict decrease, = = exact preservation of run-decomposition cardinality); no uniform per-step monotonicity is asserted, and the concatenation construction (spatial partitioning into disjoint sub-ranges with RE-ext bridging between steps) supplies the per-step realisability | none (existential; concatenation construction proves it) | abstract (from RE-frag/coal/eq single-step witnesses + RE-ext for sub-range pointwise preservation across non-targeting steps) | introduced |
| RE-origin★ | Multi-step origin invariance: origin(a) is unchanged across the sequence for every I-address a | none | structural (state-independent) | introduced |

## Open Questions

What guarantees must rearrangement preserve about cross-document transclusion when a cut splits a span transcluded from the same source document into two non-contiguous pieces?
What semantics, if any, should rearrangement carry on the link subspace, and what invariants would such an operation be required to preserve?
Under what conditions are two distinct rearrangement transitions observationally equivalent at the level of link discoverability rather than at the level of arrangement equality?
What upper bound, if any, can be placed on the increase in maximal-run-decomposition cardinality from a single rearrangement invocation?
Can every bijection of dom(M(d)) that preserves the arrangement well-formedness invariants be realized by a finite composition of cut-sequence rearrangements?
