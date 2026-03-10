# ASN-0027: Address Permanence

*2026-03-10*

We are looking for the precise content of the promise "permanent address." Nelson states: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The foundations have given us the atomic invariants — P0 (immutability), P1 (monotonicity), NO-REUSE (ASN-0026) — and the allocation discipline (T8, T9 from ASN-0001). These are per-transition properties of the state. But permanence is a *system-level* guarantee: it concerns what all operations, taken jointly, may and may not do to address assignments. Our task is to develop this joint guarantee, identify its boundary, and derive the consequences.

---

## Three Layers of Permanence

We observe that "permanent address" conflates three distinct properties. To separate them, consider a user who stores a reference to I-address `a` — perhaps in a link endset, a citation, or a transclusion record. That user needs three things.

**Validity.** The address `a` remains in `dom(Σ.I)` across all future states. This is P1 (ISpaceMonotone), applied inductively over any sequence of transitions. Once an address enters I-space, no operation removes it.

**Immutability.** The content at `a` never changes: `a ∈ dom(Σ.I) ⟹ Σ'.I(a) = Σ.I(a)` for every transition. This is P0 (ISpaceImmutable). The byte at `a` today is the byte at `a` forever.

**Accessibility.** The address `a` can be *retrieved through a document* — some document's V-space currently maps a position to `a`. This is sharply different from the first two.

We make the third layer precise.

> **Definition (Reachable).** An I-address `a` is *reachable* in state `Σ` iff
>
>     reachable(a, Σ)  ≡  refs(a) ≠ ∅
>
> where `refs(a) = {(d, p) : d ∈ Σ.D ∧ 1 ≤ p ≤ n_d ∧ Σ.V(d)(p) = a}` (from ASN-0026).

Validity and immutability are *unconditional architectural invariants*. They hold for all content, for all time, by the structure of I-space. Accessibility is *contingent* — it depends on what operations users perform.

> **A0** (ReachabilityNonPermanent). There exist transitions `Σ → Σ'` such that `reachable(a, Σ) ∧ ¬reachable(a, Σ')`.

Nelson acknowledges the resulting state directly: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" The bytes exist in I-space. The address is valid. The content is immutable. But no document's current arrangement includes them.

This three-layer separation is the central insight. The architecture guarantees the first two layers unconditionally. The third requires mechanisms above the architecture — versioning, publication contracts, franchise obligations — to sustain.

---

## The I-Space Frame

We now establish the master invariant: every primitive operation preserves I-space completely. ASN-0026 classified operations by their I-space effect (`+_ext`). We sharpen that classification into a frame condition.

> **A1** (ISpaceFrame). For each primitive operation, the I-space transition is:
>
> | Operation | I-space transition |
> |-----------|-------------------|
> | INSERT | `Σ'.I = Σ.I ∪ {(a_j, c_j) : 1 ≤ j ≤ k}`, each `a_j ∉ dom(Σ.I)` |
> | DELETE | `Σ'.I = Σ.I` |
> | REARRANGE | `Σ'.I = Σ.I` |
> | COPY | `Σ'.I = Σ.I` |
> | CREATENEWVERSION | `Σ'.I = Σ.I` |

Four of the five operations leave I-space *literally unchanged* — the same domain, the same values. INSERT is the sole operation that extends I-space, and it does so only with fresh addresses disjoint from the existing domain (by GlobalUniqueness from ASN-0001).

The consequence is immediate and strong: **no sequence of operations can modify, remove, or reassign any I-space address.** The function `Σ.I` is a permanent, monotonically growing record. Every byte ever created persists exactly as created, at exactly the address where it was created.

Gregory's evidence confirms this exhaustively. DELETE operates exclusively on the POOM (V→I mapping), never touching the granfilade (I-space storage). REARRANGE modifies only V-displacements — the I-displacement field of each POOM entry is not written. COPY creates new POOM entries pointing to existing I-addresses without allocating new content. The granfilade is append-only; only INSERT writes to it.

---

## DELETE

DELETE is the operation most directly in tension with permanence. It removes content from a document. We must specify what exactly it removes — and what it does not.

