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

**Reachability** is a different matter entirely. It is the ability to obtain content through a document's V-space arrangement. Using `refs(a)` from ASN-0026:

    reachable(a, d) ≡ (E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)

Address `a` is *reachable through document d* when some position in `d`'s V-space maps to `a`. The global form:

    reachable(a) ≡ (E d : d ∈ Σ.D : reachable(a, d))

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

These are exhaustive and mutually exclusive. State (i) is the normal operational condition: content exists and at least one document displays it. State (ii) is Nelson's "DELETED BYTES" — content persists in I-space, but no V-space arrangement maps to it. State (iii) comprises the ghost elements: "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

The partition is over the state Σ — an address may transition between states as operations execute. But not all transitions are permitted.

**A3 (AccessibilityTransitions).**

    (a)  (iii) → (i):   permitted — allocation followed by insertion into a document
    (b)  (i) → (ii):    permitted — DELETE from all referencing documents
    (c)  (ii) → (i):    permitted — transclusion into any document
    (d)  (i) → (iii):   forbidden — would violate P1
    (e)  (ii) → (iii):  forbidden — would violate P1
    (f)  (iii) → (ii):  permitted — allocation without V-space insertion

The forbidden transitions are the permanence guarantee stated negatively: content, once allocated, cannot become unallocated. The allocated set only grows; the address space never contracts. Gregory's implementation evidence is definitive on this point. The function `deleteseq` — the only code that could remove a granfilade entry and thereby reduce the I-space — is dead code: defined in `edit.c` but called nowhere in the system. No code path from DELETE reaches the granfilade. DELETE operates exclusively on the POOM (the V→I mapping), removing V-space positions while leaving I-space untouched.

Transition (b) is the critical one for understanding the system. A user deletes content from their document. The V-space contracts; positions shift (P9-right, ASN-0026, applied in reverse). The I-addresses that were at the deleted positions leave the document's V-space. If those I-addresses appear in other documents (via transclusion), they remain active. If they appear nowhere, they become unreferenced. Either way, the content at those I-addresses is unchanged — A0 applies regardless.

Transition (c) is the recovery mechanism. Nelson lists unreferenced content as "awaiting historical backtrack functions." But transclusion provides a more immediate path: if any operation creates a new V-space mapping to an unreferenced I-address, the content becomes active again. No modification to the content or its address is required. The I-address is a permanent name; V-space is merely the question of who is currently using that name.

Transition (f) arises when content is allocated — INSERT creates fresh I-addresses (P9-new, ASN-0026) — but then immediately deleted from V-space before any other document transcludes it. The content enters state (ii) directly. This is a normal consequence of the separation: allocation is permanent, arrangement is editorial.

---

## Operations and the Two Properties

We now examine each operation through the lens of identity and reachability. The question for each: does it preserve identity? does it preserve reachability?

### DELETE

**A4 (DeletePreservesIdentity).** DELETE(d, p, k) — remove k positions starting at p from document d — satisfies:

    (a)  Σ'.I = Σ.I
    (b)  (A j : p ≤ j < p + k :
            let a = Σ.V(d)(j) :
            a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a))

Part (a) is an instance of +_ext (ASN-0026) with `fresh = ∅`. Part (b) is the pointed consequence: the specific I-addresses removed from `d`'s V-space persist in I-space with their content unchanged.

The wp reasoning makes the necessity transparent. We want to maintain R: "all I-addresses ever allocated remain in dom(Σ.I) with their original content." Then wp(DELETE, R) requires that DELETE not modify dom(Σ.I) or any value in Σ.I. Since DELETE's definition operates exclusively on Σ.V(d) — removing positions from a single document's V-space — the weakest precondition is trivially satisfied. DELETE does not touch I-space. There is nothing to prove because there is nothing to threaten.

