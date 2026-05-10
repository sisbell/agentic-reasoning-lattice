# ASN-0003: I-Space and V-Space

*2026-02-23*

We are looking for the invariant that connects permanent content storage to mutable document arrangement. The system maintains two address spaces — one for content identity, one for content presentation — and the relationship between them is the architectural foundation. We want to know: what must be true of this relationship for permanence, transclusion, and version reconstruction to hold?

**Scope.** This ASN models the text content subspace only. Link content occupies a separate subspace with its own structure (three endsets per link orgl, immutable once created). MAKELINK and its invariants are deferred to a future ASN. Consequences that depend on a formalized link model are noted as claims, not theorems.

---

## The Problem

A content system that permits editing faces a tension: content must be both *permanent* (for citation, attribution, and link survivability) and *rearrangeable* (for editing, versioning, and quotation). These are contradictory if content and arrangement occupy the same space. The resolution is to separate them.

We posit two spaces. **I-space** is the space of content identity — where bytes live permanently. **V-space** is the space of content arrangement — where a document's current presentation is defined. The central question is: what properties must the I-space/V-space separation satisfy for the system's guarantees to hold?

We proceed by deriving these properties from what the system must guarantee.

---

## The State

We need a model of what the system *is*, before we can reason about what it *maintains*.

Let `Σ` denote the system state. We introduce three components:

**IV-Σ1.** `Σ.I : Addr → Byte` is a partial function from I-space addresses to content bytes. The domain `dom(Σ.I)` is the set of all allocated I-addresses.

**IV-Σ2.** For each document-version `d`, `Σ.V(d) : Nat⁺ → Addr` is a total function from positive natural numbers (V-positions) to I-space addresses. The domain is `{1, ..., #Σ.V(d)}` where `#Σ.V(d)` is the document-version's current length. We write `n` for `#Σ.V(d)` when the document is clear from context.

**IV-Σ3.** `Σ.docs` is the set of all document-versions that currently exist.

The distinction is already visible: `Σ.I` grows monotonically (we shall prove this), while each `Σ.V(d)` changes freely under editing. But the connection between them — the fact that `Σ.V(d)` only ever points *into* `Σ.I` — is the invariant we are after.

Note that IV-Σ2 already specifies both the domain shape (dense contiguity: `{1, ..., n}`) and the functionality (total function: each position maps to exactly one address). These are not separate invariants — they are part of the definition of V-space.

---

## The Axioms

We now state the properties the system must maintain. These are the load-bearing assumptions — the independently assumed invariants from which all consequences follow.

