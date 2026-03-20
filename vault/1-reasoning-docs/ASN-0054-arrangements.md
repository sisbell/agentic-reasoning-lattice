# ASN-0054: Arrangements

*2026-03-19*

We are looking for the structural properties of a document's arrangement — the mapping from virtual positions to permanent content addresses. ASN-0036 introduced the arrangement Σ.M(d) as a partial function and proved a span decomposition exists (S8). But S8 only asserts that *some* decomposition into correspondence runs is possible; the degenerate case — one run per position — always works. We have not yet characterized the *shape* of the domain, nor asked whether there is a *canonical* decomposition. These are the questions for this note.

They matter because the arrangement is the only mutable component of document state. Content is permanent (S0). Entities are permanent (P1). Provenance is permanent (P2). Only M(d) changes as the document is edited. What we establish about the arrangement's structure constrains what editing can and cannot produce.

## The Text Domain

We restrict attention to the text subspace — the portion of the arrangement carrying content as opposed to link references.

**Definition.** The *text domain* of document d is V(d) = {v ∈ dom(Σ.M(d)) : v₁ = 1}, where v₁ denotes the first component of v. We restrict to the single subspace v₁ = 1 — the primary text subspace.

By S8a, every element of V(d) is a zero-free positive tumbler. Since all elements share v₁ = 1, S8-depth (which guarantees depth uniformity within a single subspace) gives a common tumbler depth we call L(d). By S8-fin, V(d) is finite. These three constraints leave the shape of V(d) underdetermined — a finite set of depth-L tumblers with positive components could be scattered across the text subspace. Can a document have positions at [1, 3] and [1, 7] but not [1, 5]?

Nelson's answer is unequivocal: no. The virtual byte stream is a *stream* — "logical addressing of the byte stream is in the form of virtual spans, or vspans" — with ordinal positions that run consecutively. INSERT shifts subsequent addresses forward; DELETE closes gaps. The V-stream is always dense and contiguous. There is no "deleted slot" in V-space; deletion removes positions and the remainder renumber.

The implementation evidence corroborates: `deletend` shifts all crums past the deletion point leftward by the deleted width; `makegappm` in `insertnd` shifts crums at or past the insertion point rightward by the inserted width. Both maintain contiguity by construction. The backend's `acceptablevsa` stub, which unconditionally accepts any V-address, is a validation omission rather than design intent. The specification-level invariant is clear.

**A0 (V-Domain Contiguity).** For every document d, V(d) is convex at depth L(d):

`(A v, u, w : u ∈ V(d) ∧ w ∈ V(d) ∧ u ≤ v ≤ w ∧ #v = L(d) : v ∈ V(d))`

The empty set is convex vacuously. A0 is a *composite-boundary invariant*: it holds in every state reachable by valid composite transitions, but may be temporarily violated at intermediate states within a composite. This distinguishes it from S2, S3, S8a, S8-depth, and S8-fin, which hold at every elementary transition (the arrangement invariants lemma preserves them by restriction for K.μ⁻, by precondition for K.μ⁺ and K.μ~, and by frame for the rest). Contiguity is not preserved by arbitrary restriction — a raw K.μ⁻ removing an interior V-position from a contiguous domain produces a non-contiguous domain. The formal mechanism: A0 is a *coupling constraint* on valid composite transitions, alongside J0, J1, and J1' (ASN-0047). Every valid composite must produce a post-state satisfying A0 for all documents. This resolves enforcement cleanly: A0 holds for all valid composites by definition — including Fork (J4) and any future composite operations — without requiring exhaustive per-operation preservation proofs. INSERT, for instance, first shifts positions rightward via K.μ~ (opening a gap in V(d)), then fills the gap via K.μ⁺; DELETE removes positions via K.μ⁻ and closes the gap via K.μ~ in the same composite. Intermediate states may violate A0, but the completed composite must restore it. The per-operation arguments in the sequel demonstrate that each specific operation *can* produce a post-state satisfying A0 — they are existence arguments showing the constraint is achievable, not the source of A0's authority.

