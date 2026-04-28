# ASN-0016: Content Provenance

*2026-02-25*

We wish to understand what the system must guarantee about the origin of content. Given a byte visible at some position in some document, what can be determined — structurally, without external metadata — about where that byte came from, how it arrived at its present location, and its relationship to the same byte appearing elsewhere? The word "provenance" is our name for these guarantees collectively.

This is not a feature. It is the foundation on which attribution, compensation, correspondence, and link discovery all rest. If the system cannot answer "who created this?" then it cannot pay the creator. If it cannot answer "does this appear elsewhere?" then it cannot maintain links across transclusions. If it cannot distinguish independent creation from deliberate sharing, it cannot tell quotation from coincidence. The provenance guarantees are the load-bearing structure beneath the entire system.

The difficulty is in stating precisely which questions provenance must answer and which it need not. Nelson demands that the origin of every byte be permanently discoverable. But he does not demand that the full operational history — the sequence of COPY operations that carried a byte from document to document — be recorded. The architecture achieves provenance through structural encoding in addresses, not through an operation journal. We seek the exact boundary: what is structurally guaranteed, what is computable on demand, and what is deliberately outside the specification.


## State components

We require a minimal model. Let the system state Σ contain:

- **ispace** : Addr ⇀ Content — the permanent, append-only content store. Once `a ∈ dom.ispace`, it remains forever and `ispace.a` is immutable.
- **poom(d)** : VPos → Addr — for each document d, the arrangement mapping from virtual positions to I-space addresses. This is what gives a document its reading order.
- **spanindex** : Addr → Set(DocId) — a reverse index recording which documents contain which I-address ranges. Append-only: entries are added but never removed.
- **links** : a set of link structures, each with three endsets (from, to, type), where endsets reference I-space address ranges.
- **docs** : Set(DocId) — all documents in the system.
- **owner** : DocId → UserId — the owner of each document.

We write `dom.ispace` for the set of allocated addresses, `ispace.a` for the content at address `a`, and `poom(d).v` for the I-address that document d maps V-position v to. We write `img(poom(d))` for the image — the set of I-addresses document d references. Primed names denote the state after an operation.


## The structure of addresses

Before we can reason about provenance, we must establish what an address carries. Every I-space address in the system has a hierarchical structure:

    Node.0.User.0.Document.0.Element

where the zeros are field separators. We do not need the full tumbler arithmetic here — only the fact that the address encodes, as syntactic components, the identity of the server (Node), the account (User), the document (Document), and the position within that document (Element). We define three extraction functions:

    home(a)    = the Document prefix of address a
    account(a) = the User prefix of address a
    server(a)  = the Node prefix of address a

These are purely syntactic — they extract a prefix of the address by truncating at the appropriate field boundary. No index is consulted; no external state is needed. The extraction is defined for every address `a ∈ dom.ispace` and is permanent: since addresses are immutable, so are their prefixes.

Nelson states the user-facing guarantee this encoding makes possible: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. The word "ascertain" is important — it implies a computable determination, not a trust assertion. The system does not merely claim provenance; it computes it from the address.


## P0: Structural provenance

We now state the central property. It is the single most important provenance guarantee in the system.

**P0 (Structural provenance).** Every I-space address permanently encodes its origin document:

    [a ∈ dom.ispace ⇒ home(a) ∈ docs]

and the content at address `a` was created by an INSERT operation in document `home(a)` — that is, the allocation of address `a` was performed under the authority of `home(a)`. Furthermore, `home` is permanent:

    [home(a) is determined by the address a alone, independent of Σ]

This property is structural, not metadata. An alternative implementation using a completely different storage engine would still need to satisfy it, because every downstream guarantee depends on it. The system does not record provenance as an annotation attached to content; the address IS the provenance record. To fetch content at address `a`, the system must contact `home(a)` — the connection between content and origin cannot be severed because the fetching mechanism requires it.

Nelson makes the mechanism explicit: "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations" [LM 4/11]. The words "home locations" are the key: every byte has exactly one home, and that home is encoded in the address.