> **A2** (DeleteSpec).
>
> *Precondition:* `d ∈ Σ.D ∧ 1 ≤ p ∧ p + k − 1 ≤ n_d ∧ k ≥ 1`
>
> *Post (length):* `|Σ'.V(d)| = n_d − k`
>
> *Post (left frame):* `(A j : 1 ≤ j < p : Σ'.V(d)(j) = Σ.V(d)(j))`
>
> *Post (compaction):* `(A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))`
>
> *Frame (I-space):* `Σ'.I = Σ.I`
>
> *Frame (cross-document):* `(A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))`

The compaction clause deserves attention. V-space is always a dense interval `{1, ..., n_d}` — no gaps. When positions `p` through `p + k − 1` are removed, positions `p + k` through `n_d` shift leftward by `k` to close the gap. Nelson specifies this explicitly for INSERT: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." DELETE is the mirror: following positions decrease by the deleted width. Gregory confirms the mechanism: `tumblersub` on POOM V-displacements closes the gap.

What is absent from the specification matters as much as what is present. There is no mention of I-addresses being freed, released, or made available. The I-addresses that were mapped from the deleted V-positions still exist in I-space, unchanged. They have merely lost one route of access. We verify: P0 is preserved (I-space unchanged), P1 is preserved (`dom(Σ.I)` unchanged), P2 is preserved on the surviving V-space (every surviving position retains its original I-address, which is in `dom(Σ.I)` by the pre-state P2 and the I-space frame). P7 holds by the cross-document frame.

---

## REARRANGE, COPY, and CREATENEWVERSION

Three operations share a structural property: they affect V-space without creating new I-space content. Each preserves or extends the set of reachable I-addresses.

> **A3** (RearrangeIdentity). REARRANGE takes a document `d` and an ordered sequence of `m` cut positions `c_1 < c_2 < ... < c_m` with `m ∈ {3, 4}`. The cuts define segments of V-space; the operation transposes designated segments.
>
> *Precondition:* `d ∈ Σ.D ∧ m ∈ {3, 4} ∧ 1 ≤ c_1 < c_2 < ... < c_m ≤ n_d + 1`
>
> The cuts determine a bijection `σ` on `{1, ..., n_d}`:
>
> *Pivot (m = 3):* Segments `[c_1, c_2)` and `[c_2, c_3)` transpose:
>
>     σ(j) = j + (c_3 − c_2)      for c_1 ≤ j < c_2
>     σ(j) = j − (c_2 − c_1)      for c_2 ≤ j < c_3
>     σ(j) = j                     otherwise
>
> *Swap (m = 4):* Segments `[c_1, c_2)` and `[c_3, c_4)` transpose; the middle segment `[c_2, c_3)` shifts by the width difference:
>
>     σ(j) = j + (c_4 − c_2)                       for c_1 ≤ j < c_2
>     σ(j) = j + (c_4 − c_3) − (c_2 − c_1)        for c_2 ≤ j < c_3
>     σ(j) = j − (c_3 − c_1)                       for c_3 ≤ j < c_4
>     σ(j) = j                                      otherwise
>
> *Post (length):* `|Σ'.V(d)| = n_d`
>
> *Post (permutation):* `(A j : 1 ≤ j ≤ n_d : Σ'.V(d)(σ(j)) = Σ.V(d)(j))`
>
> *Post (range preservation):* `range(Σ'.V(d)) = range(Σ.V(d))`
>
> *Frame (I-space):* `Σ'.I = Σ.I`
>
> *Frame (cross-document):* P7

Range preservation follows from the permutation clause — a bijection preserves the multiset of values. We state it separately because it is the property that matters for permanence: the same I-addresses are reachable through document `d` before and after the operation. Both forms change only the arrangement within the affected range; positions outside `[c_1, c_m)` are identity-mapped. That `σ` is a bijection follows from the segment structure: for pivot, the images of `[c_1, c_2)` and `[c_2, c_3)` are two disjoint intervals covering `[c_1, c_3)` exactly; for swap, the three moving segments' images are three disjoint intervals covering `[c_1, c_4)`.

