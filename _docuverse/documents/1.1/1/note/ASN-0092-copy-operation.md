# ASN-0092: COPY Operation
*2026-05-24*

We are asked: what does it mean to place existing Istream content at a position in a Vstream? What is preserved about the content's identity, what shifts, and what invariants must the operation maintain?

The phrasing of the question already conceals a tension that the answer must dissolve. Istream content is permanent and immutable — `Σ.C` is append-only with values fixed once written (S0, ASN-0036). One cannot *place* anything in Istream after the fact; one can only *allocate* into it, and allocation always introduces fresh content. So if the topic is "existing content," then no Istream activity is in question at all. Whatever COPY does, it must do entirely within the Vstream — the arrangement layer `Σ.M(d) : T ⇀ T`, which binds V-positions to I-addresses. The "place at a position" is a Vstream act: extending some target arrangement with a new binding from a V-position to an I-address that is already in `dom(Σ.C)`.

This rephrasing exposes the architectural fact that resolves the puzzle. The system's transition vocabulary, looked at structurally, has two independent capabilities: allocation (K.α, which extends `dom(C)` with a fresh I-address bound to a value; ASN-0093) and arrangement extension (K.μ⁺, which extends `dom(M(d))` with V→I bindings whose I-addresses must already lie in `dom(C)`; ASN-0047). The two are independent in the sense that neither subsumes the other and either can be performed without the other. INSERT, intuitively, performs both: allocate fresh content, then bind a V-position to it. COPY performs only the second: bind new V-positions to I-addresses that already exist in `dom(C)` — I-addresses originally allocated by some prior K.α event, possibly in a different document, possibly long ago.

We will introduce K.γ as the formal COPY transition and derive its properties. The work is not in inventing machinery — the machinery is K.μ⁺ — but in characterising exactly what COPY constrains and what it leaves free, and what consequences follow from the constraint that no new I-address enters `dom(C)`.

## What Is Preserved, What Is Read, What Is Written

We begin by stipulating the data K.γ requires. A COPY is parameterised by:

  — a source document `d_s ∈ dom(M)`,
  — a target document `d_t ∈ dom(M)` (with `d_s = d_t` permitted),
  — a finite, non-empty set of source V-positions `V_s ⊆ dom(M(d_s))` selected by the caller,
  — a target placement point `v_t` that admits the new V-positions into `M(d_t)`.

The source positions `V_s` resolve, via `M(d_s)`, to a sequence of I-addresses. Calling the source positions in V-order `v_{s,1} < v_{s,2} < ... < v_{s,n}` and setting `a_k = M(d_s)(v_{s,k})`, we obtain a sequence of pairs `(v_{s,k}, a_k)` that K.γ must transport into `M(d_t)` under new V-coordinates while preserving every `a_k` exactly.

What must the new V-coordinates be? The arrangement model (ASN-0036) constrains arrangements per subspace to satisfy D-CTG, D-MIN, and consequently D-SEQ — each subspace's V-positions form a contiguous prefix of a uniform-depth tuple starting at `[S, 1, ..., 1]`. The available extension point — what ASN-0036 calls `ValidInsertionPosition(d_t, v_t)` (or `ValidFirstInsertionPosition` if the subspace is initially empty) — is the unique next slot in the subspace's sequence. The new V-positions then must be `v_{t,k} = shift(v_t, k - 1)` for `k = 1, ..., n`, filling the next `n` ordinal slots consecutively.

This is the formal effect of K.γ:

```
K.γ (Copy)
  Preconditions:
    d_s, d_t ∈ dom(M)
    V_s ⊆ dom(M(d_s)), |V_s| = n ≥ 1, finite
    (A v ∈ V_s :: subspace(v) = S_v)   — common subspace within V_s
    Either V_{S_v}(d_t) ≠ ∅ and ValidInsertionPosition(d_t, v_t) holds,
        or V_{S_v}(d_t) = ∅ and ValidFirstInsertionPosition(d_t, v_t, m) holds
        with m = the common depth of V_s
    (Admissibility) Extending M(d_t) with the new bindings preserves
        S8a, S8-depth, S8-fin, D-CTG, D-MIN, D-SEQ for subspace S_v in d_t

  Effect:
    Let v_{s,1} < v_{s,2} < ... < v_{s,n} be V_s in V-order, a_k = M(d_s)(v_{s,k}).
    Let v_{t,k} = shift(v_t, k - 1) for k = 1, ..., n (so v_{t,1} = v_t).
    M'(d_t) extends M(d_t) by M'(d_t)(v_{t,k}) = a_k for each k = 1, ..., n.
    M'(d_t)(v) = M(d_t)(v) for every v ∈ dom(M(d_t)).

  Frame:
    C' = C
    L' = L
    dom(M') = dom(M)
    M'(d) = M(d) for every d ∉ {d_t}
```

