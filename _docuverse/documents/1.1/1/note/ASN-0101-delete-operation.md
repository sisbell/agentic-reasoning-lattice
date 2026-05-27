# ASN-0101: DELETE Operation

*2026-05-27*

We seek a precise account of DELETE — the operation by which content disappears from a document's current view but never from the system. The contrast with conventional editing is stark. In a "destructive replacement" model, deletion overwrites prior bytes; the only record of what was removed is whatever the system happened to log. In Xanadu, deletion is a Vstream operation: it modifies the arrangement of references a document presents to its readers while leaving the underlying content store entirely untouched. The architectural commitment is unconditional:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The two halves of this commitment — content persistence and cross-document non-interference — are not independent. Each rests on the same structural fact: that *what exists* (the Istream of allocated I-addresses) is held in a different state component from *how it is currently arranged* (the Vstream of V→I mappings). DELETE manipulates the second without touching the first. Our task is to make this separation precise: to state exactly what DELETE changes, exactly what it preserves, and exactly which invariants the completed operation must re-establish.

## The setting

We adopt the state space of the foundations. A state `Σ = (C, L, E, M, R)` carries at least:

- the content store `C : T ⇀ Val`, with `dom(C)` the set of allocated I-addresses bearing values;
- the link store `L : T ⇀ Link`, with `dom(L)` the set of allocated link addresses;
- the entity set `E ⊆ T` of allocated node, account, and document addresses (ASN-0047);
- the family of arrangements `M : T ⇀ (T ⇀ T)`, with `M(d) : T ⇀ T` the arrangement of document `d` whenever `d ∈ dom(M)`;
- the provenance relation `R ⊆ T × E_doc` recording, for each I-address that has ever been arranged in a document, the documents into which it has been placed (ASN-0047).

The standing invariants are those established in the strand model, link model, and substrate: every `a ∈ dom(C)` is an element-level tumbler with `subspace_I(a) = s_C` and `#E(a) ≥ 2`; every `ℓ ∈ dom(L)` is similarly element-level with `subspace_I(ℓ) = s_L`; for each `d ∈ dom(M)` the arrangement `M(d)` is finite (S8-fin), functional (S2), referentially valid (S3★), and per-subspace contiguous with minimum at `[S, 1, ..., 1]` and sequential ordering (D-CTG★, D-MIN★, D-SEQ★ of ASN-0047). The two stores are disjoint (L14) and immutable across all transitions in their respective ways (P0 for content, L12 for links). Link-subspace V-positions, when present, are constrained by CL-OWN (the link must be home-document allocated) and CL-UNIQ (at most one V-position per link), both inherited from ASN-0047.

For each document `d ∈ dom(M)` and each subspace `S ∈ {s_C, s_L}`, write

`V_S(d) := {v ∈ dom(M(d)) : subspace(v) = S}`

— the set of V-positions in subspace `S`. By S8-depth, all V-positions in `V_S(d)` share a common depth `m_S ≥ 2`. By D-SEQ★, when non-empty `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`. We write `δ(n, m)` for the ordinal displacement of ASN-0034 — the tumbler `[0, ..., 0, n]` of length `m` — and `shift(v, n)` for `v ⊕ δ(n, #v)`, the OrdinalShift advancing `v`'s last component by `n`.

## The operation

We specify DELETE as an atomic state transition `DEL[d, σ]` removing a V-span `σ` from document `d`'s arrangement. The operation generalises the contraction of ASN-0082 (which fixes `S = s_C` and `m = 2`) to any subspace and depth.

Nelson's FEBE protocol treats DELETE as a single primitive — `DELETEVSPAN` (LM 4/66) — over arbitrary spans, with no syntactic distinction between deletions at the end of a document (suffix truncation) and deletions in the interior. We adopt this stance: `DEL[d, σ]` is a *new atomic transition kind* extending the foundation's transition vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ}` (ASN-0047, ASN-0093). It is *not* a derived composite of `K.μ⁻` (suffix truncation, ASN-0047) and `K.μ~` (reordering, ASN-0047). Two distinct obstacles block the composite substitution.

First, when the composite is well-formed, it exposes an *observable intermediate state*. On an interior span with `|dom_S(M(d))| ≥ 2`, one could in principle apply `K.μ~` with an admissible permutation that moves the to-be-deleted I-addresses to the suffix of `V_S(d)` (the permutation is admissible because `K.μ~-FIX` preserves `dom(M(d))`, and rebinding I-addresses across V-positions preserves D-CTG★, D-MIN★, D-SEQ★ and S3★), then apply `K.μ⁻` to truncate that suffix. The post-`K.μ~` arrangement is a state in which the to-be-deleted I-addresses still inhabit `dom(M(d))` but at different V-positions than in either the pre- or post-state of the composite. By SequentialAtomicTransitions (ASN-0093), each elementary transition is atomic and uninterruptible; the composite is therefore observable as two distinct state transitions, not one.

Second, the composite is not always *available*. K.μ~ (ASN-0047) requires `|dom_C(M(d))| ≥ 2` as a formal precondition. When DEL operates on a content subspace with `n_S = 1` (a single-position content subspace deleted in full, i.e., `p = 1` and `n = 1`), no admissible permutation exists and the composite cannot be constructed at all. Even cases with `|dom_C(M(d))| ≥ 2` where the *only* admissible re-arrangement is the identity (forbidden by K.μ~'s `π ≠ id` clause) fall outside the composite's domain. Moreover, ASN-0047 defines K.μ~ exclusively over the content subspace — its precondition `|dom_C(M(d))| ≥ 2` ranges over `V_{s_C}(d)`, not over `V_S(d)` for arbitrary `S`, and the foundation supplies no analogue K.μ~_L over the link subspace. For every link-subspace interior deletion — even those with `|V_{s_L}(d)| ≥ 2` and with multiple admissible permutations — the K.μ⁻ + K.μ~ composite is structurally unconstructable in the existing vocabulary, independent of any cardinality or admissibility argument. The composite-substitute strategy is therefore unavailable on a non-trivial sub-class of DEL instances: every link-subspace interior deletion, every content-subspace interior deletion with `n_S = 1`, and every content-subspace case in which all admissible permutations equal the identity.

Nelson treats DELETEVSPAN as a primitive precisely to forbid the intermediate observability and to cover the cases where no composite suffices, and Gregory's `bed.c` realises it as a run-to-completion procedure. DEL accordingly enters the foundation's transition vocabulary as a new elementary transition kind, closing the gap in a single indivisible step.

The coupling constraints J0, J1★, and J1'★ of ASN-0047's ValidComposite★ — each of which records what must be true of a composite *that places new content into arrangements* — hold vacuously at any DEL step. D0 below ensures `dom(C') = dom(C)`, `dom(L') = dom(L)`, and `R' = R`, so no allocation can be required to "match" a placement, no extension can be required to "match" a provenance record, and no new provenance pair is added. The formal extension of ValidComposite★ to admit DEL is recorded as D10 below.

**Operation DEL[d, σ].**

*Parameters.* A document `d` and a level-uniform V-span `σ = (s, ℓ)` of ordinal type.

*Preconditions.*

- *Document membership:* `d ∈ dom(M)`.
- *Span well-formedness:* `s ∈ V_S(d)` for some subspace `S = subspace(s) ∈ {s_C, s_L}`; `Pos(ℓ)`; `#ℓ = #s = m_S`; the action point of `ℓ` is `m_S` (equivalently `ℓ = δ(n, m_S)` for some `n ≥ 1`).
- *Containment:* writing `r := s ⊕ ℓ`, every depth-`m_S` position `v` with `subspace(v) = S` and `s ≤ v < r` lies in `V_S(d)`. Under D-SEQ★ this reduces to `s = [S, 1, ..., 1, p]` for some `p ∈ {1, ..., n_S}` and `p + n − 1 ≤ n_S`, equivalently `p + n ≤ n_S + 1`.

*Effect.* Let `Λ := {v ∈ V_S(d) : v < s}` (the *left region* — positions strictly before the deleted span), `X := {v ∈ V_S(d) : s ≤ v < r}` (positions in the deleted span), `Ρ := {v ∈ V_S(d) : v ≥ r}` (the *right region* — positions strictly after). The capitals Λ (Greek lambda) and Ρ (Greek rho) are chosen to avoid notational collision with the link store `Σ.L` and the provenance relation `Σ.R`.

The *shift function* `σ_d : Ρ → T` decrements its argument's last component by `n` while leaving earlier components unchanged. Formally, `σ_d(v)` is the unique tumbler `u ∈ T` satisfying `shift(u, n) = v`. Well-definedness: by the length-preservation postcondition `#shift(u, n) = #u` of OrdinalShift (ASN-0034), the equation forces `#u = #v = m_S`; by TS2 (ShiftInjectivity, ASN-0034) on length-`m_S` tumblers, at most one such `u` exists. Existence: for each `v = [S, 1, ..., 1, k] ∈ Ρ` (form fixed by D-SEQ★) with `k ≥ p + n`, the tumbler `u := [S, 1, ..., 1, k − n]` (with `k − n ≥ p ≥ 1`, so all components positive) satisfies `shift(u, n) = u ⊕ δ(n, m_S) = [S, 1, ..., 1, (k − n) + n] = [S, 1, ..., 1, k] = v` by TumblerAdd's componentwise definition. So `σ_d(v) = [S, 1, ..., 1, k − n]`. The map `σ_d` is therefore a bijection from `Ρ` onto `Q := {σ_d(v) : v ∈ Ρ} = {[S, 1, ..., 1, j] : p ≤ j ≤ n_S − n}`. The post-state arrangement `M'(d)` satisfies:

- *Domain:* `V_S(M'(d)) = Λ ∪ Q`, and `V_{S'}(M'(d)) = V_{S'}(d)` for every `S' ∈ {s_C, s_L}` with `S' ≠ S`.
- *Values, left of the cut:* `(A v ∈ Λ :: M'(d)(v) = M(d)(v))`.
- *Values, shifted right of the cut:* `(A v ∈ Ρ :: M'(d)(σ_d(v)) = M(d)(v))`.
- *Values, other subspace:* `(A v : v ∈ V_{S'}(d) ∧ S' ≠ S :: M'(d)(v) = M(d)(v))`.

*Frame.*

- *Content store:* `C' = C` exactly — `dom(C') = dom(C)` and `(A a ∈ dom(C) :: C'(a) = C(a))`.
- *Link store:* `L' = L` exactly — `dom(L') = dom(L)` and `(A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`.
- *Entity set:* `E' = E` exactly — no entity is added or removed (DELETE does not allocate or de-allocate documents, accounts, or nodes).
- *Provenance:* `R' = R` exactly — no provenance pair is added or removed (DELETE only removes arrangement entries; the historical record of which I-addresses have ever inhabited which documents is preserved).
- *Document set:* `dom(M') = dom(M)` — `d` is not removed, and no other document is added.
- *Other documents:* `(A d' ∈ dom(M) : d' ≠ d :: M'(d') = M(d'))`.

We refer to this transition specification as **D0**.

The form of the effect makes explicit a structural fact that is easy to miss: DELETE does not "remove and then re-number" as two operations. It is one operation whose post-state arrangement is determined by the pre-state and the span alone. The shift function `σ_d` is the bijection from `Ρ` to `Q` that closes the gap, and the post-state mapping is obtained by composing `M(d)` with `σ_d^{-1}` on the shifted region. No intermediate state with "holes" is observable — the operation is atomic.

## What shifts: closing the gap

The ASN-0034 algebra fixes the shift mechanism precisely. Let `v ∈ Ρ` with `v = [S, 1, ..., 1, k]` and `k ≥ p + n`. The shift function `σ_d(v)` is the unique tumbler `u` with `shift(u, n) = v`. Because OrdinalShift advances only the last component of its argument by `n` while leaving earlier components fixed (shift(v, n)ᵢ = vᵢ for i < m; shift(v, n)ₘ = vₘ + n), the inverse simply decrements the last component: `u = [S, 1, ..., 1, k − n]`. Verification: `shift([S, 1, ..., 1, k − n], n) = [S, 1, ..., 1, k − n] ⊕ δ(n, m_S) = [S, 1, ..., 1, (k − n) + n] = [S, 1, ..., 1, k] = v` ✓. The boundary case `v = r = [S, 1, ..., 1, p + n]` maps to `σ_d(r) = [S, 1, ..., 1, p] = s`, so the first shifted position lands exactly where the deletion began — closing the gap precisely.

That the operation actually closes the gap, rather than leaving it open with placeholders, is Nelson's explicit design choice. We extract it from the dense-sequence convention: the V-stream is defined to be a contiguous ordering with no notion of "empty positions" between consecutive members. There is nothing in the abstract specification of the V-stream to denote — and nothing for a reader to observe — at a vacated position. The closure of the gap follows from the choice of representation, not from a separate gap-closing pass.

We record the basic structural consequence of the shift:

**D1 — Gap closure.** Let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ)`. The shift function `σ_d` is an order-preserving bijection from `Ρ` onto `Q`. Writing `n_S' := |V_S(d)| − n`: when `n_S' ≥ 1`, `V_S(M'(d)) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S'}` is contiguous with minimum `[S, 1, ..., 1]` of depth `m_S`; when `n_S' = 0`, `V_S(M'(d)) = ∅` and D-CTG★, D-MIN★, D-SEQ★ hold vacuously for subspace `S`.

*Justification.* Structural form of `σ_d(v)`: by the D0 effect's existence argument, for each `v = [S, 1, ..., 1, k] ∈ Ρ` (form fixed by D-SEQ★) with `k ≥ p + n`, `σ_d(v) = [S, 1, ..., 1, k − n]` — the unique length-`m_S` tumbler whose shift by `n` gives `v`. Order preservation: for `v₁, v₂ ∈ Ρ` with `v₁ < v₂`, set `uᵢ := σ_d(vᵢ)` so that `shift(uᵢ, n) = vᵢ` and `#u₁ = #u₂ = m_S`. By TS1 (ShiftOrderPreservation, ASN-0034), `u₁ < u₂` would imply `shift(u₁, n) < shift(u₂, n)`, i.e., `v₁ < v₂`. The contrapositive at the order-preserving inverse: from `v₁ < v₂` and equal lengths, T1 trichotomy on `u₁, u₂` yields one of `u₁ < u₂`, `u₁ = u₂`, or `u₂ < u₁`. The middle case is excluded because `shift` is injective (TS2) and would force `v₁ = v₂`; the last is excluded by applying TS1 directly (which would yield `v₂ < v₁`, contradicting `v₁ < v₂`). So `u₁ < u₂`, i.e., `σ_d(v₁) < σ_d(v₂)`. Injectivity then follows from order preservation by trichotomy. Surjectivity onto `Q` is by construction. The post-state characterisation: each `v ∈ Λ` has `v = [S, 1, ..., 1, k]` with `1 ≤ k ≤ p − 1`; each `σ_d(v')` with `v' = [S, 1, ..., 1, k']` and `p + n ≤ k' ≤ n_S` has the form `[S, 1, ..., 1, k' − n]` with `p ≤ k' − n ≤ n_S − n` (the leading components stay at `S, 1, ..., 1` because `shift` modifies only the last component, so the inverse `σ_d` likewise leaves the leading components fixed). The union Λ ∪ Q is `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S − n}`. When this set is empty (`n_S = n`), there are no positions to order, and the contiguity, minimum, and sequentiality predicates hold vacuously. ∎

This is the natural generalisation of ASN-0082's D-BJ (which discharges the same conclusion at the fixed depth `m = 2` and the fixed subspace `S = s_C`) to arbitrary subspaces and depths. The argument is uniform in `m_S`: TS1 (order preservation) and TS2 (injectivity) of OrdinalShift in ASN-0034 hold at every length `m ≥ 2`, so the shift-inverse `σ_d` is well-defined and order-preserving at every depth at which `V_S(d)` can exist.

Gregory's implementation realises this through a two-phase protocol on the tree of POOM crums that materialises `M(d)`. Phase 1 establishes "knives" at the boundaries `s` and `r`, splitting any crum interior to either knife into a pair of crums boundary-aligned with the knife. Phase 2 walks the affected children of the spanning node and applies one of three actions per crum: untouched (the crum lies before `s`), freed (the crum lies in `[s, r)`), or shifted (the crum lies at or after `r`, and its V-displacement is reduced by `width(σ)`). After the walk, a width-recomputation pass propagates the changes upward.

The abstract specification is silent on the tree structure but does require *some* such mechanism — the operation must be able, in finite work proportional to the affected region, to produce a post-state arrangement satisfying D0's domain and value conditions. The two-knife structure is an implementation choice that realises this in a particularly direct way. Two observations sharpen the abstract picture:

- *Boundary alignment is necessary, not incidental.* Any implementation that represents the arrangement compactly (as runs, or as B-tree nodes) must arrange for the deletion boundaries `s` and `r` to coincide with representation boundaries before the per-region action can be applied uniformly. Without such alignment, individual cells of the representation would span the boundary and require special-case handling. The two-knife pattern (cut at both endpoints, then classify) generalises beyond tree representations to any compact arrangement.

- *No reconciliation across the gap.* After the shift, two runs that were previously separated by the deleted region become V-adjacent. Whether their I-extents are now I-adjacent — and could therefore be merged into a single run under the bundle-algebra rules — is in general indeterminate. The abstract specification does not require a reconciliation pass, and Gregory confirms that none is performed: formerly non-adjacent crums whose V-positions become contiguous remain separate. This is consistent with the principle that DELETE preserves arrangement information without re-canonicalising; merging would conflate the boundaries of two independently inserted runs with the boundaries of a single uninterrupted run.

## A worked example

We instantiate the operation on a concrete arrangement to verify the postconditions. Consider a document `d` with content-subspace arrangement (`S = s_C = 1`, depth `m_S = 3`):

```
V_1(d) = {[1, 1, 1], [1, 1, 2], [1, 1, 3], [1, 1, 4]}
M(d)(v) = a_v  where a_1, a_2, a_3, a_4 are the first four emissions of d's
                content sub-allocator A_C(d): a_k = [d, 0, 1, k] for k ∈ {1, 2, 3, 4},
                with #a_k = #d + 3
```

so `n_S = 4`. We apply `DEL[d, σ]` with `s = [1, 1, 2]` and `ℓ = δ(2, 3) = [0, 0, 2]`. Then `r = s ⊕ ℓ = [1, 1, 4]`, `p = 2`, `n = 2`.

*Region computation.*

- `Λ = {v ∈ V_1(d) : v < [1, 1, 2]} = {[1, 1, 1]}`.
- `X = {v ∈ V_1(d) : [1, 1, 2] ≤ v < [1, 1, 4]} = {[1, 1, 2], [1, 1, 3]}`.
- `Ρ = {v ∈ V_1(d) : v ≥ [1, 1, 4]} = {[1, 1, 4]}`.

*Shift function.* For the single element of `Ρ`, `σ_d([1, 1, 4])` is the unique tumbler `u` with `shift(u, 2) = [1, 1, 4]`. Setting `u = [1, 1, 2]`:

```
shift([1, 1, 2], 2) = [1, 1, 2] ⊕ δ(2, 3) = [1, 1, 2] ⊕ [0, 0, 2] = [1, 1, 4]    ✓
```