Gregory's evidence confirms the cut-based interface: the backend accepts exactly 3 or 4 V-address cut points (`typecutseq`), sorts them via `sortknives`, and computes segment offsets via `makeoffsetsfor3or4cuts`. The rearrangement code path modifies only `cdsp.dsas[V]` (V-displacement). The I-displacement field `cdsp.dsas[I]` is never written by the displacement-adjustment step. The only path that touches I-displacements is tree restructuring during the cut phase — and there the absolute I-address is preserved, only the relative encoding changes when a crum moves to a new parent.

> **A4** (CopySharing). COPY from source document `d_s`, span `(p_s, k)`, to target document `d_t` at position `p_t` creates V-space mappings to the *same* I-addresses.
>
> *Precondition:* `d_s ∈ Σ.D ∧ d_t ∈ Σ.D ∧ k ≥ 1 ∧ 1 ≤ p_s ∧ p_s + k − 1 ≤ n_{d_s} ∧ 1 ≤ p_t ≤ n_{d_t} + 1`
>
> *Post (identity):* `(A j : 0 ≤ j < k : Σ'.V(d_t)(p_t + j) = Σ.V(d_s)(p_s + j))`
>
> *Post (length):* `|Σ'.V(d_t)| = n_{d_t} + k`
>
> *Post (left frame):* `(A j : 1 ≤ j < p_t : Σ'.V(d_t)(j) = Σ.V(d_t)(j))`
>
> *Post (right shift):* `(A j : p_t ≤ j ≤ n_{d_t} : Σ'.V(d_t)(j + k) = Σ.V(d_t)(j))`
>
> *Frame (I-space):* `Σ'.I = Σ.I`
>
> *Frame (source):* `Σ'.V(d_s) = Σ.V(d_s)` (when `d_s ≠ d_t`)

The identity clause is the heart of transclusion. The target document's V-space maps to the *same* I-addresses as the source. No new content is created. Two documents now share identity — the bytes in the target are not merely identical to the bytes in the source; they *are* the same bytes, at the same I-address, with the same origin, the same attribution, the same link attachments.

This is sharply distinct from INSERT, which always allocates fresh I-addresses. The distinction is semantic: COPY preserves identity (same origin, same provenance); INSERT creates new identity (different origin, independent provenance). Nelson: content identity is based on creation, not value. Two independently created identical passages have different I-addresses. Transcluded content shares the same I-address. Only COPY produces the latter.

Gregory confirms that COPY stores independent *value copies* of the I-displacement — each document's V→I mapping is independently owned, with no pointer sharing. Mutation of one document's POOM cannot corrupt another's. But the values themselves are the same I-addresses, and this identity is what makes transclusion work.

> **A5** (VersionIdentitySharing). CREATENEWVERSION creates a new document whose V-space maps, position by position, to the same I-addresses as the original.
>
> *Post (new document):* `d' ∈ Σ'.D ∧ d' ∉ Σ.D`
>
> *Post (identity):* `|Σ'.V(d')| = n_d ∧ (A j : 1 ≤ j ≤ n_d : Σ'.V(d')(j) = Σ.V(d)(j))`
>
> *Frame (original):* `Σ'.V(d) = Σ.V(d)`
>
> *Frame (I-space):* `Σ'.I = Σ.I`