The effect clause is intentionally minimal. The substantive content is in the frame: `C' = C`. *No I-address enters or leaves `dom(C)`*. The bytes in Istream do not move, do not multiply, do not change. The arrangement of every document other than `d_t` is preserved — in particular `M(d_s)`, the source. Only `M(d_t)` grows, and even there the growth consists entirely of bindings whose I-addresses already lay in `dom(C)`.

The K.γ operation is the K.μ⁺ skeleton with the additional structural constraint that the I-addresses bound were *not freshly allocated in this operation*. Looked at from K.μ⁺'s perspective, every K.μ⁺ event is either coupled with a preceding K.α (yielding the INSERT composite) or stands alone (yielding K.γ — COPY). The distinguishing fact of COPY is precisely this absence of K.α.

## Identity Preservation as the Defining Property

The defining property of K.γ — what makes "COPY" structurally different from "duplicate the bytes under a new I-address" — is identity preservation at the I-address level. The I-addresses bound in the target are the *same tumblers* as the I-addresses they were drawn from in the source, not merely equal in value.

  IP1 (Identity Preservation). After K.γ, for each `k ∈ {1, ..., n}`:
       `M'(d_t)(v_{t,k}) = M(d_s)(v_{s,k}) = a_k`.

The tumbler `a_k` appears literally — by sequence equality — in both arrangements. This is sharper than the assertion `C'(M'(d_t)(v_{t,k})) = C(M(d_s)(v_{s,k}))` (equality of values), which would be satisfied also by a hypothetical "value-copying" operation that allocates fresh I-addresses and binds them to the same values. K.γ is not value-copying.

We can read off three consequences immediately.

*First*, no growth of `dom(C)`. By the frame `C' = C`, the content store is exactly invariant. Allocation activity in the system is unaffected: the sub-allocator chains `A_C(d)` (ASN-0093) advance only when K.α fires, and K.γ fires no K.α. A subsequent K.α in any document will allocate the same I-address it would have allocated had K.γ never occurred.

*Second*, the bytes do not move. There is no operation in the substrate that moves bytes between I-addresses; `Σ.C(a)` is fixed forever once written (S0). When K.γ extends `M(d_t)` to reference `a_k`, the value `C(a_k)` is read on demand by any retrieval against `M(d_t)(v_{t,k})` — and that retrieval consults the same Istream location it would have consulted via `M(d_s)(v_{s,k})`. There is one byte, and there are two arrangements that name it.

*Third*, distinguishability is preserved at the tumbler level. Two pieces of content in the system are the same iff their I-addresses are equal (S4, OriginBasedIdentity, ASN-0036). After K.γ, the content at `M'(d_t)(v_{t,k})` and the content at `M(d_s)(v_{s,k})` are the same — not merely equal-valued — because their I-addresses coincide as tumblers. The system has no mechanism for telling them apart, because there is nothing to tell apart.

We observe the contrapositive: if K.γ did *not* preserve I-address identity — if it allocated fresh I-addresses and bound them to copies of the values — then the resulting target bindings would refer to different I-addresses, and S4 would classify them as distinct content. Origin attribution would be lost (origin of the new I-addresses would be `d_t`, not the actual creating document). Subsequent intercomparison would not find these I-addresses on common ground. The entire fabric of permanent reference would unravel one allocation at a time. The structural minimality of K.γ — its refusal to allocate — is precisely what makes the fabric hold.

## Source Invariance

The source document is structurally untouched by K.γ. By the frame, `M'(d_s) = M(d_s)`. The bindings `(v_{s,k}, a_k)` from which K.γ read still hold in the post-state; the source arrangement is bit-for-bit identical to its pre-state.

This is a frame property, not a derived theorem: K.γ writes only to `M(d_t)`. Even in the self-copy case `d_s = d_t`, the construction extends `M(d_t)` with new V-positions chosen from the *available* extension slot (`ValidInsertionPosition`), which is disjoint from `dom(M(d_t))` by construction. So the existing source bindings in `V_s` are not overwritten, and the V-positions to which the new bindings attach are new.