Gregory confirms the implementation. The allocation function for content addresses operates within a document-scoped namespace. When INSERT creates fresh content for document d, it allocates I-addresses that are sub-tumblers of d's own address, specifically within d's element field. The allocation never crosses document boundaries — no operation in the system can allocate an I-address under a different document's prefix. This means:

    [a ∈ dom.ispace ⇒ home(a) was the document performing INSERT when a was created]

The extraction function `home` is not a lookup in a table. It is prefix truncation on the address itself, using the known depth of the document field in the tumbler hierarchy. Gregory traces the precise mechanism: the allocation function receives a "hint" containing the document's address, and the hint's address length determines the truncation depth. The address prefix is structurally recoverable.


## P1: Identity by creation, not by value

We require a second fundamental property that shapes what provenance means. In conventional systems, "same content" means "same bytes." In Xanadu, "same content" means "same address."

**P1 (Identity by creation).** Two content references denote the same content if and only if they resolve to the same I-space address:

    same(r₁, r₂)  ≡  iaddr(r₁) = iaddr(r₂)

Value equality is neither necessary nor sufficient for identity. Independent creation of byte-identical text yields different I-addresses. Transclusion of the same text yields the same I-address.

This is not merely a design choice — it is forced by the provenance requirements. Nelson poses the scenario directly: if Alice types "Hello" and Bob independently types "Hello," the two instances must be identity-distinct. No attribution link, no royalty flow, no correspondence relationship should connect them. But if Bob transcludes Alice's "Hello," the system must recognize Bob's display as Alice's content — links to Alice's text must reach Bob's reader, Alice must receive attribution and compensation, and correspondence must hold.

The formal consequence is that INSERT and COPY are the system's only two mechanisms for placing content in a document, and they produce structurally distinguishable results:

- **INSERT** allocates fresh addresses: `(A i : 1 ≤ i ≤ n : aᵢ ∉ dom.ispace)` — the addresses are new, the content is original.
- **COPY** references existing addresses: `dom.ispace' = dom.ispace` — no new addresses are created, the content is shared.

This is the sole architectural distinction between independent creation and deliberate sharing. Every other provenance property flows from it.


## P2: The native/transcluded distinction

Given P0 and P1, we can now define the classification that makes provenance actionable.

**P2 (Native decidability).** For every document d and every I-address a in `img(poom(d))`, whether content a is native to d or transcluded from elsewhere is decidable from the address alone:

    native(d, a)      ≡  home(a) = d
    transcluded(d, a)  ≡  home(a) ≠ d

The predicate `native(d, a)` holds when d is the document that created the content — the document under whose authority the I-address was allocated. The predicate `transcluded(d, a)` holds when the content originated elsewhere and appears in d through a COPY operation (possibly via intermediate documents — we address this below).

Nelson draws the distinction explicitly: "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations" [LM 4/11]. And further: "Non-native byte-spans are called inclusions or virtual copies" [LM 4/11].

Gregory confirms that the distinction is decidable at the data level. The allocation function places I-addresses within the document's own address subtree — specifically, content addresses for document d fall in the range bounded by d's address extended into the element field. A comparison of the I-address prefix with the document's own address yields a definitive answer. No global index is needed; no table is consulted. The comparison is a tumbler prefix operation on the address and the document's own identifier.

We note an important edge case that Gregory identifies: self-transclusion. When a document copies content from itself (COPY within the same document), the resulting POOM entry maps a new V-position to an I-address that is already native to the document. The `native` predicate returns true — correctly, since the content was indeed created in this document. What is lost is the fact that a COPY operation (rather than an INSERT) placed it at this V-position. The system cannot, from the POOM alone, distinguish "authored here" from "self-copied here." This is not a defect — P2 answers "where was this content created?" not "how did it arrive at this V-position?"


## P3: Transclusion depth collapse

We come now to a property that elevates Xanadu's provenance from a chain-following mechanism to a direct-lookup mechanism. Consider: Alice creates content in document A. Bob transcludes it into document B. Carol transcludes the same passage from Bob's document into document C. What does Carol's document "know" about the content?

