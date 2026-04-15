# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-26) — Extracted: 2026-04-14*

## D0 — DisplacementWellDefined

Given two tumblers a < b whose divergence point lies within a's length, displacement b ⊖ a is itself a valid tumbler and is strictly positive, with its action point at the divergence. The round-trip a ⊕ (b ⊖ a) = b holds only when a is no longer than b; if a is strictly longer, the reconstruction may not recover b exactly.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a
- *Postconditions:* b ⊖ a ∈ T, b ⊖ a > 0, actionPoint(b ⊖ a) = divergence(a, b), #(b ⊖ a) = max(#a, #b), a ⊕ (b ⊖ a) ∈ T, #a > #b → a ⊕ (b ⊖ a) ≠ b

---

## D1 — DisplacementRoundTrip

Under the additional constraint that a is no longer than b, displacement is faithful: a ⊕ (b ⊖ a) = b exactly. This is the core round-trip lemma that ties subtraction and addition into an inverse pair.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b
- *Postconditions:* a ⊕ (b ⊖ a) = b

---

## D2 — DisplacementUnique

The displacement carrying a to b is unique: if any tumbler w satisfies a ⊕ w = b under D1's preconditions, then w must equal b ⊖ a. This rules out multiple distinct displacements for the same source–target pair.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b, a ⊕ w = b
- *Postconditions:* w = b ⊖ a

---

## Divergence — Divergence