Combining `M'(d_s) = M(d_s)` with `C' = C`, every readable property of `d_s` is invariant across K.γ:

  SI1 (Arrangement). `dom(M'(d_s)) = dom(M(d_s))` and `M'(d_s)(v) = M(d_s)(v)` for every `v ∈ dom(M(d_s))`.
  SI2 (Content). For every `v ∈ dom(M(d_s))`, `C'(M'(d_s)(v)) = C(M(d_s)(v))`.
  SI3 (Origin). For every `v ∈ dom(M(d_s))`, `origin(M'(d_s)(v)) = origin(M(d_s)(v))` — `origin` is a function of the I-address's tumbler structure (S7, ASN-0036) and no tumbler is altered.

The mechanism by which K.γ *could* affect the source — if any existed — would have to be a write into `M(d_s)` or into the content at addresses bound by `M(d_s)`. K.γ has no such write in its effect clause. The source's preservation is enforced by the absence of any path that could violate it.

## What Shifts

The question asks what shifts. The answer is somewhat subtle. The bytes in Istream do not shift — they are immutable. The I-addresses do not shift — they are fixed tumblers. The source's arrangement does not shift — it is invariant by frame. So in what sense does anything shift?

What shifts is the *available V-extension slot in the target*. Pre-state, the target's subspace `S_v` had `n_S` positions and the next available slot was `[S_v, 1, ..., 1, n_S + 1]`. Post-state, the subspace has `n_S + n` positions and the next available slot is `[S_v, 1, ..., 1, n_S + n + 1]`. The boundary marker — the V-position at which the next K.μ⁺ or K.γ could extend — has shifted forward by `n`.

Looked at this way, "shift" is a *bookkeeping displacement of the boundary*, not a translation of any concrete entity. No piece of content has moved; no I-address has been reassigned; no V-position has changed its binding. The new V-positions are *added* on the trailing edge of the subspace, and the trailing edge itself moves.

This is the formal reflection of Nelson's "no copying among documents" remark. The bytes do not flow. The arrangement does not shuffle. What changes is solely that `M(d_t)` now has additional entries — entries that, by the design of K.γ, reference I-addresses that already existed.

  ED (Extension Displacement). After K.γ binding `n` new V-positions in subspace `S_v` of `d_t`:
       `n_{S_v}(M'(d_t)) = n_{S_v}(M(d_t)) + n`,
       and the next valid insertion position in `S_v` shifts by `shift(·, n)`.

For other subspaces in `d_t`, and for every other document in `dom(M)`, nothing shifts. The bookkeeping displacement is strictly local to subspace `S_v` of `d_t`.

A note on "in-place insertion." A naive question one might ask is: what if we wanted to copy *between* existing positions in a target — say, between positions `v` and `shift(v, 1)`? In the abstract model of ASN-0036, this is not directly admissible: arrangements satisfy D-SEQ, and there are no "in-between" positions available in a uniform-depth sequence. To realise the apparent effect of in-place insertion, the substrate would compose K.μ⁻ (contract to remove the tail), K.γ (place the copied content at the new boundary), and a re-application that re-establishes the original tail at fresh ordinal slots. None of these constituents is K.γ itself; K.γ is an extension, not a relocation, and its semantics is to add at the boundary. Treating "in-place insertion" as a composite places it outside the K.γ specification proper.

## Reference Semantics: One Instance, Many Pointers

A consequence of identity preservation is that K.γ produces many-to-one bindings: distinct V-positions, possibly across many documents, bind to the same I-address.

  M2P (Multi-Position Sharing). After K.γ from `V_s` in `d_s` to `v_t` in `d_t`:
       for each `k`, the I-address `a_k` satisfies `a_k ∈ ran(M(d_s)) ∩ ran(M'(d_t))`.
       In particular, after `n ≥ 1` distinct K.γ events copying the same V-positions into `n + 1` arrangements (the original plus `n` copies), each `a_k` is in `n + 1` arrangement images.

The arrangement function is a partial function from V-positions to I-addresses, not an injection. Image multiplicity is permitted — even encouraged. K.γ is the operation that creates such multiplicity: every successful K.γ event adds at least one V-position to some `M(d_t)` whose I-address already appears elsewhere.

The architectural implication is the *single instance, many views* model. The content lives once in Istream at I-address `a_k`. Every arrangement that has been the target of a K.γ event placing `a_k` provides a "view" of this single instance through its own V-coordinates. Reading the value at any such view retrieves the same value `C(a_k)` from the same Istream location. The retrieval mechanism does not — cannot — distinguish "original" from "copy" because both are equivalent V→I bindings against the same `a_k`.