In a chain-following system, Carol's reference would point to Bob's reference, which would point to Alice's content — and every query would require traversing two hops. If the chain grows to N documents, provenance becomes an N-hop traversal. The system would need to record the chain, and a broken link in the chain would sever all downstream provenance.

Xanadu's architecture eliminates the chain entirely.

**P3 (Depth collapse).** Transclusion at any depth produces V→I mappings that reference the original creator's I-addresses directly. For any chain of transclusion operations:

    d₁ creates content (INSERT) → d₂ copies from d₁ → d₃ copies from d₂ → ... → dₙ copies from dₙ₋₁

every document in the chain maps to the same I-addresses:

    (A k : 2 ≤ k ≤ n : iaddrs(dₖ, copied_region) = iaddrs(d₁, original_region))

and in particular:

    (A k : 2 ≤ k ≤ n : (A a : a ∈ iaddrs(dₖ, copied_region) : home(a) = d₁))

The chain is architecturally invisible. There is no pointer from dₙ to dₙ₋₁ — only a mapping from dₙ's V-space directly to d₁'s I-addresses.

This property follows from the mechanics of COPY. When dₖ copies from dₖ₋₁, the system converts dₖ₋₁'s V-span to I-addresses by reading dₖ₋₁'s POOM. Those I-addresses are whatever dₖ₋₁'s POOM already holds — which, by induction, are d₁'s original I-addresses. The conversion yields the same addresses regardless of how many intermediate documents the content has passed through. The COPY operation is defined on I-addresses, not on references to references.

Nelson describes the user experience: "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely" [LM 2/34]. Yet despite this layering: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. The phrase "at once" — not "after following the chain" — confirms that resolution is direct.

Gregory confirms the implementation in precise detail. The COPY function converts source V-spans to I-spans by reading the source document's POOM. Those I-spans are then written into the target document's POOM. The operation that assigns I-addresses for new content is never invoked during COPY. The V→I conversion on the source returns whatever I-addresses the source already holds. If the source itself contains transcluded content, those I-addresses are the original creator's — and they pass through unchanged into the target.


## The COPY operation does not record its source

We should pause and make an important negative statement explicit, because it is essential to understanding what provenance does and does not include.

**P4 (No operation chain).** The system does not record the chain of COPY operations through which content arrived at its current location. Given content at V-position v in document d, the system can determine `home(poom(d).v)` — the original creating document — but not the sequence of intermediate documents through which the content was copied.

Nelson is explicit about this. The system must record "where content originated" and "what each version looked like," but not "the sequence of operations that produced the current arrangement" [LM 2/14-15]. The I-address IS the provenance record. The V→I mapping IS the current arrangement. No separate operation log is specified.

We can see why this is a deliberate choice rather than an omission. If Alice creates content, Bob transcludes it, and Carol transcludes from Bob, the system's guarantees require:

1. That Carol can determine Alice is the creator (P0 — from the I-address)
2. That Alice receives attribution and compensation (P0, P2 — from `home`)
3. That links to Alice's content are discoverable from Carol's document (through shared I-addresses)
4. That FINDDOCSCONTAINING on Alice's content finds Carol's document (through the span index)

None of these require knowing that Carol's copy came via Bob rather than directly from Alice. The intermediate path is irrelevant to every guarantee the system provides. Recording it would add storage cost without supporting any specified operation.

Gregory confirms that no operation chain is stored at the implementation level. The POOM stores V→I mappings with no indication of which COPY operation created each mapping. The span index stores (document, I-address) pairs with no indication of which operation created each entry. The only "provenance" field in POOM entries is a `homedoc` value that records the I-address origin document — which is always the creating document, not the most recent copy source.

We observe a subtle consequence: the POOM round-trip. If content is deleted from document A, and later the same I-addresses are transcluded back into A from another document that had previously copied them, the resulting POOM state is logically equivalent to the original state. The V→I mapping points to the same I-addresses. The `native` predicate gives the same answer (the content is native to A, since `home(a) = A`). The round-trip is invisible at the observable level. Gregory confirms this: the internal tree structure may differ (different number of crums, different topology), but every query — retrieval, link discovery, comparison — returns identical results.