The new version is a new *view* — a fresh V-space arrangement — over *existing* I-space content. No content is duplicated. The two documents share I-addresses, which means correspondence between them is immediate: every position in the version corresponds to the same position in the original, because both map to the same I-address. Nelson's `correspond` relation (ASN-0026) gives `correspond(d, j, d', j) = true` for all `1 ≤ j ≤ n_d` in the post-state.

This is the mechanism that makes version comparison work. Nelson: "a facility that holds multiple versions of the same material is not terribly useful unless it can help you intercompare them in detail." If CREATENEWVERSION allocated fresh I-addresses (like INSERT), correspondence would be undetectable — there would be no structural basis for determining which bytes "are the same."

---

## The Non-Invertibility of Deletion

We are now in a position to formalize an observation made in ASN-0026: DELETE followed by INSERT is not a no-op.

> **A6** (NonInvertibility). Let `Σ_0.V(d)(p + j) = a_j` for `0 ≤ j < k`. Let `Σ_1 = DELETE(Σ_0, d, p, k)`. Let `Σ_2 = INSERT(Σ_1, d, p, k, c)` for any content `c`. Then:
>
>     (A j : 0 ≤ j < k : Σ_2.V(d)(p + j) ≠ a_j)

*Proof.* INSERT allocates fresh I-addresses `a'_j` for the `k` new positions (P9-new from ASN-0026). By `+_ext`, `{a'_j} ∩ dom(Σ_1.I) = ∅`. Since A2 gives `Σ_1.I = Σ_0.I`, we have `dom(Σ_1.I) = dom(Σ_0.I)`. Each `a_j ∈ dom(Σ_0.I)` by P2 applied to the pre-state. Therefore `a'_j ∉ dom(Σ_0.I)`, and in particular `a'_j ≠ a_j`. Since `Σ_2.V(d)(p + j) = a'_j` (by P9-new), we have `Σ_2.V(d)(p + j) ≠ a_j`. ∎

The V-space positions may be numerically restored. The content bytes may even be identical. But the I-space *identity* is different. Every link, transclusion, and correspondence relationship that depended on addresses `a_0, ..., a_{k-1}` does not attach to the newly inserted content. The I-address at position `p + j` in `Σ_2` differs from the I-address at position `p + j` in `Σ_0`: `Σ_2.V(d)(p + j) ≠ Σ_0.V(d)(p + j)` for all `0 ≤ j < k`.

We trace this through a concrete state. Let `Σ_0.V(d) = [a_1, a_2, a_3, a_4, a_5]` with each `a_i ∈ dom(Σ_0.I)`. DELETE(d, 2, 2) yields `Σ_1.V(d) = [a_1, a_4, a_5]` — A2's left frame preserves position 1, compaction shifts positions 4–5 to positions 2–3, and `|Σ_1.V(d)| = 3`. INSERT(Σ_1, d, 2, 2, "XY") yields `Σ_2.V(d) = [a_1, a'_1, a'_2, a_4, a_5]` where `a'_1, a'_2 ∉ dom(Σ_0.I)` by freshness. Verify: `a'_1 ≠ a_2` and `a'_2 ≠ a_3`, since `a_2, a_3 ∈ dom(Σ_0.I)` by P2 and the fresh addresses are disjoint from `dom(Σ_0.I)`. The bytes at positions 2–3 may be identical to the original, but identity is lost.

This is not a flaw but an architectural commitment. The system distinguishes *identity* (same I-address, same origin, same provenance chain) from *coincidence* (same bytes, different origin). DELETE+INSERT produces coincidence. Only COPY preserves identity.

---

## Restoration Through Shared Identity

If DELETE+INSERT cannot restore identity, what can?

> **A7** (IdentityRestoringCopy). Let `Σ_0.V(d)(p + j) = a_j` for `0 ≤ j < k`. Let `Σ_1 = DELETE(Σ_0, d, p, k)`. Suppose there exists a document `d'` such that `Σ_1.V(d')(q + j) = a_j` for `0 ≤ j < k` — that is, `d'` still maps to the original I-addresses. Let `Σ_2 = COPY(d', (q, k), d, p)` in state `Σ_1`. Then:
>
>     (A j : 0 ≤ j < k : Σ_2.V(d)(p + j) = a_j)