The system contains, in this sense, no copies of anything in the value sense. It contains many views of single instances. The word "copy" in COPY is a Vstream-level operation, not an Istream-level event.

## Transitivity Through Chains

The structural property that K.γ binds existing I-addresses, combined with the fact that those existing I-addresses are themselves outputs of either prior K.α or prior K.γ events, gives K.γ a transitivity property: identity propagates through arbitrary chains.

Suppose document `D_0` originally allocated an I-address `a` via K.α — so `a ∈ dom(C)` and `origin(a) = D_0`. Suppose subsequently document `D_1` performed K.γ from `D_0` (placing `a` in `M(D_1)` at some V-position), and document `D_2` then performed K.γ from `D_1` at the corresponding V-position, and so on through a chain `D_0, D_1, D_2, ..., D_n`. At each link, K.γ reads the I-address from the source arrangement and writes the same tumbler into the target arrangement.

  TR (Chain Transitivity). For any K.γ chain `(D_0 → D_1 → ... → D_n)` propagating I-address `a` (originally allocated by `D_0`) through `n` copies, the I-address bound at the V-position of `a` in `M(D_n)` equals `a` as a tumbler.

The proof is straightforward induction. Base: in `M(D_0)`, the V-position of `a` is bound to `a` (by construction of the initial K.α). Step: assume the V-position of `a` in `M(D_k)` is bound to `a`. The K.γ event from `D_k` to `D_{k+1}` reads `M(D_k)(v_k) = a` and binds the target V-position to the same `a`. So in `M(D_{k+1})`, the V-position of `a` is bound to `a`.

The chain has no length bound. Identity is not lost across hops; it is not weakened; it is not transformed. The same tumbler propagates intact through any number of K.γ events. This is what permits "transclusion of a transclusion" to remain coherent: every link in the chain refers to the same Istream location, and the entire chain collapses semantically to a single reference.

The mechanism is local at each step. K.γ at the `k`-th link is oblivious to the chain's prior history; it reads only the source arrangement at that step and propagates the I-address it finds there. The history is encoded structurally in the I-address itself: its origin (`D_0`) is recoverable by `origin(a)` regardless of which arrangement it currently appears in. No "chain depth" or "hop count" is recorded anywhere, because none is needed; the I-address is the entire record.

## Origin Recoverability

The `origin` projection of a content I-address (S7, ASN-0036) is a structural property of the tumbler: it is the document-level prefix `N(a).0.U(a).0.D(a)`, extracted from the tumbler's components by T4b. K.γ does not modify any tumbler. Therefore K.γ preserves `origin` for every I-address it propagates.

  OR (Origin Recoverability). After K.γ binding `M'(d_t)(v_{t,k}) = a_k`:
       `origin(a_k)` is unchanged from its pre-state value.

In particular: even when `D_0`, the originally allocating document, is far removed from `d_t` in a long K.γ chain, `origin(a_k) = D_0` remains decidable from `a_k`'s tumbler structure alone. The reader of `d_t`, retrieving the I-address at `v_{t,k}`, recovers `a_k`, and from `a_k` recovers `D_0`. No metadata about the COPY chain is needed; the I-address suffices.

This is the structural foundation for content attribution. Whoever owns `D_0` is determinable from any I-address that traces back to a K.α event in `D_0`. K.γ propagates the I-address; the I-address carries its origin within itself; therefore attribution flows.

The contrapositive sharpens the point: were K.γ to alter the I-address even subtly — say, by rewriting its origin field to `d_t` — origin recoverability would be lost. The bytes would still be retrievable but their attribution would silently drift toward whichever document last copied them. Such a system could not support the kind of credit-and-payment infrastructure Nelson envisages, in which the original author of content is paid every time anyone, anywhere, reads it. K.γ's pure transport of the I-address is what keeps attribution intact across arbitrary distance.

## Source Resolution and Run Structure

The source positions `V_s` of a K.γ event need not, in general, map under `M(d_s)` to a single contiguous I-address range. The arrangement of `d_s` may have been built up through past K.γ events bringing in content from multiple origins, interleaved with locally-allocated content; what looks like a contiguous V-range in `d_s` may resolve to several disjoint I-address ranges.

By S8 (SpanDecomposition, ASN-0036) — equivalently by the maximally-merged decomposition of ASN-0058 — any arrangement decomposes uniquely into correspondence runs `(v, a, n)` such that `M(d)(shift(v, k)) = shift(a, k)` for `0 ≤ k < n`. The restriction of `M(d_s)` to `V_s`, by the lemma C1a of ASN-0058, similarly decomposes into a finite ordered sequence of runs.