## P5: Reverse discovery

Provenance is not merely a forward question ("given this byte, who created it?"). It is also a reverse question ("given this content, who else has it?"). The system must answer both.

**P5 (Reverse discovery completeness).** For any set of I-addresses S, the system provides an operation FINDDOCSCONTAINING that returns the set of all documents whose arrangements reference any address in S:

    FINDDOCSCONTAINING(S) ⊇ { d : (E a : a ∈ S : a ∈ img(poom(d))) }

Nelson specifies this as one of the core protocol operations: "This returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. The word "all" is critical — the result is not a sample, not a best-effort approximation, but the complete set.

We write ⊇ rather than = because the span index is append-only and entries are never removed. If document d once contained I-address a but later deleted it from V-space, d's entry in the span index persists. The result may over-approximate: it includes every document that currently contains or has ever contained the queried content. Gregory confirms this: the span index has no deletion function, and even stale references persist permanently.

This over-approximation is a consequence of the append-only design, not a defect. It means that FINDDOCSCONTAINING answers a question that is strictly stronger than "who currently has this content?" — it answers "who has ever had this content?" This is the correct behavior for a system that preserves all historical state. A document that once transcluded content and later removed it is still historically connected to that content; the span index preserves this connection.

The key structural fact is that FINDDOCSCONTAINING operates on I-addresses, not on byte values. Two documents containing byte-identical text created independently will NOT appear in each other's FINDDOCSCONTAINING results, because they have different I-addresses. Two documents sharing content through transclusion WILL appear, because they share the same I-addresses. This is P1 in action: identity by creation, not by value.

Gregory traces the mechanism. Both INSERT and COPY register the destination document in the span index for the relevant I-address ranges. The registration call is identical in both cases — the index stores `(document_ISA, I-address-start, I-width)` tuples with no flag distinguishing original from transcluded content. The query function performs a two-dimensional range search on the index, collecting all document ISAs whose entries overlap the queried I-address range, deduplicating the result. The returned set is flat — no ordering, no "original" marker, no temporal information.

A consequence of P5 combined with P3 (depth collapse):

**P5a (Transitive discoverability).** If content originating in document A passes through a chain A → B → C → D of transclusions, then FINDDOCSCONTAINING on the content returns {A, B, C, D} — every document in the chain is discoverable, because every document registered the same I-addresses in the span index:

    (A k : 1 ≤ k ≤ n : dₖ ∈ FINDDOCSCONTAINING(iaddrs(d₁, region)))


## P6: Attribution is structural and direct

We can now assemble the provenance guarantees into the attribution property that Nelson considers fundamental.

**P6 (Attribution).** For any byte visible at V-position v in any document d, the system can determine the identity of the creating account:

    account(poom(d).v)

This is computable from the I-address alone (P0), requires no chain-following (P3), is permanent (addresses are immutable), and cannot be severed by any operation within the system (the fetching mechanism requires the address).

Nelson states the guarantee: "the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]. The phrase "determined automatically" confirms that attribution is computed, not claimed. The "proportion to who wrote what" is decidable: for each V-position in the document, `native(d, poom(d).v)` classifies it as the current document's contribution or as transcluded content from `home(poom(d).v)`.

Two caveats must be stated precisely:

**P6a (Account, not person).** Attribution traces to an account in the tumbler hierarchy, not necessarily to a real-world person. Nelson explicitly permits anonymous publication: "there is no reason that anonymous publication by walk-in and transient users of this system should not be allowed. We may call this 'John Doe publication'" [LM 2/60]. The system guarantees structural traceability to an address. The mapping from address to human identity is contractual, not architectural.

**P6b (Trust, not verification).** The system provides no cryptographic proof that content at an I-address was actually created by the account holding that address. Nelson's architecture is pre-cryptographic: "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials" [LM 5/17]. The structural guarantee is: the address encodes the origin. The trust guarantee is: the Storage Vendor preserves this encoding faithfully. There is no mathematical proof that the encoding has not been tampered with — only a contractual obligation.


## P7: Version history preserves transclusion relationships