Defines the divergence index for two distinct tumblers as the first position where their components differ, or min(#a, #b) + 1 when all shared components agree but the tumblers have unequal length. Exactly one of these two cases applies for any unequal pair, with exhaustiveness guaranteed by T3.

*Formal Contract:*
- *Definition:* For `a, b ∈ T` with `a ≠ b`: (i) if `∃ k ≤ min(#a, #b)` with `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`; (ii) if `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1`. Exactly one case applies (exhaustiveness by T3: if neither case holds, `a = b`).

---

## GlobalUniqueness — GlobalUniqueness

No two distinct allocation events — whether from the same allocator, sibling allocators, or allocators at different hierarchy levels — ever produce the same address. The proof proceeds by strong induction on allocator tree depth, with five structural cases covering all possible relationships between the two producing allocators.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` produced by distinct allocation events — where an allocation event is either root initialization or an invocation of `inc(t, k)` — within a system conforming to T10a (allocator discipline). Each address is assigned a producing allocator by its generating event: the root's base address to root by initialization; each `inc` output to a single allocator via the event-taxonomy rule (`k = 0` to the executing allocator, `k > 0` to the newly created child). The domain prefix of a non-root allocator `A`, spawned by `c₀ = inc(t, k')`, is the parent domain element `t`; every `a ∈ dom(A)` satisfies `t ≼ a` (by TA5(b), TA5(d), TA5-SigValid, and T10a.1).
- *Invariant:* For every pair of addresses `a, b` arising from distinct allocation events (root initialization or `inc` invocations) in any reachable system state: `a ≠ b`.
- *Proof structure:* Strong induction on allocator tree depth *d*. Claim `U(d)`: all pairs at depth ≤ *d* produce distinct outputs. Base (`d = 0`): sole root allocator, Case 1. Step (`d → d + 1`): Cases 1–5 are self-contained; the `p₁ = p₂` exhaustiveness routing invokes `U(d)` to establish shared parentage — identical prefix values held by distinct parents at depth ≤ *d* would be a repeated output contradicting `U(d)` — then applies T10a's per-parent uniqueness to separate spawning parameters.

---

## NoDeallocation — NoDeallocation

The system contains no operation that removes an address from the allocated set — the allocated set is strictly append-only. This is a foundational design constraint, not a derived fact, and it is what makes permanence guarantees possible.

*Formal Contract:*
- *Axiom:* The system's operation vocabulary contains no operation that removes an element from the allocated set.

---

## OrdinalDisplacement — OrdinalDisplacement

Defines the canonical displacement vector δ(n, m) as the length-m tumbler that is zero in all positions except the last, where it holds n ≥ 1. This is the primitive unit for incrementing a tumbler at a specific depth without touching any shallower components.

*Formal Contract:*
- *Preconditions:* n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, 0, …, 0, n] of length m with action point m
- *Postconditions:* δ(n, m) ∈ T (by T0), δ(n, m) > 0 (by PositiveTumbler)

---

## OrdinalShift — OrdinalShift

Defines shift(v, n) as the result of adding the ordinal displacement δ(n, #v) to v, which increments v's deepest component by n while preserving its length and all shallower components. This gives a closed-form expression for the standard "next sibling" operation within a tumbler's own depth.

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1
- *Definition:* shift(v, n) = v ⊕ δ(n, m) where m = #v
- *Postconditions:* shift(v, n) ∈ T, #shift(v, n) = #v, shift(v, n)ᵢ = vᵢ for i < m, shift(v, n)ₘ = vₘ + n ≥ 1

---

## PartitionMonotonicity — PartitionMonotonicity

Within any prefix-delimited partition, all allocated addresses are totally ordered by T1 in a way that is consistent with each allocator's local allocation order. Additionally, for any two sibling sub-partitions whose prefixes are ordered p₁ < p₂, every address under p₁ precedes every address under p₂ — so the prefix structure alone determines the cross-allocator ordering.

*Formal Contract:*
- *Preconditions:* A system conforming to T10a (allocator discipline); a partition with prefix `p ∈ T`; a child prefix `t₀ = inc(s, k)` with `k > 0` and `p ≼ s`, established by the parent allocator's single deep increment; sub-partition prefixes `t₀, t₁, t₂, ...` where `t₀` is the initial child prefix and `tₙ₊₁ = inc(tₙ, 0)` for all `n ≥ 0`.
- *Postconditions:* (1) For sibling sub-partition prefixes `tᵢ < tⱼ` (with `0 ≤ i < j`) and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. (2) Within each sub-partition with prefix `tᵢ` (for `i ≥ 0`), for any `a, b` allocated by the same allocator: `allocated_before(a, b) ⟹ a < b`.
- *Invariant:* For every reachable system state, the set of allocated addresses within any prefix-delimited partition is totally ordered by T1 consistently with per-allocator allocation order.

---

## PositiveTumbler — PositiveTumbler

A tumbler is positive if it contains at least one nonzero component; a tumbler is a zero tumbler if all components are zero. Every positive tumbler is strictly greater under T1 than every zero tumbler of any length, establishing a clean separation between the all-zero tumblers (which form an ascending chain by length) and the rest of the address space.

*Formal Contract:*
- *Definition:* `t > 0` (positive) iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. Zero tumbler: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Postconditions:* `(A t ∈ T, z ∈ T : t > 0 ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) :: z < t)` — every positive tumbler is strictly greater under T1 than every zero tumbler of any length.

---

## Prefix — PrefixRelation

A tumbler p is a prefix of q (p ≼ q) when p is no longer than q and every component of p matches the corresponding component of q at the same position. A proper prefix (p ≺ q) additionally requires p ≠ q, which combined with the canonical representation guarantee (T3) forces p to be strictly shorter than q.

*Formal Contract:*
- *Definition:* `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. Proper prefix: `p ≺ q` iff `p ≼ q ∧ p ≠ q`.
- *Derived postcondition:* `p ≺ q ⟹ #p < #q` (by T3).

---

## PrefixOrderingExtension — PrefixOrderingExtension

If two non-nested tumblers are ordered (p₁ < p₂), that ordering propagates to all their extensions: every tumbler rooted at p₁ is less than every tumbler rooted at p₂. This means the comparison between two subtrees can be resolved entirely at their roots.

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ < p₂` (T1) and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (non-nesting); `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a < b` under T1.

---

## ReverseInverse — ReverseInverse

Tumbler subtraction and addition are mutually inverse under the right conditions: subtracting a displacement w from an address a and then re-adding w recovers a exactly, provided a ≥ w, both have the same depth, and all components of a before the action point of w are zero.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊖ w) ⊕ w = a`

---

## Span — Span

A span is a start address paired with a positive displacement length, denoting the contiguous set of tumblers from the start up to (but not including) the start plus the length; it is a half-open interval in tumbler address space.

*Formal Contract:*
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`, where `s ∈ T` is the start address and `ℓ ∈ T` with `ℓ > 0` is the displacement length

---

## T0 — CarrierSetDefinition

Establishes the carrier set T as all finite sequences of natural numbers with at least one component, taken as an axiom — the foundation on which all tumbler arithmetic is built.

*Formal Contract:*
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under successor and addition.

---

## T0(a) — UnboundedComponentValues

For every tumbler and every component position, the value at that position is unbounded — no matter what bound M you choose, a tumbler exists that agrees with the original everywhere except at that position, where it exceeds M. This guarantees siblings at any level are inexhaustible.

*Formal Contract:*
- *Postcondition:* For every tumbler `t ∈ T` and every component position `i` with `1 ≤ i ≤ #t`, and for every bound `M ∈ ℕ`, there exists `t' ∈ T` that agrees with `t` at all positions except `i`, where `t'.dᵢ > M`.

---

## T0(b) — UnboundedLength

There is no maximum tumbler length — for every natural number n, a tumbler of at least n components exists in T. Together with T0(a), this makes the address space infinite in two independent dimensions: unlimited siblings at any level, and unlimited nesting depth.

*Formal Contract:*
- *Postcondition:* For every `n ∈ ℕ` with `n ≥ 1`, there exists `t ∈ T` with `#t ≥ n`.

T0 is what separates the tumbler design from fixed-width addressing. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — it means the process of creating new addresses never terminates. Between any two sibling addresses, the forking mechanism can always create children: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." Each daughter can have daughters without limit, and each digit is itself unbounded.

The address space is unbounded in two dimensions: T0(a) ensures each component is unbounded (unlimited siblings at any level) and T0(b) ensures the number of components is unbounded (unlimited nesting depth). Together they make the address space infinite in both dimensions, which Nelson calls "finite but unlimited" — at any moment finitely many addresses exist, but there is no bound on how many can be created: "A span that contains nothing today may at a later time contain a million documents."

We observe that Gregory's implementation uses a fixed 16-digit mantissa of 32-bit unsigned integers, giving a large but finite representable range. When the allocation primitive `tumblerincrement` would exceed this range structurally (requiring a 17th digit), it detects the overflow and terminates fatally. The general addition routine `tumbleradd` silently wraps on digit-value overflow. Both behaviors violate T0. The abstract specification demands unbounded components; a correct implementation must either provide them or demonstrate that the reachable state space never exercises the bound. The comment `NPLACES 16 /* increased from 11 to support deeper version chains */` records that the original bound of 11 was concretely hit in practice — version chains deeper than 3–4 levels caused fatal crashes.

---

## T1 — LexicographicOrder

Tumblers are totally ordered lexicographically: compare component by component, and if one tumbler is a proper prefix of the other, the shorter one comes first. This total order is architecturally necessary because spans are defined as contiguous intervals on the tumbler line — incomparable addresses would make span endpoints undefined.

*Formal Contract:*
- *Definition:* `a < b` iff `∃ k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(m,n) ∧ aₖ < bₖ`, or (ii) `k = m+1 ≤ n`.
- *Postconditions:* (a) Irreflexivity — `(A a ∈ T :: ¬(a < a))`. (b) Trichotomy — `(A a,b ∈ T :: exactly one of a < b, a = b, b < a)`. (c) Transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`.

Nelson's assertion that the tumbler line is total — that two addresses are never incomparable — is architecturally load-bearing. Spans are defined as contiguous regions on the tumbler line: "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." If two addresses were incomparable, the interval between them would be undefined, and the entire machinery of span-sets, link endsets, and content reference would collapse.

Nelson requires that comparison be self-contained — no index consultation needed:

---

## T10 — PartitionIndependence

If two tumblers p₁ and p₂ are non-nested (neither is a prefix of the other), then any address descended from p₁ and any address descended from p₂ are guaranteed to be distinct. This is the formal basis for coordination-free allocation: owners of disjoint subtrees can allocate addresses independently with no risk of collision.

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a ≠ b`.

The proof is elementary, but the property is architecturally profound. Nelson: "The owner of a given item controls the allocation of the numbers under it." No central allocator is needed. No coordination protocol is needed. The address structure itself makes collision impossible.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." Baptism is the mechanism by which ownership domains are established — the owner of a number creates sub-numbers beneath it, and those sub-numbers belong exclusively to the owner.

---

## T10a-N — AllocatorDisciplineNecessity

Relaxing the allocator's sibling restriction (k=0 only) to allow child increments (k=1) after a sibling increment causes the produced addresses to fall into a prefix relationship, which violates T10's non-nesting precondition and breaks the uniqueness guarantee. This proves the k=0 restriction is not a convenience but a necessity.

*Formal Contract:*
- *Preconditions:* `t₀ ∈ T`; allocator produces `t₁ = inc(t₀, 0)` and `t₂ = inc(t₁, 1)` (the `k = 0` sibling restriction is relaxed for the second step).
- *Postconditions:* `t₁ ≼ t₂` — prefix nesting occurs among the produced addresses, violating T10's non-nesting precondition (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`).

---

## T10a.1 — UniformSiblingLength

All siblings produced by a single allocator share the same tumbler length as the base address. Because sibling production uses only inc(·, 0), which preserves length by TA5, the entire sibling stream is length-uniform.

*Formal Contract:*
- *Precondition:* Allocator with base address `t₀`, producing siblings by `inc(·, 0)`.
- *Postcondition:* `(A n ≥ 0 : #tₙ = #t₀)` — all siblings have the same length as the base address.

---

## T10a.2 — NonNestingSiblingPrefixes

Distinct siblings from the same allocator are prefix-incomparable — neither address is a prefix of the other. This follows from their equal length (T10a.1) combined with T1 and T10: equal-length tumblers can only be related by equality, not strict prefix.

*Formal Contract:*
- *Precondition:* `tᵢ`, `tⱼ` are distinct siblings from the same allocator (`i ≠ j`).
- *Postcondition:* `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ` — neither is a prefix of the other.

---

## T10a.3 — LengthSeparation

Child allocator outputs are strictly longer than any parent sibling output, with the length gap accumulating additively across nesting levels. A descendant at depth d has output length exactly γ + k'₁ + … + k'_d (each k'ᵢ ∈ {1, 2}), so outputs at different nesting depths are always length-distinct and therefore never collide.

*Formal Contract:*
- *Precondition:* Parent allocator with sibling length `γ`; `t` is a parent sibling (so `#t = γ` by T10a.1); child spawned via `inc(t, k')` with `k' ∈ {1, 2}` (per T10a).
- *Postcondition:* All child outputs have length `γ + k' > γ`. No child output equals any parent sibling (by T3, tumblers of different lengths are distinct). Descendant at depth `d` along a lineage with child-spawning parameters `k'₁, …, k'_d` (each `k'_i ∈ {1, 2}`) has output length exactly `γ + k'₁ + … + k'_d ≥ γ + d`; along any lineage the cumulative length is strictly increasing with depth, so outputs at different nesting depths never collide (by T3).

---

## T10a.4 — T4PreservationUnderDiscipline

Every address produced by a conforming allocator tree satisfies the T4 tumbler-validity condition. The root's base satisfies T4 by initialization, inc(·, 0) preserves T4 unconditionally (TA5a), and child-spawning uses k' ∈ {1, 2} within TA5a's preservation bounds — so T4 holds at every depth by induction.

*Formal Contract:*
- *Preconditions:* Allocator tree conforming to T10a (including initialization: root base address satisfies T4).
- *Postconditions:* Every output at every depth satisfies T4.
- *Proof structure:* Induction on allocator tree depth. Base: T10a initialization constraint. Step: TA5a preservation under `inc(·, 0)` and `inc(·, k')` with `k' ∈ {1, 2}`.

---

## T10a — AllocatorDiscipline

The allocator discipline specifies that sibling outputs are produced exclusively by inc(·, 0) and child allocators are spawned by exactly one inc(·, k') with k' ∈ {1, 2}, with each (t, k') pair used at most once. This discipline is both sufficient to guarantee uniform sibling lengths, prefix-incomparability, length separation across depths, and T4 preservation — and necessary, since relaxing it allows a prefix relationship between siblings, violating the T10 precondition.

*Formal Contract:*
- *Axiom:* The root allocator's base address satisfies T4. Allocators produce sibling outputs exclusively by `inc(·, 0)`; child-spawning uses exactly one `inc(·, k')` with `k' ∈ {1, 2}` satisfying the TA5a bounds (`k' = 1` when `zeros(t) ≤ 3`, `k' = 2` when `zeros(t) ≤ 2`) to establish the child's prefix, after which the parent resumes sibling production with `inc(·, 0)`. Each `(t, k')` pair — domain element and spawning parameter — yields at most one child-spawning event.
- *Postconditions:*
  - T10a.1 (Uniform sibling length): For every allocator with base address b, all sibling outputs a satisfy #a = #b.
  - T10a.2 (Non-nesting sibling prefixes): For all siblings a, b from the same allocator, same_allocator(a, b) ∧ a ≠ b → a and b are prefix-incomparable, satisfying the precondition of T10.
  - T10a.3 (Length separation): For every child allocator spawned by `inc(·, k')` with k' ∈ {1, 2} from a parent with base length m, all child outputs c satisfy #c = m + k', and across d nesting levels the separation is exact: #output = m + k'₁ + k'₂ + … + k'_d.
  - T10a.4 (T4 preservation): The root allocator's base address satisfies T4 (initialization constraint); since `inc(·, 0)` unconditionally preserves T4 (TA5a) and child-spawning uses `k' ∈ {1, 2}` within TA5a bounds, every output of a conforming allocator satisfies T4 by induction on the allocator tree.
  - T10a-N (Necessity): Under the relaxed rule (any k ≥ 0 in the sibling stream), the pair a₁ = inc(b, 0) and a₂ = inc(a₁, k') with k' > 0 are sibling outputs satisfying a₁ ≺ a₂ — by TA5(b) (agreement on all positions of a₁) and TA5(d) (#a₂ > #a₁), invoking T1 case (ii). This violates the T10 precondition. The axiom is therefore both sufficient (T10a.1–T10a.3) and necessary for prefix-incomparability of sibling outputs.

---

## T12 — SpanWellDefinedness

A span is well-defined whenever its preconditions hold: the displaced endpoint s ⊕ ℓ exists in T (by TA0), the span is non-empty because s is always a member (by TA-strict), and the span is order-convex under the tumbler ordering (by T1) — any tumbler between two members of the span is itself a member.

*Formal Contract:*
- *Preconditions:* `s ∈ T`, `ℓ ∈ T`, `ℓ > 0`, `actionPoint(ℓ) ≤ #s`
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`
- *Postconditions:* (a) `s ⊕ ℓ ∈ T` (endpoint exists, by TA0). (b) `s ∈ span(s, ℓ)` (non-empty, by TA-strict). (c) `span(s, ℓ)` is order-convex under T1 (for all `a, c ∈ span(s, ℓ)` and `b ∈ T`, `a ≤ b ≤ c` implies `b ∈ span(s, ℓ)`).

---

## T2 — IntrinsicComparison

The ordering between any two tumblers is determined solely by their component sequences and lengths, with no external data structures consulted. The comparison is a pure function that terminates after examining at most min(#a, #b) component pairs.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` — two well-formed tumblers (finite sequences over ℕ with `#a ≥ 1` and `#b ≥ 1`, per T0).
- *Postconditions:* (a) The ordering among `a` and `b` under T1 is determined. (b) At most `min(#a, #b)` component pairs are examined. (c) The only values consulted are `{aᵢ : 1 ≤ i ≤ #a}`, `{bᵢ : 1 ≤ i ≤ #b}`, `#a`, and `#b`.
- *Frame:* No external data structure is read or modified — the comparison is a pure function of the two tumblers.

---

## T3 — CanonicalRepresentation

Each tumbler has exactly one representation as a component sequence — equality holds if and only if the sequences have the same length and matching components at every position. No normalization, quotient, or external identification is imposed on T.

*Formal Contract:*
- *Postconditions:* Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. No quotient, normalization, or external identification is imposed on T.

---

## T4 — HierarchicalParsing

Address tumblers encode a four-level containment hierarchy (network, user, document, element) using zero components as field separators, with at most three separating zeros, all non-separator components strictly positive, and every present field containing at least one component.

*Formal Contract:*
- *Axiom:* Valid address tumblers satisfy: `zeros(t) ≤ 3`; every non-separator component is strictly positive (positive-component constraint); every field present in the address has at least one component (non-empty field constraint).
- *Preconditions:* T3 (CanonicalRepresentation) — tumbler equality is sequence equality, guaranteeing that the component sequence of `t` is fixed and the separator positions computed by scanning for zeros are uniquely determined. Required for the T4b uniqueness result.
- *Corollaries (separate properties with independent formal blocks):* T4a (SyntacticEquivalence) — equivalence of the non-empty field constraint to the three syntactic conditions; proved in its own property file. T4b (UniqueParse) — well-definedness and uniqueness of `fields(t)`; proved in its own property file. T4c (LevelDetermination) — bijection between `zeros(t) ∈ {0, 1, 2, 3}` and hierarchical level; proved in its own property file.

---

## T4a — SyntacticEquivalence

The structural constraint that every present field in an address tumbler is non-empty is equivalent to three purely syntactic conditions on the raw component sequence: the sequence neither starts nor ends with zero, and no two zeros appear adjacently. This equivalence holds under T4's requirement that all field components are strictly positive.

*Formal Contract:*
- *Preconditions:* `t` is an address tumbler satisfying T4's positive-component constraint (`tᵢ > 0` for every non-separator component).
- *Postconditions:* The non-empty field constraint (each present field has `≥ 1` component) holds if and only if (i) no two zeros are adjacent in `t`, (ii) `t₁ ≠ 0`, and (iii) `t_{#t} ≠ 0`.

---

## T4b — UniqueParse

Under T4's constraints, the zero-valued components of a tumbler serve exclusively as field separators — never as field values — so separator positions are recoverable by a single scan. This makes the decomposition into node, user, document, and element subsequences uniquely determined by the tumbler itself, with no ambiguity.

*Formal Contract:*
- *Preconditions:* `t` satisfies T3 (CanonicalRepresentation): the component sequence of `t` is fixed by sequence identity, with no alternative encoding yielding different component values. `t` satisfies the T4 constraints (at most three zero-valued components, positive-component constraint, non-empty field constraint).
- *Postconditions:* `fields(t)` — the decomposition into node, user, document, and element sub-sequences — is well-defined and uniquely determined by `t`.

---

## T4c — LevelDetermination

Counting the zeros in a valid T4 tumbler exactly counts its field separators and therefore determines the tumbler's hierarchical level (server, account, document, or element). The mapping from zero-count to level is a bijection on {0, 1, 2, 3}, so level determination requires only a scan of the raw component sequence.

*Formal Contract:*
- *Preconditions:* `t` satisfies the T4 constraints.
- *Postconditions:* `zeros(t) ∈ {0, 1, 2, 3}`, and the mapping `zeros(t) → hierarchical level` is a bijection on `{0, 1, 2, 3}`.

---

## T5 — ContiguousSubtrees

If two addresses share a common prefix and a third address falls between them in the total lexicographic order, that third address must also share the prefix. This means every subtree maps to a contiguous interval on the tumbler line, so span endpoints alone implicitly determine all addresses in between — no addresses from unrelated subtrees can interleave.

*Formal Contract:*
- *Preconditions:* `a, b, c ∈ T`; `p` is a tumbler prefix with `#p ≥ 1`; `p ≼ a`; `p ≼ c`; `a ≤ b ≤ c` under the lexicographic order T1.
- *Postconditions:* `p ≼ b` — the tumbler `b` extends the prefix `p`, and therefore belongs to the same subtree as `a` and `c`.

This is Nelson's key insight: "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." T5 is what makes this true. A span between two endpoints under the same prefix captures exactly the addresses under that prefix between those endpoints — no addresses from unrelated subtrees can interleave.

Because the hierarchy is projected onto a flat line (T1), containment in the tree corresponds to contiguity on the line. Nelson: "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." Every subtree maps to a contiguous range, and every contiguous range within a subtree stays within the subtree.

---

## T6 — DecidableContainment

Containment at any hierarchical level — same server, same account, same document, subdocument prefix — is decidable using only the two tumbler representations, by extracting fields via T4b and comparing componentwise. The result introduces no new mathematics beyond T4 but states the decidability claim explicitly because it is load-bearing for correct decentralized operation.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` are valid tumblers satisfying T4 (positive-component constraint, at most three zeros, no adjacent zeros, no leading or trailing zero).
- *Postconditions:* (a) The procedure terminates and returns YES iff `N(a) = N(b)` (componentwise). (b) The procedure terminates and returns YES iff `zeros(a) ≥ 1 ∧ zeros(b) ≥ 1 ∧ N(a) = N(b) ∧ U(a) = U(b)`; returns NO if either tumbler lacks a user field. (c) The procedure terminates and returns YES iff `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2 ∧ N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)`; returns NO if either tumbler lacks a document field. (d) The procedure terminates and returns YES iff `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2 ∧ #D(a) ≤ #D(b) ∧ (A k : 1 ≤ k ≤ #D(a) : D(a)ₖ = D(b)ₖ)`; returns NO if either tumbler lacks a document field. All decisions use only the tumbler representations of `a` and `b`, via `fields(t)` (T4(b)) and componentwise comparison on finite sequences of natural numbers.

T6 is a corollary: it follows immediately from T4 — we extract the relevant fields and compare. We state it separately because the decidability claim is load-bearing for decentralized operation, but it introduces no independent content beyond T4.

We must note what T6(d) does NOT capture. The document field records the *allocation hierarchy* — who baptised which sub-number — not the *derivation history*. Version `5.3` was allocated under document `5`, but this tells us nothing about which version's content was copied to create `5.3`. Nelson: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." Formal version-derivation requires the version graph, not just the address.

Nelson confirms that shared prefix means shared containing scope: "The owner of a given item controls the allocation of the numbers under it." The prefix IS the path from root to common ancestor. But he cautions: "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." Shared prefix guarantees containment and ownership, never semantic categorization.

Gregory's implementation confirms the distinction between ordering and containment. The codebase provides both `tumblercmp` (total order comparison) and `tumbleraccounteq` (prefix-matching predicate with zero-as-wildcard semantics). The latter truncates the candidate to the length of the parent and checks for exact match — this is the operational realization of T6, and it is a genuinely different algorithm from the ordering comparison.

---

## T7 — SubspaceDisjointness

Within the element space, the first element component identifies the subspace (e.g., 1 for text, 2 for links), and addresses in different subspaces are permanently disjoint. Arithmetic within one subspace cannot produce addresses in another, because the subspace identifier is part of the address structure itself, not metadata.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` with `zeros(a) = zeros(b) = 3` (both are element-level addresses with well-formed field structure per T4).
- *Postconditions:* `a.E₁ ≠ b.E₁ ⟹ a ≠ b`.

We state T7 explicitly because it is load-bearing for the guarantee that operations within one content type do not interfere with another. T7 is the structural basis — arithmetic within subspace 1 cannot produce addresses in subspace 2, because the subspace identifier is part of the address, not metadata.

The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position. This is a consequence, not an assumption — it falls out of the lexicographic order.

---

## T8 — AllocationPermanence

Once an address is allocated it is never removed — the allocated set grows monotonically across every state transition. This follows directly from the NoDeallocation axiom, which precludes any removal operation; read-only and arithmetic operations preserve the set exactly, while allocation operations extend it.

*Formal Contract:*
- *Invariant:* For every state transition s → s', `allocated(s) ⊆ allocated(s')`.
- *Depends:* NoDeallocation (the system defines no removal operation — the sole premise required for the monotonicity conclusion; any transition either preserves or modifies the allocated set, and the axiom precludes removal, so every modification is an addition).
- *Frame:* The currently defined operations confirm this: read-only operations (T1, T2, T4) and pure arithmetic (⊕, ⊖) preserve the allocated set exactly, while allocation transitions (T10a) extend it. The monotonicity conclusion holds for any future operation as well, since NoDeallocation constrains the entire operation vocabulary.

---

## T9 — ForwardAllocation

Addresses produced by the same allocator's sibling stream are assigned in strictly increasing tumbler order. If address a is allocated before b by the same allocator, then a < b under the tumbler ordering established by T1.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` with `same_allocator(a, b) ∧ allocated_before(a, b)` — both addresses produced by the same allocator's sibling stream, `a` allocated before `b`.
- *Postconditions:* `a < b` under the tumbler order T1.

---

## TA-LC — LeftCancellation

Tumbler addition is left-cancellative: if a ⊕ x = a ⊕ y (both well-defined), then x = y. This holds because TumblerAdd's constructive definition determines each result component from exactly one input, so equality of results propagates back component-by-component to equality of the displacements.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w

### Verification of TA4

**Claim.** `(a ⊕ w) ⊖ w = a` under the full precondition: `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`.

*Proof.* Let `k` be the action point of `w`. Since `k = #a`, the addition `a ⊕ w` produces a result `r` with: `rᵢ = aᵢ = 0` for `i < k` (by the zero-prefix condition), `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `i > k`. Crucially, there are no components of `a` beyond position `k` — the tail replacement discards nothing. By the result-length identity, `#r = #w = k`, so `r = [0, ..., 0, aₖ + wₖ]`.

Now subtract `w` from `r`. The subtraction scans for the first divergence between `r` and `w`. For `i < k`: `rᵢ = 0 = wᵢ` (both are zero — `aᵢ` by the zero-prefix precondition, `wᵢ` by definition of action point). Two sub-cases arise at position `k`.

*Sub-case (i): `aₖ > 0`.* Then `rₖ = aₖ + wₖ > wₖ`, and the first divergence is at position `k`. The subtraction produces: positions `i < k` get zero, position `k` gets `rₖ - wₖ = aₖ`, and positions `i > k` copy from `r`, giving `rᵢ = wᵢ`. Since `k = #a` and `#w = k`, there are no trailing components. The result is `[0, ..., 0, aₖ] = a`. For valid addresses, T4's positive-component constraint guarantees `aₖ > 0`, so this sub-case always applies in the address context.

*Sub-case (ii): `aₖ = 0`.* Then `a` is a zero tumbler. The addition gives `rₖ = wₖ`. Since `#r = #w` (result-length identity) and `#w = k` (precondition), we have `r = w`. The subtraction `w ⊖ w` yields the zero tumbler of length `k`, which is `a`. ∎

### Cancellation properties of ⊕

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.

**TA-LC (LeftCancellation).** If a ⊕ x = a ⊕ y with both sides well-defined (TA0 satisfied for both), then x = y.

*Proof.* We show that from the hypothesis `a ⊕ x = a ⊕ y`, with both additions satisfying TA0, it follows that `x = y`. The argument proceeds in two stages: first we establish that `x` and `y` share the same action point, then we show component-wise and length equality.

Let `k₁` be the action point of `x` and `k₂` the action point of `y`. Both exist because TA0 requires `x > 0` and `y > 0`, so each has at least one nonzero component. We eliminate both strict orderings.

**Case k₁ < k₂.** Since `k₁ < k₂` and the action point is the first nonzero component, every component of `y` before position `k₂` is zero — in particular `y_{k₁} = 0`. Position `k₁` therefore falls in the prefix-copy region of the addition `a ⊕ y`: by TumblerAdd, `(a ⊕ y)_{k₁} = a_{k₁}`. In the addition `a ⊕ x`, position `k₁` is the action point itself, so TumblerAdd gives `(a ⊕ x)_{k₁} = a_{k₁} + x_{k₁}`. From `a ⊕ x = a ⊕ y` we obtain `a_{k₁} + x_{k₁} = a_{k₁}`, hence `x_{k₁} = 0`. But `k₁` is the action point of `x`, so by definition `x_{k₁} > 0` — contradiction.

**Case k₂ < k₁.** Since `k₂ < k₁` and the action point is the first nonzero component, every component of `x` before position `k₁` is zero — in particular `x_{k₂} = 0`. Position `k₂` therefore falls in the prefix-copy region of the addition `a ⊕ x`: by TumblerAdd, `(a ⊕ x)_{k₂} = a_{k₂}`. In the addition `a ⊕ y`, position `k₂` is the action point itself, so TumblerAdd gives `(a ⊕ y)_{k₂} = a_{k₂} + y_{k₂}`. From `a ⊕ x = a ⊕ y` we obtain `a_{k₂} = a_{k₂} + y_{k₂}`, hence `y_{k₂} = 0`. But `k₂` is the action point of `y`, so by definition `y_{k₂} > 0` — contradiction.

Both strict orderings are impossible, so `k₁ = k₂`. Write `k` for this common action point. We now verify that `x` and `y` agree at every position and have the same length.

**Positions i < k.** Both `x` and `y` have action point `k`, so by definition of action point every component before `k` is zero: `xᵢ = 0` and `yᵢ = 0`. Therefore `xᵢ = yᵢ = 0`.

**Position i = k.** TumblerAdd gives `(a ⊕ x)_k = a_k + x_k` and `(a ⊕ y)_k = a_k + y_k`. From `a ⊕ x = a ⊕ y` we get `a_k + x_k = a_k + y_k`, hence `x_k = y_k` by cancellation in ℕ.

**Positions i > k.** For both additions, positions after the action point fall in the tail-copy region of TumblerAdd: `(a ⊕ x)_i = x_i` and `(a ⊕ y)_i = y_i`. From `a ⊕ x = a ⊕ y` we get `x_i = y_i`.

**Length.** By T3 (CanonicalRepresentation), `a ⊕ x = a ⊕ y` implies `#(a ⊕ x) = #(a ⊕ y)`. The result-length identity (TumblerAdd) gives `#(a ⊕ w) = #w` for any well-defined addition. Applying this to both sides: `#x = #(a ⊕ x) = #(a ⊕ y) = #y`.

All components of `x` and `y` agree at every position and `#x = #y`, so `x = y` by T3 (CanonicalRepresentation).  ∎

TumblerAdd is *left-cancellative*: the start position can be "divided out" from equal results, recovering the displacement uniquely. This is a direct consequence of TumblerAdd's constructive definition — each component of the result is determined by exactly one input, so equality of results propagates back to equality of inputs.

*Worked example.* Let a = [2, 5] and suppose a ⊕ x = a ⊕ y = [2, 8]. We recover x and y uniquely. First, the action points must agree. Suppose k_x = 1: then (a ⊕ x)₁ = a₁ + x₁ = 2 + x₁ = 2, giving x₁ = 0, which contradicts k_x = 1 being the first nonzero component. So k_x ≠ 1, and since #x ≤ 2 (from the result length), k_x = 2. Now suppose k_y = 1: then (a ⊕ y)₁ = a₁ + y₁ = 2 + y₁ = 2, giving y₁ = 0, which contradicts k_y = 1. So k_y = 2. At position k = 2: a₂ + x₂ = 5 + x₂ = 8 gives x₂ = 3, and a₂ + y₂ = 5 + y₂ = 8 gives y₂ = 3. For i < k: x₁ = 0 = y₁ (both zero before the action point). From the result-length identity: #(a ⊕ x) = #x, so #x = 2 = #y. By T3, x = y = [0, 3].

*Formal Contract:*
- *Preconditions:* a, x, y ∈ T; x > 0; y > 0; actionPoint(x) ≤ #a; actionPoint(y) ≤ #a; a ⊕ x = a ⊕ y
- *Postconditions:* x = y

---

## TA-MTO — ManyToOne

Two tumblers a and b produce the same result under displacement w if and only if they agree on every component up to and including w's action point k. Components after position k are discarded by TumblerAdd's tail replacement, so only the prefix up to k influences the result.

*Formal Contract:*
- *Preconditions:* w ∈ T, w > 0, a ∈ T, b ∈ T, #a ≥ actionPoint(w), #b ≥ actionPoint(w)
- *Postconditions:* a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)

---

## TA-RC — RightCancellationFailure

Right cancellation fails: distinct tumblers can yield identical results under the same displacement. Any two start addresses that agree on components 1..k but differ only beyond position k will produce the same output under any displacement with action point k, because TumblerAdd discards and replaces the tail after the action point.

*Formal Contract:*
- *Postconditions:* ∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w

The mechanism is TumblerAdd's tail replacement: components of the start position after the action point are discarded and replaced by the displacement's tail. Any two starts that agree on components 1..k and differ only on components after k will produce the same result under any displacement with action point k. Formally:

---

## TA-assoc — AdditionAssociative

Tumbler addition is associative — `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` — when action points are compatible with the depths of their left operands. The result always has depth `#c`, and the action point of the composed displacement `b ⊕ c` is `min(actionPoint(b), actionPoint(c))`.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `b ∈ T`, `c ∈ T`, `b > 0`, `c > 0`, `k_b ≤ #a`, `k_c ≤ #b` (where `k_b = actionPoint(b)`, `k_c = actionPoint(c)`; these left-side conditions subsume the right-side conditions since `k_b ≤ #a` implies `min(k_b, k_c) ≤ #a`)
- *Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `actionPoint(b ⊕ c) = min(k_b, k_c)`

**Addition is not commutative.** We do NOT require `a ⊕ b = b ⊕ a`. The operands play asymmetric roles: the first is a *position*, the second is a *displacement*. Swapping them is semantically meaningless. Gregory's `absadd` confirms: the first argument supplies the prefix, the second the suffix — the reverse call gives a different (and typically wrong) result.

**There is no multiplication or division.** Gregory's analysis of the complete codebase confirms: no `tumblermult`, no `tumblerdiv`, no scaling operation of any kind. The arithmetic repertoire is: add, subtract, increment, compare. Tumblers are *addresses*, not quantities. You don't multiply two file paths or divide an address by three.

**Tumbler differences are not counts.** Nelson is emphatic: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." The difference between two addresses specifies *boundaries*, not *cardinality*. What lies between those boundaries depends on the actual population of the tree, which is dynamic and unpredictable. Between sibling addresses 3 and 7, document 5 might have arbitrarily many descendants — the span from 3 to 7 encompasses all of them, and their count is unknowable from the addresses alone. The arithmetic is an *addressing calculus*, not a *counting calculus*.

The absence of algebraic structure beyond a monotone shift is not a deficiency. It is the *minimum* that addressing requires. An ordered set with an order-preserving shift and an allocation increment is sufficient. Anything more would be unused machinery and unverified obligation.

---

## TA-strict — StrictIncrease

Adding any positive displacement to a tumbler strictly advances it: `a ⊕ w > a` whenever the operation is well-defined. This excludes degenerate models where addition is a no-op, and directly guarantees that spans `[s, s ⊕ ℓ)` are non-empty.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k ≤ #a` where `k` is the action point of `w`
- *Postconditions:* `a ⊕ w > a`

---

## TA0 — WellDefinedAddition

Tumbler addition is well-defined whenever the action point of the displacement fits within the depth of the base address. The result is a tumbler whose depth equals the depth of the displacement, not the base.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w

---

## TA1-strict — StrictOrderPreservation

When two tumblers are in strict order and the displacement's action point falls at or after their divergence, addition strictly preserves that order (`a ⊕ w < b ⊕ w`). If the action point precedes the divergence, both results become identical — order degrades to equality but never reverses.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, w > 0, actionPoint(w) ≤ min(#a, #b), actionPoint(w) ≥ divergence(a, b)
- *Postconditions:* a ⊕ w < b ⊕ w

But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:

---

## TA1 — OrderPreservationUnderAddition

Tumbler addition weakly preserves order: if `a < b` and both additions are well-defined, then `a ⊕ w ≤ b ⊕ w`. This is the universal (but non-strict) guarantee; strict preservation requires the additional constraint that the action point meets or exceeds the divergence of `a` and `b`.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, w > 0, actionPoint(w) ≤ min(#a, #b)
- *Postconditions:* a ⊕ w ≤ b ⊕ w

Strict order preservation holds under a tighter condition. We first need a precise notion of where two tumblers first differ.

---

## TA2 — WellDefinedSubtraction

Tumbler subtraction is closed on T: whenever a ≥ w, the result a ⊖ w is itself a valid tumbler. This establishes that the subtraction operator is well-defined and stays within the type.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w
- *Postconditions:* a ⊖ w ∈ T

---

## TA3-strict — OrderPreservationUnderSubtractionStrict

Subtracting a common lower bound w from two equal-length tumblers a < b strictly preserves their order: a ⊖ w < b ⊖ w. The equal-length precondition (#a = #b) is required for the strict inequality to hold.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Postconditions:* a ⊖ w < b ⊖ w

---

## TA3 — OrderPreservationUnderSubtractionWeak

A weak form of order preservation under subtraction: if a < b and both dominate w, then a ⊖ w ≤ b ⊖ w, with no equal-length requirement. This relaxes TA3-strict by allowing the result to collapse to equality when lengths differ.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w

---

## TA4 — PartialInverse

Tumbler addition and subtraction are a partial inverse pair: (a ⊕ w) ⊖ w = a, but only when w's action point equals #a and all of a's non-final components are zero. In general, ⊕ is asymmetric — it replaces the low-level suffix of the result with w's tail — so components of a below the action point are discarded and cannot be recovered by subtracting w.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`

Gregory's analysis confirms that `⊕` and `⊖` are NOT inverses in general. The implementation's `absadd` is asymmetric: the first argument supplies the high-level prefix, the second supplies the low-level suffix. When `d = a ⊖ b` strips a common prefix (reducing the exponent), `b ⊕ d` puts the difference in the wrong operand position — `absadd`'s else branch discards the first argument entirely and returns the second. The operand-order asymmetry causes total information loss even before any digit overflow.

The reverse direction is equally necessary:

---

## TA5-SIG — LastSignificantPosition

Defines sig(t) as the index of the rightmost nonzero component of tumbler t; for an all-zero tumbler, sig(t) = #t by convention. The result always satisfies 1 ≤ sig(t) ≤ #t, giving a well-defined handle on where a tumbler's significant content ends.

*Formal Contract:*
- *Preconditions:* `t ∈ T` (any tumbler with `#t ≥ 1`).
- *Definition:* `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; `sig(t) = #t` when `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Postconditions:* `1 ≤ sig(t) ≤ #t`.

---

## TA5-SigValid — SigOnValidAddresses

Because every valid address satisfying T4 has strictly positive components in every field and at least one component in its last field, the rightmost nonzero position is always the final position — so sig(t) = #t for all valid addresses.

*Formal Contract:*
- *Precondition:* `t` satisfies T4 (valid address tumbler: at most three zero-valued field separators, every field component strictly positive, every present field non-empty).
- *Guarantee:* `sig(t) = #t`.

---

## TA5 — HierarchicalIncrement

inc(t, k) is the allocation increment operator: for k = 0 it advances the counter at the rightmost nonzero position to produce the next sibling at the same hierarchical depth; for k > 0 it extends the address by k positions (k−1 zeros then a 1) to produce a child. In neither case does it produce the true immediate successor in the total order — that gap contains t's entire subtree — but for allocation purposes advancing past all existing addresses is all that is required.

*Formal Contract:*
- *Definition:* `inc(t, k)` for `t ∈ T`, `k ≥ 0`: when `k = 0`, modify position `sig(t)` (TA5-SIG) to `t_{sig(t)} + 1`; when `k > 0`, extend by `k` positions with `k - 1` zeros and final `1`.
- *Postconditions:* (a) `t' > t` under T1. (b) When `k = 0`: `(A i : 1 ≤ i < sig(t) : t'ᵢ = tᵢ)`. When `k > 0`: `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)`. (c) When `k = 0`: `#t' = #t`, modification only at `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, positions `#t + 1 ... #t + k - 1` are `0`, position `#t + k` is `1`.

Gregory's analysis reveals a critical distinction: `inc(t, 0)` does NOT produce the immediate successor of `t` in the total order. In the general case, it produces the smallest same-length tumbler that agrees with `t` on positions `1, ..., sig(t) − 1` and has a strictly larger component at position `sig(t)`. When `sig(t) = #t` — which holds for valid addresses by TA5-SigValid — this is the smallest same-length tumbler strictly greater than `t`: the *next peer* at the same hierarchical depth. When `sig(t) < #t` (i.e., trailing zeros exist beyond the rightmost nonzero component), the gap between `t` and `inc(t, 0)` contains same-length tumblers as well — for example, `(2, 0, 0)` and `inc((2, 0, 0), 0) = (3, 0, 0)` have `(2, 0, 1)` strictly between them. The gap between `t` and `inc(t, 0)` contains the entire subtree of `t`: all tumblers of the form `t.x₁. ... .xₘ` for any `m ≥ 1` and any `x₁ ≥ 0`. The true immediate successor in the total order is `t.0` — the zero-extension — by the prefix convention (T1 case (ii)). For any `k > 0`, `inc(t, k)` does NOT produce the immediate successor of `t` in the total order. For `k = 1` the result is `t.1`; for `k = 2` the result is `t.0.1`. In both cases, `t.0` (the true immediate successor) lies strictly between `t` and the result. The gap between `t` and `inc(t, k)` contains `t`'s entire subtree of zero-extensions. For address allocation, the distinction is harmless: allocation cares about advancing the counter past all existing addresses, not about visiting every point in the total order.

The conditions under which `inc` preserves the structural validity constraint T4 — including the boundary on `k` and the role of `zeros(t)` — are established in TA5a (IncrementPreservesT4).

| Label | Statement | Status |
|-------|-----------|--------|
| TA5 | `inc(t, k)` produces `t' > t` with same-length structure for `k = 0` (sibling) and extended structure for `k > 0` (child) | proved (this property) |
| TA5-SIG | `sig(t)` is the rightmost nonzero component position of `t`, or `#t` when all components are zero | definition (separate property) |
| TA5-SigValid | For every valid address satisfying T4, `sig(t) = #t` | proved (separate property) |
| TA5a | `inc(t, k)` preserves T4 iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`; violated for `k ≥ 3` | proved (separate property) |

---

## TA5a — IncrementPreservesT4

The allocation increment inc(t, k) preserves T4 validity if and only if no new empty field (adjacent zeros) is introduced: k = 0 always preserves validity, k = 1 preserves it when the address already has at most 3 zero separators, k = 2 preserves it only when zeros(t) ≤ 2, and k ≥ 3 always violates T4 by creating an empty field.

*Formal Contract:*
- *Precondition:* `t` satisfies T4 (valid address tumbler), `k ≥ 0`. `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` (T4).
- *Guarantee:* `inc(t, k)` satisfies T4 iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`.
- *Failure:* For `k ≥ 3`, `inc(t, k)` violates T4 (adjacent zeros create an empty field).

---

## TA6 — ZeroTumblers

No all-zero tumbler designates content — every such tumbler fails T4's positive-component requirement and is therefore not a valid address. Zero tumblers sit below all positive tumblers in the total order and serve as sentinels for uninitialized values and unbounded span endpoints.

*Formal Contract:*
- *Postconditions:* (a) `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`. (b) `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`.

Zero tumblers serve as *sentinels*: they mark uninitialized values, denote "unbounded" when used as span endpoints, and act as lower bounds.

---

## TA7a — SubspaceClosure

Defines the subspace S as the set of tumblers with all positive components (matching T4's field constraint) and characterizes when ⊕ and ⊖ preserve membership in S. Addition stays in S when all tail components of the width are positive; subtraction stays in S in most cases but exits S when the divergence point forces a zero into the first component — for example, [5,3] ⊖ [5,1] = [0,2] ∉ S.

*Formal Contract:*
- *Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #o`. For `⊖`: `o ∈ S`, `w ∈ T`, `w > 0`, `o ≥ w`.
- *Postconditions:* `o ⊕ w ∈ T`, `#(o ⊕ w) = #w`. `o ⊖ w ∈ T`. For `⊕`, the result is in S when all tail components of `w` (after the action point) are positive. For `⊖` with `actionPoint(w) ≥ 2` and `#w ≤ #o`: the divergence falls at position 1, TumblerSub produces `o` itself (a no-op), and the result is in S. For `⊖` with `actionPoint(w) = 1` and divergence at position `d = 1` (i.e., `o₁ ≠ w₁`): `r₁ = o₁ - w₁ > 0` and `rᵢ = oᵢ > 0` for `i > 1`, so the result is in S when `#w ≤ #o`. For `⊖` with `actionPoint(w) = 1` and divergence at position `d > 1` (i.e., `o₁ = w₁`): the result has `r₁ = 0` and lies in `T \ S` (counterexample: `[5, 3] ⊖ [5, 1] = [0, 2]`). For `⊖` when `#w > #o`: the result inherits trailing zeros at positions `#o + 1` through `#w` and lies in `T \ S`. For `⊖` on single-component ordinals (`#o = 1`, `#w = 1`): the result is in `S ∪ Z`: `[x] ⊖ [n] ∈ S` when `x > n`, and `[x] ⊖ [n] ∈ Z` when `x = n`.
- *Frame:* The subspace identifier `N`, held as structural context, is not an operand and is never modified by either operation.
- *Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields.

---

## TS1 — ShiftOrderPreservation

Shift is order-preserving on equal-length tumblers: if v₁ < v₂ and both have length m, shifting both by the same positive amount n yields shift(v₁, n) < shift(v₂, n). The relative ordering of same-length tumblers is invariant under shift.

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m, v₁ < v₂
- *Postconditions:* shift(v₁, n) < shift(v₂, n)

---

## TS2 — ShiftInjectivity

Shift is injective on equal-length tumblers: if two tumblers of the same length m produce the same result under the same positive shift n, they must have been identical. No two distinct same-length tumblers can collide under shift.

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m
- *Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂

---

## TS3 — ShiftComposition

Two successive shifts compose into a single shift: applying shift by n₁ and then by n₂ is identical to a single shift by n₁ + n₂. Shift preserves tumbler length throughout.

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ ≥ 1, #v = m
- *Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
- *Frame:* #shift(shift(v, n₁), n₂) = #v = m (shift preserves tumbler length)

---

## TS4 — ShiftStrictIncrease

Every positive shift strictly increases the tumbler: shift(v, n) > v for all n ≥ 1. No tumbler can be shifted in place or backward — shift always moves strictly forward in tumbler order.

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1, #v = m
- *Postconditions:* shift(v, n) > v

---

## TS5 — ShiftAmountMonotonicity

Larger shift amounts produce strictly larger results on the same tumbler: if n₂ > n₁ ≥ 1, then shift(v, n₂) > shift(v, n₁). The output of shift is strictly monotone in the shift amount.

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ > n₁, #v = m
- *Postconditions:* shift(v, n₁) < shift(v, n₂)

---

## TumblerAdd — TumblerAdd

Defines tumbler addition `a ⊕ w`, the operation that advances position `a` by displacement `w`. The result copies `a`'s components before the displacement's action point, adds at that level, then takes `w`'s deeper components — producing a tumbler strictly greater than `a` with the same length as `w`.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
- *Definition:* k = min{i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0}; rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w, a ⊕ w > a (T1), a ⊕ w ≥ w (T1)

---

## TumblerSub — TumblerSub

Defines tumbler subtraction `a ⊖ w` as the component-wise difference computed at the first point of zero-padded divergence: components before that point become zero, the divergence point is subtracted, and deeper components are copied from the minuend. The roundtrip `a ⊕ (b ⊖ a) = b` requires two independently necessary conditions — that the divergence point falls within `a`'s length and that `a` is no longer than `b` — explaining why TumblerSub's domain is strictly narrower than the ordering `a ≥ w` alone would suggest.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w (T1). Consequence (by Divergence case analysis via T1, Divergence, ZPD): when zpd(a, w) is defined, aₖ ≥ wₖ at k = zpd(a, w).
- *Definition:* a ⊖ w computed by case analysis on k = zpd(a, w) (ZPD), all component references using zero-padded values (aᵢ = 0 for i > #a, wᵢ = 0 for i > #w); rᵢ = 0 for i < k, rₖ = aₖ − wₖ, rᵢ = aᵢ (zero-padded) for i > k; when zpd(a, w) is undefined, a ⊖ w = [0, …, 0]; #(a ⊖ w) = max(#a, #w)
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = max(#a, #w)

---

## ZPD — ZeroPaddedDivergence

Defines `zpd(a, w)` as the index of the first position where two tumblers disagree after both are zero-padded to the same length. The function is partial — undefined when the padded sequences agree everywhere, a condition that arises not only when `a = w` but also when one tumbler is a zero-trailing prefix of the other.

*Formal Contract:*
- *Domain:* a ∈ T, w ∈ T
- *Definition:* Pad to length L = max(#a, #w): aᵢ = 0 for i > #a, wᵢ = 0 for i > #w. If (A i : 1 ≤ i ≤ L : aᵢ = wᵢ), zpd(a, w) is undefined. Otherwise, zpd(a, w) = min {k : 1 ≤ k ≤ L ∧ aₖ ≠ wₖ}.
- *Codomain:* When defined, zpd(a, w) ∈ {1, ..., max(#a, #w)}.
- *Partiality:* zpd(a, w) is undefined iff a and w are zero-padded-equal.

---

