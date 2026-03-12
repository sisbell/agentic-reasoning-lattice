# ASN-0030: Address Permanence

*2026-03-11*

We are looking for the precise content of the guarantee that Xanadu addresses are "permanent." Three foundation properties each assert something different: T8 (AddressPermanence, ASN-0001) says an address once assigned remains assigned; P0 (ISpaceImmutable, ASN-0026) says content at an I-address never changes; P1 (ISpaceMonotone, ASN-0026) says I-addresses are never freed. These are separate assertions about separate things. What is the combined guarantee? And — more delicately — what does it *not* guarantee?

The intuitive answer — "an address refers to the same content forever" — is correct but incomplete. It describes what IS permanent but not what ISN'T. We are looking for the boundary.

---

## Identity and Reachability

We begin by observing that "permanent address" conflates two independent properties. The first step is to separate them.

**Identity** is the timeless association between an I-address and its content. We write:

    identity(a) ≡ a ∈ dom(Σ.I)

and observe that when `a ∈ dom(Σ.I)`, the value `Σ.I(a)` is fixed forever (P0). Identity, once established, is a conservation law: it cannot be created conditionally, cannot degrade, cannot be revoked. P0 and P1 together give us the combined guarantee that we label A0.

**A0 (IdentityPermanence).** For any state transition Σ → Σ':

    [a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a)]

A0 is the conjunction of P0 and P1. We restate it as a single invariant because the consequences we derive use both parts in concert, and because the combined claim — identity at an I-address is permanent — is the one assertion the rest of this note depends upon.

**Reachability** is a different matter entirely. It is the ability to obtain content through a document's V-space arrangement. ASN-0026 defines `refs(a) = {(d, p) : d ∈ Σ.D ∧ 1 ≤ p ≤ n_d ∧ Σ.V(d)(p) = a}`. We introduce a predicate that captures the existential projection of this set:

    reachable(a, d) ≡ (E p : (d, p) ∈ refs(a))

which is equivalent to `(E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)` by unfolding the definition of `refs`. Address `a` is *reachable through document d* when some position in `d`'s V-space maps to `a`. The global form:

    reachable(a) ≡ refs(a) ≠ ∅

equivalently, `(E d : d ∈ Σ.D : reachable(a, d))`.

Now: is reachability permanent? It is not.