So `σ_d([1, 1, 4]) = [1, 1, 2]` and `Q = {[1, 1, 2]}`.

*Post-state.*

- *Domain:* `V_1(M'(d)) = Λ ∪ Q = {[1, 1, 1], [1, 1, 2]}`, of cardinality `n_S − n = 4 − 2 = 2`.
- *Values:* `M'(d)([1, 1, 1]) = a_1` (from `Λ`); `M'(d)([1, 1, 2]) = M(d)(σ_d^{-1}([1, 1, 2])) = M(d)([1, 1, 4]) = a_4` (from the shifted `Ρ`).
- *Stores:* `dom(C') = dom(C)`, with `a_1, a_2, a_3, a_4` all still in `dom(C')` (D2). The originals `a_2` and `a_3` are now orphaned with respect to `M'(d)` but remain addressable from `C'`.

*Verification of D1.* The post-state `V_1(M'(d)) = {[1, 1, 1], [1, 1, 2]}` is `{[1, 1, k] : 1 ≤ k ≤ 2}` (depth-3 form with `S = 1`, one middle component fixed at `1`, last component varying over `1..n_S − n`), matching D1's predicted form `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S − n}`. The shift `σ_d` is a bijection from `Ρ = {[1, 1, 4]}` to `Q = {[1, 1, 2]}` — trivially so on a singleton.

*Verification of D8.* S8a holds on every post-state V-position (zeros = 0, depth = 3, components positive). S8-depth holds (both surviving positions have depth 3). S2 holds (the domain is two distinct keys, each with a single value). S3★ holds: `a_1, a_4 ∈ dom(C') = dom(C)` by D2. D-CTG★, D-MIN★, D-SEQ★ hold: the post-state is the contiguous prefix of depth-3 positions in subspace 1 starting at `[1, 1, 1]`, with maximum `[1, 1, 2]`.

*Verification of D9 (link projection).* We extend the example with a concrete link. Let `ℓ_0 ∈ dom(L)` be any link, and consider slot 1 with endset `L(ℓ_0).e_1 = {(a_1, δ(4, #a_1))}` — a single span anchored at `a_1` of ordinal width 4. (Slots 2 and 3 carry whatever other-endset and type-endset data the link bears; D9 quantifies over each slot independently, so the local computation depends only on the slot under examination.) By the ASN-0053 denotation, `coverage(L(ℓ_0).e_1) = {t ∈ T : a_1 ≤ t < a_1 ⊕ δ(4, #a_1)}`. Computing the upper bound: `a_1 = [d, 0, 1, 1]` and `δ(4, #a_1) = [0, ..., 0, 4]` of length `#a_1`, so by TumblerAdd's componentwise rule `a_1 ⊕ δ(4, #a_1) = [d, 0, 1, 5]`. Hence `coverage(L(ℓ_0).e_1) = {t ∈ T : [d, 0, 1, 1] ≤ t < [d, 0, 1, 5]} ⊇ {a_1, a_2, a_3, a_4}` (each `a_k = [d, 0, 1, k]` with `1 ≤ k ≤ 4` lies in this half-open interval).

*Pre-state projection.* `project(L(ℓ_0).e_1, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(L(ℓ_0).e_1)}`. Element by element:
- `v = [1, 1, 1]` → `M(d)(v) = a_1`: in coverage ✓
- `v = [1, 1, 2]` → `M(d)(v) = a_2`: in coverage ✓
- `v = [1, 1, 3]` → `M(d)(v) = a_3`: in coverage ✓
- `v = [1, 1, 4]` → `M(d)(v) = a_4`: in coverage ✓

So `project(L(ℓ_0).e_1, d, Σ) = V_1(d) = {[1, 1, 1], [1, 1, 2], [1, 1, 3], [1, 1, 4]}`.

*Post-state projection.* By D3, `L'(ℓ_0).e_1 = L(ℓ_0).e_1`, so `coverage(L'(ℓ_0).e_1) = coverage(L(ℓ_0).e_1)`. Then `project(L'(ℓ_0).e_1, d, Σ') = {v ∈ dom(M'(d)) : M'(d)(v) ∈ coverage(L(ℓ_0).e_1)}`. Element by element over the post-state domain restricted to subspace 1:
- `v = [1, 1, 1]` → `M'(d)(v) = a_1`: in coverage ✓
- `v = [1, 1, 2]` → `M'(d)(v) = a_4`: in coverage ✓

So `project(L'(ℓ_0).e_1, d, Σ') ∩ V_1(M'(d)) = {[1, 1, 1], [1, 1, 2]}`.

*Verification of D9's third bullet.* The equation requires
```
project(L'(ℓ_0).e_1, d, Σ') ∩ V_1(M'(d))
  = (project(L(ℓ_0).e_1, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ_0).e_1, d, Σ) ∩ Ρ}
```
LHS, from the post-state computation above: `{[1, 1, 1], [1, 1, 2]}`. RHS, computed directly:
- `project(L(ℓ_0).e_1, d, Σ) ∩ Λ = V_1(d) ∩ {[1, 1, 1]} = {[1, 1, 1]}`
- `project(L(ℓ_0).e_1, d, Σ) ∩ Ρ = V_1(d) ∩ {[1, 1, 4]} = {[1, 1, 4]}`, so `{σ_d([1, 1, 4])} = {[1, 1, 2]}`
- Union: `{[1, 1, 1]} ∪ {[1, 1, 2]} = {[1, 1, 1], [1, 1, 2]}`

LHS = RHS = `{[1, 1, 1], [1, 1, 2]}` ✓. The verification exercises both contributions: the unshifted summand from `Λ` (carrying `[1, 1, 1] → a_1`) and the shifted summand from `Ρ` (carrying `[1, 1, 4] → a_4`, renamed to `[1, 1, 2]` by `σ_d`).

The link `ℓ_0` itself remains in `dom(L')` with `L'(ℓ_0) = L(ℓ_0)` by D3. Its discoverability from `d` has shrunk from 4 positions to 2 positions; the I-addresses `a_2` and `a_3` that were referenced by the deleted V-positions `[1, 1, 2]` and `[1, 1, 3]` are still in `coverage(L'(ℓ_0).e_1)` but no longer projected from `d`. They remain in `dom(C')` by D2 and could be re-projected by a subsequent insertion mapping a V-position in `d` to either of them.

### A link-subspace example

The content-subspace example above does not exercise CL-OWN, CL-UNIQ, or the `dom(L)` clause of D9 — these are non-trivial only when the deleted positions reach into the link subspace. We supply a second example, with the same document `d` now carrying a link-subspace arrangement (`S = s_L = 2`, depth `m_L = 2` by LinkVPositionDepthAxiom):

```
V_2(d) = {[2, 1], [2, 2], [2, 3]}
M(d)([2, k]) = ℓ_k  where ℓ_1, ℓ_2, ℓ_3 are the first three emissions of d's
                     link sub-allocator A_L(d): ℓ_k = [d, 0, 2, k] for k ∈ {1, 2, 3},
                     with #ℓ_k = #d + 3
```

so `n_L = 3`. Pre-state invariants hold: `subspace_I(ℓ_k) = 2 = s_L` for each `k` (L0); `origin(ℓ_k) = d` for each `k`, so CL-OWN holds on `V_2(d)`; the three V-positions map to three distinct link addresses, so CL-UNIQ holds.

We apply `DEL[d, σ]` with `s = [2, 2]` and `ℓ_σ = δ(1, 2) = [0, 1]`. Then `r = s ⊕ ℓ_σ = [2, 3]`, `p = 2`, `n = 1` — a singleton interior deletion in the link subspace.

*Region computation.*

- `Λ = {v ∈ V_2(d) : v < [2, 2]} = {[2, 1]}`.
- `X = {v ∈ V_2(d) : [2, 2] ≤ v < [2, 3]} = {[2, 2]}`.
- `Ρ = {v ∈ V_2(d) : v ≥ [2, 3]} = {[2, 3]}`.

*Shift function.* For `[2, 3] ∈ Ρ`, `σ_d([2, 3])` is the unique `u` with `shift(u, 1) = [2, 3]`. Setting `u = [2, 2]`: `shift([2, 2], 1) = [2, 2] ⊕ δ(1, 2) = [2, 2] ⊕ [0, 1] = [2, 3]` ✓. So `σ_d([2, 3]) = [2, 2]` and `Q = {[2, 2]}`.

*Post-state.*

- *Domain:* `V_2(M'(d)) = Λ ∪ Q = {[2, 1], [2, 2]}`, of cardinality `n_L − n = 2`.
- *Values:* `M'(d)([2, 1]) = ℓ_1` (from `Λ`); `M'(d)([2, 2]) = M(d)(σ_d^{-1}([2, 2])) = M(d)([2, 3]) = ℓ_3` (from the shifted `Ρ`).
- *Stores:* `dom(L') = dom(L)`, with `ℓ_1, ℓ_2, ℓ_3` all still in `dom(L')` (D3). The original `ℓ_2` is now orphaned with respect to `M'(d)` but remains addressable in `L'`.

*Verification of CL-OWN.* The post-state link-subspace restriction `M'(d)|_{V_2(M'(d))}` carries V-position `[2, 1]` to `ℓ_1` and `[2, 2]` to `ℓ_3`. Both target addresses satisfy `origin(ℓ_1) = origin(ℓ_3) = d`, inherited from pre-state CL-OWN on `V_2(d) = Λ ⊎ {[2, 2]} ⊎ Ρ`. The re-mapping at the post-state `[2, 2]` (which now carries `ℓ_3` rather than the pre-state `ℓ_2`) does not break CL-OWN: the new image is itself a pre-state link with `origin = d`. CL-OWN holds at the post-state.