We come to a subtler question: does provenance have a temporal dimension? If content was once transcluded into a document and then removed, is the historical fact of that transclusion preserved?

**P7 (Version-preserved provenance).** The system need not record transclusion events separately, because the version mechanism preserves all past states. When content is removed from a document's V-space, the previous version — in which the content was present — remains permanently accessible:

    (A d, v_old : v_old is a past version of d :
        v_old is reconstructable on demand)

and for any reconstructed past version, the POOM mappings are intact, so the `home` function yields the same origin it always did.

Nelson is precise: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" [LM 4/9]. And: "the file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15].

The version history IS the provenance journal. No separate mechanism is needed because no state is ever destroyed. The SHOWRELATIONOF2VERSIONS operation can compare any two versions and identify exactly which content was added or removed:

    correspond(v₁, v₂) = { (p₁, p₂) : poom(v₁).p₁ = poom(v₂).p₂ }

where corresponding positions share I-addresses. Content that appears in v₁ but not in v₂ was removed between those versions. Content in v₂ but not v₁ was added. Content in both was preserved. The effect of each edit is fully recoverable from comparing adjacent version states — the type of operation (insert, delete, rearrange) is inferable from the structural differences, without being explicitly stored.

This is a stronger statement than it first appears. It means:

1. The system can determine what content was present in any document at any past version.
2. For each piece of content present in a past version, `home` identifies the creator.
3. The span index, being append-only, records every document that ever contained the content.
4. SHOWRELATIONOF2VERSIONS can identify exactly what changed between versions.

The full provenance record is implicit in the structure. It does not require an operation journal.


## P8: Temporal ordering from allocation

Although the system does not record timestamps in addresses, the append-only nature of I-space allocation provides a partial temporal ordering.

**P8 (Allocation ordering).** I-space allocation is strictly monotonic. If address a was allocated before address b, then a < b in the tumbler ordering:

    allocated_before(a, b) ⇒ a < b

Nelson: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically" [LM 2/14]. The address ordering reflects creation order within a single document (and, within a single server, across documents on that server).

However — and this is the boundary of what allocation ordering provides — absolute time is not encoded: "Note that 'time' is not included in the tumbler. Time is kept track of separately" [LM 4/18]. The system can determine that byte A was stored before byte B (lower I-address), but not the absolute time of either event.

**P8a (Allocation does not provide cross-document temporal ordering for transclusion.)** Given that documents on different servers allocate I-addresses independently, the allocation ordering does not extend to a global timeline. Two documents on different servers may allocate addresses concurrently, and no ordering between those allocations is implied by the addresses.


## P9: Correspondence is structural, not operational

Provenance enables a derived property that Nelson considers essential: the ability to compare two documents and determine what they share.

**P9 (Correspondence from shared identity).** Two documents d₁ and d₂ share content at positions (v₁, v₂) if and only if they map to the same I-address:

    correspond(d₁, v₁, d₂, v₂)  ≡  poom(d₁).v₁ = poom(d₂).v₂

This is computable from the POOMs alone — no operation history is needed. The result is symmetric (if d₁ corresponds with d₂ at some positions, d₂ corresponds with d₁ at the same positions). And it is correct by construction: two positions correspond if and only if they reference identical content in I-space.

Nelson states the user requirement: "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same" [LM 2/20]. The implementation reduces this to I-address set intersection — conceptually, `img(poom(d₁)) ∩ img(poom(d₂))`.

Gregory confirms the algorithm: convert each document's V-spans to I-spans via their POOMs, compute the intersection of the I-span sets, then project the shared I-spans back to V-positions in each document. The result is a set of paired V-address ranges, one from each document, identifying content that is identical (same I-address, therefore same bytes, same provenance, same links).