K.γ, applied to `V_s`, produces in the target one extension event per source run: each source run contributes a contiguous I-address range; the K.γ binds the next chunk of available V-positions in `d_t` to those I-addresses. The target's V-range is contiguous (filling consecutive ordinal slots starting at `v_t`); the I-addresses it points to remain in the same multiple runs they occupied in the source.

  RUN (Run Decomposition). If `M(d_s)|_{V_s}` decomposes into runs `(v_{s,j}, a_j, n_j)` for `j = 1, ..., r` (ordered by `v_{s,j}`), then after K.γ, `M'(d_t)` contains the runs `(shift(v_t, p_j), a_j, n_j)` where `p_j = (+ i : 1 ≤ i < j : n_i)` — the cumulative width of preceding runs.

The number of runs is preserved: `r` source runs produce `r` target runs. The widths are preserved: each source run of width `n_j` produces a target run of width `n_j`. The I-coordinates are preserved exactly. What changes is only the V-coordinate at which each run begins in `d_t`.

This has a consequence for the *information density* of the copied region. A source V-range that decomposed into many small runs (because the source had been frequently re-edited, with content interleaved from many origins) is more structurally complex than one that decomposed into a single large run. K.γ does not flatten this complexity; it transports it. The target arrangement's decomposition, restricted to the copied V-range, has exactly as many runs as the source's decomposition restricted to `V_s`.

We note that the abstract specification does not constrain whether the target's correspondence runs may merge with adjacent runs already present in `M(d_t)`. Merging is permissible whenever it preserves the V→I function and the canonical maximally-merged decomposition (M11–M12, ASN-0058). The merge condition is purely structural: V-adjacency and I-adjacency at run boundaries. Whether a target run merges with its neighbours depends on whether the boundary I-addresses happen to be contiguous, which is itself a function of which source content adjoins which existing content at the placement boundary.

## Multi-Source COPY

A natural generalisation of K.γ allows the source positions to be drawn from several documents in a single operation: `V_{s,1} ⊆ dom(M(d_{s,1})), V_{s,2} ⊆ dom(M(d_{s,2})), ...`. The semantics of multi-source COPY is fully determined by the per-source K.γ machinery applied independently: each `(d_{s,i}, V_{s,i})` resolves to a sequence of I-addresses via `M(d_{s,i})`, and the resulting I-addresses are bound to consecutive target V-positions in the order specified.

What matters at the multi-source level is what does *not* blend. Each I-address is bound to one target V-position; its origin remains the originally allocating document (by OR). Two consecutive target V-positions in a multi-source COPY may reference I-addresses with different origins, and the origin information is fully recoverable from each I-address separately. The system does not collapse multi-source content into a single uniform region — it cannot, because origin is a per-I-address structural property, not a per-document tag.

  MS (Multi-Source Independence). In a multi-source K.γ binding I-addresses `a_1, ..., a_n` to consecutive target V-positions:
    for each `k`, `origin(a_k)` is determined by `a_k` alone, independent of `k`'s neighbours;
    no two `a_k`s with different origins can be merged into a single I-address; their distinctness is structural.

The "single span" effect that a multi-source COPY presents at the V-level — `n` consecutive target V-positions filled by a single COPY event — is at the I-level a sequence of `n` independent address bindings. The V-coordinates are contiguous; the I-coordinates are heterogeneous. This is exactly the model under which Nelson's quoted documents can carry attribution: a reader, examining position by position, can recover the origin of each character without any per-document boundary metadata.

## Self-COPY

When `d_s = d_t`, K.γ reads from and writes to the same arrangement. Two questions arise: is the read-write ordering well-defined, and is the result consistent?

The atomicity of K.γ as an elementary transition (by SequentialTransitionAxiom, ASN-0047) settles both questions at once. The pre-state Σ supplies all values K.γ reads — including the source V-position bindings `M(d_s)(v_{s,k}) = a_k`. The post-state Σ' contains all of K.γ's effects committed simultaneously. There is no observable intermediate state in which some of the source bindings have been overwritten and others read.