*Verification of CL-UNIQ.* The post-state restriction `M'(d)|_{V_2(M'(d))}` has two distinct keys `[2, 1] ≠ [2, 2]` mapping to two distinct values `ℓ_1 ≠ ℓ_3` (distinct by pre-state CL-UNIQ on the original V-positions `[2, 1]` and `[2, 3]`, whose images must be distinct). Injectivity holds. The argument exercises D8's CL-UNIQ source-correspondence: `M'(d)(Λ) = M(d)(Λ) = {ℓ_1}` and `M'(d)(Q) = M(d)(Ρ) = {ℓ_3}` are disjoint, so the post-state restriction is injective with image `{ℓ_1, ℓ_3}`.

*Verification of D9's third bullet under the `dom(L)` clause of S3★.* Consider another link `ℓ_0 ∈ dom(L)` (not one of `ℓ_1, ℓ_2, ℓ_3`) with slot-1 endset `L(ℓ_0).e_1 = {(ℓ_1, δ(3, #ℓ_1))}` — a single span anchored at `ℓ_1` of ordinal width 3. By the span semantics of ASN-0053 and the TumblerAdd componentwise rule, `coverage(L(ℓ_0).e_1) = {t ∈ T : [d, 0, 2, 1] ≤ t < [d, 0, 2, 4]} ⊇ {ℓ_1, ℓ_2, ℓ_3}`. Pre-state projection:
- `v = [2, 1]` → `ℓ_1`: in coverage ✓
- `v = [2, 2]` → `ℓ_2`: in coverage ✓
- `v = [2, 3]` → `ℓ_3`: in coverage ✓

(Any content-subspace positions of `d` map to I-addresses with `subspace_I = s_C = 1`, which fall outside the link-subspace coverage and so do not enter the projection.) So `project(L(ℓ_0).e_1, d, Σ) ∩ V_2(d) = {[2, 1], [2, 2], [2, 3]}`.

Post-state projection over `V_2(M'(d))`:
- `v = [2, 1]` → `ℓ_1`: in coverage ✓
- `v = [2, 2]` → `ℓ_3`: in coverage ✓

So `project(L'(ℓ_0).e_1, d, Σ') ∩ V_2(M'(d)) = {[2, 1], [2, 2]}`.

D9's third bullet, with `Λ = {[2, 1]}` and `Ρ = {[2, 3]}`:
- `project(L(ℓ_0).e_1, d, Σ) ∩ Λ = {[2, 1]}`
- `project(L(ℓ_0).e_1, d, Σ) ∩ Ρ = {[2, 3]}`, so `{σ_d([2, 3])} = {[2, 2]}`
- Union: `{[2, 1]} ∪ {[2, 2]} = {[2, 1], [2, 2]}`

LHS = RHS = `{[2, 1], [2, 2]}` ✓. The verification exercises both contributions in the link subspace: the unshifted summand from `Λ` (carrying `[2, 1] → ℓ_1`) and the shifted summand from `Ρ` (carrying `[2, 3] → ℓ_3`, renamed to `[2, 2]` by `σ_d`). The deleted link reference `[2, 2] → ℓ_2` is gone from the post-state projection, while `ℓ_2` itself remains in `dom(L')`.

*Verification of D7.* For each I-address in `ran(M(d)|_{V_2(d)}) = {ℓ_1, ℓ_2, ℓ_3}`: `ℓ_1, ℓ_3 ∈ dom(L')` by D3 (the surviving link references); `ℓ_2 ∈ dom(L')` by D3 (the deleted link reference's target still exists). All three `origin(·) = d` projections are unchanged because `origin` is a structural projection of the I-address's tumbler, depending on no state component. D7 holds in the link-subspace classification: `ℓ_k ∈ dom(L')` for every `k`, and `origin` is preserved.

The two examples — content-subspace (depth 3) and link-subspace (depth 2) — together cover the cases that exercise D8's source-correspondence argument: the content example tests S3★'s `dom(C)` clause and shows the shift mechanism at depth ≥ 3, while the link example tests CL-OWN, CL-UNIQ, and D9 under the `dom(L)` clause of S3★ at depth 2. No constraint of D0 is specialised to a particular depth or subspace; both examples follow the same formulas.

## Boundary cases

We enumerate configurations that stress different parts of the specification, verifying that D0 and D8 hold uniformly.

*Empty post-state (`n = n_S`, `p = 1`).* The entire content subspace is deleted: `Λ = ∅`, `X = V_S(d)`, `Ρ = ∅`, `Q = ∅`. The post-state `V_S(M'(d)) = ∅`. D-MIN★ holds vacuously (no minimum to predicate over). D-CTG★ and D-SEQ★ hold vacuously. By D6, `V_{S'}(M'(d))` for `S' ≠ S` is unchanged — the other subspace's arrangement, its links, and its discoverability all survive the emptying of the affected subspace. D8 holds: S8-fin reduces `|dom(M'(d))| ≤ |dom(M(d))|` to a strict inequality, and the empty subspace contributes no constraints.

*Deletion at the start (`p = 1`, `n < n_S`).* `Λ = ∅`, `X = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`, `Ρ = {[S, 1, ..., 1, k] : n + 1 ≤ k ≤ n_S}`. The first position of `Ρ` is `r = [S, 1, ..., 1, n + 1]`. Computing `σ_d(r)`: σ_d(r) is the unique `u` with `shift(u, n) = r`. Setting `u = [S, 1, ..., 1, 1]`: `shift(u, n) = u ⊕ δ(n, m_S) = [S, 1, ..., 1, 1 + n] = r` ✓. So `σ_d(r) = [S, 1, ..., 1, 1] = [S, 1, ..., 1]`. D-MIN★ holds: the post-state minimum is `σ_d(r) = [S, 1, ..., 1]`, exactly the form D-MIN★ requires.

*Deletion at the end (`p + n = n_S + 1`).* `Ρ = ∅`, so no shift occurs. `V_S(M'(d)) = Λ = {[S, 1, ..., 1, k] : 1 ≤ k ≤ p − 1}`. This is the case that ASN-0047's `K.μ⁻` (suffix truncation) covers as a special case; DEL generalises by allowing arbitrary `s` rather than requiring `p` to start at any specific position. D1's post-state characterisation reduces correctly: `n_S' = n_S − n = p − 1`.

*Singleton subspace deletion (`n_S = 1`, `n = 1`, `p = 1`).* Both `Λ = ∅` and `Ρ = ∅`. The subspace is emptied in one step. This is a specialisation of the empty post-state case above.

*Singleton interior deletion (`n = 1`, `1 < p < n_S`).* The most arithmetically subtle of the small cases. `Λ = {[S, 1, ..., 1, k] : 1 ≤ k ≤ p − 1}` (non-empty), `X = {[S, 1, ..., 1, p]}` (singleton), `Ρ = {[S, 1, ..., 1, k] : p + 1 ≤ k ≤ n_S}` (non-empty). Every position in `Ρ` is shifted by 1: `σ_d([S, 1, ..., 1, k]) = [S, 1, ..., 1, k − 1]`. The post-state is `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S − 1}` — the contiguous prefix of length `n_S − 1`.

*Cross-subspace independence.* For each boundary case above, D6 ensures the other subspace's arrangement is preserved bytewise. A document with both content and link subspaces populated, on which DEL affects only the content subspace, leaves CL-OWN and CL-UNIQ trivially intact for the link subspace because no link-subspace V-position is altered.

In each case, D0's effect, D1's gap-closure characterisation, and D8's well-formedness preservation hold. The specification is not specialised by case; the same formulas apply, and degenerate sub-expressions (empty `Λ`, `Ρ`, or `Q`) reduce predictably.

## What is preserved

We turn to the structural commitments that distinguish DELETE from destructive replacement. Each appears as a frame condition in D0; each deserves an explicit statement because each was load-bearing for Nelson's design intent.

### Content store: the Istream is untouched

**D2 — Content immutability under DELETE.** For every transition `Σ → Σ'` arising from DEL[d, σ]:

`dom(C') = dom(C)  ∧  (A a ∈ dom(C) :: C'(a) = C(a))`

*Justification.* Direct from the frame clause of D0. The operation specification names `M(d)` as its only modified component; `C` is not mentioned in the effect, so the equality `C' = C` is structural. ∎

D2 is a strict equality, not merely the monotonic `dom(C) ⊆ dom(C')` of P0 (which would permit growth). DELETE does not grow `C` — it does not allocate, modify, or remove content. Every I-address that was bound to a value before the operation remains bound to the same value after.

The architectural significance is precisely the contrast with destructive replacement. In a system where editing a document overwrites the bytes that were there, the bytes are *gone* — recoverable only from external logs. In Xanadu, the bytes are not gone. They are still in `dom(C)`, addressable by their original I-address. What has changed is only the arrangement that references them. Several downstream guarantees flow from D2:

- **The deleted content remains addressable.** Any I-address `a` that appeared in `ran(M(d))` before DELETE remains in `dom(C')`. A consumer that holds `a` — a link's endset, an external record, another document's arrangement — can still retrieve `C'(a) = C(a)`.

- **Prior versions of `d` can be reconstructed.** Reconstructing the pre-DELETE arrangement requires only `M(d)` (which the system retains as a prior version, when versioning is in effect) and `C` (which is unchanged). The bytes needed for reconstruction are all still present.

- **No I-address space is reclaimed.** The architectural commitment to permanent addresses, expressed by `dom(C) ⊆ dom(C')` in P0, is strengthened by D2 to `dom(C) = dom(C')` for DELETE specifically. Reclamation would require a separate operation; DELETE itself does not provide one, and the design intent is that no such operation exists.

The cardinality consequence is that `|dom(C)|` is non-decreasing across all DELETE transitions. Combined with the cardinality non-decrease across allocation (K.α), the content store is monotonically non-decreasing across the entire transition vocabulary. The implication for resource accounting is intentional: storage is consumed at allocation and is never freed by deletion.