**A1 (ReachabilityNonMonotone).**

    ¬[reachable(a, d) in Σ ⟹ reachable(a, d) in Σ']

DELETE on document `d` can remove the V-space mappings that made `a` reachable through `d`. If `d` was the only document referencing `a`, then after DELETE, `reachable(a)` becomes false. Yet by A0, `a ∈ dom(Σ'.I)` and `Σ'.I(a)` is unchanged. The content exists; no protocol path delivers it.

This is the separation we are after. The delivery function RETRIEVE(d, p) computes Σ.I(Σ.V(d)(p)) (P3, ASN-0026). Delivery requires V-space membership — a document and a position within it. Content that exists in I-space but appears in no document's V-space is real but undeliverable through RETRIEVE. Nelson describes this state precisely: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" The phrase "not currently addressable" refers to V-space; the bytes remain in I-space, permanently, at the same address.

---

## The Accessibility Partition

With identity and reachability separated, we can classify the states an I-address may occupy. The address space T (all well-formed tumblers satisfying T4) is fixed and infinite. The allocated subspace dom(Σ.I) grows monotonically within it. At any given moment, a valid address falls into exactly one of three categories.

**A2 (AccessibilityPartition).** For any address `a` satisfying T4 and state Σ, exactly one of:

    (i)   a ∈ dom(Σ.I) ∧ reachable(a)       — active
    (ii)  a ∈ dom(Σ.I) ∧ ¬reachable(a)       — unreferenced
    (iii) a ∉ dom(Σ.I)                         — unallocated

These are exhaustive and mutually exclusive. Exhaustiveness requires ruling out the fourth combination: reachable ∧ ¬allocated. P2 (ReferentiallyComplete, ASN-0026) gives `Σ.V(d)(p) ∈ dom(Σ.I)` for every valid position, so `reachable(a) ⟹ a ∈ dom(Σ.I)`. Contrapositively, `a ∉ dom(Σ.I) ⟹ ¬reachable(a)` — the fourth case is impossible. Mutual exclusivity is immediate from the definitions. State (i) is the normal operational condition: content exists and at least one document displays it. State (ii) is Nelson's "DELETED BYTES" — content persists in I-space, but no V-space arrangement maps to it. State (iii) comprises the ghost elements: "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

The partition is over the state Σ — an address may transition between states as operations execute. But not all transitions are permitted.

**A3 (AccessibilityTransitions).**

    (a)  (iii) → (i):   permitted — allocation followed by insertion into a document
    (b)  (i) → (ii):    permitted — DELETE from all referencing documents
    (c)  (ii) → (i):    permitted — but see qualification below
    (d)  (i) → (iii):   forbidden — would violate P1
    (e)  (ii) → (iii):  forbidden — would violate P1
    (f)  (iii) → (ii):  achievable — via (a) then (b)

Note: A3 classifies which state-pairs are achievable, not single-step transitions. Transitions (a), (b), (d), and (e) are each achievable by a single operation. Transition (c) is permitted by the invariants but not achievable by any currently defined operation for truly unreferenced addresses — see qualification below. Transition (f) is composite: no single operation allocates an I-address without placing it in V-space. INSERT atomically allocates fresh I-addresses *and* inserts them into the target document (P9-new, P9-left, P9-right), so fresh content enters state (i) directly. The path to state (ii) requires a subsequent DELETE — that is, (iii)→(i) via INSERT, then (i)→(ii) via DELETE.

The forbidden transitions are the permanence guarantee stated negatively: content, once allocated, cannot become unallocated. The allocated set only grows; the address space never contracts. Gregory's implementation evidence is definitive on this point. The function `deleteseq` — the only code that could remove a granfilade entry and thereby reduce the I-space — is dead code: defined in `edit.c` but called nowhere in the system. No code path from DELETE reaches the granfilade. DELETE operates exclusively on the POOM (the V→I mapping), removing V-space positions while leaving I-space untouched.

Transition (b) is the critical one for understanding the system. A user deletes content from their document. The V-space contracts; positions shift (P9-right, ASN-0026, applied in reverse). The I-addresses that were at the deleted positions leave the document's V-space. If those I-addresses appear in other documents (via transclusion), they remain active. If they appear nowhere, they become unreferenced. Either way, the content at those I-addresses is unchanged — A0 applies regardless.

Transition (c) requires careful qualification. Nelson lists unreferenced content as "awaiting historical backtrack functions." We must distinguish two cases. If the I-address remains reachable in some other document or version — i.e., `refs(a) ≠ ∅` in the global state — then the content was never truly unreferenced (it was active, state (i), in another document), and COPY from that document recovers it into the target. This is the normal case: version creation (D12, ASN-0029) preserves all V-space mappings in the source, so content deleted from one version often remains reachable through another.

But if the I-address is in state (ii) — `refs(a) = ∅`, present in no document's V-space — then no currently defined operation recovers it. COPY requires a source position in some document's V-space (it reads through `specset2ispanset`); INSERT allocates only fresh I-addresses (P9-new, ASN-0026). Gregory's implementation confirms the constraint: every code path that writes an I-address into a document's POOM either allocates a fresh address through `inserttextingranf` or reads an existing address from another document's V-space through `specset2ispanset`. No path accepts a raw I-address for direct insertion.

Nelson's intent is clear: "The true storage of text should be in a system that stores each change and fragment individually... keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." The recovery mechanism is the historical trace enfilade — an index over the append-only I-space that reconstructs any previous arrangement on demand. This mechanism is consistent with our invariants (no operation would need to violate A0 or modify I-space) but is not yet specified. We record transition (c) as *permitted by the invariants* but *not achievable by any currently defined operation* for truly unreferenced addresses. The I-address is a permanent name; V-space is merely the question of who is currently using that name.

Transition (f) requires two operations: INSERT followed by DELETE. INSERT creates fresh I-addresses (P9-new, ASN-0026) and places them in d's V-space — state (i). A subsequent DELETE removes them from V-space before any other document transcludes them — state (ii). The content never enters state (ii) in a single step. This is a normal consequence of the separation: allocation is permanent, arrangement is editorial.

---

## A Worked Example

We trace identity and reachability through a concrete scenario to anchor the preceding definitions. Let document `d` have V-space mapping `Σ.V(d) = [a₁, a₂, a₃]` with `n_d = 3`, where `a₁, a₂, a₃ ∈ dom(Σ.I)` are distinct I-addresses. Suppose no other document references `a₂`: formally, `refs(a₂) = {(d, 2)}`. Both `a₁` and `a₃` appear also in some other document `d'`.

**DELETE position 2 from d.** After DELETE(d, 2, 1) producing Σ':

- *Identity:* By +_ext (ISpaceExtension, ASN-0026) with `fresh = ∅`, `Σ'.I = Σ.I`. By A0, `a₂ ∈ dom(Σ'.I)` and `Σ'.I(a₂) = Σ.I(a₂)`. The content is unchanged.
- *V-space:* `Σ'.V(d) = [a₁, a₃]` with `|Σ'.V(d)| = 2`. Position 2 now maps to `a₃` (P9-right applied in reverse).
- *Reachability of a₂:* `refs(a₂)` in Σ' is `∅` — `d` no longer maps to `a₂`, and no other document did. The address transitions from active (i) to unreferenced (ii).
- *Reachability of a₁, a₃:* Both remain in `range(Σ'.V(d))` and in `range(Σ'.V(d'))`, so they stay active (i).

Now suppose a version `d_v` of `d` was created *before* the DELETE (via D12, ASN-0029), so `Σ.V(d_v) = [a₁, a₂, a₃]` and this V-space was not modified by the DELETE (P7, CrossDocVIndependent). Then `refs(a₂)` in Σ' includes `(d_v, 2)` — `a₂` was never truly unreferenced, it remained active through `d_v`.

**COPY from the version.** COPY(d_v, 2, 1, d, 2) in state Σ' produces Σ'':

- `Σ''.V(d) = [a₁, a₂, a₃]` — position 2 of `d` again maps to `a₂`.
- `Σ''.I = Σ'.I = Σ.I` — no I-space change.
- `a₂` is active (i) in Σ'' with `refs(a₂) ⊇ {(d, 2), (d_v, 2)}`.

The scenario demonstrates: identity is untouched throughout; reachability fluctuates with V-space editing; recovery through COPY requires a reachable source — the version provided one.

---

## Operations and the Two Properties

We now examine each operation through the lens of identity and reachability. The question for each: does it preserve identity? does it preserve reachability?

### INSERT

INSERT is the only operation that extends dom(Σ.I). It is the primary witness for transition (iii)→(i) and the operation most central to address permanence.

**A0 for existing addresses.** INSERT(d, p, k) allocates k fresh I-addresses and places them in d's V-space. By +_ext (ISpaceExtension, ASN-0026), `Σ'.I = Σ.I +_ext fresh` where `fresh ∩ dom(Σ.I) = ∅`. For all previously allocated addresses, A0 holds: `(A a ∈ dom(Σ.I) : a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a))`.

**Fresh content is immediately reachable.** By P9-new (FreshPositions, ASN-0026), `(A j : p ≤ j < p + k : Σ'.V(d)(j) ∈ fresh)`. Each fresh I-address enters dom(Σ'.I) and appears in d's V-space in the same atomic step. Fresh content is born into state (i) — active — with `refs(a) ⊇ {(d, j)}` for the corresponding position j. There is no intermediate state in which the content is allocated but unreachable.