In particular: the new V-positions `v_{t,k}` are chosen from the *available extension slot* (`ValidInsertionPosition`), which by construction is disjoint from `dom(M(d_t))` pre-state. So the new V-positions are distinct from the source V-positions, and the new bindings extend the arrangement without colliding with the existing ones.

  SC (Self-Copy Consistency). For K.γ with `d_s = d_t`:
       The I-addresses `a_k = M(d_t)(v_{s,k})` read pre-state remain the I-addresses bound at the new positions `v_{t,k}` post-state.
       The original source bindings at `v_{s,k}` are unaltered.
       Each `a_k` is bound twice in `M'(d_t)`: once at `v_{s,k}` (pre-existing, unchanged) and once at `v_{t,k}` (newly bound).

The self-copy is therefore the cleanest illustration of M2P: the same I-address occupies two V-positions in the same arrangement, the same document presents two "views" of the same content instance. The Istream is unchanged; the Vstream of `d_t` has gained `n` new bindings to `n` already-present I-addresses.

## What COPY Does Not Do (the Negative Specification)

The frame clauses of K.γ enumerate, by negation, what COPY's effect cannot reach. We collect them:

  ¬C1. No content is created. `dom(C') = dom(C)`.
  ¬C2. No content is destroyed. `dom(C') ⊇ dom(C)`.
  ¬C3. No content value is altered. `(A a ∈ dom(C) :: C'(a) = C(a))`.
  ¬M1. No document is created. `dom(M') = dom(M)`.
  ¬M2. The source arrangement is unchanged. `M'(d_s) = M(d_s)`.
  ¬M3. No other document's arrangement is changed. `(A d ∉ {d_t} :: M'(d) = M(d))`.
  ¬L1. No link is created. `dom(L') = dom(L)`.
  ¬L2. No link is destroyed. (Link store has its own monotonicity from L12, ASN-0093.)
  ¬O1. No I-address is reassigned origin. `(A a ∈ dom(C) :: origin'(a) = origin(a))`, since `origin` is determined by `a`'s tumbler structure.
  ¬A1. No allocator chain advances. The sub-allocator chains `A_C(d)`, `A_L(d)` for every `d ∈ dom(M)` (ASN-0093) are unchanged.

These negatives are the load-bearing content of COPY's specification. The positive content — extending `M(d_t)` with `n` new bindings — is structurally trivial. What makes COPY *transclusion* rather than *duplication* is the conjunction of negatives that flow from the absence of any K.α coupling.

A hypothetical alternative implementation of "copy" that allocated fresh I-addresses for each placed item and bound them to copies of the source values would violate ¬C1 (creating new content), ¬C2 vacuously, ¬O1 (origins would point to the copy site, not the source), and ¬A1 (allocator chains would advance). Every one of these would have downstream consequences: attribution would drift, intercomparison would fail, allocation pressure would compound, and the "single instance, many views" architecture would degrade into "many copies, drifting from each other." K.γ as specified rules all of this out by construction.

## Invariants Maintained Across K.γ

K.γ must preserve every invariant of the substrate state. Most are preserved vacuously by the frame, since they constrain components K.γ does not touch. The non-vacuous obligations concern `M(d_t)` and require explicit verification.

  IM1 (Functionality of `M(d_t)`). `M'(d_t)` is a partial function. *Verification.* The new bindings `v_{t,k} ↦ a_k` are placed at V-positions disjoint from `dom(M(d_t))` (by construction of `ValidInsertionPosition`), so no key collision arises; the new V-positions are pairwise distinct (`v_{t,k} = shift(v_t, k - 1)`, and shift is strictly monotone in `k`).

  IM2 (Referential integrity of `M(d_t)`). Every new mapping `M'(d_t)(v_{t,k}) = a_k` has `a_k ∈ dom(C')`. *Verification.* `a_k ∈ dom(C)` because `a_k = M(d_s)(v_{s,k})` and S3 ensures `ran(M(d_s)) ⊆ dom(C)`. `C' = C` by frame, so `a_k ∈ dom(C')`.

  IM3 (Finite domain of `M(d_t)`). `dom(M'(d_t))` is finite. *Verification.* `dom(M'(d_t)) = dom(M(d_t)) ∪ {v_{t,1}, ..., v_{t,n}}`, the union of a finite set with a finite set.

  IM4 (Per-subspace common depth). For the subspace `S_v` of the new V-positions, all V-positions share a common depth. *Verification.* If `V_{S_v}(d_t)` was non-empty pre-state, S8-depth fixed the depth at `m_{S_v}`; the new V-positions are constructed by `shift(v_t, k - 1)` where `v_t` was a `ValidInsertionPosition` at depth `m_{S_v}`, and shift preserves length. If `V_{S_v}(d_t)` was empty, `v_t` is a `ValidFirstInsertionPosition` at the depth supplied by `V_s` (the common depth of source positions in subspace `S_v`); this becomes the fixed depth for `S_v` in `d_t` going forward.

  IM5 (Sequential V-positions; D-CTG, D-MIN, D-SEQ). The new V-positions extend `V_{S_v}(d_t)` contiguously. *Verification.* By the construction of `ValidInsertionPosition`, `v_t` is the unique next slot `[S_v, 1, ..., 1, n_{S_v} + 1]` of depth `m_{S_v}`; successive `shift(v_t, k - 1)` for `k = 1, ..., n` produces `[S_v, 1, ..., 1, n_{S_v} + k]`, filling slots `n_{S_v} + 1` through `n_{S_v} + n` in order. The post-state `V_{S_v}(d_t)` is `{[S_v, 1, ..., 1, k] : 1 ≤ k ≤ n_{S_v} + n}`, satisfying D-SEQ. D-MIN holds because the minimum `[S_v, 1, ..., 1, 1]` is unchanged (or, if the subspace was empty, is set to the appropriate value by `ValidFirstInsertionPosition`). D-CTG follows from D-SEQ.

  IM6 (Content immutability, S0). `dom(C') ⊇ dom(C)` and `(A a ∈ dom(C) :: C'(a) = C(a))`. *Verification.* By frame `C' = C`, both clauses are equalities.

  IM7 (Allocation permanence). `dom(M') ⊇ dom(M)`, `dom(C') ⊇ dom(C)`, `dom(L') ⊇ dom(L)`. *Verification.* By frame, all three are equalities — monotonicity holds in the degenerate case where nothing was added.

  IM8 (Source preservation). `M'(d_s) = M(d_s)` and `C'|_{ran(M(d_s))} = C|_{ran(M(d_s))}`. *Verification.* By frame, both equalities hold directly.

  IM9 (Origin invariance). For every `a ∈ dom(C)` (including every `a_k` newly bound in `M(d_t)`), `origin'(a) = origin(a)`. *Verification.* The `origin` projection (S7, ASN-0036) is a structural function of `a`'s tumbler representation. K.γ does not alter any tumbler in `dom(C)`; it only binds existing tumblers to new V-positions. Hence `origin` is invariant.

  IM10 (Composite coupling J0). For each `a` newly entering `dom(C')`: K.γ adds no such `a`, so J0 is vacuously satisfied.

  IM11 (Composite coupling J1, J1' on provenance). For each `a` newly entering `ran(M'(d_t)) \ ran(M(d_t))`, ASN-0047 requires provenance `(a, d_t) ∈ R'`. *Verification.* K.γ does not satisfy this automatically; the composite that uses K.γ to add referenced I-addresses to a target's arrangement must couple K.γ with a corresponding K.ρ event recording `(a, d_t)` in the provenance relation. K.γ itself is a structural arrangement extension; provenance recording is a separate concern handled by composition with K.ρ at the boundary.

These invariants discharge K.γ's obligations to the substrate. The verification is uniformly mechanical: each invariant is either preserved by frame (most) or by the careful construction of new V-positions (IM4, IM5).

## Atomicity

K.γ is an elementary transition. By the SequentialTransitionAxiom (ASN-0047), each elementary transition is atomic: the precondition is evaluated against `Σ`, the effect is committed to `Σ'` in one indivisible step, and the system admits no observable intermediate state. Composite operations are sequences of elementary transitions, each atomic in isolation.

For K.γ, atomicity means that the `n` new bindings `(v_{t,k}, a_k)` for `k = 1, ..., n` all appear in `M'(d_t)` simultaneously, or none of them do. A reader observing `M(d_t)` between two consecutive transitions cannot see a partially-completed K.γ.

  AT (Atomicity). For K.γ with effect adding `n` new bindings to `M(d_t)`:
       Either `(A k : 1 ≤ k ≤ n : M'(d_t)(v_{t,k}) = a_k)` (all committed)
       or `(A k : 1 ≤ k ≤ n : v_{t,k} ∉ dom(M'(d_t)))` (none committed).
       No intermediate is observable.

The justification rests entirely on the substrate's atomicity axiom. K.γ adds no concurrency machinery of its own; it relies on the same total ordering of transitions that governs every other elementary operation.

## A Discovery in Reverse

Looking back at the analysis, we observe that the structural content of K.γ is almost entirely *negative*. The effect clause — bind `n` new V→I pairs in `M(d_t)` — is the same shape as any K.μ⁺ extension. The frame — preserve `C`, preserve `L`, preserve all other arrangements — is the same shape as the K.μ⁺ frame. What distinguishes K.γ from a fresh-content K.μ⁺ is the additional fact that the I-addresses bound were drawn from an existing arrangement, not allocated in this event.

This is the formal capture of Nelson's "the word 'copy' is perhaps unfortunate." There is no copy operation in the literal sense. There is allocation (K.α), which writes new content. There is arrangement extension (K.μ⁺), which writes new bindings. The combination — allocate, then bind — is INSERT. The bind-without-allocate alone is COPY. The character of COPY is exhausted by the *absence* of the K.α coupling.

The bytes do not move because nothing tells them to move. The source is unchanged because nothing writes to it. The I-addresses are preserved because they are read intact and written intact, never recomputed. Identity flows through chains because each link in the chain merely reads and writes the same tumbler. Origin is recoverable because origin lives in the tumbler's structure and the tumbler is never modified. All these properties are corollaries of the single decision to model COPY as K.μ⁺ without K.α.

That decision, in turn, is the formalisation of Nelson's reference architecture. By making COPY structurally a Vstream-only operation, the system makes "duplication" a non-event: there is no operation in the vocabulary that can do it. Whatever "the same content in two places" might mean colloquially, in this substrate it means precisely that two V-positions bind the same I-address. There is one place — the I-address in dom(C) — and two pointers.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| K.γ | COPY transition: extends `M(d_t)` with V→I mappings drawn from `M(d_s)` without altering `dom(C)`. | introduced |
| IP1 | Identity Preservation: target I-addresses are identical (as tumblers) to source I-addresses. | introduced |
| SI1 | Source arrangement preserved: `M'(d_s) = M(d_s)`. | introduced |
| SI2 | Source content values preserved: `C'(M'(d_s)(v)) = C(M(d_s)(v))` for every `v ∈ dom(M(d_s))`. | introduced |
| SI3 | Source content origins preserved: `origin(M'(d_s)(v)) = origin(M(d_s)(v))` for every `v ∈ dom(M(d_s))`. | introduced |
| ED | Extension Displacement: the trailing edge of the target subspace shifts by `n`; nothing else shifts. | introduced |
| M2P | Multi-Position Sharing: distinct V-positions may bind the same I-address after K.γ. | introduced |
| TR | Chain Transitivity: I-address identity is preserved through arbitrary K.γ chains. | introduced |
| OR | Origin Recoverability: `origin(a)` is preserved across K.γ; origin is determined by `a`'s tumbler structure. | introduced |
| RUN | Run Decomposition: source correspondence runs become target correspondence runs without consolidation; per-run widths, I-coordinates, and ordering are preserved. | introduced |
| MS | Multi-Source Independence: in a multi-source COPY, per-I-address origin is structurally recoverable; distinct origins do not merge. | introduced |
| SC | Self-Copy Consistency: source bindings unchanged, new bindings disjoint, atomic. | introduced |
| ¬C1–¬A1 | Negative frame: no content created, no content destroyed, no value altered, no document created, no source change, no other document change, no link change, no origin change, no allocator advance. | introduced |
| IM1–IM11 | Invariant preservation obligations K.γ must discharge over `M(d_t)` (functionality, referential integrity, finiteness, depth, sequentiality), `C` (immutability, permanence), source preservation, origin invariance, and composite couplings. | introduced |
| AT | Atomicity: all `n` new bindings commit simultaneously or none do; no observable intermediate. | introduced |

## Open Questions

What must abstract COPY guarantee when the source V-range includes positions whose I-addresses have been removed from arrangement (deleted) but persist in `dom(C)`?
Under what conditions may target correspondence runs merge with pre-existing adjacent runs in `M(d_t)`, and is such merging observable to subsequent queries?
What invariants must hold for a COPY composite that couples K.γ with K.ρ to record provenance in `Σ.R`?
How must abstract COPY behave when the source arrangement is concurrently being modified by another transition (assuming concurrency is admitted at the substrate level)?
What additional structural conditions on source and target arrangements would permit COPY to satisfy a stronger "single bound representation" guarantee — that the entire copied region appears as one maximal run in the target's decomposition?
What is the abstract characterisation of the inverse problem — given a target arrangement, which subranges could have originated from a COPY event versus an INSERT event, and is this distinction structurally decidable?
What guarantees must COPY preserve when the source document is itself removed from `dom(M)` after a chain of COPYs has propagated its I-addresses into many other documents?