### Link store: the link graph is untouched

**D3 — Link store immutability under DELETE.** For every transition `Σ → Σ'` arising from DEL[d, σ]:

`dom(L') = dom(L)  ∧  (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`

*Justification.* Direct from the frame clause of D0. The operation specification names `M(d)` as its only modified component. ∎

D3 is the structural basis for what Nelson called *link survivability*. The architectural fact that supports it is the form of an endset: a set of well-formed spans, each given by a *start I-address* and an *ordinal length*. The endset has no V-stream coordinates anywhere in its structure. A link does not say "from position 47 of document A to position 92 of document B"; it says "from I-address range `[a, a ⊕ ℓ)` to I-address range `[b, b ⊕ m)`". When `M(d)` changes, the link is unaware.

We can be sharper about what D3 entails. Consider a link `ℓ ∈ dom(L)` and a slot `i`. The coverage `coverage(L(ℓ).eᵢ)` is the set of I-addresses that the slot references — defined by the spans in the endset, evaluated via the span semantics of ASN-0053. Coverage is a function of the endset alone; it depends on no part of state except `L(ℓ).eᵢ` itself. Under D3, `L'(ℓ).eᵢ = L(ℓ).eᵢ`, so `coverage(L'(ℓ).eᵢ) = coverage(L(ℓ).eᵢ)`. Whatever I-addresses the link referenced before DELETE, it references after.

What changes is *discoverability* — the property of being projectable into a document's current arrangement. The projection

`project(L(ℓ).eᵢ, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(L(ℓ).eᵢ)}`

depends on `M(d)`. After DELETE, the projection can lose elements: V-positions in `X` (the deleted span) that referenced I-addresses in the coverage are removed from `dom(M'(d))`, and so removed from the projection. V-positions in `Ρ` are renamed by `σ_d` and reappear in the projection at their new V-positions. V-positions in `Λ` are unchanged.

The link itself is intact. Its discoverability from `d` may shrink. Its discoverability from other documents `d' ≠ d` is unchanged (by the frame condition on other arrangements; see D5). And — crucially — its discoverability can be *restored* by a subsequent operation that reintroduces a V-position mapping to an I-address in the coverage. The link is not erased; it is, at worst, temporarily without a witnessing arrangement entry.

This pattern of "structural persistence with conditional visibility" is the architectural pattern that DELETE establishes. It is the same pattern by which content survives deletion: the bytes persist in `C`, even if no `M(d)(v)` currently references them. The link case is the natural extension of the content case to the second store.

### Document identity: the document is not destroyed

**D4 — Document identity persistence under DELETE.** For every transition `Σ → Σ'` arising from DEL[d, σ]:

`d ∈ dom(M')  ∧  dom(M') = dom(M)`

*Justification.* The frame clause of D0 states `dom(M') = dom(M)`. Since `d ∈ dom(M)` by the precondition of DEL, `d ∈ dom(M')` follows. ∎

D4 is the abstract analogue of Nelson's *evolving braid*. The document `d` is not a snapshot but a trajectory through arrangement-space; DELETE modifies the current point of the trajectory without altering which trajectory it is. The document's tumbler address `d` — which serves both as its identifier and as the prefix of every address allocated under it — is unchanged.

The contrast is with a distinct operation that would create a new document by forking: such an operation appears in the foundations as the depth-1 child case of K.δ, producing `d' = inc(d, 1)` with `d' ≠ d`. DELETE does no such thing. The post-state arrangement `M'(d)` is bound to the same `d` as the pre-state arrangement `M(d)`. References to `d` — by name, by external citation, by another document's transclusion — remain valid and point to the same trajectory, now at a different state.

A subtle consequence: D4 binds `d`'s allocator chains as well. The substrate associates `d` with content sub-allocator `A_C(d)` and link sub-allocator `A_L(d)`; these chains are functions of `d`, not of `d`'s arrangement state. After DELETE, the next address emitted by `A_C(d)` is still determined by the prior maximum of `{a' ∈ dom(C) : origin(a') = d}`, which is unchanged by DELETE (because `dom(C)` is unchanged by D2). The deletion of arrangement entries does not free up positions in the allocator chain. New content allocated to `d` after DELETE continues to receive fresh, monotonically advancing I-addresses.

### Cross-document isolation

**D5 — Cross-document arrangement isolation under DELETE.** For every transition `Σ → Σ'` arising from DEL[d, σ]:

`(A d' ∈ dom(M) : d' ≠ d :: M'(d') = M(d'))`

*Justification.* Direct from the frame clause of D0. ∎

D5 is the deepest of the structural commitments because it is the one that makes transclusion safe. If two documents `d` and `d'` reference the same I-address `a` — either because `d'` was forked from `d`, or because their arrangements were independently populated to share content — then they hold V-positions whose images coincide. The pre-DELETE condition

`(E v ∈ dom(M(d)) :: M(d)(v) = a)  ∧  (E v' ∈ dom(M(d')) :: M(d')(v') = a)`