**Reachability of existing content.** P9-left (LeftUnchanged) preserves positions below p. P9-right (RightShifted) shifts positions at and above p by k, preserving the I-address mappings. P7 (CrossDocVIndependent) preserves all other documents. No existing I-address loses reachability through INSERT.

### DELETE

**A4 (DeletePreservesIdentity).** DELETE(d, p, k) — remove k positions starting at p from document d — satisfies:

    pre:  d ∈ Σ.D ∧ 1 ≤ p ∧ p + k − 1 ≤ n_d ∧ k ≥ 1
    post:
    (a)  Σ'.I = Σ.I
    (b)  (A j : p ≤ j < p + k :
            let a = Σ.V(d)(j) :
            a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a))
    (c)  |Σ'.V(d)| = n_d − k
    (d)  (A j : 1 ≤ j < p : Σ'.V(d)(j) = Σ.V(d)(j))
    (e)  (A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))
    frame:
    (f)  (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))
    (g)  Σ'.D = Σ.D

Note: Like A4a and A5, the V-space postcondition is a *specification requirement* — what a correct DELETE must satisfy. No foundation ASN specifies DELETE's V-space behavior (ASN-0026 classifies it only as `fresh = ∅`). Parts (c)–(e) are the symmetric counterpart to INSERT's P9 properties: (c) mirrors P9-length, (d) mirrors P9-left, and (e) mirrors P9-right with the shift reversed. Part (f) is P7 (CrossDocVIndependent, ASN-0026).