*Proof.* By A2 (cross-document frame), DELETE on `d` does not modify `Σ.V(d')`. So `Σ_1.V(d')(q + j) = a_j` holds. We verify the precondition of A4 for COPY in state `Σ_1`: `d' ∈ Σ_1.D` (unchanged by DELETE on `d`), `d ∈ Σ_1.D`, `k ≥ 1` (given), `1 ≤ q` and `q + k − 1 ≤ |Σ_1.V(d')|` (the source span is valid in `d'`). For the target: `|Σ_1.V(d)| = n_d − k` (by A2 length), and `p ≤ n_d − k + 1` since the original precondition of A2 gives `p + k − 1 ≤ n_d`, so `p` is a valid insertion point. By A4 (identity sharing), COPY maps positions `p + j` in `d` to the same I-addresses as positions `q + j` in `d'`. Therefore `Σ_2.V(d)(p + j) = Σ_1.V(d')(q + j) = a_j`. ∎

We now derive that A7 yields *full* document restoration — not just the `k` deleted positions but the entire V-space.

> **Corollary** (Full restoration). Under the conditions of A7, `Σ_2.V(d) = Σ_0.V(d)`.
>
> *Left frame.* For `1 ≤ j < p`: A4 (left frame) gives `Σ_2.V(d)(j) = Σ_1.V(d)(j)`, and A2 (left frame) gives `Σ_1.V(d)(j) = Σ_0.V(d)(j)`. Therefore `Σ_2.V(d)(j) = Σ_0.V(d)(j)`.
>
> *Restored positions.* For `p ≤ j < p + k`: A7 gives `Σ_2.V(d)(j) = a_{j−p} = Σ_0.V(d)(j)`.
>
> *Right frame.* For `p + k ≤ m ≤ n_d`: A4 (right shift) gives `Σ_2.V(d)(m) = Σ_1.V(d)(m − k)`, and A2 (compaction) gives `Σ_1.V(d)(m − k) = Σ_0.V(d)(m)`. Therefore `Σ_2.V(d)(m) = Σ_0.V(d)(m)`.
>
> *Length.* `|Σ_2.V(d)| = |Σ_1.V(d)| + k = (n_d − k) + k = n_d`.
>
> The three ranges `[1, p)`, `[p, p+k)`, `[p+k, n_d]` cover `{1, ..., n_d}`, and on each `Σ_2.V(d)` agrees with `Σ_0.V(d)`. ∎

This gives us the pattern for identity-preserving restoration: **create a version before editing, then COPY from the version to restore.** A5 (VersionIdentitySharing) ensures the version shares all I-addresses with the original. After editing the original, the version retains the pre-edit addresses. COPY from the version restores not merely the same bytes but the *same identity* — with all links, correspondence, and attribution intact.

The pattern is:

1. `d' = CREATENEWVERSION(d)` — `d'` shares all I-addresses with `d` (A5)
2. `DELETE(d, p, k)` — `d` loses positions; `d'` is unchanged (A2 cross-doc frame)
3. `COPY(d', (p, k), d, p)` — `d` recovers original I-addresses from `d'` (A7)

After step 3, the corollary establishes `Σ_2.V(d) = Σ_0.V(d)` — full correspondence is restored. DELETE+COPY-from-version is the identity-preserving undo. DELETE+INSERT is not.

Nelson designed this deliberately. CREATENEWVERSION is not merely a backup mechanism; it is the architectural prerequisite for non-destructive editing. Nelson: "for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version."

---

## Reference Permanence

We now state the strongest consequence for external references.

> **A8** (ReferencePermanence). Let `a ∈ dom(Σ.I)`. For any finite sequence of operations producing state `Σ_n`:
>
> (i) `a ∈ dom(Σ_n.I)` — the address remains valid
>
> (ii) `Σ_n.I(a) = Σ.I(a)` — the content is unchanged
>
> (iii) Any reference expressed as I-address `a` resolves to content by evaluating `Σ_n.I(a)`

*Proof.* By induction on the sequence length. Base: `n = 0`, trivial. Step: assume (i)–(iii) hold at `Σ_k`. By A1, either `Σ_{k+1}.I = Σ_k.I` (identity operations) or `Σ_{k+1}.I = Σ_k.I ∪ fresh` (INSERT). In both cases `a ∈ dom(Σ_k.I)` implies `a ∈ dom(Σ_{k+1}.I)` and `Σ_{k+1}.I(a) = Σ_k.I(a) = Σ.I(a)`. ∎