DELETE does affect reachability. After DELETE(d, p, k), the I-addresses at positions p through p+k−1 are no longer in range(Σ'.V(d)). They may still be in range(Σ'.V(d')) for other documents d'. Whether an address transitions from active to unreferenced depends on whether any other document references it — a global property that DELETE on a single document cannot locally determine.

### COPY

**A5 (TransclusionIdentity).** COPY(d_s, p_s, k, d_t, p_t) — copy k positions from d_s into d_t — satisfies:

    (a)  (A j : 0 ≤ j < k : Σ'.V(d_t)(p_t + j) = Σ.V(d_s)(p_s + j))
    (b)  Σ'.I = Σ.I

The target document's new positions map to the *same I-addresses* as the source. No fresh I-space content is allocated. This is what distinguishes transclusion from conventional copying: the operation creates shared references, not duplicate content. Two documents that share an I-address share identity — the system can compute that they contain the same content, because "the same content" means "the same I-address," not "matching bytes."

Nelson: "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." There is nothing to update because there is nothing duplicated. There is only one instance of the content, at one I-address, referenced from multiple V-spaces.

The consequence for reachability is that COPY *increases* it. After COPY, content that was reachable through d_s is now also reachable through d_t. If d_s later deletes the content, it remains reachable through d_t. The transclusion acts as a firewall against reachability loss — each additional reference is an independent path to the same permanent content.

Gregory confirms the mechanism: `docopyinternal` calls `specset2ispanset` to read the source POOM's I-addresses, then `insertpm` to place them verbatim into the target's POOM. The I-address values in `crumorigin.dsas[I]` are copied without transformation. No call to `inserttextingranf` (the only function that allocates fresh I-addresses) occurs anywhere in the COPY path.

### REARRANGE

**A4a (RearrangePreservesIdentity).** REARRANGE(d, cuts) satisfies:

    (a)  Σ'.I = Σ.I
    (b)  |Σ'.V(d)| = |Σ.V(d)|
    (c)  {Σ'.V(d)(p) : 1 ≤ p ≤ n_d} = {Σ.V(d)(p) : 1 ≤ p ≤ n_d}

Part (c) asserts that the *set* of I-addresses in d's V-space is unchanged — the same content, at different positions. REARRANGE permutes the V-space arrangement without adding or removing I-addresses.

This means REARRANGE preserves both identity (trivially, by (a)) and reachability: every I-address that was reachable through d before remains reachable through d after, and conversely. Positions change; the set of referenced I-addresses does not.

Gregory traces the mechanism: `rearrangend` operates exclusively on `cdsp.dsas[V]` — the V-displacement of POOM crums. The I-dimension `cdsp.dsas[I]` is never written. The code applies `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], ...)` for each affected region, shifting V-positions while the I-mappings remain untouched.

### CREATENEWVERSION

Version creation is an instance of transclusion over the entire document. D12 (VersionCreation, ASN-0029) establishes:

    (A p : 1 ≤ p ≤ |Σ.V(d_s)| : Σ'.V(d_v)(p) = Σ.V(d_s)(p))

and Σ'.I = Σ.I. The version shares all I-addresses with the source. No new content is allocated.

**A6 (VersionCorrespondence).** At the moment of version creation:

    (A p : 1 ≤ p ≤ |Σ.V(d_s)| : correspond(d_s, p, d_v, p))

where `correspond` is defined in ASN-0026. Every position in both documents corresponds — they share the same I-address mapping. As the documents diverge through subsequent editing, some positions will be deleted or shifted. But the *I-addresses* of the shared content remain permanent. Correspondence between versions is computable as a set intersection over I-address ranges — exact and efficient — because shared I-addresses are permanent.

Nelson: "a facility that holds multiple versions of the same material... is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." This facility works precisely because version creation shares I-addresses rather than allocating fresh copies. If CREATENEWVERSION allocated new I-addresses for the version's content, correspondence would require byte-level comparison — expensive and ambiguous. With shared I-addresses, two positions correspond if and only if their V-space mappings point to the same I-address. Identity replaces comparison.

Gregory confirms: `docreatenewversion` calls `docopyinternal`, which calls `specset2ispanset` (reading source POOM I-addresses) followed by `insertpm` (writing them verbatim into the version's POOM). At no point is `inserttextingranf` called. Zero fresh I-addresses are allocated — not even for metadata or structural bookkeeping. The version's POOM entries carry the exact same I-address values as the source.

---

## Link Integrity

We are now in a position to derive link integrity from address permanence. A link L connects endsets — each endset is a set of I-address spans. The content at those spans is the link's semantic anchor. Does the content remain stable?

We work backward from the desired postcondition. We want:

    R: (A a ∈ endset(L) : Σ'.I(a) = Σ.I(a))

The wp of any operation with respect to R:

    wp(op, R)
    = {by A0: a ∈ dom(Σ.I) suffices for Σ'.I(a) = Σ.I(a)}
      (A a ∈ endset(L) : a ∈ dom(Σ.I))

This precondition holds permanently. At link creation, endset I-addresses were obtained from some document's V-space (the link's source content must exist to be linked). By P2 (ReferentiallyComplete, ASN-0026), those I-addresses are in dom(Σ.I). By P1 (ISpaceMonotone), they remain in dom(Σ.I) in every subsequent state. Therefore:

**A7 (LinkTargetStability).** For any link L whose endset addresses are in dom(Σ.I), and any operation:

    (A a ∈ endset(L) : Σ'.I(a) = Σ.I(a))

The content at every link endpoint is unchanged. This is a direct consequence of A0 — no special link-preservation mechanism is needed. The permanence of I-space content is sufficient.

But link target stability is not the same as link *resolvability*. We must distinguish two properties.

**A7a (EndsetPermanence).**

    (A a ∈ endset(L) : a ∈ dom(Σ'.I))

Link endsets permanently reference valid I-addresses. This is monotone — once true, always true.

**A7b (EndsetResolvability).**

    resolvable(L, d) ≡ (E a ∈ endset(L) : reachable(a, d))

A link is *resolvable in document d* when at least one endpoint I-address is in d's current V-space. This property is NOT monotone. DELETE on d can remove the V-space mappings that made L's endpoints reachable through d, rendering L dormant with respect to d.

Gregory's implementation illuminates the distinction precisely. When `retrieveendsets` processes a link, the spanfilade lookup succeeds — the I-address entries were permanently indexed at link creation and no operation removes them. But the subsequent I→V conversion through `linksporglset2specset` attempts to resolve each I-address back to a V-position in the target document's POOM. If DELETE has removed those POOM entries, `retrieverestricted` returns NULL, and `span2spanset` silently returns an empty result. The filtering is per-span: if the entire I-address range of an endpoint has no POOM mapping, the span is dropped atomically.

The link exists. Its endsets reference valid I-addresses. The content at those addresses is unchanged. But no V-space path reaches its endpoints in the queried document. The link is structurally intact but operationally dormant.

**Transclusion recovers resolvability.** When unreferenced I-addresses are transcluded into a new document, the link becomes discoverable again. The link's I-address endsets were permanently indexed in the spanfilade at creation time. The new document's V→I mapping now includes those I-addresses. Link discovery through I-address matching — `find_links` converts query V-positions to I-addresses via the POOM, then searches the spanfilade for matching link entries — succeeds immediately. No modification to the link or its index entries is required. Gregory confirms: stale DOCISPAN entries from the original (now-empty) document do not interfere, because link discovery searches a structurally independent sub-index (LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN entries, tags 1-3) that never overlaps with DOCISPAN entries (tag 4).

---

## The Ghost Domain

Nelson's design includes addresses that are valid points in tumbler space but have no content. The accessibility partition (A2) captures these as state (iii): `a ∉ dom(Σ.I)` with `a` satisfying T4. We record a specific consequence.

**A8 (GhostLinkValidity).** A link may reference an address `a` where `a ∉ dom(Σ.I)`. Such a link is structurally valid — the endset contains a well-formed tumbler — but content retrieval at `a` yields no bytes. We define:

    ghost(a) ≡ a ∉ dom(Σ.I) ∧ T4(a)

Ghost links enable forward references: a link created to a document or account address that has not yet received content. Nelson: "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." When content is eventually placed at that address (transition (iii) → (i)), the link becomes resolvable without any modification to the link itself.

Ghost addresses at intermediate positions — between existing allocations — remain ghosts permanently. T9 (ForwardAllocation, ASN-0001) guarantees that new allocations occur only at the frontier. No future allocation will "fill in" a ghost address between existing ones.

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
| A4 | DELETE: `Σ'.I = Σ.I` and removed I-addresses persist with unchanged content | introduced |
| A4a | REARRANGE: `Σ'.I = Σ.I` and range of V-space I-addresses unchanged | introduced |
| A5 | COPY: `Σ'.V(d_t)(p_t + j) = Σ.V(d_s)(p_s + j)` and `Σ'.I = Σ.I` — shared identity | introduced |
| A6 | Version correspondence computable from shared I-addresses | introduced |
| A7 | `(A a ∈ endset(L) : Σ'.I(a) = Σ.I(a))` — link target content is stable | introduced |
| A7a | `(A a ∈ endset(L) : a ∈ dom(Σ'.I))` — endset addresses are permanent | introduced |
| A7b | `resolvable(L, d)` is non-monotone — DELETE can make links dormant | introduced |
| A8 | Links may reference ghost addresses; `ghost(a) ≡ a ∉ dom(Σ.I) ∧ T4(a)` | introduced |
| A9 | Address permanence is coordinate-level, independent of physical storage | introduced |
| A10 | No client-verifiable mechanism for content authenticity at retrieval | introduced |
| reachable(a, d) | `(E p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)` — V-space reachability | introduced |
| reachable(a) | `(E d : d ∈ Σ.D : reachable(a, d))` — global reachability | introduced |
| resolvable(L, d) | `(E a ∈ endset(L) : reachable(a, d))` — link resolvability | introduced |
| ghost(a) | `a ∉ dom(Σ.I) ∧ T4(a)` — valid address without content | introduced |

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