Part (a) is an instance of +_ext (ASN-0026) with `fresh = ∅`. Part (g) is the document-set frame: DELETE neither creates nor removes documents (D2 forbids removal; DELETE has no reason to create). Part (b) is the pointed consequence: the specific I-addresses removed from `d`'s V-space persist in I-space with their content unchanged.

The wp reasoning makes the necessity transparent. We want to maintain R: "all I-addresses ever allocated remain in dom(Σ.I) with their original content." Then wp(DELETE, R) requires that DELETE not modify dom(Σ.I) or any value in Σ.I. Since DELETE's definition operates exclusively on Σ.V(d) — removing positions from a single document's V-space — the weakest precondition is trivially satisfied. DELETE does not touch I-space. There is nothing to prove because there is nothing to threaten.

DELETE does affect reachability. After DELETE(d, p, k), by (d) and (e), positions below p retain their I-address mappings and positions at and above p+k shift down by k. The I-addresses at positions p through p+k−1 are no longer in range(Σ'.V(d)). They may still be in range(Σ'.V(d')) for other documents d' (which are unchanged by (f)). Whether an address transitions from active to unreferenced depends on whether any other document references it — a global property that DELETE on a single document cannot locally determine.

### COPY

**A5 (TransclusionIdentity).** We require that COPY(d_s, p_s, k, d_t, p_t) — copy k positions from d_s into d_t — satisfy:

    pre:  d_s ∈ Σ.D ∧ d_t ∈ Σ.D ∧ k ≥ 1
        ∧ 1 ≤ p_s ∧ p_s + k − 1 ≤ n_{d_s}
        ∧ 1 ≤ p_t ≤ n_{d_t} + 1
    post:
    (a)  (A j : 0 ≤ j < k : Σ'.V(d_t)(p_t + j) = Σ.V(d_s)(p_s + j))
    (b)  Σ'.I = Σ.I
    (c)  |Σ'.V(d_t)| = n_{d_t} + k
    (d)  (A j : 1 ≤ j < p_t : Σ'.V(d_t)(j) = Σ.V(d_t)(j))
    (e)  (A j : p_t ≤ j ≤ n_{d_t} : Σ'.V(d_t)(j + k) = Σ.V(d_t)(j))
    frame:
    (f)  d_s ≠ d_t ⟹ Σ'.V(d_s) = Σ.V(d_s)
    (g)  (A d' : d' ∈ Σ.D ∧ d' ≠ d_t : Σ'.V(d') = Σ.V(d'))
    (h)  Σ'.D = Σ.D

Note: ASN-0026 asserts only that COPY has `fresh = ∅` (+_ext) and writes to the target document (P7). The V-space postconditions — that target positions map to the same I-addresses as source positions (a), that existing content is preserved with insert semantics (c)–(e), and that non-target documents are unchanged (g) — are not derivable from any foundation. A5 is a *specification requirement*, matching A4a's treatment: what a correct COPY must satisfy, not a derived property. Part (h) is the document-set frame: COPY shares existing I-addresses and has no reason to create or remove documents. Part (f) is conditioned on `d_s ≠ d_t` because self-transclusion is valid (P5, ASN-0026): when the source and target are the same document, the target's V-space changes by (a)–(e). When `d_s ≠ d_t`, (f) is an instance of (g); we state it separately for clarity. If a future ASN formalizes COPY, A5 becomes a required postcondition to verify. Parts (c)–(e) follow INSERT semantics: existing positions below `p_t` are unchanged, existing positions at and above `p_t` shift by k. Gregory's implementation confirms this: `docopyinternal` calls `insertpm` — the same insert-into-POOM routine used by INSERT — to place the copied I-addresses into the target.

The target document's new positions map to the *same I-addresses* as the source. No fresh I-space content is allocated. This is what distinguishes transclusion from conventional copying: the operation creates shared references, not duplicate content. Two documents that share an I-address share identity — the system can compute that they contain the same content, because "the same content" means "the same I-address," not "matching bytes."

Nelson: "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." There is nothing to update because there is nothing duplicated. There is only one instance of the content, at one I-address, referenced from multiple V-spaces.

The consequence for reachability is that COPY *increases* it. After COPY, content that was reachable through d_s is now also reachable through d_t — by (a), the new positions map to the source's I-addresses. Existing content in d_t remains reachable — by (d) and (e), positions below p_t are unchanged and positions at and above p_t shift by k without losing any mapping. If d_s later deletes the content, it remains reachable through d_t (by (g), d_t is unaffected by operations on d_s). The transclusion acts as a firewall against reachability loss — each additional reference is an independent path to the same permanent content.

Gregory confirms the mechanism: `docopyinternal` calls `specset2ispanset` to read the source POOM's I-addresses, then `insertpm` to place them verbatim into the target's POOM. The I-address values in `crumorigin.dsas[I]` are copied without transformation. No call to `inserttextingranf` (the only function that allocates fresh I-addresses) occurs anywhere in the COPY path.

### REARRANGE

**A4a (RearrangePreservesIdentity).** We require that REARRANGE(d, cuts) satisfy:

    pre:  d ∈ Σ.D
    post:
    (a)  Σ'.I = Σ.I
    (b)  |Σ'.V(d)| = |Σ.V(d)|
    (c)  (E π : π is a bijection [1..n_d] → [1..n_d] :
            (A p : 1 ≤ p ≤ n_d : Σ'.V(d)(p) = Σ.V(d)(π(p))))
    frame:
    (d)  (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))
    (e)  Σ'.D = Σ.D

Note: REARRANGE has no formal specification in any foundation ASN. A4a is a *specification requirement* — what a correct REARRANGE must satisfy — not a derived property. If a future ASN formalizes REARRANGE, A4a becomes a required postcondition to verify. Part (d) is P7 (CrossDocVIndependent, ASN-0026). Part (e) is the document-set frame: REARRANGE permutes positions within a single document and has no reason to create or remove documents.

Part (c) asserts that the post-state V-space is a *permutation* of the pre-state — the same content, at different positions. Set equality would be insufficient: a V-space `[a, a, b]` → `[a, b, b]` preserves the set `{a, b}` and the length, but silently duplicates one I-address reference and drops another. Permutation prevents this — every position in the post-state maps to exactly one position in the pre-state, and conversely. REARRANGE permutes the V-space arrangement without adding, removing, or duplicating I-address references.

This means REARRANGE preserves both identity (trivially, by (a)) and reachability: every I-address that was reachable through d before remains reachable through d after, and conversely. Positions change; the set of referenced I-addresses does not.

Gregory's implementation is consistent with this requirement: `rearrangend` operates exclusively on `cdsp.dsas[V]` — the V-displacement of POOM crums. The I-dimension `cdsp.dsas[I]` is never written. The code applies `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], ...)` for each affected region, shifting V-positions while the I-mappings remain untouched.

### CREATENEWVERSION

Version creation is an instance of transclusion over the entire document. D12 (VersionCreation, ASN-0029) establishes:

    (A p : 1 ≤ p ≤ |Σ.V(d_s)| : Σ'.V(d_v)(p) = Σ.V(d_s)(p))

and Σ'.I = Σ.I. The version shares all I-addresses with the source. No new content is allocated.

**A6 (VersionCorrespondence).** At the moment of version creation:

    (A p : 1 ≤ p ≤ |Σ.V(d_s)| : correspond(d_s, p, d_v, p))

where `correspond` is defined in ASN-0026. Every position in both documents corresponds — they share the same I-address mapping. As the documents diverge through subsequent editing, some positions will be deleted or shifted. But the *I-addresses* of the shared content remain permanent. Correspondence between versions is computable as a set intersection over I-address ranges — exact and efficient — because shared I-addresses are permanent.

Nelson: "a facility that holds multiple versions of the same material... is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." This facility works precisely because version creation shares I-addresses rather than allocating fresh copies. If CREATENEWVERSION allocated new I-addresses for the version's content, correspondence would require byte-level comparison — expensive and ambiguous. With shared I-addresses, two positions correspond if and only if their V-space mappings point to the same I-address. Identity replaces comparison.

Gregory confirms: `docreatenewversion` calls `docopyinternal`, which calls `specset2ispanset` (reading source POOM I-addresses) followed by `insertpm` (writing them verbatim into the version's POOM). At no point is `inserttextingranf` called. Zero fresh I-addresses are allocated — not even for metadata or structural bookkeeping. The version's POOM entries carry the exact same I-address values as the source.

### PUBLISH

PUBLISH(d, status) changes d's publication state (D10a, ASN-0029). Its frame condition leaves Σ.I, Σ.V(d), and all other documents unchanged. Identity and reachability are both trivially preserved — PUBLISH modifies neither I-space nor any V-space.

---

## Link Integrity

We are now in a position to derive link integrity from address permanence. A link L has three endsets — from, to, and type — each being a set of I-address spans. The content at those spans is the link's semantic anchor. Does the content remain stable?

We define the set of individual I-addresses covered by a link's endsets. Each endset is a set of spans `(s, l)` with `l > 0`; by T12 (SpanWellDefined, ASN-0001), each span denotes the contiguous set `{t : s ≤ t < s ⊕ l}`. The union across all three endsets gives the complete set of addresses a link references:

    endset(L) = ∪{[s, s ⊕ l) : (s, l) ∈ from(L) ∪ to(L) ∪ type(L)}

When we write `a ∈ endset(L)`, we mean `a` is an individual I-address in this union — not a span.

We work backward from the desired postcondition. We want:

    R: (A a ∈ endset(L) : Σ'.I(a) = Σ.I(a))

The wp of any operation with respect to R:

    wp(op, R)
    = {by A0: a ∈ dom(Σ.I) suffices for Σ'.I(a) = Σ.I(a)}
      (A a ∈ endset(L) : a ∈ dom(Σ.I))

We must distinguish two cases. For links whose endset addresses were drawn from a document's V-space — the typical case — the precondition holds permanently. At link creation, P2 (ReferentiallyComplete, ASN-0026) guarantees those I-addresses are in dom(Σ.I). By P1 (ISpaceMonotone), they remain in dom(Σ.I) in every subsequent state. For ghost links (A8 below), the precondition does not hold at creation — the endset contains addresses `a ∉ dom(Σ.I)`. A7 does not apply to those addresses until they are allocated. When content is eventually placed at a ghost address (transition (iii)→(i)), the address enters dom(Σ.I), P1 ensures it stays, and A7 applies from that state onward. Therefore:

**A7 (LinkTargetStability).** For any link L whose endset addresses are in dom(Σ.I), and any operation:

    (A a ∈ endset(L) : Σ'.I(a) = Σ.I(a))

The content at every link endpoint is unchanged. This is a direct consequence of A0 — no special link-preservation mechanism is needed. The permanence of I-space content is sufficient.

But link target stability is not the same as link *resolvability*. We must distinguish two properties.

**A7a (EndsetPermanence).**

    (A a ∈ endset(L) : a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I))

Endset addresses that are allocated remain allocated. This is the restriction of P1 to endset members and is monotone — once an endset address is in dom(Σ.I), it stays. Note the conditional: a link may contain ghost endset addresses (A8) that are not in dom(Σ.I); A7a makes no claim about those until they are allocated.

**A7b (EndsetResolvability).**

    resolvable(L, d) ≡ (E a ∈ endset(L) : reachable(a, d))

A link is *resolvable in document d* when at least one endpoint I-address is in d's current V-space. This property is NOT monotone. DELETE on d can remove the V-space mappings that made L's endpoints reachable through d, rendering L dormant with respect to d.

Gregory's implementation illuminates the distinction precisely. When `retrieveendsets` processes a link, the spanfilade lookup succeeds — the I-address entries were permanently indexed at link creation and no operation removes them. But the subsequent I→V conversion through `linksporglset2specset` attempts to resolve each I-address back to a V-position in the target document's POOM. If DELETE has removed those POOM entries, `retrieverestricted` returns NULL, and `span2spanset` silently returns an empty result. The filtering is per-span: if the entire I-address range of an endpoint has no POOM mapping, the span is dropped atomically.

The link exists. Its endsets reference valid I-addresses. The content at those addresses is unchanged. But no V-space path reaches its endpoints in the queried document. The link is structurally intact but operationally dormant.

**Transclusion can recover resolvability — when a reachable source exists.** If a link's endset I-addresses are reachable in some document or version (i.e., `(E d : d ∈ Σ.D : reachable(a, d))` for `a ∈ endset(L)`), then COPY from that document into a new context restores the link's resolvability there. The link's I-address endsets were permanently indexed in the spanfilade at creation time. The new document's V→I mapping now includes those I-addresses. Link discovery through I-address matching — `find_links` converts query V-positions to I-addresses via the POOM, then searches the spanfilade for matching link entries — succeeds immediately. No modification to the link or its index entries is required. Gregory confirms: stale DOCISPAN entries from the original (now-empty) document do not interfere, because link discovery searches a structurally independent sub-index (LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN entries, tags 1-3) that never overlaps with DOCISPAN entries (tag 4).

If no document's V-space contains the endset I-addresses — the addresses are truly unreferenced — then no currently defined operation recovers resolvability. The link remains structurally intact (A7 still holds for allocated endsets) but dormant in all documents, awaiting the historical backtrack mechanism noted in the accessibility transitions.

---

## The Ghost Domain

Nelson's design includes addresses that are valid points in tumbler space but have no content. The accessibility partition (A2) captures these as state (iii): `a ∉ dom(Σ.I)` with `a` satisfying T4. We record a specific consequence.

**A8 (GhostLinkValidity).** A link may reference an address `a` where `a ∉ dom(Σ.I)`. Such a link is structurally valid — the endset contains a well-formed tumbler — but content retrieval at `a` yields no bytes. We define:

    ghost(a) ≡ a ∉ dom(Σ.I) ∧ T4(a)

Ghost links enable forward references: a link created to a document or account address that has not yet received content. Nelson: "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." When content is eventually placed at that address (transition (iii) → (i)), the link becomes resolvable without any modification to the link itself.

We observe that ghosts arise in two structurally distinct situations, and their permanence follows from different arguments.

*Frontier ghosts.* Each allocator's sibling stream advances by `inc(·, 0)` — sequential increment at the last significant position (T10a, AllocatorDiscipline, ASN-0001). If the highest allocated sibling is `t_h`, then every same-level address `t > t_h` is a ghost. These are *frontier ghosts*: they lie beyond the allocation frontier. By T9 (ForwardAllocation), all future sibling allocations produce addresses strictly greater than `t_h`, advancing the frontier monotonically. Frontier ghosts below the current frontier cannot exist — T10a's sequential discipline means the allocator passed through every intermediate value to reach `t_h`. Between any two siblings `t₁ < t₃` produced by the same allocator, every same-level address was necessarily allocated by the sequential stream. Combined with T8/P1, same-level gaps between siblings are impossible.

Frontier ghosts are permanent in a precise sense: any particular frontier ghost `t_g > t_h` either remains a ghost forever (if the allocator never reaches it) or transitions to allocated when the frontier advances past it. Once allocated (transition (iii)→(i)), it can never return to ghost status (A3, transitions (d) and (e) are forbidden). The ghost set at the frontier only shrinks — it never grows.

*Subtree ghosts.* Addresses within an unestablished prefix subtree are ghosts. Consider `t₁ = [1]` and `t₃ = [3]`: the address `[1, 0, 1]` satisfies `t₁ < [1, 0, 1] < t₃` under T1 and has `t₁ ≼ [1, 0, 1]`. These ghosts *can* be filled: child allocation `inc([1], 2)` produces exactly `[1, 0, 1]` by TA5(d). This is correct behavior — the ghost is within `t₁`'s prefix subtree, and child allocation establishes that subtree on demand. Subtree ghosts are fillable precisely because they fall under an existing allocation's prefix, and the parent can spawn child allocators into its own subtree (T10a).

---

## The Coordinate Principle

Address permanence is a property of the *coordinate system*, not of physical storage.

**A9 (CoordinateIndependence).** The I-address of content is a permanent logical coordinate. The physical storage location of the content may change without affecting the address or the content. A0 holds:

    (A a ∈ dom(Σ.I), Σ → Σ' : Σ'.I(a) = Σ.I(a))

regardless of whether the bytes at `a` have been migrated between servers, cached, replicated, or reorganized in physical storage.

Nelson designed this explicitly. Content actively migrates between servers: "The contents can slosh back and forth dynamically." The I-address encodes *provenance* — which node, user, and document created the content — not *location*. The Node field in a tumbler is a birth certificate, not a GPS coordinate. Each server holds "a microcosm that shrinks and grows," and content replicates toward demand.

The formal consequence is that A0 through A7 are properties of the abstract state (Σ.I, Σ.V, Σ.D) and must be maintained regardless of physical storage organization. An implementation is free to migrate, replicate, compact, or redistribute content, provided the abstract state is preserved. The permanence guarantee lives in the coordinate space, not in any particular arrangement of disk blocks.

---

## The Verification Gap

We must note one limit of the permanence guarantee. The system provides no cryptographic mechanism to verify that content returned at an I-address is what was originally stored. Nelson acknowledges this: "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users."

**A10 (AuthenticityCaveat).** A0 is an invariant of the abstract specification. It asserts what correct implementations preserve. It does not provide a mechanism for a client to verify that a particular retrieval satisfies A0.

The distinction between "the invariant holds" and "the client can verify the invariant holds" is significant. The former is a property of the system design. The latter would require additional mechanisms — content hashing, digital signatures, Merkle proofs — not present in Nelson's architecture. The trust model is contractual (faithful storage vendors within a franchise agreement), not mathematical (proofs accompanying each byte). This is a pre-cryptographic architecture: the addressing system is sound; verification relies on institutional trust.

---

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| A0 | `[a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a)]` — identity at I-address is permanent | introduced |
| A1 | `¬[reachable(a, d) ⟹ reachable(a, d) in Σ']` — reachability is non-monotone | introduced |
| A2 | Every valid address is in exactly one of: active, unreferenced, unallocated | introduced |
| A3 | Transitions (i)→(iii) and (ii)→(iii) forbidden; all others permitted | introduced |
| A4 | DELETE: `Σ'.I = Σ.I`, removed I-addresses persist, V-space contracts with left-unchanged and right-shifted, `Σ'.D = Σ.D` | introduced (requirement) |
| A4a | REARRANGE: `Σ'.I = Σ.I`, V-space is a permutation of pre-state, other documents unchanged, `Σ'.D = Σ.D` | introduced (requirement) |
| A5 | COPY: target positions share source I-addresses, `Σ'.I = Σ.I`, insert semantics on target V-space, source unchanged when `d_s ≠ d_t`, `Σ'.D = Σ.D` | introduced (requirement) |
| A6 | Version correspondence computable from shared I-addresses | introduced |
| A7 | `(A a ∈ endset(L) : Σ'.I(a) = Σ.I(a))` — link target content is stable | introduced |
| A7a | `(A a ∈ endset(L) : a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I))` — allocated endset addresses are permanent | introduced |
| A7b | `resolvable(L, d)` is non-monotone — DELETE can make links dormant | introduced |
| A8 | Links may reference ghost addresses; `ghost(a) ≡ a ∉ dom(Σ.I) ∧ T4(a)` | introduced |
| reachable(a, d) | `(E p : (d, p) ∈ refs(a))` — V-space reachability (equiv. `(E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)`) | introduced |
| reachable(a) | `refs(a) ≠ ∅` — global reachability | introduced |
| endset(L) | `∪{[s, s ⊕ l) : (s, l) ∈ from(L) ∪ to(L) ∪ type(L)}` — I-addresses covered by a link | introduced |
| resolvable(L, d) | `(E a ∈ endset(L) : reachable(a, d))` — link resolvability | introduced |
| ghost(a) | `a ∉ dom(Σ.I) ∧ T4(a)` — valid address without content | introduced |

**Design Remarks** (not formal invariants):

| Label | Statement | Status |
|-------|-----------|--------|
| A9 | Address permanence is coordinate-level, independent of physical storage | remark |
| A10 | No client-verifiable mechanism for content authenticity at retrieval | remark |

## Open Questions

- What protocol mechanism restores reachability to unreferenced content, and what invariants must it satisfy?
- Must the system maintain a reverse index from I-addresses to referencing documents, or is absence of such an index acceptable?
- Under what conditions may a storage operator refuse to serve content that remains in dom(Σ.I)?
- What properties must a content authentication mechanism satisfy to close the verification gap identified in A10?
- Does ghost link resolution require any notification or update when content is allocated at a previously ghost address?
- What obligations does publication impose on the active-to-unreferenced transition — can published content become unreferenced?
- Must the system distinguish between content that is unreferenced because deleted and content that was allocated but never inserted into V-space?
- What invariants must historical backtrack satisfy to recover unreferenced content without violating address permanence?
- Can reachability loss be made atomic with respect to concurrent readers, or may a reader observe a partially-deleted V-space?