This is the guarantee that makes Nelson's "web of literature" possible. A link created today, referencing I-address `a`, resolves to the same content in every future state. The content may be edited out of every document's current V-space — deleted, rearranged away, superseded by new versions — but the link still resolves. The content is still there, unchanged, at the same address.

Nelson: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them."

The phrase "if any of the bytes are left" refers to V-space presence — whether the linked content appears in some document's current view. A8 strengthens this to the I-space level: the link's target is always *defined*, because I-space never loses content. The link always *resolves*. Whether the resolved content is currently *displayed in a document* is a separate question — the accessibility question.

---

## The Boundary: Accessibility

We return to the distinction between existence and accessibility. A8 guarantees that references always resolve against I-space. But the user experience — seeing content in a document — depends on V-space reachability, and that is not permanent.

> **A9** (ReachabilityDecay). If `reachable(a, Σ)`, then there exists a finite sequence of operations producing `Σ'` with `¬reachable(a, Σ')`.

*Proof.* Let `D_a = {d : (E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)}` be the set of documents referencing `a`. We process documents one at a time. For each `d ∈ D_a`, let `r_d = |{p : 1 ≤ p ≤ n_d ∧ Σ.V(d)(p) = a}|` be the count of positions in `d` mapping to `a`. Repeatedly delete the *lowest*-numbered position mapping to `a` in `d`. Each such DELETE reduces `r_d` by exactly one: A2's compaction shifts higher positions leftward, preserving the I-address at each surviving position, so the remaining positions mapping to `a` are renumbered but still present. After `r_d` deletions on `d`, no position in `d` maps to `a`. By A2 (cross-document frame), these deletions on `d` do not modify `Σ.V(d')` for any `d' ≠ d`, so the references in other documents persist until their turn. After processing all documents in `D_a`, `refs(a) = ∅`. By A1 (ISpaceFrame), `a ∈ dom(Σ'.I)` — the content exists but is unreachable. ∎

Note the asymmetry. Each deletion is a separate operation with a specific write target (A2). The sequence of `m` deletions across `m` documents is a *coordinated* effort — it requires access to every document that references `a`. For published content with many transclusions, this coordination is difficult by design.

For *private* content, reachability decay is by design — the owner may withdraw content from their document. For *published* content, Nelson imposes an additional obligation outside the architecture:

> **A10** (PublicationObligation). For content that has been published, the system should maintain `reachable(a, Σ)` across all states. Nelson: "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process."

This obligation is *contractual*, not architectural. The architecture permits DELETE on any V-space position — it does not check publication status. Enforcement comes from the publication protocol, franchise obligations, and economic incentives (storage rental, per-byte delivery charges). The architecture provides the *mechanism* for permanent accessibility — I-space never loses content, versions preserve I-addresses for COPY restoration, the franchise distributes content across servers for resilience — but it does not *enforce* accessibility by preventing deletion.

The separation is deliberate. Nelson recognizes that perpetual accessibility requires perpetual funding: "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily." The architecture guarantees that accessibility is always *recoverable* (the content still exists in I-space and can be re-linked via COPY from any document that retains the I-addresses), but not that it is *maintained without effort*.

---

## The Permanence Summary

We can now state the full permanence guarantee as three interlocking properties:

**What no operation can do:**
- Remove an I-address from `dom(Σ.I)` — A1, all operations
- Change the content at an I-address — A1, all operations
- Cause two distinct pieces of content to share an I-address — GlobalUniqueness (ASN-0001)
- Modify any document's V-space other than the operation's write target — A2/A3/A4/A5 cross-document frames

**What only INSERT can do:**
- Extend `dom(Σ.I)` with fresh addresses — A1

**What only DELETE can do:**
- Reduce `|refs(a)|` — A9; all other operations either preserve or increase reachability

This classification is exhaustive. We verify: INSERT adds V-space mappings (to fresh I-addresses) and extends I-space — it cannot reduce `|refs(a)|` for any pre-existing `a`, because it does not remove V-space mappings. COPY adds V-space mappings (to existing I-addresses) — it increases `|refs(a)|`. CREATENEWVERSION creates a new document with V-space mappings — it increases `|refs(a)|` for every `a` in the source's range. REARRANGE permutes V-space without changing the set of mapped I-addresses — `|refs(a)|` is unchanged for every `a`. Only DELETE removes V-space mappings, and it is the sole operation that can decrease `|refs(a)|`.

---

## Observation: Index Staleness

Gregory's evidence reveals a consequence of the I-space/V-space separation worth noting. An index structure that records "document `d` contains I-address `a`" at insertion time but does not update on deletion satisfies:

    actual(a) ⊆ INDEX(a)

where `actual(a) = {d : (E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)}`. The index returns a *superset* of documents currently containing `a`. At the time of INSERT or COPY, both `actual(a)` and `INDEX(a)` gain `d`. On DELETE, `actual(a)` loses `d` but `INDEX(a)` does not. The index can only grow relative to actuality, never shrink.

This is a design trade-off, not an architectural requirement. An implementation that updates the index on DELETE satisfies `actual(a) = INDEX(a)`. The abstract requirement is only *soundness*: the index must not miss a document that currently contains the content. False positives (stale entries) are acceptable because consumers can cross-check by attempting I-to-V resolution — if no V-position maps to the queried I-address, the reference is stale.

Gregory confirms: the spanfilade is write-only with respect to DOCISPAN entries. `FINDDOCSCONTAINING` queries the spanfilade directly with no POOM cross-check. The result is a superset. The consumer must filter.

---

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.reachable | `reachable(a, Σ) ≡ refs(a) ≠ ∅` — whether an I-address is accessible through any document | introduced |
| A0 | Reachability is not permanent: transitions exist where `reachable(a)` goes from true to false | introduced |
| A1 | Every primitive operation preserves I-space; only INSERT extends it with fresh addresses; the other four leave `Σ.I` identical | introduced |
| A2 | DELETE removes `k` positions from V-space, compacts remaining positions leftward, leaves I-space and other documents unchanged | introduced |
| A3 | REARRANGE transposes V-space segments defined by 3 or 4 ordered cut positions, preserving the multiset of I-addresses | introduced |
| A4 | COPY creates V-space mappings in the target to the same I-addresses as the source, without I-space extension | introduced |
| A5 | CREATENEWVERSION creates a new document with position-by-position identical I-address mapping, no I-space extension | introduced |
| A6 | DELETE followed by INSERT at the same position does not restore original I-addresses: `Σ_2.V(d)(p+j) ≠ a_j` | introduced |
| A7 | COPY from a document retaining original I-addresses restores identity after deletion | introduced |
| A8 | Any reference to an I-space address resolves to unchanged content in all future states | introduced |
| A9 | Successive deletions can reduce `refs(a)` to `∅`, making content unreachable but not non-existent | introduced |
| A10 | For published content, maintaining reachability is a contractual obligation, not an architectural invariant | introduced |

---

## Open Questions

What invariants must the system maintain about unreferenced I-content (`refs(a) = ∅`) — must it be recoverable through a bounded number of version backtracks, or is unbounded search permitted?

Must the system guarantee that COPY-based identity restoration (A7) is always possible for published content — that is, must at least one version retaining the original I-addresses exist at all times?

What obligations does the franchise structure impose on storage providers regarding the accessibility of content whose owner has ceased paying storage rental?

Must the system distinguish between "content was never referenced by any document" and "content was referenced but all references were deleted" — are these observably different states, or only historically different?

Under what conditions may the publication obligation (A10) be relaxed — must the system provide a "due process" mechanism, and what must that mechanism guarantee about the content's state during the withdrawal process?

What must a correct content-discovery index guarantee about the relationship between `INDEX(a)` and `actual(a)` — is soundness (`actual(a) ⊆ INDEX(a)`) sufficient, or must the index converge toward exactness over time?

Must the system provide a mechanism to transition content from unreachable (`refs(a) = ∅`) back to reachable, or is the existence of COPY (A7) sufficient as the restoration mechanism?