This is the fundamental structural property of arrangements. Everything that follows depends on it.

## Fixed-Prefix Form

A0 combined with finiteness yields a surprisingly rigid shape.

**A1 (Fixed-Prefix Form).** If V(d) ≠ ∅, there exists a tumbler prefix p = [p₁, ..., p_{L-1}] and integers k_min, k_max with 1 ≤ k_min ≤ k_max such that:

`V(d) = {[p₁, ..., p_{L-1}, k] : k_min ≤ k ≤ k_max}`

and |V(d)| = k_max − k_min + 1.

*Proof.* Suppose V(d) contains positions u = [q₁, ..., q_{L-1}, j] and w = [r₁, ..., r_{L-1}, k] with [q₁, ..., q_{L-1}] < [r₁, ..., r_{L-1}] under T1. Then u < [q₁, ..., q_{L-1}, j+1] < [q₁, ..., q_{L-1}, j+2] < ⋯ is an infinite ascending chain of depth-L tumblers, all less than w (they share a prefix that is lexicographically smaller than w's prefix). By T0(a), components are unbounded, so this chain is genuinely infinite. By A0, every element of this chain at depth L(d) between u and w lies in V(d). But V(d) is finite (S8-fin). Contradiction.

So all positions in V(d) share the same prefix at the first L − 1 components. Among same-prefix depth-L tumblers [p, k], the T1 ordering reduces to the natural ordering on k. By A0, the set of k-values is convex among the naturals — an interval. By S8a, every component is strictly positive, so k_min ≥ 1. ∎

This result is strong: V(d) is completely characterized by a fixed tumbler prefix and a range of ordinals at the last component. The arrangement, restricted to V(d), becomes a function from the interval [k_min, k_max] to I-addresses.

**A1a (Depth Fixity).** While V(d) ≠ ∅, the depth L(d) is fixed: no valid composite transition can change it. This follows directly from S8-depth, which requires all V-positions in a subspace to share the same tumbler depth. Any operation that adds new V-positions to a non-empty V(d) must match the existing depth — otherwise S8-depth is violated in the post-state. Only after complete deletion (V(d) = ∅, L(d) undefined) and subsequent re-insertion can a different depth be established.

## Ordinal Enumeration

**Definition.** The *unit V-displacement* for depth L is the tumbler u_V = [0, ..., 0, 1] of length L (action point at position L, value 1).

By TumblerAdd, for any v = [p₁, ..., p_{L-1}, k]:

`v ⊕ u_V = [p₁, ..., p_{L-1}, k + 1]`

The successor preserves the prefix and increments the final component. We observe that no depth-L tumbler lies between v and v ⊕ u_V: any such tumbler would agree on the first L − 1 components (since both endpoints do) and have its L-th component strictly between k and k + 1, which is impossible for natural numbers.

**A2 (Ordinal Enumeration).** V(d) admits a unique enumeration v₀, v₁, ..., v_{n-1} where n = |V(d)|, v₀ = v_min, and:

`(A j : 0 ≤ j < n − 1 : v_{j+1} = v_j ⊕ u_V)`

In concrete terms: v_j = [p₁, ..., p_{L-1}, k_min + j]. The arrangement on V(d) is a finite sequence of I-addresses, indexed by ordinal position. We write M_j for M(d)(v_j) when the document is clear from context.

## I-Space Adjacency

To decompose this sequence into correspondence runs, we need a notion of when consecutive V-positions map to "consecutive" I-addresses — when the arrangement preserves ordinal progression across both spaces simultaneously.

I-addresses are element-level tumblers (S7b: zeros(a) = 3). Within a single allocating document, content bytes are assigned consecutive addresses by sequential allocation (T9). Two I-addresses are adjacent when one is the immediate element-level successor of the other.

**Definition.** For an I-address a of length m, the *unit I-displacement* is u_I(a) = [0, ..., 0, 1] of length m. We say a' is the *I-successor* of a, written a →_I a', when a' = a ⊕ u_I(a).

By TumblerAdd, I-succession preserves all components except the last: (a ⊕ u_I(a))_i = a_i for i < m. In particular, the document prefix that T4 parses from a is preserved, so origin(a ⊕ u_I(a)) = origin(a). I-adjacent addresses always share the same allocating document — a structural consequence of tumbler arithmetic, not a separate axiom.

**Observation.** If origin(a) ≠ origin(a'), or if #a ≠ #a', then a →_I a' cannot hold. I-adjacency requires shared origin and shared tumbler length.

## Breaks

**Definition (Break).** For j with 0 < j < n, position v_j is a *break* when M_{j-1} →_I M_j does not hold — that is, M_j ≠ M_{j-1} ⊕ u_I(M_{j-1}).

The formal predicate M_j ≠ M_{j-1} ⊕ u_I(M_{j-1}) is the exhaustive definition. Common circumstances that produce breaks include: the I-addresses at consecutive V-positions have different origins (different allocating documents, hence structurally non-adjacent); they have the same origin but different tumbler depths (#M_{j-1} ≠ #M_j, as when a document allocates through child allocators per T10a — by the result-length identity, the successor a ⊕ u_I(a) has length #a, so a length mismatch forces the break); or they share origin and depth but skip at least one element-field ordinal. The set of breaks B ⊆ {v₁, ..., v_{n-1}} is determined entirely by the arrangement function M(d).

## The Canonical Decomposition

**Definition (Maximal Correspondence Run).** A *maximal correspondence run* in V(d) is a maximal contiguous subsequence v_s, v_{s+1}, ..., v_{s+r-1} (with r ≥ 1) such that no position v_{s+1}, ..., v_{s+r-1} is a break. We write each run as R = (v_s, a_s, r) where a_s = M_s and r is the length.

Within a run, M_s = a_s (by definition), and for 1 ≤ i < r:

`M_{s+i} = a_s ⊕ [0, ..., 0, i]`

where [0, ..., 0, i] has length #a_s. (At i = 0 no displacement arithmetic is needed — the base case is the definition of a_s. We restrict to i ≥ 1 because TumblerAdd requires a positive displacement.) The inductive step uses absence of a break to conclude M_{s+i} = M_{s+i-1} ⊕ u_I = (a_s ⊕ [0,...,0,i-1]) ⊕ u_I = a_s ⊕ [0,...,0,i] by TA-assoc (the action points coincide at position #a_s, and i − 1 + 1 = i).

The length #a_s is invariant within a run: by the result-length identity (#(a ⊕ w) = #w), each I-successor has the same length as its predecessor. So u_I is uniform within a run.

**A3 (Existence).** For every document d, V(d) admits a decomposition into maximal correspondence runs R₁, R₂, ..., R_p (ordered by V-position) with p ≥ 0. When V(d) = ∅, p = 0. When V(d) ≠ ∅, runs are constructed by scanning V(d) in order and starting a new run at each break. The scan terminates because V(d) is finite.

**A4 (Uniqueness).** The decomposition in A3 is unique.

*Proof.* The break set B is a deterministic function of M(d) — position v_j is a break iff M_{j-1} →_I M_j fails. The maximal break-free intervals of {v₀, ..., v_{n-1}} are uniquely determined by B. Since B is unique, the decomposition is unique. ∎

We call this the *canonical decomposition* of M(d). Nelson puts it crisply: this is "the unique run decomposition of the V→I mapping's first difference." The breaks are forced by the mapping; the non-breaks are forced by maximality.

**A5 (Minimality).** For any decomposition of M(d) into correspondence runs with q pieces, q ≥ p.

*Proof.* Every break in the canonical decomposition is *forced*: at a break, the I-addresses on either side are not I-adjacent, so no single correspondence run can span the break. With p − 1 forced breaks (between p consecutive runs), every alternative decomposition must place at least one run boundary at each. Hence q ≥ p. ∎

**Observation.** Any other valid decomposition is a *refinement* of the canonical one — obtained by introducing additional break points that subdivide existing runs.

## Properties of the Canonical Decomposition

We write each run as R_j = (v_{s_j}, a_j, r_j) for 1 ≤ j ≤ p.

**A6 (Partition).** The canonical decomposition partitions V(d):

(a) s₁ = 0 — the first run starts at the beginning.

(b) s_{j+1} = s_j + r_j for 1 ≤ j < p — runs are contiguous; no gap separates consecutive runs.

(c) s_p + r_p = n — the last run extends to the end.

Parts (a)–(c) follow from A0 (no gaps in V(d)) and the construction (runs are maximal contiguous break-free intervals). Every V-position in V(d) belongs to exactly one run: maximal break-free intervals of a contiguous index set partition it by construction — the break points divide {v₀, ..., v_{n-1}} into non-overlapping, exhaustive segments.

**A7 (Width Preservation).** Within each run R = (v_s, a, r), the V-extent and I-extent cover the same count of positions. The arrangement restricted to a single run is a bijection between r consecutive V-positions and r consecutive I-addresses:

`(A i : 0 ≤ i < r : M(d)(v_{s+i}) = a ⊕ [0,...,0,i])`

This is the abstract counterpart of the implementation's width-value equivalence: the V-width and I-width of a correspondence run encode the same integer count, even when their tumbler representations differ in length and precision.

**A8 (I-Order Independence).** The canonical decomposition imposes no ordering constraint on the I-addresses of distinct runs. For runs R_j and R_k with j < k (so v_{s_j} < v_{s_k} in V-space):

- a_j < a_k is possible (I-order agrees with V-order).
- a_j > a_k is possible (I-order reverses V-order).
- origin(a_j) ≠ origin(a_k) is possible (runs from different source documents).

REARRANGE produces arrangements where I-order disagrees with V-order — content created later can precede content created earlier. Transclusion (COPY) places content from arbitrary source documents at arbitrary V-positions. The V-stream's ordering is independent of I-space ordering. This is the design's fundamental separation: V-space is arrangement; I-space is identity.

**A9 (I-Span Overlap).** The I-spans of distinct runs within a single document may overlap. For runs R_j and R_k with j ≠ k, the I-address sets {a_j, ..., a_j ⊕ [0,...,0,r_j-1]} and {a_k, ..., a_k ⊕ [0,...,0,r_k-1]} may share elements. This occurs when the same content is transcluded to multiple V-positions.

This follows from S5 (unrestricted sharing): the same I-address may appear at multiple V-positions. The canonical decomposition does not merge runs at different V-positions merely because they reference overlapping I-spans.

**Contrast.** V-spans are always disjoint (A6). I-spans may overlap (A9). This asymmetry is structural: V-space is a unique arrangement; I-space is a shared pool.

**A10 (Cross-Document Independence).** For documents d₁ and d₂, the canonical decompositions of M(d₁) and M(d₂) are independent. Even when ran(M(d₁)) ∩ ran(M(d₂)) ≠ ∅, the run boundaries in d₁ are determined by d₁'s V→I mapping alone.

*Proof.* The canonical decomposition is defined entirely in terms of M(d) — the arrangement function of one document. No cross-document information enters the break predicate. ∎

Two documents may share I-space content but decompose it into runs of different sizes, at different V-positions, in different orders. Nelson's Shakespeare example illustrates: Jewett's modified Hamlet transcludes most of the original play as a single large run, inserts a few bytes of native content, then transcludes the remainder. The original play's own arrangement is a single run covering all its content. The shared bytes appear in differently-sized runs across the two documents.

**A11 (Empty Arrangement).** When V(d) = ∅, the canonical decomposition is the empty sequence (p = 0). This is the state of a newly created document — K.δ produces M(d) = ∅ — and is always reachable by deleting all content. A0 is satisfied vacuously.

## Span Representation

Each run R_j = (v_{s_j}, a_j, r_j) corresponds to a pair of spans:

- σ_V(R_j) = (v_{s_j}, w_V) where w_V = [0, ..., 0, r_j] of length L(d) — the V-span.
- σ_I(R_j) = (a_j, w_I) where w_I = [0, ..., 0, r_j] of length #a_j — the I-span.

Both widths encode the same integer count r_j, though as tumblers of different lengths. The V-span and I-span are well-formed spans (T12: width is positive and the action point falls within the start position's length). The arrangement restricted to this run maps the j-th position within σ_V to the j-th position within σ_I, preserving ordinal offset.

The canonical decomposition of M(d) is the sequence ⟨(σ_V(R₁), σ_I(R₁)), ..., (σ_V(R_p), σ_I(R_p))⟩ — a finite list of span pairs. This list has the properties:

(i) The V-spans partition V(d) (A6), and consecutive V-spans are adjacent: reach(σ_V(R_j)) = start(σ_V(R_{j+1})).

(ii) Each pair encodes an ordinal-preserving mapping (A7).

(iii) The I-spans have no ordering constraint (A8) and may overlap (A9).

This list is the *arrangement descriptor*: a finite sequence of span pairs that completely determines the V→I mapping.

**A12 (Arrangement Equality).** M(d₁) = M(d₂) as partial functions iff their canonical decompositions agree: same number of runs p, and for each j, start(σ_V(R_j^{d₁})) = start(σ_V(R_j^{d₂})) and σ_I(R_j^{d₁}) = σ_I(R_j^{d₂}). (V-span width need not be checked separately: I-span equality gives equal run lengths r_j, and V-span width is [0,...,0,r_j] at the shared depth L(d), so V-spans are fully determined by V-start and I-span.)

*Proof.* Forward: identical functions produce identical break sets and hence identical maximal runs. Reverse: identical span-pair sequences reconstruct identical functions, since each V-position's I-address is determined by the run that contains it and the ordinal offset within that run. V-start equality forces L(d₁) = L(d₂) (the starts are depth-L tumblers), and I-span equality gives matching run lengths, so the V-spans match. ∎

## Worked Example

We verify the canonical decomposition concretely. Let document d have V-depth L(d) = 2 and I-addresses at element depth (zeros = 3). Define an arrangement with five V-positions:

| V-position | I-address |
|------------|-----------|
| [1, 1] | [3, 0, 1, 0, 1, 0, 5] |
| [1, 2] | [3, 0, 1, 0, 1, 0, 6] |
| [1, 3] | [3, 0, 1, 0, 1, 0, 8] |
| [1, 4] | [3, 0, 1, 0, 1, 0, 9] |
| [1, 5] | [3, 0, 1, 0, 1, 0, 10] |

**A0 check.** The prefix is p = [1], and the ordinals are {1, 2, 3, 4, 5} — a contiguous interval. A0 is satisfied.

**Break set.** The unit I-displacement is u_I = [0, 0, 0, 0, 0, 0, 1] (length 7). We check I-succession at each consecutive pair:

- v₁ to v₂: M₀ ⊕ u_I = [3, 0, 1, 0, 1, 0, 5] ⊕ [0, 0, 0, 0, 0, 0, 1] = [3, 0, 1, 0, 1, 0, 6] = M₁. Not a break.
- v₂ to v₃: M₁ ⊕ u_I = [3, 0, 1, 0, 1, 0, 6] ⊕ [0, 0, 0, 0, 0, 0, 1] = [3, 0, 1, 0, 1, 0, 7] ≠ [3, 0, 1, 0, 1, 0, 8] = M₂. **Break at v₂** (ordinal index 2).
- v₃ to v₄: M₂ ⊕ u_I = [3, 0, 1, 0, 1, 0, 8] ⊕ [0, 0, 0, 0, 0, 0, 1] = [3, 0, 1, 0, 1, 0, 9] = M₃. Not a break.
- v₄ to v₅: M₃ ⊕ u_I = [3, 0, 1, 0, 1, 0, 9] ⊕ [0, 0, 0, 0, 0, 0, 1] = [3, 0, 1, 0, 1, 0, 10] = M₄. Not a break.

B = {v₂}. One break yields p = 2 runs.

**Canonical decomposition.**

R₁ = ([1, 1], [3, 0, 1, 0, 1, 0, 5], 2). Verify A7: M(d)([1, 1]) = [3, 0, 1, 0, 1, 0, 5] = a₁ (base case); M(d)([1, 2]) = [3, 0, 1, 0, 1, 0, 6] = [3, 0, 1, 0, 1, 0, 5] ⊕ [0, 0, 0, 0, 0, 0, 1] = a₁ ⊕ [0, 0, 0, 0, 0, 0, 1]. ✓

R₂ = ([1, 3], [3, 0, 1, 0, 1, 0, 8], 3). Verify A7: M(d)([1, 3]) = [3, 0, 1, 0, 1, 0, 8] (base); M(d)([1, 4]) = [3, 0, 1, 0, 1, 0, 9] = a₂ ⊕ [0, 0, 0, 0, 0, 0, 1]; M(d)([1, 5]) = [3, 0, 1, 0, 1, 0, 10] = a₂ ⊕ [0, 0, 0, 0, 0, 0, 2]. ✓

**A6 check.** s₁ = 0 (first run starts at beginning). s₂ = s₁ + r₁ = 0 + 2 = 2 (contiguous). s₂ + r₂ = 2 + 3 = 5 = n (last run extends to end). ✓

**Span representation.** σ_V(R₁) = ([1, 1], [0, 2]), σ_I(R₁) = ([3, 0, 1, 0, 1, 0, 5], [0, 0, 0, 0, 0, 0, 2]). σ_V(R₂) = ([1, 3], [0, 3]), σ_I(R₂) = ([3, 0, 1, 0, 1, 0, 8], [0, 0, 0, 0, 0, 0, 3]). Reach: reach(σ_V(R₁)) = [1, 1] ⊕ [0, 2] = [1, 3] = start(σ_V(R₂)). V-spans are adjacent. ✓

**DELETE applied.** Delete w = 1 position at ordinal j = 1 (removing v₁ = [1, 2], which maps to I-address [3, 0, 1, 0, 1, 0, 6]). The deletion falls in the interior of R₁, which spans ordinals 0–1. The right portion of R₁ (ordinal 1, the sole element) is removed, leaving a left survivor of length 1. R₂ is unaffected except its V-positions shift left by 1.

Post-state:

| V-position | I-address |
|------------|-----------|
| [1, 1] | [3, 0, 1, 0, 1, 0, 5] |
| [1, 2] | [3, 0, 1, 0, 1, 0, 8] |
| [1, 3] | [3, 0, 1, 0, 1, 0, 9] |
| [1, 4] | [3, 0, 1, 0, 1, 0, 10] |

Break set: M₀ ⊕ u_I = [3, 0, 1, 0, 1, 0, 6] ≠ [3, 0, 1, 0, 1, 0, 8] = M₁. Break at v₁. No other breaks. Still p = 2 runs: R'₁ = ([1, 1], [3, 0, 1, 0, 1, 0, 5], 1), R'₂ = ([1, 2], [3, 0, 1, 0, 1, 0, 8], 3). A6: s₁ = 0, s₂ = 1, s₂ + r₂ = 4 = n. ✓

## Preservation Under Operations

A0, as a coupling constraint, holds by definition for every valid composite transition. The following arguments demonstrate that each of the four arrangement-modifying operations — INSERT, DELETE, REARRANGE, and COPY — *can* produce a post-state satisfying A0, given A0 in the pre-state. These are existence arguments: they show each operation is compatible with the constraint, not vacuously excluded by it.

### INSERT

INSERT at ordinal position j (with 0 ≤ j ≤ n) of width w > 0 adds w new V-positions and shifts existing positions at or past j rightward by w. We reason backward from the postcondition.

`A0 ∧ 0 ≤ j ≤ n ⟹ wp(INSERT(d, j, w), A0)`

That is: A0 in the pre-state together with a valid insertion index suffices to guarantee A0 in the post-state. Inserting at j > n would leave a gap between v_{n-1} and the new content, violating A0. Inserting at j = n is an append; j = 0 is a prepend; 0 < j < n is a mid-stream insertion.

**Post-state.** V'(d) has n + w positions: the first j positions retain their I-addresses, the next w positions carry new content, and the remaining n − j positions retain the I-addresses of the pre-state's positions j through n − 1. The enumeration is v'₀ = v₀, ..., v'_{j-1} = v_{j-1}, then w new positions, then v'_{j+w} corresponding to the old v_j, and so on. The domain is contiguous by construction. A0 is preserved. ∎

**Effect on the canonical decomposition.** The I-addresses of existing runs are unchanged; only their V-positions shift. If j falls in the interior of a run R_k (meaning s_k < j < s_k + r_k), that run splits into a left portion of length j − s_k and a right portion of length s_k + r_k − j, separated by the inserted content. At most one run splits. If j falls at a run boundary (j = s_k for some k), no existing run splits. The inserted content introduces one or more new runs.

### DELETE

DELETE of w positions starting at ordinal position j (with 0 ≤ j and j + w ≤ n) removes w V-positions and shifts surviving positions at or past j + w leftward by w, closing the gap.

`A0 ∧ 0 ≤ j ∧ j + w ≤ n ⟹ wp(DELETE(d, j, w), A0)`

**Post-state.** V'(d) has n − w positions (or is empty if w = n). The first j positions retain their I-addresses. Positions j through j + w − 1 are removed. Positions j + w through n − 1 shift to positions j through n − w − 1, retaining their I-addresses. The domain is contiguous. A0 is preserved. ∎

**Effect on the canonical decomposition.** Runs entirely within the deleted range disappear. A run straddling the left boundary of the deletion is truncated (its right portion is removed). A run straddling the right boundary is truncated (its left portion is removed). A single run may span both deletion boundaries — when R = (v_s, a, r) contains the entire deleted range (s < j and s + r > j + w), that one run splits into a left survivor [s, j) and a right survivor [j + w, s + r). These two survivors are never I-adjacent: the w deleted I-positions create an I-gap of width w between them (the left survivor ends at a ⊕ [0,...,0, j − s] and the right survivor starts at a ⊕ [0,...,0, j − s + w], separated by w I-addresses), so they remain distinct runs in the post-state. After the gap closes, the left survivor of one run and right survivor of another (or the same run) become V-adjacent. If they happen to be I-adjacent as well (an uncommon coincidence), the canonical decomposition of the post-state merges them into a single run, since maximality demands it. The number of runs in the post-state is at most p + 1 (when one run splits into two survivors) and at least 1 (when surviving content forms a single run) or 0 (when all content is deleted).

### REARRANGE

REARRANGE with cuts 0 ≤ c₁ < c₂ < c₃ ≤ n transposes two regions: positions [c₁, c₂) and [c₂, c₃) swap, while positions outside [c₁, c₃) are unaffected. This is a K.μ~ reordering.

**Post-state.** dom(M'(d)) = dom(M(d)) — the V-domain is unchanged. The bijection permutes V-positions: region [c₁, c₂) (of size c₂ − c₁) moves to [c₁, c₁ + (c₃ − c₂)), and region [c₂, c₃) (of size c₃ − c₂) moves to [c₁ + (c₃ − c₂), c₃). The combined interval [c₁, c₃) is still fully covered, and positions outside it are unchanged. A0 is preserved trivially.

The multiset of I-addresses is preserved: ran(M'(d)) = ran(M(d)).

**Effect on the canonical decomposition.** A run whose V-positions lie entirely within one region moves as a unit — its V-span shifts but its I-span is unchanged. A run straddling a cut boundary splits at the cut point: the two halves receive different V-displacements and become separate runs. With three cuts, at most three runs split. No structural coalescing pass follows the rearrangement, though the canonical decomposition of the post-state may merge runs that become I-adjacent by coincidence. The implementation confirms: `slicecbcpm` produces exactly two positive-width pieces when cutting at an interior point, and no coalescing pass follows `rearrangend`.

### COPY

COPY (transclusion) places content from a source document into V(d) at a specified position, shifting subsequent positions rightward — the same V-space mechanics as INSERT. The only difference is I-address provenance: INSERT allocates fresh I-addresses via K.α, while COPY references existing I-addresses from the source. Since A0 concerns only the V-domain structure and is indifferent to I-address provenance, INSERT's preservation argument subsumes COPY.

**Effect on the canonical decomposition.** COPY has the same V-space mechanics as INSERT — it opens a gap of width w at position j and fills it. If j falls in the interior of an existing run, that run splits (at most one split, as with INSERT). The transcluded content introduces one or more new runs, whose I-addresses reference existing I-space content from the source document rather than freshly allocated addresses. The resulting decomposition effects are identical to INSERT's; only I-address provenance differs.

## Merging Is Not Required

We note explicitly: the specification does not require that adjacent correspondence runs referencing I-contiguous content be merged. Nelson is clear — the document's virtual byte stream is defined at the byte level, not the span level. Whether two adjacent runs that happen to be I-contiguous are represented as one merged run or two separate runs is semantically invisible: every user-facing operation (RETRIEVEV, FINDDOCSCONTAINING, SHOWRELATIONOF2VERSIONS) produces identical results either way.

The canonical decomposition merges such runs by definition (maximality), but this is a mathematical property of the decomposition, not an implementation obligation. A system may internally store a refinement of the canonical decomposition without violating any specification-level property.

This observation has a converse: the canonical decomposition is the *coarsest* valid representation. It uses the fewest runs (A5). Any finer representation carries redundant boundaries but is equally correct.

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| A0 | V(d) is convex at depth L(d) — no gaps in the text V-domain | introduced |
| A1 | If V(d) ≠ ∅, then V(d) = {[p, k] : k_min ≤ k ≤ k_max} for a fixed prefix p | introduced |
| A1a | While V(d) ≠ ∅, L(d) is fixed — only re-settable after total deletion | introduced |
| A2 | V(d) admits ordinal enumeration via unit V-displacement: v_{j+1} = v_j ⊕ u_V | introduced |
| A3 | The canonical decomposition into maximal correspondence runs exists | introduced |
| A4 | The canonical decomposition is unique | introduced |
| A5 | The canonical decomposition is minimal (fewest runs of any valid decomposition) | introduced |
| A6 | The V-spans of the canonical decomposition partition V(d) with no gaps | introduced |
| A7 | Each run maps r V-positions to r I-addresses bijectively | introduced |
| A8 | No ordering constraint relates the I-addresses of distinct runs | introduced |
| A9 | I-spans of distinct runs within a single document may overlap | introduced |
| A10 | Each document's canonical decomposition is independent of all others | introduced |
| A11 | The empty arrangement (V(d) = ∅) has zero runs | introduced |
| A12 | Two arrangements are equal iff their canonical decompositions are equal | introduced |

## Open Questions

- What invariants govern the link subspace (v₁ < 1) of a document's arrangement, given that link addresses are permanent and deletion leaves gaps?
- What is the maximum number of runs in the canonical decomposition as a function of the number of editing operations performed?
- Under what conditions does DELETE cause two formerly-separate runs to merge in the canonical decomposition of the post-state?
- What structural invariant must a version fork preserve about the source document's canonical decomposition?
- Can the canonical decomposition serve as a normal form for version comparison — can version difference be expressed as a diff over run sequences?
- What constraints, if any, does the allocation discipline (T10a) place on the I-addresses that can appear within a single run?