may transition under DEL[d, σ] to a post-state where the first conjunct fails (if `a` was removed from the projection of `M(d)` over the deleted span). The second conjunct is unaffected. From `d'`'s view, `a` is still present: still in `ran(M'(d'))` (because `M'(d') = M(d')` by D5), still in `dom(C')` (by D2). The content remains visible in `d'` as it was before.

This is the property that distinguishes Xanadu transclusion from copy-and-paste. In copy-and-paste, the shared bytes are duplicated; each copy lives independently, and deletion from one is structurally independent of the other only because they were never linked. In Xanadu transclusion, the I-addresses *are* shared; deletion from one document's arrangement is structurally independent of the other only because of D5.

Without D5, a deletion in `d` would have to either:
- propagate to every document that shares the deleted content (violating the autonomy of `d'`'s owner), or
- prevent the deletion (because some other document depends on the content), or
- somehow allow the deletion to be "local" while leaving global effects.

D5 chooses the third option, and the structural separation between Istream (shared, immutable) and Vstream (per-document, mutable) is what makes it coherent. `d` modifies its own Vstream; `d'`'s Vstream is unaffected; the shared Istream is unchanged. Each document gets a different "view" of the same persistent content; deletion changes the view, not the content.

### Subspace isolation within a document

**D6 — Subspace isolation under DELETE.** For every transition `Σ → Σ'` arising from DEL[d, σ] with `S = subspace(s)`:

`(A S' ∈ {s_C, s_L} : S' ≠ S :: V_{S'}(M'(d)) = V_{S'}(d)  ∧  (A v ∈ V_{S'}(d) :: M'(d)(v) = M(d)(v)))`

*Justification.* The effect clauses of D0 state that the post-state agrees with the pre-state on every V-position in subspaces other than `S`. ∎

D6 is the within-document analogue of D5. A document carries (in the working framework) two parallel sequences of V-positions — one in the content subspace, one in the link subspace. The two subspaces share the document `d` but are otherwise independent: their V-positions live at disjoint addresses (different first components), their depths can differ, their contents address disjoint stores. DELETE in one subspace must not perturb the other.

The implementation evidence reinforces this from an unexpected angle. Gregory's `tumblersub` uses an exponent-guarded subtraction: when the width's exponent is finer than a crum's V-displacement exponent, the subtraction is a no-op. Because text and link addresses sit at different exponents in the tree representation, the exponent guard *coincidentally* protects the unrelated subspace from being shifted by a deletion in the other. This is a happy accident at the implementation level — the abstract specification requires subspace isolation as a frame condition, but the tree implementation happens to deliver it through ordinary arithmetic rather than through a special-case check.

The opposite direction of isolation (deletion in the link subspace not perturbing the content subspace) is also required by D6 but is delivered by a different implementation mechanism in Gregory's code: positional ordering puts text addresses entirely below link addresses, so a link-subspace deletion's classification routine simply classifies every text crum as "before the deletion" and skips it. Two unrelated mechanisms — arithmetic short-circuit and positional ordering — converge on the same abstract guarantee. The abstract specification does not care which mechanism is used; it requires only the guarantee itself.

### Attribution survival

**D7 — Attribution survival under DELETE.** For every transition `Σ → Σ'` arising from DEL[d, σ] and every I-address `a` that appeared in `ran(M(d))` before the operation:

`a ∈ dom(C') ∪ dom(L')  ∧  origin(a) at Σ' = origin(a) at Σ`

Equivalently, restricted by subspace: when `subspace_I(a) = s_C`, `a ∈ dom(C')`; when `subspace_I(a) = s_L`, `a ∈ dom(L')`. By L14 (store disjointness), these are mutually exclusive.

*Justification.* The pre-condition `a ∈ ran(M(d))` together with S3★ at the pre-state gives `a ∈ dom(C) ∪ dom(L)`, with the partition determined by S3★: a content-subspace V-position maps into `dom(C)`, a link-subspace V-position maps into `dom(L)`. By D2 and D3, both stores are unchanged: `dom(C') = dom(C)` and `dom(L') = dom(L)`. So `a` remains in `dom(C') ∪ dom(L')` with the same subspace classification. The origin function `origin(a)` is a structural projection of `a` (specifically, the document-level prefix of `a`'s tumbler under T4-parsing), and depends only on `a`'s components, not on any state component. So `origin(a)` is unchanged across the transition. ∎

D7 is what Nelson called the structural anchor of attribution. Attribution is not a metadata field that DELETE could accidentally strip; it is encoded *in the address itself*. The I-address `a = [d_0, 0, s_C, k]` has `d_0` as the document-level prefix, identifying the document `d_0` that allocated `a`. No operation can change `d_0` without changing `a`, and no operation removes `a`. So no operation can sever the connection between `a` and `d_0`.

D7's significance is that authorship survives in a form that cannot be tampered with by editing operations. A document that transcluded a paragraph from another author still references the original author's I-addresses after the transcluding document deletes the paragraph from its arrangement. The author's name is implicit in every I-address that ever bore the paragraph's bytes, and DELETE does not touch those I-addresses. A reader who later reconstructs the deletion's history can trace the deleted I-addresses to their allocating document and identify the original author by structural means alone — no external registry, no metadata table, no signature scheme.

We should be careful what D7 does *not* claim. It does not claim that the deleted content's *attribution* is visible in the post-DELETE arrangement — manifestly, the V-positions are gone. What survives is the attribution *of the underlying I-addresses*, which remain in `dom(C')`. Any process that holds (or can rediscover) those I-addresses can read off attribution. The mechanisms by which a post-DELETE reader might rediscover them (historical backtrack, version comparison, transclusion in other documents) are downstream features that depend on additional state components beyond what DELETE itself maintains.

### Well-formedness preservation

**D8 — Arrangement well-formedness preservation under DELETE.** For every transition `Σ → Σ'` arising from DEL[d, σ], the post-state satisfies every foundation invariant that the pre-state was required to satisfy. The invariants partition into three groups by the mechanism that preserves them.

*Group (i): Arrangement invariants on the modified document `d`.* The post-state arrangement `M'(d)` satisfies:

- *Functionality (S2):* `M'(d)` is a well-defined partial function.
- *Finite domain (S8-fin):* `|dom(M'(d))| < ∞`.
- *Well-formed V-positions (S8a):* `(A v ∈ dom(M'(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`.
- *Per-subspace common depth (S8-depth):* within each subspace, all V-positions share a common depth.
- *Referential integrity (S3★):* `(A v ∈ dom(M'(d)) :: (subspace(v) = s_C ⟹ M'(d)(v) ∈ dom(C')) ∧ (subspace(v) = s_L ⟹ M'(d)(v) ∈ dom(L')))`.
- *Per-subspace contiguity, minimum, sequentiality (D-CTG★, D-MIN★, D-SEQ★):* `V_S(M'(d)) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S − n}` for the affected subspace; unchanged for the other. When `n_S − n = 0`, all three predicates hold vacuously for subspace `S`.
- *Per-subspace span decomposition (S8★):* the per-subspace arrangement decomposes into finite correspondence runs.
- *Subspace exhaustiveness (S3★-aux):* every V-position lies in `s_C` or `s_L`.
- *Link-subspace ownership (CL-OWN):* every link-subspace V-position maps to a link with `origin = d`.
- *Link-subspace position uniqueness (CL-UNIQ):* the link-subspace restriction is injective.

*Group (ii): Allocation and store invariants.* All of M0, S4, S7a, S7b, S7c, S7d, C1, C1b, C1c, C2, L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, C-fin, NodeLineage (ASN-0036, ASN-0043, ASN-0093) hold trivially at the post-state because `C' = C`, `L' = L`, `E' = E`, and `dom(M') = dom(M)` by D0's frame — every clause of every invariant in this group is a predicate over one or more of these components, and equality of each component pointwise propagates the predicate from `Σ` to `Σ'`. M0 (DocumentTumblerWellFormed, ASN-0093) ranges over `dom(M)`, which is unchanged by D0's frame, so each post-state `d' ∈ dom(M')` inherits its pre-state T4-validity and `zeros = 2` directly. C1, C1b, C1c, C2 (ASN-0093) range over `dom(C)`, with C2 additionally over `dom(M)`; both are pointwise preserved by `dom(C') = dom(C)` and `dom(M') = dom(M)`. S4 (OriginBasedIdentity, ASN-0036) is a predicate over allocation events under T10a: distinct allocation events produce distinct addresses. DEL introduces no new allocation events, and `dom(C') = dom(C)` by D2, so the set of allocation-event addresses is unchanged across the transition; S4 carries to `Σ'` pointwise.

*Group (iii): Transition and per-state invariants discharged by frame.* The group mixes transition predicates (which compare `Σ` and `Σ'`) with per-state predicates (which range over a single state); both kinds reduce to triviality under D0's frame because the components they predicate over — `(C, L, E, R, dom(M))` — are pointwise unchanged. Members: M1 (arrangement monotonicity, ASN-0093), C0 (content immutability, ASN-0093), P0, P1, P2, P3 (permanence and arrangement-mutability-only), P4★, P4a (provenance bounds and historical fidelity), P6, P7, P7a (existence and grounding), P8 (entity hierarchy), and L12a, L12b (link-store monotonicity and home persistence). Each is preserved trivially: M1 by `dom(M') = dom(M)` (which entails `dom(M) ⊆ dom(M')` vacuously); C0 by `dom(C') = dom(C)` together with the value-preservation conjunct of D2; P0 by `dom(C') = dom(C)`; P1 by `E' = E`; P2 by `R' = R`; P3 as the conjunction of P0, P1, P2 plus L12; P4★ by the conjunction `R' = R` and `Contains_C(Σ') ⊆ Contains_C(Σ)` (DELETE can only shrink the content-subspace range, so historical containment is preserved); P4a by `R' = R` combined with the fact that any pair `(a, d) ∈ R` was witnessed at some `Σ_k` in the pre-state history, which remains in the post-state history; P6, P7, P7a, P8 by `dom(C') = dom(C)`, `dom(L') = dom(L)`, `E' = E`, `R' = R`, and the structural definition of `origin`; L12a, L12b similarly.

*Justification (Group (i)).* By D1, `V_S(M'(d))` has the stated form `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S − n}` (or `∅` when `n_S = n`), so D-CTG★, D-MIN★, D-SEQ★ hold (vacuously when empty, as noted). By D6, the other subspace is unchanged, inheriting D-CTG★, D-MIN★, D-SEQ★ from the pre-state. S8-depth at the post-state holds because all positions in `V_S(M'(d))` have depth `m_S`: positions in `Λ` inherit depth `m_S` from the pre-state; positions `u = σ_d(v) ∈ Q` satisfy `shift(u, n) = v` by definition, and `#u = #shift(u, n) = #v = m_S` by OrdinalShift's length-preservation postcondition (`#shift(u, n) = #u`). S8a holds at each post-state position: positions in `Λ` satisfy S8a directly; positions in `Q` have the form `[S, 1, ..., 1, k − n]` with `1 ≤ k − n ≤ n_S − n` (derived in D0's effect by construction), satisfying `zeros = 0`, `#v = m_S ≥ 2`, all components positive (since `S ≥ 1` and `k − n ≥ 1`). S8-fin holds because `|dom(M'(d))| ≤ |dom(M(d))|` (positions in `X` are removed; positions in `Ρ` are bijected by `σ_d` and so preserved in count; positions in `Λ` are unchanged). S2 holds by the construction of `M'(d)`: the disjoint sources `Λ`, `Q`, and `V_{S'}(d)` for `S' ≠ S` each provide a single value for each position, and they cover disjoint subsets of the post-state domain.