**IV0 (Referential Integrity).** For all document-versions `d` and positions `p`:

    [d ∈ Σ.docs ∧ 1 ≤ p ≤ #Σ.V(d)  ⇒  Σ.V(d)(p) ∈ dom(Σ.I)]

That is: every position in a document's visible arrangement maps to an I-space address at which content exists. There are no dangling references. No V-position points into the void.

This is not a defensive check bolted on afterward — it is the property from which the system's guarantees flow. Nelson states it through the retrieval guarantee: "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." A system in which some V-positions resolve to nothing violates this unconditionally. The part-pounce model requires that every fragment "actually exists."

**IV1 (Content Permanence).** No operation removes an address from `dom(Σ.I)`:

    [a ∈ dom(Σ.I)  ⇒  a ∈ dom(Σ'.I)]

for any state transition `Σ → Σ'`. This is Nelson's append-only principle: "suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." I-space only grows.

The consequence for IV0 is immediate: if a V-position pointed to a valid I-address before some operation, and the operation does not remove I-addresses, then the V-position still points to a valid I-address afterward. IV1 is the *persistence* half of referential integrity.

**IV2 (Content Immutability).** The content at an I-address never changes:

    [a ∈ dom(Σ.I)  ⇒  Σ'.I(a) = Σ.I(a)]

for any transition `Σ → Σ'`. Once a byte is stored at address `a`, that byte is fixed forever. This is stronger than permanence — not only does the address remain allocated, but its content is frozen.

IV2 is what makes I-addresses meaningful as *identifiers*. If content could change, then knowing the address would not tell you what content you would find. Attribution, link attachment, version correspondence — all depend on the identity between address and content being eternal.

*Theorem (NO-REUSE).* Address reuse is impossible: once an I-address `a` is allocated with content `c`, no future state can assign different content to `a`.

*Proof.* Suppose `a ∈ dom(Σ.I)` with `Σ.I(a) = c`. By IV1, `a ∈ dom(Σ'.I)` for every successor state `Σ'` — the address is never freed. By IV2, `Σ'.I(a) = Σ.I(a) = c` — the content never changes. Together: the address remains permanently occupied with its original content. There is no state in which `a` is free for reallocation, and no state in which its content differs. Nelson is explicit: allocation "goes forward. It never retreats."  ∎

We observe that the allocation mechanism must produce addresses outside the current domain — this is a mechanism property, not a state invariant. The tumbler system achieves it through monotonic counters: each new allocation increments within its document's subtree, never revisiting previous values. Gregory confirms that allocation is document-isolated, meaning fresh allocation is a *family of independent functions partitioned by document* — a property that will matter when we consider concurrency.

---

## V-Space Properties

What must be true of V-space for IV0 to hold?

The state definition IV-Σ2 specifies that `Σ.V(d)` is a total function on `{1, ..., n}`. The non-injectivity of this mapping is not an axiom but a non-constraint — it states what is *not* required:

**Observation (V→I Non-Injectivity).** The same I-address may appear at multiple V-positions, both within a single document and across documents. `Σ.V(d)` is *not* required to be injective. This is the formal basis of transclusion. When content at I-address `a` appears at V-positions 5 and 47 in the same document, both `Σ.V(d)(5) = a` and `Σ.V(d)(47) = a` hold simultaneously. The same content is referenced twice without duplication.

Nelson's "glass pane" metaphor makes this vivid: a document is layers of painted glass with transparent windows. Two windows may look through to the same underlying content. The V-space structure records both references; I-space holds the content once.

---

## The Frame Conditions

Having established what the two spaces are, we now ask: what does each operation preserve? The frame conditions are as important as the effects — an operation that establishes its postcondition but silently violates a seemingly-unrelated invariant has not been correctly specified.

**IV8 (V-operations Preserve I-space).** No operation that modifies V-space alters I-space content:

    [(A a : a ∈ dom(Σ.I) : Σ'.I(a) = Σ.I(a))]

for any V-space operation (DELETE, REARRANGE, COPY) applied to any document. These operations modify the arrangement; they never touch the content. Nelson is definitive: "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

INSERT is special: it both extends I-space (allocating new addresses for the inserted content) and modifies V-space (placing the new content and shifting subsequent positions). But even INSERT satisfies IV8 for all *pre-existing* I-addresses — it adds to `dom(Σ.I)` without changing the content at any existing address.

We can state this more precisely. For any operation `op`:

    Σ'.I = Σ.I ⊕ fresh

where `⊕` denotes extension — `Σ'.I` agrees with `Σ.I` on all of `dom(Σ.I)` and may additionally be defined on new addresses `fresh` where `fresh ∩ dom(Σ.I) = ∅`. For DELETE, REARRANGE, and COPY, `fresh = ∅`. For INSERT, `fresh` is the set of newly allocated I-addresses.

**IV10 (Cross-Document V-Independence).** An operation on document `d` does not modify `Σ.V(d')` for any `d' ≠ d`:

    [op applied to d  ⇒  (A d' : d' ≠ d : Σ'.V(d') = Σ.V(d'))]

Each document's V-space is independent of every other's. Deleting content from document A has no effect on document B's arrangement, even if both reference the same I-addresses. This is what makes the system scale: documents are coupled only through shared I-space content, never through shared V-space state.

---

## Operation Definitions

Before we can verify that operations preserve our invariants, we must define precisely what each operation does to the state. We define five text-content operations.

**INSERT(d, p, b₁...bₖ)** — insert `k` bytes at position `p` in document `d`.

*Preconditions.* `d ∈ Σ.docs`, `k ≥ 1`, and `1 ≤ p ≤ n+1` where `n = #Σ.V(d)`. (When `p = n+1`, INSERT appends. When `n = 0` and `p = 1`, INSERT populates an empty document.)

*Effect on I-space.* Allocates fresh addresses `F = {f₁, ..., fₖ}` with `F ∩ dom(Σ.I) = ∅`, and defines `Σ'.I(fᵢ) = bᵢ` for `1 ≤ i ≤ k`. All pre-existing I-content is unchanged.

*Effect on V-space.* The new mapping `Σ'.V(d)` has domain `{1, ..., n+k}` and is defined by:

    Σ'.V(d)(q) = Σ.V(d)(q)          for 1 ≤ q < p        (unshifted)
    Σ'.V(d)(q) = f_{q-p+1}          for p ≤ q ≤ p+k-1    (new)
    Σ'.V(d)(q) = Σ.V(d)(q-k)        for p+k ≤ q ≤ n+k    (shifted)

*Frame.* `Σ'.V(d') = Σ.V(d')` for all `d' ≠ d`.

**DELETE(d, p, k)** — remove `k` bytes starting at position `p` from document `d`.

*Preconditions.* `d ∈ Σ.docs`, `k ≥ 1`, and `1 ≤ p` and `p+k-1 ≤ n`.

*Effect on I-space.* None. `Σ'.I = Σ.I`.

*Effect on V-space.* The new mapping `Σ'.V(d)` has domain `{1, ..., n-k}` and is defined by:

    Σ'.V(d)(q) = Σ.V(d)(q)          for 1 ≤ q < p        (below deletion)
    Σ'.V(d)(q) = Σ.V(d)(q+k)        for p ≤ q ≤ n-k      (closed gap)

Positions `p` through `p+k-1` are removed; positions above shift down by `k`.

*Frame.* `Σ'.V(d') = Σ.V(d')` for all `d' ≠ d`. `Σ'.I = Σ.I`.

**REARRANGE(d, cuts)** — swap two regions in document `d`. The cut set is either three or four V-positions.

*Three-cut form* `(c₁, c₂, c₃)` with `1 ≤ c₁ < c₂ < c₃ ≤ n+1`: swaps the contiguous regions `[c₁, c₂)` and `[c₂, c₃)`. Let `a = c₂ - c₁` (width of region 1) and `b = c₃ - c₂` (width of region 2). The new mapping `Σ'.V(d)` has domain `{1, ..., n}` (length is preserved) and is defined by:

    Σ'.V(d)(q) = Σ.V(d)(q)          for 1 ≤ q < c₁         (before swap)
    Σ'.V(d)(q) = Σ.V(d)(q+a-b)      for c₁ ≤ q < c₁+b      (region 2, moved left)
    Σ'.V(d)(q) = Σ.V(d)(q-b+a)      for c₁+b ≤ q < c₃      (region 1, moved right)
    Σ'.V(d)(q) = Σ.V(d)(q)          for c₃ ≤ q ≤ n          (after swap)

Equivalently: position `q` in region 2 maps to the I-address that was at `q - b + a` (shifted left by the difference), and position `q` in region 1's new location maps to the I-address that was at `q + a - b`.

*Four-cut form* `(c₁, c₂, c₃, c₄)` with `1 ≤ c₁ < c₂ ≤ c₃ < c₄ ≤ n+1`: swaps the non-contiguous regions `[c₁, c₂)` and `[c₃, c₄)`, with intervening content `[c₂, c₃)` repositioning to fill. Let `a = c₂ - c₁`, `b = c₄ - c₃`, `m = c₃ - c₂`. The new mapping `Σ'.V(d)` has domain `{1, ..., n}` and is defined by:

    Σ'.V(d)(q) = Σ.V(d)(q)                  for 1 ≤ q < c₁             (before)
    Σ'.V(d)(q) = Σ.V(d)(q + (c₃ - c₁))     for c₁ ≤ q < c₁+b         (region 2)
    Σ'.V(d)(q) = Σ.V(d)(q + a - b)          for c₁+b ≤ q < c₁+b+m    (middle)
    Σ'.V(d)(q) = Σ.V(d)(q - (c₃ - c₁))     for c₁+b+m ≤ q < c₄      (region 1)
    Σ'.V(d)(q) = Σ.V(d)(q)                  for c₄ ≤ q ≤ n            (after)

*Preconditions.* `d ∈ Σ.docs`. Cut values must satisfy the ordering constraints above and fall within `{1, ..., n+1}`.

*Effect on I-space.* None. `Σ'.I = Σ.I`.

*Frame.* `Σ'.V(d') = Σ.V(d')` for all `d' ≠ d`.

**COPY(d_s, p_s, k, d_t, p_t)** — copy `k` bytes from position `p_s` in source document `d_s` to position `p_t` in target document `d_t`. This is the transclusion operation: no new I-addresses are allocated.

*Preconditions.* `d_s, d_t ∈ Σ.docs`, `k ≥ 1`, `1 ≤ p_s` and `p_s+k-1 ≤ #Σ.V(d_s)`, and `1 ≤ p_t ≤ #Σ.V(d_t)+1`. Self-transclusion (`d_s = d_t`) is permitted.

*Effect on I-space.* None. `Σ'.I = Σ.I`.

*Effect on V-space (target).* Let `m = #Σ.V(d_t)`. The new mapping `Σ'.V(d_t)` has domain `{1, ..., m+k}` and is defined by:

    Σ'.V(d_t)(q) = Σ.V(d_t)(q)              for 1 ≤ q < p_t           (unshifted)
    Σ'.V(d_t)(q) = Σ.V(d_s)(p_s + q - p_t)  for p_t ≤ q ≤ p_t+k-1    (copied)
    Σ'.V(d_t)(q) = Σ.V(d_t)(q-k)            for p_t+k ≤ q ≤ m+k      (shifted)

Gregory confirms that COPY uses the identical V-space insertion path as INSERT: it shifts all subsequent V-content forward via the same mechanism. The only difference is the source of I-addresses — INSERT allocates fresh ones, COPY reuses existing ones.

*Frame.* `Σ'.V(d') = Σ.V(d')` for all `d' ∉ {d_t}`. If `d_s ≠ d_t`, then `Σ'.V(d_s) = Σ.V(d_s)` (the source is unchanged). If `d_s = d_t`, the copied positions reference the I-addresses that existed in `Σ.V(d_s)` before the shift — the copy reads from the pre-operation state.

**CREATENEWVERSION(d)** — create a new document-version `d'` from document `d`.

*Preconditions.* `d ∈ Σ.docs`.

*Effect on I-space.* None (for text content). `Σ'.I = Σ.I`.

*Effect on V-space.* `Σ'.V(d')(p) = Σ.V(d)(p)` for all `1 ≤ p ≤ #Σ.V(d)`. The new version initially references the same I-addresses — no content is duplicated.

*Frame.* `Σ'.V(d) = Σ.V(d)`. All other document-versions unchanged.

Nelson: versions are "the same materials" refracted through different arrangements — "there is thus no 'basic' version of a document set apart from other versions."

---

## The Coherence Theorem

We are now in a position to prove that all axioms are maintained by all operations. We must verify two things for each operation: (1) IV0 — every V-position in `Σ'` maps to a valid I-address, and (2) IV-Σ2 — the domain of `Σ'.V(d)` is `{1, ..., #Σ'.V(d)}` with no gaps or overlaps. We combine these into a single claim.

*Claim (PRES).* If `Σ` satisfies IV0 and IV-Σ2, and `Σ → Σ'` is a valid operation, then `Σ'` satisfies IV0 and IV-Σ2.

We reason by cases on the operation type.

**Case: INSERT(d, p, b₁...bₖ).**

*IV-Σ2 (contiguity).* We must show that `Σ'.V(d)` has domain `{1, ..., n+k}`. The definition partitions `{1, ..., n+k}` into three ranges: `{1, ..., p-1}` (unshifted), `{p, ..., p+k-1}` (new), `{p+k, ..., n+k}` (shifted). These are disjoint and their union is `{1, ..., n+k}` because they tile the interval: the unshifted range ends at `p-1`, the new range starts at `p` and ends at `p+k-1`, and the shifted range starts at `p+k` and ends at `n+k`. At each position in each range, the definition gives a value, so `Σ'.V(d)` is total on `{1, ..., n+k}`.

*Boundary cases.* When `p = 1`: the unshifted range `{1, ..., 0}` is empty. All original positions are shifted. The tiling becomes `∅ ∪ {1, ..., k} ∪ {k+1, ..., n+k} = {1, ..., n+k}`. When `p = n+1` (append): the shifted range `{n+k+1, ..., n+k}` is empty. All original positions are unshifted. The tiling becomes `{1, ..., n} ∪ {n+1, ..., n+k} ∪ ∅ = {1, ..., n+k}`. When `n = 0` and `p = 1`: both unshifted and shifted ranges are empty. Only the new range `{1, ..., k}` remains.

*IV0 (referential integrity).* For new positions `p ≤ q ≤ p+k-1`: `Σ'.V(d)(q) = f_{q-p+1} ∈ F ⊆ dom(Σ'.I)` by construction — the content is allocated in I-space before (or simultaneously with) the V-space mapping. For shifted positions `p+k ≤ q ≤ n+k`: `Σ'.V(d)(q) = Σ.V(d)(q-k)`. Since `p ≤ q-k ≤ n`, by IV0 on `Σ`, `Σ.V(d)(q-k) ∈ dom(Σ.I)`. By IV1, `dom(Σ.I) ⊆ dom(Σ'.I)`. For unshifted positions `1 ≤ q < p`: `Σ'.V(d)(q) = Σ.V(d)(q) ∈ dom(Σ.I) ⊆ dom(Σ'.I)`, same reasoning. For other documents: `Σ'.V(d') = Σ.V(d')` by IV10. Their V-positions pointed to valid I-addresses before, and IV1 keeps those addresses valid.

**Case: DELETE(d, p, k).**

*IV-Σ2 (contiguity).* The definition partitions `{1, ..., n-k}` into two ranges: `{1, ..., p-1}` (below deletion) and `{p, ..., n-k}` (closed gap). These are contiguous and their union is `{1, ..., n-k}`. Each position has a defined value: for `q < p`, `Σ.V(d)(q)` is defined by IV-Σ2 on `Σ`; for `q ≥ p`, `Σ.V(d)(q+k)` is defined because `p+k ≤ q+k ≤ n`.

*IV0.* For positions below `p`: unchanged, valid by IV0 on `Σ` and IV1. For positions at or above `p`: `Σ'.V(d)(q) = Σ.V(d)(q+k)` where `q+k ≤ n`, so `Σ.V(d)(q+k) ∈ dom(Σ.I) ⊆ dom(Σ'.I)`.

Gregory adds an important observation: after deletion, the POOM completely erases the V→I association — no structure remains that records which I-addresses were once referenced. But the I-addresses themselves persist in I-space. The association is erased *from the document's perspective*, not from the system's. This is precisely the separation of concerns: V-space forgets; I-space remembers.

**Case: REARRANGE(d, cuts) — three-cut form (c₁, c₂, c₃).**

*IV-Σ2 (contiguity).* The definition partitions `{1, ..., n}` into four ranges: before the swap `{1, ..., c₁-1}`, region 2 moved left `{c₁, ..., c₁+b-1}`, region 1 moved right `{c₁+b, ..., c₃-1}`, and after the swap `{c₃, ..., n}`. These are contiguous (each range's upper bound is one less than the next range's lower bound) and their union is `{1, ..., n}`, since `c₁ + b + a = c₁ + (c₃ - c₂) + (c₂ - c₁) = c₃`. Each position maps to a pre-operation position within `{1, ..., n}`: for region 2 moved left, `q + a - b = q + (c₂ - c₁) - (c₃ - c₂)`, which ranges over `{c₂, ..., c₃-1}` as `q` ranges over `{c₁, ..., c₁+b-1}`; for region 1 moved right, `q - b + a` ranges over `{c₁, ..., c₂-1}`.

*IV0.* Every position `q` in `Σ'.V(d)` maps to some position `q'` in `Σ.V(d)` where `1 ≤ q' ≤ n`. By IV0 on `Σ`, `Σ.V(d)(q') ∈ dom(Σ.I)`. By IV8, `dom(Σ'.I) = dom(Σ.I)` (REARRANGE does not touch I-space). Therefore `Σ'.V(d)(q) ∈ dom(Σ'.I)`.

*Edge cases.* When `c₁ = 1`: the "before" range is empty. When `c₃ = n+1`: the "after" range is empty. When `a = 0` (empty region 1, i.e. `c₁ = c₂`): region 1 moved right is empty; region 2 stays in place; REARRANGE is a no-op. Similarly when `b = 0`.

The four-cut form follows the same structure: five contiguous ranges tile `{1, ..., n}`, and each position maps to a valid pre-operation position. The intervening content shifts by `b - a` to accommodate the size difference between the swapped regions. When `a = b`, the middle region is stationary.

**Case: COPY(d_s, p_s, k, d_t, p_t).**

*IV-Σ2 (contiguity).* The argument is identical to INSERT's: three ranges tile `{1, ..., m+k}` where `m = #Σ.V(d_t)`.

*IV0.* For copied positions `p_t ≤ q ≤ p_t+k-1`: `Σ'.V(d_t)(q) = Σ.V(d_s)(p_s + q - p_t)`. Since `p_s ≤ p_s + q - p_t ≤ p_s + k - 1 ≤ #Σ.V(d_s)`, by IV0 on `Σ`, this I-address is in `dom(Σ.I)`. By IV1, `dom(Σ.I) ⊆ dom(Σ'.I)`. For shifted and unshifted positions: same reasoning as INSERT, using IV0 on `Σ` and IV1.

This is where non-injectivity becomes operationally relevant: COPY may cause the same I-address to appear at multiple V-positions (within the same document or across documents). IV-Σ2 is not violated because each V-position still maps to exactly one I-address — it is just that multiple V-positions may share that address.

**Case: CREATENEWVERSION(d).**

*IV-Σ2 (contiguity).* `Σ'.V(d')` has the same domain shape as `Σ.V(d)` by definition.

*IV0.* `Σ'.V(d')(p) = Σ.V(d)(p) ∈ dom(Σ.I) ⊆ dom(Σ'.I)` by IV0 on `Σ` and IV1.

This completes PRES. In each case, the argument has the same structure: newly created V-positions point to I-addresses that were just allocated or already existed, and IV1 ensures existing I-addresses persist. The uniformity of the proof is the sign that the invariant is well-chosen.  ∎

---

## The Monotonicity Theorem

From IV1, a structural theorem follows.

*Theorem (MON-I).* `dom(Σ.I)` is monotonically non-decreasing:

    [dom(Σ.I) ⊆ dom(Σ'.I)]

for any transition `Σ → Σ'`.

*Proof.* IV1 states that no operation removes addresses from `dom(Σ.I)`. Operations may add addresses (INSERT adds fresh ones; CREATENEWVERSION may allocate structural addresses). Therefore the domain only grows.  ∎

This is a one-line proof, but its consequence is profound: the set of things that exist never shrinks. Every I-address ever allocated, every byte ever stored, every identity ever created — all persist. The system accumulates content monotonically.

Note that V-space has no corresponding monotonicity. Documents grow and shrink freely. V-positions come and go. The total number of V-positions across all documents may decrease (through deletions). Monotonicity is an I-space property, not a system-wide property.

---

## Consequences

Having established the axioms and their preservation, we now derive the properties that motivate the entire design.

### Version Correspondence

When two versions share I-addresses (which they always do initially, by the definition of CREATENEWVERSION), the system can determine *which parts correspond* without metadata. Correspondence is structural: V-positions in version `d₁` and version `d₂` correspond when they map to the same I-address.

    correspond(d₁, p₁, d₂, p₂)  ≡  Σ.V(d₁)(p₁) = Σ.V(d₂)(p₂)

This is computable because both sides are deterministic lookups. Nelson: "a facility that holds multiple versions is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same."

If CREATENEWVERSION duplicated content (assigning fresh I-addresses), this correspondence would be impossible to compute — there would be no structural basis for determining which bytes are "the same." The entire version-comparison model depends on I-space sharing.

### Origin Traceability

Because I-addresses encode their origin structurally (the tumbler hierarchy includes node, user, document, and element fields), and because content immutability (IV2) means the address is *the* permanent identifier, the origin of any content is always recoverable.

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character."

This is not metadata that can be stripped or lost. It is the address itself. To retrieve content, the system must ask the home location. The connection between identity and origin is architectural.

### Attribution and Accounting

The non-injectivity of V→I (combined with COPY producing shared rather than fresh I-addresses) means the system can account for content usage. When document B transcludes content from document A, the shared I-addresses allow the system to trace the content back to A's home location. Nelson's royalty model depends on this: every byte delivered to a reader has a traceable origin, and that origin determines compensation.

### Link Survivability (Claim)

This property depends on a link model not formalized in this ASN, so we state it as a claim rather than a theorem. A link attaches to I-space addresses — not V-positions. When content is deleted from a document, only the V→I mapping is removed. The I-addresses persist (IV1), the content persists (IV2), and the link's endset addresses remain valid. More precisely, if a link `L` has endset addresses in `S ⊆ dom(Σ.I)`, then after any sequence of operations producing `Σ'`, we have `S ⊆ dom(Σ'.I)` by IV1, so the I-addresses the link references continue to exist. Whether the link itself remains *discoverable* depends on the link index structure, which is deferred.

Nelson foresaw this precisely: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing."

---

## The V→I Mapping as Document Identity

We observed that `Σ.V(d)` defines a document-version's content. But we should be more precise: a document-version *is* its V→I mapping. Two document-versions with the same mapping are, from the system's perspective, the same arrangement.

**IV11 (Viewer Independence).** The mapping `Σ.V(d)` is a property of the document-version, not the viewer:

    [(A viewers u₁, u₂ : Σ.V(d) as observed by u₁ = Σ.V(d) as observed by u₂)]

Two users requesting the same V-position in the same version receive the same I-space content. The back-end operation RETRIEVEV takes a document-version and a set of V-spans; it returns the corresponding I-space content deterministically. No viewer parameter exists in the protocol.

Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" — where "you" is universal.

Viewer experience may *diverge* — different users may view different versions (front-end choice), filter links differently (front-end presentation), or render content differently (front-end typography). But the V→I mapping itself, which is the back-end's responsibility, is viewer-invariant. The front end chooses *which* version to request; the back end serves *that* version's mapping deterministically.

This property is architecturally necessary for attribution, correspondence, and accounting to be well-defined. If the mapping varied by viewer, "the home document of any specific word" would be viewer-dependent — an indeterminacy fatal to every guarantee.

---

## Atomicity of State Transitions

We asserted that operations produce coherent new states. We now make this precise.

*Claim (ATOM).* Each operation transitions the system from one state satisfying IV0 to another state satisfying IV0, with no observable intermediate state that violates IV0:

    [IV0(Σ) ∧ op(Σ, Σ')  ⇒  IV0(Σ')]

There is no point at which a client can observe a V-position pointing to an unallocated I-address, or a gap in V-space, or an I-address whose content is partially written. Nelson does not use the word "atomic," but his operation descriptions and retrieval guarantees require it.

Consider INSERT: Nelson specifies that the command inserts text at a position *and* shifts all following addresses as part of one operation. If only one happened — content placed but addresses not shifted, or addresses shifted but no content placed — the V-space would be inconsistent (gap or overlap). The canonical order mandate confirms this: "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." The phrase "once made" implies the transition is complete — there is no observable state where the file is not in canonical order.

We note that ATOM is a restatement of PRES in operational terms — PRES proves the state-to-state transition property; ATOM adds the observability condition that no intermediate state is visible. The observability condition is an implementation concern: Gregory reveals that the implementation achieves it through single-threaded execution (a `select()` event loop) rather than through a transactional mechanism. The abstract property (no intermediate state visible to clients) is implementation-independent; the mechanism (single thread vs transactions vs locks) is implementation-specific.

A consequence of atomicity and IV-Σ2: for any operation that extends both I-space and V-space (i.e., INSERT), the I-space extension must be established before or atomically with the V-space mapping. If the V-space mapping were created first, there would be a transient state violating IV0. Gregory confirms the ordering: fresh I-addresses are allocated before POOM mappings are created.

---

## The Deletion Asymmetry

We have shown that DELETE removes V-space mappings while preserving I-space content. But the implications of this asymmetry deserve explicit treatment.

After DELETE of positions `p` through `p+k-1` from document `d`:

1. `Σ'.V(d)` no longer maps any position to the I-addresses that were at those positions (the V→I association is erased)
2. Those I-addresses remain in `dom(Σ'.I)` (by IV1)
3. Their content is unchanged (by IV2)

The content has not been destroyed. It has been made *unreachable from this document*. Other documents that reference the same I-address are unaffected (IV10). Previous versions of the document still reference the content (their V-spaces are independent snapshots).

Nelson distinguishes this from conventional deletion: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" The bytes are "not currently addressable" in V-space — they have been removed from the document's visible arrangement. But they remain permanently addressable in I-space.

We observe that *DELETE is not the inverse of INSERT*. If we INSERT content (allocating I-addresses `F`), then DELETE it, then INSERT identical bytes, the second INSERT allocates *fresh* I-addresses `F' ≠ F` (by NO-REUSE and the allocation mechanism). The V-space looks the same, but the I-space identity is different. All links, transclusions, and correspondence relationships that attached to `F` do not attach to `F'`. The identity has been severed.

This is not a deficiency — it is a consequence of the fundamental design. Addresses are permanent and unique (NO-REUSE). The only way to restore a severed I-space identity is through COPY from a document that still references the original I-addresses.

---

## The Referent Set

For an I-address `a ∈ dom(Σ.I)`, define the *referent set* across the entire system:

    refs(a) = {(d, p) : d ∈ Σ.docs ∧ 1 ≤ p ≤ #Σ.V(d) ∧ Σ.V(d)(p) = a}

This is the set of all (document, position) pairs that currently reference `a`. The set may be empty (the address exists in I-space but no document currently displays it), a singleton (one document at one position), or arbitrarily large (many documents transcluding the same content).

*Theorem (REF-IND).* Deleting content from one document removes exactly the affected pairs from the referent set; all other references are unaffected.

*Proof.* DELETE(d, p, k) modifies only `Σ.V(d)` (by IV10, all other documents are unchanged). The deleted positions `p` through `p+k-1` are removed from `Σ.V(d)`; the remaining positions are shifted but their I-address mappings are unchanged. Therefore `refs'(a) = refs(a) \ {(d, q) : p ≤ q ≤ p+k-1 ∧ Σ.V(d)(q) = a}`. No document has privileged access to the I-address — even the document that originally allocated it cannot destroy references from other documents. Permanence is system-wide, not owner-controlled.  ∎

Nelson is emphatic: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

### The Empty Referent Set

When `refs(a) = ∅`, the I-address `a` has no current V-space references. But `a ∈ dom(Σ.I)` by IV1 — the content persists. This is the state Nelson calls "not currently addressable, awaiting historical backtrack functions."

Such addresses are *unreachable* through normal V-space traversal but *reachable* through I-space queries (if you know the address) or historical reconstruction (if a previous version's V-space referenced them). The system never garbage-collects I-space.

---

## The Width Invariant

A technical observation from Gregory's evidence deserves formal treatment. In the implementation's POOM, each entry stores both a V-width and an I-width. At creation, these encode the same logical magnitude (the number of bytes in the span). But they use different tumbler exponents — V-width reflects insertion depth in the tumbler hierarchy, while I-width uses flat addressing.

Gregory reveals that after certain operations (specifically, crum extension when crums from different V-depths are combined), the V-width and I-width can *diverge* in their tumbler representation. The I-width remains authoritative for character count; the V-width represents tumbler-space extent, which is a different concept.

This is an implementation observation, not an abstract property. The abstract model has `Σ.V(d) : Nat⁺ → Addr`, which maps positions to addresses without any notion of "width." Width is a compression mechanism in the enfilade — a way to represent many individual mappings as a single (start, width) entry. The abstract model does not need it.

But the observation illuminates why the domain shape must be stated as part of the state definition (IV-Σ2): the implementation's internal representation does not trivially guarantee it. The enfilade's width-based compression introduces the possibility of representational divergence. An alternative implementation that uses a different data structure (e.g., a flat array) would not face this issue, but would still need to satisfy IV-Σ2.

---

## The Two-Space Architecture as a Design Claim

We have derived four axioms (IV0, IV1, IV2, IV8/IV10), proved their preservation under all text-content operations, and derived consequences for version correspondence, origin traceability, attribution, and link survivability. But they all follow from a single architectural decision: *separate content identity from content arrangement*. If we had one space that served both purposes, we could not have:

- Permanence (because editing would modify content)
- Transclusion (because sharing would require duplication)
- Link survivability (because links would break when content moved)
- Version correspondence (because versions would have independent copies)
- Origin traceability (because addresses would change)

The I-space/V-space separation is not one feature among many — it is the architectural commitment from which all other guarantees flow.

We summarize what has been established and what remains claimed:

*Established (proven from axioms and operation definitions):*

(a) **Permanence**: content survives all V-space operations — by IV1, IV2, IV8, verified per-operation in PRES.

(b) **Transclusion feasibility**: the V→I mapping permits multiple V-positions to share an I-address — by IV-Σ2's non-injectivity and COPY's definition (which preserves I-addresses rather than allocating fresh ones).

(c) **Version correspondence**: structural comparison across versions is computable — by CREATENEWVERSION's definition (which shares I-addresses with the source).

(d) **Retrieval guarantee**: every visible position resolves — IV0 directly, maintained by PRES.

*Claimed (depends on structures not formalized in this ASN):*

(e) **Link survivability**: links survive editing — requires a formalized link model (endsets, link index, MAKELINK operation). What we have established is that I-addresses referenced by link endsets persist (IV1), which is necessary but not sufficient. Discoverability depends on the link index.

(f) **Origin traceability**: every byte traceable to its creator — requires the tumbler hierarchy to encode provenance, which is an addressing-system property, not an I-space/V-space property per se. IV2 ensures the address is permanent; the address structure ensures it encodes origin.

---

## Properties Introduced

| Label | Statement | Kind |
|-------|-----------|------|
| IV-Σ1 | `Σ.I : Addr → Byte` is a partial function (I-space) | definition |
| IV-Σ2 | `Σ.V(d) : Nat⁺ → Addr` is a total function on `{1, ..., n}` per document-version | definition |
| IV-Σ3 | `Σ.docs` is the set of all document-versions | definition |
| IV0 | Referential Integrity: every V-position maps to an allocated I-address | axiom |
| IV1 | Content Permanence: no operation removes an address from `dom(Σ.I)` | axiom |
| IV2 | Content Immutability: content at an I-address never changes | axiom |
| IV8 | V-operations Preserve I-space: editing never alters existing I-space content | axiom |
| IV10 | Cross-Document V-Independence: editing `d` does not affect `Σ.V(d')` for `d' ≠ d` | axiom |
| IV11 | Viewer Independence: `Σ.V(d)` is viewer-invariant | axiom |
| NO-REUSE | Address reuse is impossible (from IV1 + IV2) | theorem |
| MON-I | `dom(Σ.I)` is monotonically non-decreasing (from IV1) | theorem |
| PRES | All operations preserve IV0 and IV-Σ2 | theorem |
| REF-IND | DELETE from one document removes exactly the affected referent pairs | theorem |
| ATOM | No intermediate state violating IV0 is observable | claim |

---

## Open Questions

What invariants must the system maintain when I-space content is distributed across multiple storage nodes?

Must the allocation-before-mapping ordering be strengthened to a durability guarantee — must the I-space write survive a crash before the V-space mapping becomes visible?

What must the system guarantee about the referent set `refs(a)` when `a` is unreferenced — must it be queryable, or only recoverable through exhaustive search?

Does the V-space contiguity property (IV-Σ2) extend to the version graph — must the set of versions itself be densely numbered, or can version identifiers have gaps?

What must the system guarantee about content at I-addresses that were allocated but never successfully mapped to any V-position (orphaned by a failed INSERT)?

Can two documents that independently INSERT identical byte sequences ever have their content share I-addresses, or must content identity be tied to the originating document?

What invariants must hold between the link index (spanfilade) and the V-space mappings (POOMs) when DELETE creates stale index entries that reference documents no longer containing the content?

What must MAKELINK preserve with respect to IV0 — does link creation modify the text-content V-space, or does it operate on a separate link subspace that requires its own invariant?
