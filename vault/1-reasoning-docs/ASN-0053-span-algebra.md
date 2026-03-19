# ASN-0053: Span Algebra

*2026-03-18*

ASN-0034 gave us the tumbler space T with its total order (T1) and its arithmetic — the addition ⊕ that advances along the tumbler line, the subtraction ⊖ that recovers displacements. It defined a span σ = (s, ℓ) as a well-formed pair satisfying T12: ℓ is positive, the action point of ℓ falls within #s, and σ denotes the half-open interval ⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}. By TA-strict, every span is non-empty.

But a single span is merely a building block. The system must compare spans — do they overlap? It must combine them — what do they jointly cover? It must decompose them — what results from splitting at a point? And it must reduce collections of them to canonical form — is there a unique minimal representation? We are looking for the laws this algebra satisfies. The question, as always, is: what must any implementation maintain?

Nelson provides span-sets as the mechanism for arbitrary content designation: "if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans" (LM 4/25). And he expects front-ends to manipulate them fluently: "The manipulation of request sets is an important aspect of what front-end functions do. Understanding spans is a key to appropriate software design for handling request-sets" (LM 4/37). Gregory confirms the implementation: two dedicated merge sites in the backend (the enfilade-level `isanextensionnd` and the output-level `putvspaninlist`) enforce precise adjacency and overlap conditions on spans. The algebra is not merely convenient — it is load-bearing.


## The reach function

For a span σ = (s, ℓ), we write:

  start(σ) = s,    width(σ) = ℓ,    reach(σ) = s ⊕ ℓ

The reach is the first position beyond σ — the exclusive upper bound. It is well-defined by TA0 and satisfies reach(σ) > start(σ) by TA-strict. Two spans with the same start and reach denote the same set of positions, because a span's content is entirely determined by its endpoints: Nelson states that "there is no choice as to what lies between; this is implicit in the choice of first and last point" (LM 4/25).

We shall need the reverse: given two positions a ≤ b on the tumbler line, can we recover the displacement from a to b — the unique width w such that a ⊕ w = b?

From TumblerAdd, a ⊕ w acts at the action point k of w: it copies a₁..aₖ₋₁, advances aₖ by wₖ, and replaces the tail with w's tail. So if a ⊕ w = b, then a and b agree on components 1..k−1 and diverge at k, with bₖ = aₖ + wₖ and bᵢ = wᵢ for i > k. Reading off the width:

  wᵢ = 0  for i < k,    wₖ = bₖ − aₖ,    wᵢ = bᵢ  for i > k

where k = divergence(a, b). This is exactly the formula for b ⊖ a from ASN-0034's TumblerSubtract. We write w = b ⊖ a and call it the *displacement from a to b*. The displacement is well-defined when:

**D0** (*Displacement well-definedness*). a < b, and the divergence k of a and b satisfies k ≤ #a.