The remaining four invariants — S3★, S3★-aux, S8★, CL-OWN, CL-UNIQ — require care because at positions where `Q ∩ X ≠ ∅` (which can occur whenever `n_S ≥ p + n`), a pre-state V-position that "survives" into `dom(M'(d))` may carry a different I-address in the post-state than it did in the pre-state. Concretely, at a position `v ∈ Q ∩ X` (for example, with `V_S(d) = {[S, 1, k] : 1 ≤ k ≤ 10}`, `s = [S, 1, 2]`, `n = 2`: the post-state `[S, 1, 2] ∈ Q` carries `M(d)([S, 1, 4])`, not `M(d)([S, 1, 2])`), the I-address is genuinely re-mapped. We argue these invariants by a *source correspondence*: each post-state V-position `v ∈ dom(M'(d))` has `M'(d)(v) = M(d)(u)` for a unique pre-state V-position `u ∈ dom(M(d))` — `u = v` when `v ∈ Λ`, `u = σ_d^{-1}(v) ∈ Ρ` when `v ∈ Q`, and `u = v` when `v ∈ V_{S'}(d)` for `S' ≠ S`. In all three cases `subspace(v) = subspace(u)`: the shift `σ_d` modifies only the last component (by D1's structural form `σ_d([S, 1, ..., 1, k]) = [S, 1, ..., 1, k − n]`), preserving the first.

S3★ holds via source correspondence: pre-state S3★ on `u` gives `M(d)(u) ∈ dom(C)` when `subspace(u) = s_C` and `M(d)(u) ∈ dom(L)` when `subspace(u) = s_L`; D2 and D3 give `dom(C') = dom(C)` and `dom(L') = dom(L)`; so `M'(d)(v) = M(d)(u)` lies in the correct post-state store. S3★-aux holds because `subspace(v) = subspace(u) ∈ {s_C, s_L}` by pre-state S3★-aux on `u`. S8★ holds at the post-state by the trivial singleton decomposition `{(v, M'(d)(v), 1) : v ∈ V_S(M'(d))}` for the affected subspace — S8-fin establishes finiteness, S8's condition (a) holds by construction (each post-state V-position is its own length-1 run), and condition (b) holds vacuously at length 1 — and by D6 (inheritance from the unchanged pre-state arrangement) for the other subspace.

CL-OWN: when `S ≠ s_L`, `V_{s_L}(M'(d)) = V_{s_L}(d)` and `M'(d)|_{V_{s_L}(M'(d))} = M(d)|_{V_{s_L}(d)}` by D6, transferring pre-state CL-OWN directly. When `S = s_L`, each `v ∈ V_{s_L}(M'(d)) = Λ ∪ Q` has `M'(d)(v) = M(d)(u)` for the source `u ∈ Λ ⊎ Ρ ⊆ V_{s_L}(d)`, and pre-state CL-OWN on `u` gives `origin(M(d)(u)) = d`. The re-mapping at positions in `Q ∩ X` does not break CL-OWN because the new I-address at such a position is still a pre-state value from `V_{s_L}(d)`, whose images all have `origin = d` by pre-state CL-OWN.

CL-UNIQ: when `S ≠ s_L`, the post-state link-subspace restriction equals the pre-state one (by D6) and inherits injectivity directly. When `S = s_L`, the post-state restriction `M'(d)|_{Λ ∪ Q}` is injective by three observations. (i) `Λ ∩ Ρ = ∅` by construction: `Λ`-positions have last component `≤ p − 1`, `Ρ`-positions have last component `≥ p + n > p − 1`; so by pre-state CL-UNIQ on `Λ ⊎ Ρ ⊆ V_{s_L}(d)`, the values `M(d)|_Λ` and `M(d)|_Ρ` are themselves injective and their image sets `M(d)(Λ)` and `M(d)(Ρ)` are disjoint. (ii) `M'(d)|_Λ = M(d)|_Λ` is therefore injective with image `M(d)(Λ)`. (iii) `M'(d) ∘ σ_d = M(d)|_Ρ` on `Ρ`; since `σ_d : Ρ → Q` is a bijection (D1), `M'(d)|_Q` is injective on `Q` with image `M(d)(Ρ)`. The images `M'(d)(Λ) = M(d)(Λ)` and `M'(d)(Q) = M(d)(Ρ)` are disjoint by (i), so the full post-state restriction `M'(d)|_{Λ ∪ Q}` is injective.

*Justification (Groups (ii) and (iii)).* By the frame argument outlined in each group's description above. The key uniform observation: every invariant in these groups is either (a) a predicate over `(C, L, E, R, dom(M))`, each of which is pointwise preserved by D0's frame; or (b) a transition predicate that compares pre- and post-state values of these same components, and so reduces to the equality case under D0's frame. ∎

The well-formedness preservation is what closes the loop: DELETE is not just a local edit; it is a transition between two states each of which satisfies the global invariants. A reader of the post-state sees a coherent document, indistinguishable from one whose V-positions had been allocated in their post-DELETE form from the start. The pre-state knowledge of which positions were deleted — and where the gap was — is not present in `M'(d)` at all. It can be recovered, if at all, only from external state (a versioning system, a comparison with an earlier `M(d)`).

## Link discoverability: the projection picture

The conjunction of D2, D3, D5, and D6 establishes that DELETE is, from the link store's viewpoint, an arrangement-only operation: link values are unchanged, coverage is unchanged, only the projection into the affected document's affected subspace is altered. We can characterise the alteration precisely. Let `ℓ ∈ dom(L)` and let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ_σ)`, removing span `(s, ℓ_σ)` from subspace `S` of `d`. For each slot `i` of `ℓ`:

- *Projection into `d`'s shifted subspace.* The post-state projection in subspace `S` of `d` is composed of two contributions: the unshifted contribution from `Λ` (positions before the deleted region whose mapped I-address is in the coverage) and the shifted contribution from `Ρ` (positions after the deleted region, renamed by `σ_d`). The positions in `X` (within the deleted region) that referenced coverage I-addresses are removed from the projection.

- *Projection into `d`'s other subspace.* Unchanged, by D6.

- *Projection into any other document `d'`.* Unchanged, by D5.

We extract this as an abstract characterisation:

**D9 — Link projection under DELETE.** For every link `ℓ ∈ dom(L)`, every slot `i`, every DEL[d, σ] transition `Σ → Σ'`, and every document `d''`:

- If `d'' ≠ d`: `project(L'(ℓ).eᵢ, d'', Σ') = project(L(ℓ).eᵢ, d'', Σ)`.
- If `d'' = d`, restricted to subspace `S' ≠ S`: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_{S'}(M'(d)) = project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d)`.
- If `d'' = d`, restricted to subspace `S`: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_S(M'(d)) = (project(L(ℓ).eᵢ, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Ρ}`. Here `Λ`, `X`, `Ρ ⊆ V_S(d)` are the subspace-`S` regions defined in D0; the intersection of the pre-state projection with each region is therefore a subset of `V_S(d)`, well-formed by construction.

*Justification.* For `d'' ≠ d`: `M'(d'') = M(d'')` by D5 and `coverage(L'(ℓ).eᵢ) = coverage(L(ℓ).eᵢ)` by D3, so the projection's defining set is unchanged. For `d'' = d` in subspace `S' ≠ S`: `M'(d)` agrees with `M(d)` on `V_{S'}(d)` by D6 (with the same domain and values), and `coverage(L'(ℓ).eᵢ) = coverage(L(ℓ).eᵢ)` by D3, so the projection's defining set is unchanged. For `d'' = d` restricted to subspace `S`: the post-state V-positions in subspace `S` partition as `Λ ⊎ Q`, with `Q = σ_d(Ρ)`. The post-state projection in subspace `S` contains a position `v ∈ Λ` iff `M'(d)(v) = M(d)(v) ∈ coverage(L'(ℓ).eᵢ) = coverage(L(ℓ).eᵢ)` (the latter equality by D3); these positions are exactly `project(L(ℓ).eᵢ, d, Σ) ∩ Λ`. The post-state projection in subspace `S` contains a position `σ_d(v)` for `v ∈ Ρ` iff `M'(d)(σ_d(v)) = M(d)(v) ∈ coverage(L(ℓ).eᵢ)`; these positions are exactly `{σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Ρ}`. The pre-state projection's intersections with `Λ` and with `Ρ` are well-defined: although `project(L(ℓ).eᵢ, d, Σ)` ranges over all of `dom(M(d))`, intersecting with `Λ ⊆ V_S(d)` or `Ρ ⊆ V_S(d)` automatically restricts to subspace `S`. ∎

D9 makes precise what *can* and *cannot* happen to a link's discoverability under DELETE. Discoverability from any document other than `d` is invariant. Discoverability from `d`'s other subspace is invariant. Discoverability from `d`'s affected subspace can shrink (when V-positions in the deleted span referenced the link's coverage) or rename (when V-positions in the shifted region referenced the link's coverage). The latter is invisible from outside — the projection has the same cardinality, just relocated.

The cardinality can shrink to zero. A link whose coverage was referenced only by V-positions in the deleted span becomes — temporarily — not discoverable from `d`. This is the "orphan" or "ghost" condition discussed in the link projection foundations. The orphan condition is reversible: a subsequent operation that adds a V-position in `d` mapping to an I-address in the link's coverage restores discoverability. The link itself is never lost.

## ValidComposite★ extension under DELETE

DEL must take its place as a first-class member of the foundation's elementary transition vocabulary if downstream specifications are to invoke "DEL in a ValidComposite★ chain" without further apparatus. We record the extension as a named claim.

**D10 — ValidComposite★ extension under DELETE.** ASN-0047's ValidComposite★ is extended to admit DEL as an elementary transition. A composite transition `Σ →* Σ'` is *valid* iff it is a finite sequence of atomic transitions

`Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'`

drawn from the extended vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ, DEL}`, satisfying:

(1) *Transition preconditions.* Each step `Σᵢ → Σᵢ₊₁` satisfies the elementary precondition of its transition kind, evaluated at `Σᵢ`. For a DEL step, this is D0's precondition.

(2) *Coupling constraints.* J0, J1★, and J1'★ (ASN-0047) hold between `Σ` and `Σ'` for the composite as a whole.

At any DEL step in such a sequence, J0, J1★, and J1'★ hold *vacuously*:

- *J0 (AllocationRequiresPlacement)* quantifies over `a ∈ dom(C') \ dom(C)`. By D2, `dom(C') = dom(C)`, so `dom(C') \ dom(C) = ∅` and the implication is vacuous at the DEL step.
- *J1★ (ExtensionRecordsProvenanceContentSubspace)* quantifies over pairs `(a, d)` for which some `v ∈ dom(M'(d))` has `subspace(v) = s_C` and `M'(d)(v) = a`, while no such `v` existed in `dom(M(d))`. By D0's effect, every post-state content-subspace V-position `v` either lies in `Λ` (so `M'(d)(v) = M(d)(v)`, and the pre-state V-position `v` itself witnesses the same I-address) or has the form `σ_d(u)` for some `u ∈ Ρ` (so `M'(d)(σ_d(u)) = M(d)(u)`, and the pre-state V-position `u` witnesses the same I-address). The antecedent — "no `v ∈ dom(M(d))` with subspace `s_C` mapped to `a`" — is therefore false for every `(a, d)` pair at a DEL step. The implication is vacuous.
- *J1'★ (ProvenanceRequiresExtensionContentSubspace)* quantifies over `(a, d) ∈ R' \ R`. By D0's frame, `R' = R`, so `R' \ R = ∅` and the implication is vacuous.

*Consequence.* DEL can be freely interleaved with any other elementary transitions in a ValidComposite★ chain without imposing additional coupling obligations on the composite. The composite's J0/J1★/J1'★ proofs reduce, at each DEL step, to the trivial vacuity arguments above; nontrivial coupling obligations are confined to the K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, and K.ρ steps that *do* introduce new content, new entities, new links, new V-positions, or new provenance pairs.

## A note on recoverability and historical reconstruction

Nelson's design intent goes beyond "DELETE doesn't destroy" to a stronger claim: that any prior arrangement of `d` — including the deleted V-span's positional layout — should remain reconstructible. The relevant evidence:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

This claim concerns the *system as a whole*, not the DELETE operation in isolation. DELETE alone does not provide the prior state — it produces a transition from `Σ` to `Σ'`, and the post-state `Σ'` does not, by itself, contain `M(d)` as it was at `Σ`. What DELETE does is not *destroy* the information needed for reconstruction. The information is held in two places:

- **Content.** Every I-address that was in `ran(M(d))` is in `dom(C')` (by D2). The bytes needed to reproduce the deleted content are present.
- **Prior arrangements.** The pre-state arrangement `M(d)` is whatever the system of *versions* retains. A version is, in the working framework, a separately addressed document `d_v = inc(d, 1)` — the depth-1 child case of K.δ (ASN-0047) — populated by the J4 ForkComposite (ASN-0047). K.δ alone places `d_v` in `dom(M)` with an empty arrangement (`M'(d_v) = ∅` per K.δ's effect for the IsDocument case); the J4 composite then uses K.μ⁺ to populate `d_v`'s content-subspace arrangement from `ran(M(d)|_{V_{s_C}(d)})` under transclusion (no new content addresses are introduced) and K.ρ to record provenance for each placed I-address. K.δ alone is *not* what establishes "match at a point in time"; the J4 ForkComposite is. If the ForkComposite was applied before DELETE, the resulting arrangement `M(d_v)` retains the pre-DELETE layout of `d`'s content subspace, including the V→I mappings that DELETE later removed from `M(d)`. By D5, DELETE on `d` leaves `M(d_v)` untouched.

The combination of D2 and D5 thus makes recoverability *possible*, conditional on the system having applied the J4 ForkComposite (or some equivalent composite) before the DELETE. The pre-DELETE content arrangement of `d` is exactly `M(d_v)` for any version `d_v` forked from `d` at the pre-DELETE state — and that arrangement is preserved across the DELETE on `d`. The bytes referenced by that arrangement are still in `dom(C')`. Reconstruction follows. "Versioning" in the broader sense — full historical reconstruction of arbitrary prior states — is a multi-step composite mechanism outside DEL's scope; DEL contributes only the non-destruction guarantees that make such reconstruction structurally possible.

DELETE is *necessary* for this picture: without the architectural commitment that DELETE only removes V-positions (rather than C entries or L entries or other documents' arrangements), the prior arrangement would not be reconstructible from any combination of post-state components. The system's recoverability property depends on DELETE's preservation properties.

DELETE is *not sufficient*: without versions, the pre-state of `d` itself is not preserved. The post-state has only `M'(d)`, which is the post-DELETE arrangement. Recovering `M(d)` from `M'(d)` alone is not possible — DELETE is information-destroying with respect to the current arrangement of `d`.

The conclusion is that DELETE supplies the *substrate* for recoverability — non-destruction of content, isolation across documents — without supplying the *mechanism* (which is versioning). This division of labour is structural. The DELETE operation is simpler than recoverable-DELETE would have to be; the versioning mechanism is independent of the DELETE operation; both contribute to the system-level guarantee.

## Boundaries the abstract specification does not cross

Three patterns of implementation behaviour observed in the udanax-green system represent failures or limitations relative to the abstract specification. We name them to make clear that the abstract specification does not adopt them as features:

- **Stale auxiliary indices.** In the studied implementation, a global index of "documents containing I-address" is updated when content is placed into a document's arrangement, but not when it is removed by DELETE. The result is that `find_documents_containing(a)` may return documents whose arrangements no longer contain `a` after a deletion. The abstract specification does not include this index; D2 + D5 supply the underlying truth (`a ∈ dom(C')` and `M'(d') = M(d')` for unaffected documents), from which a correct index can be derived. Implementations may, but are not required to, maintain such an index.

- **Permanent tree height.** The studied implementation grows its tree representation as the arrangement grows but does not shrink the representation when arrangement entries are removed. After DELETE empties an arrangement, the tree retains its growth-induced height with no leaf nodes. The abstract specification has no notion of "tree" and so no notion of "tree height"; the post-state arrangement is fully characterised by `M'(d)` as a partial function. Implementations are free to choose any representation that supports the operation's effect and frame.

- **No enumeration of orphaned I-addresses.** The studied implementation provides no operation by which a client can enumerate I-addresses currently absent from every arrangement. The abstract specification is silent on this — D2 establishes that orphaned I-addresses persist in `dom(C')`, but offers no operation to discover them. Implementations may, but are not required to, provide such an enumeration. The abstract operation set treats orphaned I-addresses as a feature (content survives independent of arrangement), not a bug to be papered over by enumeration support.

These observations clarify the scope of the abstract specification. DELETE's preservation guarantees are about state components named in the operation specification. Auxiliary indices, representation choices, and discovery operations are downstream concerns.

## Closing observations

The DELETE operation is small in its effect — a single document's arrangement loses some entries and renumbers others — but large in its commitments. The five preservation claims (content, links, document identity, other documents, other subspaces) and the two derived claims (attribution, well-formedness) jointly establish that DELETE is *not* the operation it appears to be in conventional systems. It is not destruction; it is not bytewise erasure; it is not a forking event that produces a new document. It is the modification of one component of one document's state, with everything else held invariant by frame condition.

The breadth of the frame is the design choice. Any one of the preservation claims could have been negotiated away: a system could erase deleted bytes (sacrificing D2 for storage reclamation); a system could break links to deleted addresses (sacrificing D3 for link-graph "cleanliness"); a system could propagate deletions across transclusions (sacrificing D5 for global consistency); a system could give the post-DELETE document a new identity (sacrificing D4 for explicit version branching). None of these would be wrong in the abstract; each represents a different architectural philosophy. The choice to preserve all five jointly is Xanadu's.

The five-fold preservation has a unifying theme. Each of the preserved components carries information that *some other party* — another document, another reader, another moment in time — might depend on. The owner of `d` has the authority to modify `d`'s arrangement; the owner does not have the authority to modify the bytes that other documents transclude, the links that other parties have created, the identity by which external citations name `d`, the unrelated subspace within `d`'s own state, or the arrangement of any other document. DELETE respects this separation of authority by not crossing any of these boundaries.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| D0 | Operation DEL[d, σ] specification: preconditions, effect (per-subspace shift `σ_d` with domain `Λ ∪ Q ∪ V_{S'}`), frame (`C' = C`, `L' = L`, `E' = E`, `R' = R`, `dom(M') = dom(M)`, `M'(d') = M(d')` for `d' ≠ d`). DEL is a new atomic transition kind extending ASN-0047's transition vocabulary. | introduced |
| D1 | Gap closure: post-state `V_S(M'(d)) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S − n}` when non-empty (and `∅` otherwise), shift bijection `σ_d` order-preserving from `Ρ` to `Q`. Justified by TS1 (ShiftOrderPreservation, ASN-0034) and TS2 (ShiftInjectivity, ASN-0034) on the shift-inverse construction — the natural generalisation of ASN-0082's D-BJ from `m = 2` to arbitrary `m_S ≥ 2`. | introduced |
| D2 | Content immutability under DELETE: `dom(C') = dom(C)` and `(A a ∈ dom(C) :: C'(a) = C(a))` | introduced |
| D3 | Link store immutability under DELETE: `dom(L') = dom(L)` and `(A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))` | introduced |
| D4 | Document identity persistence under DELETE: `d ∈ dom(M')` and `dom(M') = dom(M)` | introduced |
| D5 | Cross-document arrangement isolation under DELETE: `(A d' ∈ dom(M) : d' ≠ d :: M'(d') = M(d'))` | introduced |
| D6 | Subspace isolation under DELETE: other subspaces of `d` preserve domain and values across the transition | introduced |
| D7 | Attribution survival under DELETE: I-addresses in `ran(M(d))` persist in `dom(C') ∪ dom(L')` (partitioned by subspace) with unchanged `origin` | introduced |
| D8 | Arrangement well-formedness preservation: all foundation invariants — Group (i) arrangement invariants (S2, S8-fin, S8a, S8-depth, S3★, S3★-aux, D-CTG★, D-MIN★, D-SEQ★, S8★, CL-OWN, CL-UNIQ), Group (ii) allocation/store invariants (M0, S4, S7a–d, C1, C1b, C1c, C2, L0, L1, L1a–c, L3, L12, L14, L-fin, C-fin, NodeLineage), Group (iii) transition and per-state invariants discharged by frame (M1, C0, P0, P1, P2, P3, P4★, P4a, P6, P7, P7a, P8, L12a, L12b) — all hold at the post-state | introduced |
| D9 | Link projection under DELETE: precise characterisation (restricted by subspace) of how `project(L(ℓ).eᵢ, d'', Σ')` relates to `project(L(ℓ).eᵢ, d'', Σ)` per document and subspace | introduced |
| D10 | ValidComposite★ extension under DELETE: ASN-0047's ValidComposite★ admits DEL as an elementary transition; J0, J1★, J1'★ hold vacuously at every DEL step | introduced |

## Open Questions

- What additional preservation guarantees, beyond D2 and D5, must the broader transition vocabulary supply so that any pre-DELETE arrangement of a document remains reconstructible from the post-DELETE state plus a versioning mechanism?

- Under what abstract conditions does DELETE followed by an insertion at the same V-position recover the pre-DELETE arrangement exactly, rather than merely producing an arrangement with the same domain?

- What invariant must hold across an empty-arrangement state to ensure that subsequent insertion operations behave identically to insertion into a never-populated arrangement, given that DELETE can reduce a document's V-positions in a subspace to the empty set?

- When DELETE removes a span whose contents include I-addresses referenced by no link and by no other document's arrangement, what abstract obligation (if any) does the system have to make those I-addresses rediscoverable?

- What guarantee must the operation provide regarding *causal ordering* between DELETE on one document and DELETE on another transcluding document, given that D5 makes the two operations structurally independent but downstream observers may need to relate them?

- Under what condition on the post-DELETE arrangement does a subsequent operation observe a state indistinguishable from a state reached without the DELETE — that is, when is DELETE *fully reversible* relative to a given observer's view, even though it is information-destroying relative to the document's history?