An important consequence: correspondence cannot distinguish versioning from independent transclusion. If document B was created as a version of A, and document C independently transcluded the same content from A, both B and C would show the same correspondence with A. Gregory confirms that SHOWRELATIONOF2VERSIONS implements only I-address intersection and has no version-specific logic. The distinction between "this is a version of" and "this transcludes from" is encoded, when it exists, in the address hierarchy (version addresses are children of their parent's address) — but this structural signal is not exposed through any protocol operation and fails for cross-user versioning.


## P10: Provenance for link endsets

Links in the system reference content by I-address. This means link provenance inherits all the properties of content provenance.

**P10 (Link provenance through identity).** A link's endsets reference I-space addresses. The provenance of endset content is determined by the same mechanism as content provenance — `home(a)` for each address `a` in the endset. Links "follow" content through transclusion because they attach to I-addresses, and transclusion preserves I-addresses (P3).

The practical consequence: if Alice creates content and Charlie creates a link referencing that content (by I-address), then when Bob transcludes Alice's content into his document, Charlie's link is discoverable through Bob's document. The link was not copied, not re-created, and not re-registered. It is simply that Bob's POOM maps some V-positions to the same I-addresses that Charlie's link endset references. The link discovery mechanism searches by I-address, and both Alice's and Bob's documents map to the same addresses.

Nelson's statement: "links may be refractively followed from a point or span in one version to corresponding places in any other version" [LM 2/26]. "Refractively" is precisely the right word — the link passes through the prism of different documents' V-spaces, reaching the same I-space content through different arrangements.

**P10a (Link origin is home of hosting document).** The link itself has a home document — the document in whose link subspace the MAKELINK operation allocated it. This is separate from the provenance of the content the link points to. The link's home determines who "owns" the link (for deletion, for economic purposes); the endset's I-addresses determine what content the link connects.


## What provenance does not include

We have stated what provenance guarantees. It is equally important to state what it does not.

**Not included: the sequence of intermediary documents.** As established in P4, the system does not record that content passed through documents B and C on its way from A to D. Only the origin (A) and the current holders ({A, B, C, D} via FINDDOCSCONTAINING) are known.

**Not included: the specific operation that placed content.** The system cannot distinguish, from POOM data alone, whether a V→I mapping was created by INSERT, COPY, or CREATENEWVERSION. Gregory confirms: both INSERT and COPY flow through the same internal function, producing structurally identical POOM entries. The only discriminator is whether the I-address is native to the document (home(a) = d), which distinguishes INSERT-created from COPY-placed content — but cannot distinguish COPY from VERSION, or COPY-from-A from COPY-from-B when both yield the same I-addresses.

**Not included: absolute timestamps.** As established in P8, creation order is implicit in address ordering, but absolute time is kept separately and is not part of the structural provenance.

**Not included: cryptographic verification.** As stated in P6b, the system's provenance guarantees rest on trust in the Storage Vendor, not on mathematical proof.

**Not included: real-world identity.** As stated in P6a, provenance traces to an account, which may be anonymous.


## The provenance boundary theorem

We can now state the complete boundary of what provenance provides. Given content at V-position v in document d, the system can determine:

    1. home(poom(d).v) — the document that created the content           [P0, decidable from address]
    2. account(poom(d).v) — the account that owns the creating document   [P0, decidable from address]
    3. native(d, poom(d).v) — whether d created it or received it         [P2, decidable from address]
    4. FINDDOCSCONTAINING(poom(d).v) — all documents containing it        [P5, requires index query]
    5. correspond(d, v, d', v') for any d' — shared identity with d'      [P9, requires POOM access]
    6. links touching poom(d).v — all links to this content               [P10, requires index query]
    7. allocated_before(a, b) — relative creation order of content        [P8, decidable from address]

and the system cannot determine:

    8. the chain of COPY operations leading to this V-position             [P4, not recorded]
    9. whether COPY or VERSION placed this specific mapping                [not distinguishable]
    10. the absolute time of creation                                      [P8, not encoded]
    11. the real-world identity behind the account                         [P6a, contractual]

Items 1–3 require only the address itself — O(1), no index, no network access. Items 4–6 require index queries over potentially distributed data. Item 7 requires comparing two addresses. Items 8–11 are outside the specification.


## Provenance and the economic model

The provenance properties directly support the economic model. Nelson states: "there is a royalty on every byte transmitted... paid automatically by the user to the owner" [LM 2/43]. The mechanism:

For each byte delivered to a reader from document d at V-position v, the system computes:

    recipient = owner(home(poom(d).v))

using P0 (structural provenance) and the ownership function. The royalty flows to the owner of the home document, not to the owner of the delivering document.

When a document contains both native and transcluded content, the royalty splits. Nelson: "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]. The "proportion" is computed by classifying each V-position:

    author_share(d, u) = #{ v : v ∈ dom(poom(d)) ∧ owner(home(poom(d).v)) = u } / #dom(poom(d))

This computation requires only the POOM (to resolve V→I), the `home` function (to identify origin), and the ownership relation (to identify the creator). All are available structurally. No operation history is needed.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| P0 | Every I-address permanently encodes its origin document via syntactic prefix: home(a) = Document-field(a) | introduced |
| P1 | Content identity is I-address identity: same(r₁, r₂) ≡ iaddr(r₁) = iaddr(r₂); value equality is neither necessary nor sufficient | introduced |
| P2 | Native vs transcluded is decidable from address alone: native(d, a) ≡ home(a) = d | introduced |
| P3 | Transclusion at any depth maps to the original creator's I-addresses directly; no chain of indirection exists | introduced |
| P4 | The system does not record the chain of COPY operations; only origin (home) and current holders (spanindex) are known | introduced |
| P5 | FINDDOCSCONTAINING returns at least every document whose POOM currently maps to the queried I-addresses (may over-approximate due to append-only index) | introduced |
| P5a | Transitive discoverability: every document in a transclusion chain is returned by FINDDOCSCONTAINING on the original I-addresses | introduced |
| P6 | Attribution is computable from the I-address: account(poom(d).v) identifies the creating account for any visible byte | introduced |
| P6a | Attribution traces to an account, not necessarily a real-world person; anonymous accounts are permitted | introduced |
| P6b | No cryptographic verification; provenance integrity rests on contractual trust in the Storage Vendor | introduced |
| P7 | Version history preserves all past transclusion relationships; no separate provenance journal is needed | introduced |
| P8 | I-address allocation is monotonic: allocated_before(a, b) ⇒ a < b; provides relative creation order | introduced |
| P8a | Allocation ordering does not extend to a global cross-server timeline | introduced |
| P9 | Correspondence is I-address intersection: correspond(d₁, v₁, d₂, v₂) ≡ poom(d₁).v₁ = poom(d₂).v₂ | introduced |
| P10 | Link provenance follows content provenance: links reference I-addresses and are discoverable through any document mapping to those addresses | introduced |
| P10a | A link's home document (where it was allocated) is distinct from the provenance of the content it references | introduced |
| home | home(a) = Document-field prefix of address a — computable from address alone | introduced |
| account | account(a) = User-field prefix of address a — computable from address alone | introduced |
| native | native(d, a) ≡ home(a) = d — content was created by this document | introduced |
| transcluded | transcluded(d, a) ≡ home(a) ≠ d — content was created by another document | introduced |
| Σ.spanindex | spanindex : Addr → Set(DocId) — append-only reverse index | introduced |


## Open Questions

Must the system provide a protocol operation that explicitly returns the origin document of content at a given position, or is this always delegated to the client's ability to parse I-address prefixes?

What must the system guarantee about the freshness of FINDDOCSCONTAINING results — may the span index lag behind POOM state, and if so, within what bounds?

Must the span index eventually converge to accuracy, or is permanent over-approximation (stale entries from deleted content) the specified behavior?

What must the system guarantee about temporal provenance queries — must FINDDOCSCONTAINING support a "as of version V" parameter, or is this derivable from reconstructing historical states?

When a document's owner transfers ownership, what must the system guarantee about the provenance of content already attributed to the previous owner?

Must the system provide any mechanism to prove provenance to a third party, or is provenance always self-asserted by the system state?

What must correspondence guarantee when two documents share I-addresses through both versioning and independent transclusion simultaneously?

Under what conditions may the span index over-approximation cause incorrect royalty computation, and what reconciliation mechanism is required?

What invariant must the system maintain to ensure that self-transclusion (COPY within the same document) does not create a false impression of original authorship to an external observer?