D0 ensures the displacement b ⊖ a is a well-defined positive tumbler, and that a ⊕ (b ⊖ a) is defined (TA0 satisfied, since the displacement is positive and its action point k ≤ #a). It does not guarantee round-trip faithfulness — the identity a ⊕ (b ⊖ a) = b additionally requires #a = #b. When #a > #b, TumblerSubtract produces a displacement of length max(#a, #b) = #a, and the round-trip a ⊕ (b ⊖ a) yields a tumbler of length #a; since #a > #b, this result cannot equal b (by T3). (The case #a < #b with type (i) divergence — where a and b differ at a shared position, so k ≤ #a — also admits a faithful round-trip, since the D1 proof depends only on k ≤ #a, not on #a = #b. But when #a < #b and a is a proper prefix of b, the divergence is k = #a + 1 > #a, violating TA0 — no valid displacement exists. Since every span operation below uses level-uniform spans with #start = #reach, the equal-length case is all we need.) We formalize the sufficient condition as level compatibility in S6.

When a is a proper prefix of b (divergence type (ii) from ASN-0034), the divergence is #a + 1, exceeding #a, and no valid displacement exists.

We verify the round-trip for level-uniform spans (see S6). Given a level-uniform span σ = (s, ℓ) with #s = #ℓ and action point k, reach(σ) = s ⊕ ℓ with #reach = #s (since #(s ⊕ ℓ) = max(k − 1, 0) + (#ℓ − k + 1) = #ℓ = #s). Computing reach(σ) ⊖ start(σ): both have length #s, so no zero-padding is needed. The divergence is at position k (since sᵢ = (s ⊕ ℓ)ᵢ for i < k and sₖ ≠ (s ⊕ ℓ)ₖ because ℓₖ > 0). Then (reach ⊖ start)ₖ = (sₖ + ℓₖ) − sₖ = ℓₖ, and (reach ⊖ start)ᵢ = (s ⊕ ℓ)ᵢ = ℓᵢ for i > k, and zero for i < k. The result has length max(#reach, #start) = #s = #ℓ. This is ℓ itself. So:

  reach(σ) ⊖ start(σ) = width(σ)       (level-uniform spans)

The width is recoverable from the endpoints. Conversely, start(σ) ⊕ width(σ) = reach(σ) by definition. Of the three quantities — start, width, reach — two of the three pairings determine the third: start and width determine reach (by definition of ⊕); start and reach determine width (by the calculation above, via ⊖). But width and reach do not determine start. The many-to-one property of TumblerAdd (noted in ASN-0034) means distinct starts can produce the same reach under the same width: when the action point k falls before the last component of s, positions k+1..#s are replaced by the width's tail and are unrecoverable from the reach. For instance, s₁ = [1, 3, 5] and s₂ = [1, 3, 7] with width [0, 2, 4] (action point k = 2) both yield reach [1, 5, 4]. Same width, same reach, different starts — and different denotations.

We promote this to a general identity:

**D1** (*DisplacementRoundTrip*). For tumblers a, b ∈ T with a < b and #a = #b:

  a ⊕ (b ⊖ a) = b

*Proof.* Let k = divergence(a, b). Since #a = #b, this is type (i) divergence with k ≤ #a and aₖ < bₖ. Define w = b ⊖ a by TumblerSubtract: wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k. The result has length #a. Now w > 0 since wₖ > 0, and the action point of w is k ≤ #a, so TA0 is satisfied. Applying TumblerAdd: (a ⊕ w)ᵢ = aᵢ = bᵢ for i < k (before divergence), (a ⊕ w)ₖ = aₖ + (bₖ − aₖ) = bₖ, and (a ⊕ w)ᵢ = wᵢ = bᵢ for i > k. Every component matches: a ⊕ w = b.  ∎

When a = b, no displacement is needed; the degenerate case is handled separately since b ⊖ a produces the zero tumbler and a ⊕ (b ⊖ a) is not well-formed (TA0 requires w > 0). D0 ensures the displacement is well-defined; D1 ensures the round-trip is faithful for a < b. Every proof below that constructs a span γ = (s, r ⊖ s) and asserts ⟦γ⟧ = {t : s ≤ t < r} depends on D1: the span's reach is s ⊕ (r ⊖ s) = r.

When #start > #width, the round-trip fails: the reach has length #width (shorter than start), so TumblerSubtract zero-pads reach to length #start, producing a result of length #start ≠ #width. For instance, σ = ([1, 3, 5], [0, 2]) has reach [1, 5], but [1, 5] ⊖ [1, 3, 5] = [0, 2, 0] ≠ [0, 2].


## Convexity

The first property of spans is that they admit no gaps:

**S0** (*Convexity*). `(A p, q, r : p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ p ≤ q ≤ r : q ∈ ⟦σ⟧)`

*Proof.* If start(σ) ≤ p ≤ q ≤ r < reach(σ), then start(σ) ≤ q < reach(σ), so q ∈ ⟦σ⟧.  ∎

This follows solely from T1 being a total order. Every position between two members of a span is itself a member — a span cannot "skip" a position. In topological terms, half-open intervals on a total order are convex. The hierarchical structure of tumbler addresses does not affect this: sub-addresses like [1, 3, 0, 5] that fall numerically between [1, 3] and [1, 7] are genuinely interior to any span containing both endpoints, because `tumblercmp` compares tumblers lexicographically without treating zero-separators specially (Gregory, Q11). The ordering is flat even though the addresses are hierarchical.


## How two spans relate

**SC** (*SpanClassification*). Given spans α and β, their relationship is determined by comparing starts and reaches under T1. Since T1 is a total order, five mutually exclusive cases arise:

(i) *Separated.* reach(α) < start(β) or reach(β) < start(α). The spans share no positions and have space between them.

(ii) *Adjacent.* reach(α) = start(β) or reach(β) = start(α). The spans share no positions but touch at a single boundary point.

(iii) *Proper overlap.* The spans share positions but neither contains the other: start(α) < start(β) < reach(α) < reach(β), or symmetrically.

(iv) *Containment.* One span's denotation is a proper subset of the other's: start(α) ≤ start(β) and reach(β) ≤ reach(α) with at least one inequality strict, or symmetrically.

(v) *Equal.* start(α) = start(β) and reach(α) = reach(β).

Cases (i) and (ii) are the *disjoint* cases — ⟦α⟧ ∩ ⟦β⟧ = ∅. Cases (iii), (iv), and (v) are the *overlapping* cases — ⟦α⟧ ∩ ⟦β⟧ ≠ ∅.

*Exhaustiveness.* Assume without loss of generality that start(α) ≤ start(β) (the symmetric cases are covered by the "or symmetrically" clauses). Compare reach(α) with start(β): if reach(α) < start(β), case (i); if reach(α) = start(β), case (ii); if reach(α) > start(β), the spans share positions. In the sharing case, compare start(α) with start(β): if start(α) < start(β), compare reach(α) with reach(β) — reach(α) < reach(β) gives case (iii), reach(α) ≥ reach(β) gives case (iv). If start(α) = start(β), compare reaches — reach(α) = reach(β) gives case (v), otherwise case (iv). Every ordering of the four boundary points {start(α), reach(α), start(β), reach(β)}, subject to start < reach for each span, falls into exactly one case. No sixth case exists.


## The level constraint

The properties that follow — intersection, merge, split, normalization — require span operands to be *level-compatible*. We formalize this now, since every subsequent operation depends on it.

**S6** (*LevelConstraint*). Two tumblers t₁ and t₂ are *level-compatible*, written level_compat(t₁, t₂), when they have the same length:

  level_compat(t₁, t₂)  ≡  #t₁ = #t₂

A span σ = (s, ℓ) is *level-uniform* when level_compat(s, ℓ), i.e., #s = #ℓ. For a level-uniform span, #reach(σ) = #s: since the action point k satisfies 1 ≤ k ≤ #s = #ℓ, we have #(s ⊕ ℓ) = max(k − 1, 0) + (#ℓ − k + 1) = #ℓ = #s. The start, width, and reach all share the same tumbler length. Level-uniform spans automatically satisfy D0 for all endpoint pairs: since #start = #reach, neither is a proper prefix of the other, so divergence is of type (i) with k ≤ #start.

The constraint is not merely technical — it reflects the tree structure of the tumbler space. A tumbler [1, 3, 0, 5] has four components spanning two hierarchical levels (separated by zero). A span with start [1, 3] and width [0, 2] operates at depth 2 — it varies position 2 while position 1 is fixed. An interior point at a deeper level, such as [1, 3, 0, 1], diverges from [1, 3] at position 3 (after zero-padding), exceeding #[1, 3] = 2. No valid displacement exists. A span defined at one depth can only interact with points at that same depth.

In a flat address space (integers), every interior point would admit a valid split. The tumbler space, being hierarchical, stratifies positions by depth, and arithmetic must respect this stratification. The subspace closure TA7a from ASN-0034 captures the favorable case: within a single subspace using ordinal-only representation, addition and subtraction are fully closed. This is the abstract guarantee that span operations work for the common case of content within a document subspace.

Gregory confirms the implementation enforces this: the split operation checks `tumblerlength(cut) = tumblerlength(width)` and aborts with a fatal error when the invariant is violated (Q14, Q15). The level constraint is load-bearing.


## Intersection

**S1** (*IntersectionClosure*). For level-uniform spans α and β with level_compat(start(α), start(β)), the intersection is either empty or a single span. No configuration of two such spans produces a fragmented intersection.

Formally: for level-uniform spans α and β with level_compat(start(α), start(β)), either ⟦α⟧ ∩ ⟦β⟧ = ∅, or there exists a span γ such that ⟦γ⟧ = ⟦α⟧ ∩ ⟦β⟧.

*Proof.* Define s' = max(start(α), start(β)) and r' = min(reach(α), reach(β)). If r' ≤ s', the intersection is empty — this covers the separated and adjacent cases. Otherwise r' > s', and:

  ⟦α⟧ ∩ ⟦β⟧ = {t : s' ≤ t < r'}

This is a half-open interval. The set is non-empty (s' is a member since s' < r'). By level-uniformity and S6, all boundary tumblers — start(α), reach(α), start(β), reach(β) — share the same length. So #s' = #r', and by D1 the interval is representable as a span γ = (s', r' ⊖ s') with reach(γ) = s' ⊕ (r' ⊖ s') = r'. We verify T12 for γ: since s' < r', the divergence k satisfies k ≤ #s' (type (i) divergence, as #s' = #r' excludes the prefix case), and the width r' ⊖ s' has a positive component at position k (namely r'ₖ − s'ₖ > 0), so the width is positive and its action point k ≤ #s'. The constructed span is well-formed.  ∎

The significance is topological: convex sets in a total order have convex intersection. The tumbler space's hierarchical structure cannot fragment an intersection — there is no configuration where two contiguous regions share a disconnected collection of positions. Gregory confirms this from the implementation: the function `spanintersection` always produces at most one output span (Q10, `correspond.c:210-265`). Nelson confirms it from design intent: the system "knows precisely" what two regions share, "because correspondence is a structural relation derivable from I-addresses" (Q1).

A concrete instance: let α = ([1, 3], [0, 4]) and β = ([1, 5], [0, 6]). Then reach(α) = [1, 7], reach(β) = [1, 11], s' = [1, 5], r' = [1, 7]. The intersection is ([1, 5], [0, 2]) — a single span covering positions [1, 5] through [1, 7) exclusive.


## The empty set is not a span

**S2** (*EmptyDistinction*). The empty set of positions is not the denotation of any span. Every well-formed span denotes a non-empty set.

This follows from T12 and TA-strict: ℓ > 0 and k ≤ #s imply s ⊕ ℓ > s, so the half-open interval [s, s ⊕ ℓ) contains at least s itself.

The distinction matters: the result of intersecting two disjoint spans is the *absence* of a span, not a "span of zero width." These are categorically different. A span always designates an address range — including ranges over currently unoccupied positions. Nelson calls these "ghost elements": "Things may be addressed even though nothing is there to represent them in storage... It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them" (LM 4/23). A span over unpopulated space is a genuine reference — one can link to it, and "a span that contains nothing today may at a later time contain a million documents" (LM 4/25). An empty intersection is no reference at all.

Nelson is explicit about the three-way distinction (Q7):

| State | Meaning | Linkable? |
|-------|---------|-----------|
| Span over populated space | Covers allocated content | Yes |
| Span over unpopulated space | Valid address range, no content yet | Yes |
| Empty result (no spans) | No address range | No |

The span algebra distinguishes only the last from the first two. Whether a span's positions are populated is a content-layer concern, outside this algebra. At our level of abstraction, there are spans (non-empty, always) and the empty set (not a span, never).


## Merge

Two spans α and β are *adjacent* when the reach of one equals the start of the other:

  adjacent(α, β)  ≡  reach(α) = start(β)  ∨  reach(β) = start(α)

Adjacent spans share no positions (reach is an exclusive upper bound) but their denotations abut — there is no gap between them.

**S3** (*MergeEquivalence*). For level-uniform spans α and β with level_compat(start(α), start(β)), when they overlap or are adjacent, the union ⟦α⟧ ∪ ⟦β⟧ is the denotation of a single span. Moreover, this merged span is identical to one specified directly with the same endpoints.

*Proof.* Without loss of generality, assume start(α) ≤ start(β). The overlap-or-adjacency condition means reach(α) ≥ start(β). Define:

  s = start(α) = min(start(α), start(β))
  r = max(reach(α), reach(β))

Then ⟦α⟧ ∪ ⟦β⟧ = {t : s ≤ t < r}. To verify the union: every position in ⟦α⟧ satisfies s ≤ t (since s = start(α)) and t < r (since reach(α) ≤ r). Every position in ⟦β⟧ satisfies s ≤ t (since start(β) ≥ start(α) = s) and t < r (since reach(β) ≤ r). Conversely, any t with s ≤ t < r falls in ⟦α⟧ if t < reach(α), or in ⟦β⟧ if t ≥ start(β) — and the overlap/adjacency condition reach(α) ≥ start(β) ensures no position is missed.

The merged span γ = (s, r ⊖ s) denotes {t : s ≤ t < r}. Level-uniformity and S6 ensure #s = #r (both are starts or reaches of level-uniform spans at the same length), so by D1 the reach is s ⊕ (r ⊖ s) = r. We verify T12 for γ: since s < r (the union is non-empty), the divergence k satisfies k ≤ #s (type (i), as #s = #r), and the width r ⊖ s has a positive component at position k (rₖ − sₖ > 0 at the divergence point). The action point of the width is k ≤ #s, so γ is well-formed. The denotation depends only on the endpoints s and r, not on the history of how they were obtained — confirming Nelson's assertion that "there is no choice as to what lies between" (LM 4/25).  ∎

A concrete instance (reusing S1's spans): let α = ([1, 3], [0, 4]) and β = ([1, 5], [0, 6]). Then reach(α) = [1, 7] and reach(β) = [1, 11]. Since start(α) = [1, 3] ≤ start(β) = [1, 5] and reach(α) = [1, 7] > start(β) = [1, 5], the spans overlap. We have s = [1, 3] and r = max([1, 7], [1, 11]) = [1, 11]. The merged span is γ = ([1, 3], [1, 11] ⊖ [1, 3]) = ([1, 3], [0, 8]) — divergence at position 2 gives 11 − 3 = 8. Verify: reach(γ) = [1, 3] ⊕ [0, 8] = [1, 11]. And ⟦α⟧ ∪ ⟦β⟧ = {t : [1, 3] ≤ t < [1, 7]} ∪ {t : [1, 5] ≤ t < [1, 11]} = {t : [1, 3] ≤ t < [1, 11]} = ⟦γ⟧ — the overlap region [1, 5]..[1, 7) is covered by both spans, and the union fills the interval without gaps.

Nelson grounds this in the normalization guarantee: "A spanset may be presented to the back end with any degree of overlap among the spans. This is because the system in effect performs a boolean OR to create a normalized specset, i.e. a non-overlapping coverage of the same portion of tumbler-space" (LM 4/37, Q3). The system treats {[a, b], [b, c]} and {[a, c]} as equivalent representations of the same address range.

**S3a** (*MergeCommutativity*). The merge of α and β yields the same span as the merge of β and α: ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧. This follows from set union being commutative.


## Split

Splitting is the reverse of merging: given a span σ and a point interior to it, decompose σ into two adjacent parts that together reconstitute the original.

**Definition** (*Interior point*). A position p is *interior* to span σ when start(σ) < p < reach(σ). By S0, every interior point is in ⟦σ⟧.

**S4** (*SplitPartition*). For a level-uniform span σ = (s, ℓ) and an interior point p with level_compat(s, p), the displacements d = p ⊖ s and d' = reach(σ) ⊖ p are well-defined with #d = #s = #d' (all tumblers at the same length). The left span λ = (s, d) and right span ρ = (p, d') satisfy:

  (a) ⟦λ⟧ ∪ ⟦ρ⟧ = ⟦σ⟧                  (nothing lost)
  (b) ⟦λ⟧ ∩ ⟦ρ⟧ = ∅                      (nothing duplicated)
  (c) reach(λ) = start(ρ) = p             (the parts are adjacent)

*Proof.* First we verify T12 for both constructed spans. For λ = (s, d) where d = p ⊖ s: since s < p and #s = #p, the divergence k is of type (i) with k ≤ #s, and dₖ = pₖ − sₖ > 0, so d is positive with action point k ≤ #s. For ρ = (p, d') where d' = reach(σ) ⊖ p: since p < reach(σ) and #p = #reach(σ) (level-uniformity gives #reach = #s = #p), the divergence k' is of type (i) with k' ≤ #p, and d'ₖ' > 0. Both spans are well-formed.

(a): ⟦λ⟧ ∪ ⟦ρ⟧ = {t : s ≤ t < p} ∪ {t : p ≤ t < reach(σ)} = {t : s ≤ t < reach(σ)} = ⟦σ⟧.

(b): ⟦λ⟧ ∩ ⟦ρ⟧ = {t : s ≤ t < p ∧ p ≤ t} = ∅, since t < p and t ≥ p cannot both hold.

(c): Since #s = #p (level compatibility) and s < p, D1 gives s ⊕ (p ⊖ s) = p. So reach(λ) = s ⊕ d = p = start(ρ).  ∎

A concrete instance: let σ = ([1, 0, 1, 0, 1, 0, 5], [0, 0, 0, 0, 0, 0, 8]), a level-uniform span with #s = #ℓ = 7. The action point is k = 7, giving reach = [1, 0, 1, 0, 1, 0, 13]. Split at p = [1, 0, 1, 0, 1, 0, 9], which is interior (s < p < reach at position 7) and level-compatible (#p = 7 = #s).

We compute d = p ⊖ s: divergence at position 7 (9 vs 5), so d = [0, 0, 0, 0, 0, 0, 4]. And d' = reach ⊖ p: divergence at position 7 (13 vs 9), so d' = [0, 0, 0, 0, 0, 0, 4]. Both have length 7 = #s.

The split parts: λ = ([1, 0, 1, 0, 1, 0, 5], [0, 0, 0, 0, 0, 0, 4]) and ρ = ([1, 0, 1, 0, 1, 0, 9], [0, 0, 0, 0, 0, 0, 4]).

Verify S4: (a) ⟦λ⟧ ∪ ⟦ρ⟧ = {t : [.., 5] ≤ t < [.., 9]} ∪ {t : [.., 9] ≤ t < [.., 13]} = {t : [.., 5] ≤ t < [.., 13]} = ⟦σ⟧. (b) ⟦λ⟧ ∩ ⟦ρ⟧ = ∅ (t < [.., 9] vs t ≥ [.., 9]). (c) reach(λ) = [.., 5] ⊕ [.., 4] = [.., 9] = p = start(ρ).

Verify S5: d ⊕ d' = [0, 0, 0, 0, 0, 0, 4] ⊕ [0, 0, 0, 0, 0, 0, 4]. Action point k = 7: 4 + 4 = 8. Result = [0, 0, 0, 0, 0, 0, 8] = ℓ.

Each element of ⟦σ⟧ appears in exactly one of ⟦λ⟧ or ⟦ρ⟧ — those before p go left, those from p onward go right. The partition is forced by the total order; there is no ambiguity. Nelson confirms the structural basis: "each element occupies exactly one position on the tumbler line" and spans include "everything between their endpoints with no discretion" (Q2). The REARRANGE operation's three-cut semantics depend on this: "cut 2 is simultaneously the boundary of both regions — the first region ends where the second begins" (Q2).

We need a small lemma about tumbler addition before stating the composition property. (This is properly a tumbler arithmetic fact, belonging with ASN-0034; we state it here because S5 depends on it.)

**Lemma** (*LeftCancellation*). If a ⊕ x = a ⊕ y with both sides well-defined, then x = y.

*Proof.* Let k₁ and k₂ be the action points of x and y. If k₁ < k₂, then (a ⊕ x)ₖ₁ = aₖ₁ + xₖ₁ while (a ⊕ y)ₖ₁ = aₖ₁ (position k₁ falls in the "copy from start" range of y). Equality gives xₖ₁ = 0, contradicting k₁ being the action point of x. Symmetrically k₂ < k₁ is impossible. So k₁ = k₂ = k. At position k: aₖ + xₖ = aₖ + yₖ gives xₖ = yₖ. For i > k: xᵢ = (a ⊕ x)ᵢ = (a ⊕ y)ᵢ = yᵢ. For i < k: xᵢ = 0 = yᵢ. Every component agrees, so x = y.  ∎

**S5** (*SplitWidthComposition*). Under the same conditions as S4, the widths of the two parts compose to the original width:

  d ⊕ d' = ℓ

*Proof.* By D1, s ⊕ d = p (since s < p and #s = #d = #p). By D1 again, p ⊕ d' = reach(σ) (since p < reach(σ) and #p = #d' = #reach). Chaining:

  (s ⊕ d) ⊕ d' = reach(σ) = s ⊕ ℓ

By the Associativity lemma from ASN-0034 (both compositions are well-defined since all tumblers have length #s):

  s ⊕ (d ⊕ d') = s ⊕ ℓ

By left-cancellation, d ⊕ d' = ℓ.  ∎

This composition property makes split and merge inverses: merge the two split parts, and the resulting width is d ⊕ d' = ℓ, recovering the original span exactly. Gregory confirms the implementation achieves this by computing the second width as a remainder rather than independently: "The split is exact precisely because the code aborts rather than proceeding when the arithmetic would be approximate" (Q15). The level-uniformity constraint is "load-bearing" — it ensures the arithmetic is exact rather than approximate.


## Span-sets

A *span-set* is a finite sequence of spans Σ = ⟨σ₁, σ₂, ..., σₙ⟩. Its denotation is the union:

  ⟦Σ⟧ = ⟦σ₁⟧ ∪ ⟦σ₂⟧ ∪ ... ∪ ⟦σₙ⟧

Two span-sets are *equivalent* when they denote the same set of positions: Σ₁ ≡ Σ₂ ⟺ ⟦Σ₁⟧ = ⟦Σ₂⟧. The empty span-set ⟨⟩ denotes ∅. The singleton span-set ⟨σ⟩ denotes ⟦σ⟧.

**S7** (*FiniteRepresentability*). Every finite set of positions P ⊂ T admits a span-set Σ with ⟦Σ⟧ ⊇ P.

*Proof.* For any tumbler t, define ℓ = [0, ..., 0, 1] with #ℓ = #t (all components zero except the last, which is 1). Then ℓ > 0 (the last component is nonzero) and the action point k = #t ≤ #t, so (t, ℓ) satisfies T12. By TA-strict, t ⊕ ℓ > t, so t ∈ [t, t ⊕ ℓ) = ⟦(t, ℓ)⟧ — the span covers t. Taking one such span per position in P gives Σ with ⟦Σ⟧ ⊇ P.

Nelson confirms: "a tumbler-span may range in possible size from one byte to the whole docuverse" (LM 4/24, Q4).


## Normalization

A span-set is *normalized* when its components are sorted, non-overlapping, and non-adjacent:

**Definition** (*Normalized span-set*). A span-set Σ = ⟨σ₁, ..., σₙ⟩ is normalized iff:

  (N1) *Sorted.* `(A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))`
  (N2) *Separated.* `(A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))`

Condition N2 uses strict inequality. If reach(σᵢ) = start(σᵢ₊₁), the spans are adjacent and could be merged — so the form is not yet minimal. If reach(σᵢ) > start(σᵢ₊₁), the spans overlap and must be merged. The normalized form is the irreducible representation: every span is as large as it can be, and no two spans can be combined.

**S8** (*NormalizationExistence*). Every span-set Σ whose component spans are level-uniform and mutually level-compatible has a normalized equivalent Σ̂ with Σ̂ ≡ Σ.

*Construction.* If n = 0, the result is the empty span-set ⟨⟩, which vacuously satisfies N1 and N2. For n ≥ 1, proceed as follows. Sort the component spans by start position (T1 makes this well-defined). Scan left to right, maintaining a current interval [s, r). For each span σᵢ in sorted order:

  — If start(σᵢ) ≤ r (overlap or adjacency): extend r to max(r, reach(σᵢ)).
  — If start(σᵢ) > r (separated): emit the current interval as a span (s, r ⊖ s) — level-uniformity and S6 ensure #s = #r, so by D1 the reach is faithful — then start a new current interval at [start(σᵢ), reach(σᵢ)).

After processing all spans, emit the final interval.

*Loop invariant.* Let E be the set of emitted spans after processing σ₁..σᵢ, and [s, r) the current interval. The invariant J is:

  J: ⟦E⟧ ∪ [s, r) = ⟦σ₁⟧ ∪ ... ∪ ⟦σᵢ⟧

*Initialization.* After the first span σ₁, E = ∅ and [s, r) = [start(σ₁), reach(σ₁)) = ⟦σ₁⟧. J holds.

*Merge step.* When start(σᵢ) ≤ r, the new interval [s, max(r, reach(σᵢ))) covers [s, r) ∪ [start(σᵢ), reach(σᵢ)). The first term is the old current interval; the second is ⟦σᵢ⟧. Since start(σᵢ) ≤ r ensures no gap, the union is [s, max(r, reach(σᵢ))). E is unchanged, so ⟦E⟧ ∪ [s, max(r, reach(σᵢ))) = ⟦E⟧ ∪ [s, r) ∪ ⟦σᵢ⟧. By the inductive hypothesis, this equals ⟦σ₁⟧ ∪ ... ∪ ⟦σᵢ⟧. J is preserved.

*Emit step.* When start(σᵢ) > r, the current interval [s, r) is emitted and a new interval [start(σᵢ), reach(σᵢ)) begins. The emitted span covers exactly [s, r), so ⟦E'⟧ = ⟦E⟧ ∪ [s, r). The new current interval is ⟦σᵢ⟧. Then ⟦E'⟧ ∪ ⟦σᵢ⟧ = ⟦E⟧ ∪ [s, r) ∪ ⟦σᵢ⟧ = ⟦σ₁⟧ ∪ ... ∪ ⟦σᵢ⟧. J is preserved.

*Finalization.* After all n spans, emit the final [s, r). The total output satisfies ⟦Σ̂⟧ = ⟦σ₁⟧ ∪ ... ∪ ⟦σₙ⟧ = ⟦Σ⟧.

The result is a sequence of spans satisfying N1 (starts are sorted because we emit left-to-right from a sorted input) and N2 (each emit occurs precisely when start(σᵢ) > r, guaranteeing a gap between the emitted span's reach and the next span's start).

*Termination.* The scan visits each of the n input spans exactly once — bound function t = n − i.  ∎

**S9** (*NormalizationUniqueness*). The normalized form is unique: if Σ̂₁ and Σ̂₂ are both normalized and Σ̂₁ ≡ Σ̂₂, then Σ̂₁ = Σ̂₂.

*Proof.* Let Σ̂₁ = ⟨α₁, ..., αₘ⟩ and Σ̂₂ = ⟨β₁, ..., βₙ⟩, both normalized, with ⟦Σ̂₁⟧ = ⟦Σ̂₂⟧ = S. Suppose Σ̂₁ ≠ Σ̂₂. Let i be the smallest index where αᵢ ≠ βᵢ (if one sequence is shorter, take i past the shorter one's end). For j < i, αⱼ = βⱼ.

*Case 1:* start(αᵢ) < start(βᵢ) (or βᵢ does not exist). Then start(αᵢ) ∈ S since start(αᵢ) ∈ ⟦αᵢ⟧. But start(αᵢ) ∉ ⟦βⱼ⟧ for any j: for j < i, reach(βⱼ) = reach(αⱼ) < start(αᵢ) by N2 on Σ̂₁; for j ≥ i, start(βⱼ) ≥ start(βᵢ) > start(αᵢ) by N1 on Σ̂₂. So start(αᵢ) ∉ ⟦Σ̂₂⟧ = S. Contradiction.

*Case 2:* start(αᵢ) = start(βᵢ) but reach(αᵢ) ≠ reach(βᵢ), say reach(αᵢ) < reach(βᵢ). Set p = reach(αᵢ). Then p ∈ ⟦βᵢ⟧ since start(βᵢ) = start(αᵢ) < reach(αᵢ) = p < reach(βᵢ), so p ∈ S. But p ∉ ⟦αᵢ⟧ since p = reach(αᵢ) is the exclusive upper bound. For j < i, p ∉ ⟦αⱼ⟧ since p = reach(αᵢ) > reach(αⱼ) by N2 (reach(αⱼ) < start(αⱼ₊₁)), repeated application of N1 (start(αⱼ₊₁) < ... < start(αᵢ)), and non-emptiness (start(αᵢ) < reach(αᵢ)). For j > i, p ∉ ⟦αⱼ⟧ since p = reach(αᵢ) < start(αᵢ₊₁) ≤ start(αⱼ) by N2 and N1. So p ∉ ⟦Σ̂₁⟧, but p ∈ S. Contradiction.

*Case 3:* start(αᵢ) > start(βᵢ). Symmetric to Case 1.

All cases yield contradiction, so Σ̂₁ = Σ̂₂.  ∎

Nelson confirms both existence and uniqueness: "The tumbler line is a total order... The contiguity relation partitions S into maximal contiguous components. Each run yields exactly one span... The minimal span-set is unique" (Q4). He also identifies a critical caveat: the normalized form is unique *at a given instant* but depends on the ambient population of the tumbler line. Since "a span that contains nothing today may at a later time contain a million documents" (LM 4/25), a span-set that minimally covers a target set of positions may need revision as new addresses are allocated between existing ones. The normalization S8-S9 concerns a fixed span-set's canonical decomposition into non-overlapping components — not the evolving relationship between a span-set and a changing population.


## Union is order-independent

**S10** (*UnionOrderIndependence*). The normalized form of a span-set union is independent of the order in which spans are combined:

  normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)                  (commutativity)
  normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃))    (associativity)

*Proof.* ⟦Σ₁ ∪ Σ₂⟧ = ⟦Σ₁⟧ ∪ ⟦Σ₂⟧ = ⟦Σ₂⟧ ∪ ⟦Σ₁⟧ = ⟦Σ₂ ∪ Σ₁⟧. Since normalization depends only on the denotation (S9), normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁). Associativity follows identically from the associativity of set union.  ∎

Nelson argues this is structurally guaranteed: "spans are intervals on a total order. Combining intervals on a total order is set union, which is commutative and associative" (Q8). He notes that span-sets are described as "a series of spans" — suggesting ordered representation — but the semantics are purely set-theoretic: "what matters is which bytes are designated, not the order of the series." Two span-sets denoting the same byte collection are equivalent regardless of how their component spans are listed.


## Difference

When one span contains another, the remainder is always bounded:

**S11** (*DifferenceBound*). For level-uniform spans α and β with level_compat(start(α), start(β)) and ⟦β⟧ ⊆ ⟦α⟧, the set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most two spans.

*Proof.* Containment means start(α) ≤ start(β) and reach(β) ≤ reach(α). The difference decomposes into two intervals:

  Left:   {t : start(α) ≤ t < start(β)}      (empty when start(α) = start(β))
  Right:  {t : reach(β) ≤ t < reach(α)}       (empty when reach(β) = reach(α))

Each non-empty interval is a half-open interval on the tumbler line, representable as a span when α and β are level-uniform (ensuring D0 and D1 hold for the boundary tumblers). The result is a span-set of 0, 1, or 2 components:

  (a) Both boundaries coincide (α = β): difference is empty — 0 spans.
  (b) One boundary coincides: difference is one span.
  (c) Neither coincides: difference is two spans.

The bound of two is tight and inherent in removing a contiguous sub-range from a contiguous range on a linear order.  ∎

Nelson confirms the bound and the mechanism: "Removing a contained span from a containing span always produces at most two contiguous spans, expressible as a span-set" (Q5). The system provides span-sets precisely for representing such non-contiguous remainders. The result is "a structural consequence of the tumbler line being linearly ordered, combined with the span-set mechanism for non-contiguous selections."


## Observations from the implementation

Two findings from Gregory's implementation evidence illuminate the boundary between abstract properties and practical constraints. These observations do not affect the abstract properties — S0 through S11 hold for any correctly-implemented span algebra over the tumbler space. They identify where implementations must take particular care.

*Observation 1: Width encoding is not unique under naive comparison.* The same byte count can be encoded at different tumbler precisions — a V-dimension width of 11 characters might appear as [0, 11] (action point at position 2) while the corresponding I-dimension width appears as [0, 0, 0, 0, 0, 0, 0, 0, 11] (action point at position 9). Both decode to the integer 11, but they are distinct tumblers under T3 (Q13). The abstract algebra is unaffected: what matters is the *denotation* (the set of positions covered), not the encoding. But implementations that compare widths structurally rather than by denotation may produce incorrect results. The canonical form T3 guarantees uniqueness *per tumbler*, not across encoding conventions.

*Observation 2: Cross-depth arithmetic silently degenerates.* When the tumbler subtraction encounters operands at different hierarchical depths, the implementation returns the minuend unchanged — as if the subtrahend were zero (Q12). No error is raised. The implication: span operations that cross hierarchical levels do not fail loudly; they produce incorrect results silently. The level constraint S6 is not merely advisory — violating it yields arithmetic that looks correct but is not. Gregory describes this as span difference being "a partial function whose domain is restricted to same-exponent operands" (Q12). Any implementation must either enforce level compatibility at the point of operation or validate results post hoc. The implementation chooses enforcement: the split function aborts with a fatal error when level invariants are violated, rather than proceeding with approximate arithmetic (Q15).


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| D0 | Displacement well-definedness: a < b and divergence(a, b) ≤ #a (ensures positive displacement with TA0 satisfied) | introduced |
| D1 | Displacement round-trip: for a < b with #a = #b, a ⊕ (b ⊖ a) = b | introduced |
| S0 | Spans are convex: every position between two members is also a member | introduced |
| SC | Span classification: five exhaustive cases (separated, adjacent, proper overlap, containment, equal) | introduced |
| S6 | Level constraint: level_compat(t₁, t₂) ≡ #t₁ = #t₂; a span is level-uniform when #start = #width | introduced |
| S1 | Intersection of two level-uniform, level-compatible spans is either empty or a single span | introduced |
| S2 | The empty set is not the denotation of any span — every span is non-empty | introduced |
| S3 | Adjacent or overlapping level-uniform, level-compatible spans merge to a single span | introduced |
| S3a | Span merge is commutative | introduced |
| S4 | Split at a level-compatible interior point produces an exact partition: nothing lost, nothing duplicated, the two parts adjacent | introduced |
| LeftCancellation | a ⊕ x = a ⊕ y ⟹ x = y (tumbler arithmetic property, used locally) | introduced |
| S5 | The widths of two split parts compose under ⊕ to the original width | introduced |
| S7 | Every finite set of positions admits a covering span-set | introduced |
| S8 | Every level-compatible span-set has a normalized equivalent: sorted, non-overlapping, non-adjacent | introduced |
| S9 | The normalized form of a span-set is unique | introduced |
| S10 | Span-set union (as normalization) is commutative and associative | introduced |
| S11 | For level-uniform, level-compatible spans with containment, the difference is at most 2 spans | introduced |
| σ.reach | reach(σ) = start(σ) ⊕ width(σ) — the exclusive upper bound | introduced |
| σ.denotation | ⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)} | introduced |
| Σ.setdenotation | ⟦Σ⟧ = union of component span denotations | introduced |
| N1, N2 | Normalized form conditions: sorted starts, separated reaches | introduced |


## Open Questions

- What abstract property must a span-set satisfy to guarantee that its normalized form remains valid as new addresses are allocated in the tumbler space?
- Under what conditions does the intersection of two spans at different hierarchical levels admit a well-formed span representation?
- What invariant must a span algebra maintain to ensure that split followed by merge always recovers the original span, even when the split point is at a finer hierarchical level than the original?
- Must the system distinguish between a span over unpopulated space and a span over populated space at the algebraic level, or is this distinction purely a content-layer concern?
- What guarantees must span operations provide at subspace boundaries, where hierarchical level transitions are structurally inherent?
- When the minimal span-set covering a target population changes due to address allocation, what is the minimal update to the old normalized form that produces the new one?
