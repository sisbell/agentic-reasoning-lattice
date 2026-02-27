# ASN-0023: Deletion Economics

*2026-02-26*

We are looking for what happens to money when content disappears from view. In the system we study, content is never destroyed — deletion removes content from a document's virtual arrangement but leaves it permanently in the identity store. This creates an economic puzzle: obligations were established when the content was created and published, yet the act that hides the content from readers is a pure rearrangement, touching nothing in the permanent layer. We wish to know precisely which economic relationships survive deletion, which are merely attenuated, and whether any can be severed.

The question is forced by a collision between two independently specified mechanisms. The storage rental mechanism charges the content owner per byte stored, continuously, regardless of use. The royalty mechanism pays the content owner per byte delivered, transactionally, only when a reader requests the content. Deletion — a V-space operation that removes content from the current arrangement — reduces the probability of delivery but does not reduce the storage obligation. The owner's costs remain while income may vanish. We must understand this asymmetry formally, because it is not an accident but a necessary consequence of the architecture.

Nelson acknowledges the tension directly. On one hand: "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining" [LM 4/5]. On the other: the append-only storage model guarantees that "deleted bytes" remain permanently: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" [LM 4/9]. Someone must pay for bytes that no one may be reading. We formalize who, why, and under what invariants.


## The Economic State

We require a model of the system's economic dimension. Let Σ denote the system state. We assume the structural components are given: Σ.ispace : IAddr ⇀ Content (the permanent, append-only content store), Σ.poom(d) : Pos → IAddr (document d's current V-space arrangement), and Σ.pub : DocId → {private, published} (publication status). These are the substrate on which economic relationships are built. We add:

**Σ.owner : IAddr → AcctId.** For every allocated I-space address, the function owner(a) extracts the account identity from the address itself. The tumbler address structure encodes the creating account as a prefix:

    owner(a) = (THE u : u ∈ Σ.accounts : prefix(u, a))

This is not a lookup in a mutable database. It is a structural derivation from the address. Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. The ownership relation is constitutive of the content's identity — the content cannot exist without its address, and its address cannot exist without encoding its origin.

**Σ.storage : AcctId → Cost.** The ongoing storage rental obligation. For each account, the storage cost is proportional to the total I-space content allocated under that account:

    Σ.storage(u) = rate · #{a : a ∈ dom(Σ.ispace) ∧ owner(a) = u}

where rate is a per-byte-per-period charge. Nelson specifies: "One-time charge (including redundant storage at one other server): $20/meg... Annual maintenance, per server: $1/meg" [LM 5/11]. The key observation: the cost is determined by I-space occupancy, not V-space visibility. The function counts addresses in dom(Σ.ispace), which is append-only and never shrinks.

**Σ.nib : Cost.** The universal per-byte delivery royalty rate. Nelson: "Royalty is fixed per byte delivered. The unit of royalty is the nib" [LM 5/13]. And: "Royalty amount (Nib) will be fixed by Project Xanadu, and may be modified from time to time" [LM 5/20]. The nib is a network-wide parameter, not a per-document attribute. It is fixed by the system operator, not negotiable by publishers.

**Σ.register : DocId → N.** Each published document has a cash register — "a system-maintained counter which increments whenever bytes or links are delivered out of the document" [LM 5/13]. The register counts deliveries, and royalties are computed from this count.

We write deliver(a, reader) for the event where content at I-address a is transmitted to a reader. The delivery event triggers two effects: the cash register of a's home document increments, and the reader pays Σ.nib per byte delivered.


## D0: Economic Neutrality of Deletion

We are now in a position to state the central invariant. DELETE operates on V-space only. Economic obligations are tied to I-space. Therefore:

**D0 (Economic neutrality).** DELETE does not create, destroy, or modify any economic obligation. Formally, let Σ' be the state after DELETE(d, p, w):

    (i)   Σ'.storage(u) = Σ.storage(u)       for all accounts u
    (ii)  Σ'.nib = Σ.nib
    (iii) Σ'.register(d') = Σ.register(d')    for all documents d'
    (iv)  Σ'.owner(a) = Σ.owner(a)            for all a ∈ dom(Σ.ispace)

*Derivation.* Each clause follows from the architecture:

(i) Storage cost is a function of dom(Σ.ispace) and owner. DELETE does not modify ispace — deleted bytes remain at their permanent I-addresses: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11]. Since dom(Σ'.ispace) = dom(Σ.ispace) and owner is derived from the address itself, Σ'.storage = Σ.storage.

(ii) The nib is a network-wide parameter unrelated to any document's V-space arrangement.

(iii) DELETE is not a delivery event. No bytes are transmitted to a reader. No cash register increments.

(iv) Ownership is structural — derived from the immutable address prefix. No V-space operation can alter an I-space address.

D0 has a subtle but important consequence. It means the owner cannot reduce their economic obligations by editing. An author who creates 10,000 bytes, then deletes all of them from V-space, still bears the storage cost for 10,000 bytes in I-space. Nelson, reflecting on this: "The principle stands: the storage cost is real, someone must pay it, and ownership determines who. The author's 'delete' changes their view, not their obligation."

We observe that D0 holds not only for DELETE but for every V-space operation. INSERT creates new I-space content and therefore new obligations — but that is a consequence of I-space allocation, not of V-space arrangement. COPY creates V-space references to existing I-space content and therefore creates no new obligations. REARRANGE modifies V-space without touching I-space. In each case, economic obligations track I-space, and V-space operations are economically neutral *with respect to existing obligations*.


## D1: Delivery-Triggered Royalty

The royalty mechanism is event-driven, not state-based. This distinction is critical for understanding why deletion does not "suspend" royalties.

**D1 (Delivery trigger).** Royalty accrues if and only if a delivery event occurs:

    royalty_paid(a, reader) > 0   ⟺   deliver(a, reader) occurs

No delivery, no royalty. The obligation is not a standing debt that accumulates while content sits in storage. It is a per-transaction charge that fires when content moves from server to reader. Nelson: "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery" [LM 2/43].

**D2 (Royalty universality).** The royalty rate is uniform across all deliveries:

    (A a, a' : a ∈ dom(Σ.ispace) ∧ a' ∈ dom(Σ.ispace) :
      rate_per_byte(a) = rate_per_byte(a') = Σ.nib)

No document carries a custom rate. No author can set a premium. Nelson's reason is architectural: if authors could set their own rates, "permission has already been granted" would collapse — an author could set a prohibitively high rate as a de facto refusal of quotation. Nelson: "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document'" [LM 2/45].

D2 eliminates a class of economic complications. When content is "reintroduced" into a new document — that is, when a new document transcludes content that the original author deleted from their own document — there is no question of "new terms." The same nib applies. The same owner receives the royalty (by D0.iv). The delivery context is irrelevant to the payment structure.

**D3 (Proportional splitting).** When a compound document delivers content from multiple owners, royalties split by byte count:

    (A d, a : deliver(d, reader) ∧ a ∈ img(Σ.poom(d)) :
      royalty_to(owner(a)) = Σ.nib · bytes_delivered(a))

Nelson: "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]. The word "automatically" is the key — the system computes the split from the POOM, which records which I-addresses (and therefore which owners) contribute to each virtual position.


## D4: The Asymmetry

We can now state precisely what deletion does to the owner's economic position. Let A = {a : (E p' : p ≤ p' < p ⊕ w : poom(d).p' = a)} be the set of I-addresses removed from d's V-space by DELETE(d, p, w).

**D4 (Storage-royalty asymmetry).** After DELETE(d, p, w):

    (i)   Σ'.storage(owner(a)) = Σ.storage(owner(a))         for all a ∈ A    (by D0.i)
    (ii)  A ∩ img(Σ'.poom(d)) = ∅                            (A removed from d's current arrangement)
    (iii) (A d' : d' ≠ d : img(Σ'.poom(d')) = img(Σ.poom(d')))   (cross-document isolation)

The asymmetry is this: storage cost is a function of what *exists* (I-space), while royalty income is a function of what is *delivered* (transactional). By (i), the cost of storing A is unchanged. By (ii), delivery of A through d's current version is no longer possible. By (iii), delivery of A through other documents is unaffected. Deletion preserves the obligation structure but narrows one delivery pathway.

We must be precise about (ii). DELETE does not eliminate all delivery paths for A through d. It eliminates the current-version pathway, but two others remain:

**Historical backtrack.** Every previous version of d that contained A still exists and is accessible. Nelson: "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]. When a reader accesses an old version of d, the bytes in A are delivered, and the royalty fires.

**Transclusion by others.** If any document d' transcludes content at addresses in A, then d''s POOM still maps to A (by (iii) — deletion in d does not affect d'), and delivery of d' delivers A's bytes. Nelson: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11].

The owner's net economic position after deletion is:

    net_position(u, A) = royalty_income(A) − storage_cost(A)

where royalty_income(A) sums over all delivery events for A (from any source — historical versions, transclusions), and storage_cost(A) = rate · #A per period. Deletion reduces the first term (fewer delivery paths) but not the second (I-space occupancy unchanged).


## D5: Ownership Inseverability

We now establish that no V-space operation can sever the ownership relation, and therefore no editing act can redirect or extinguish economic obligations.

**D5 (Ownership inseverability).** For all a ∈ dom(Σ.ispace) and all operations op:

    owner(a) in Σ' = owner(a) in Σ

*Derivation.* owner(a) is defined as the account prefix of the tumbler address a. The tumbler address is permanent — once allocated, it is never modified, reassigned, or removed. Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address" [LM 4/19]. Since the address does not change, the prefix extraction cannot change, and therefore the ownership derivation cannot change.

This has three consequences we should state explicitly:

**D5a (Royalty routing is permanent).** The party to whom royalties are owed for content at address a is determined at allocation time and never changes:

    royalty_recipient(a) = owner(a)    for all a ∈ dom(Σ.ispace), in every reachable state

No subsequent operation — delete, edit, publish, withdraw, transfer, or default — can redirect this claim. If the content at address a is ever delivered to any reader in any future state, the system knows who is owed the royalty. The information is in the address.

**D5b (Storage obligation is permanent).** The party responsible for storage costs for content at address a is determined at allocation time:

    storage_obligor(a) = owner(a)    for all a ∈ dom(Σ.ispace), in every reachable state

Nelson: "Native bytes of a document are those actually stored under its control and found directly in storage under its control" [LM 4/11]. The bytes are native to the creating document forever. The creating account bears the storage cost forever. No mechanism exists to transfer this obligation.

**D5c (No orphaning).** The system has no operation that severs the ownership relation between content and its creator:

    ¬(E op, a : a ∈ dom(Σ.ispace) ∧ owner(a) in Σ' = ⊥)

Content cannot become "unowned." Every allocated I-address has an owner encoded in its structure, and that encoding survives every operation including the owner's economic default, disappearance, or death.


## The Worked Scenario

We verify the properties against a concrete scenario that exercises every pathway.

*Setup.* Alice (account 1.0.2) publishes document D containing 10,000 bytes at I-addresses A = {a₁, ..., a₁₀₀₀₀}. Bob (account 1.0.3) creates document E that transcludes 5,000 of Alice's bytes: B = {a₁, ..., a₅₀₀₀} ⊆ A. Carol creates link L from her document F to addresses {a₉₀₀₀, ..., a₁₀₀₀₀} in D.

Alice now DELETEs all 10,000 bytes from D's current V-space.

*Economic audit:*

**Storage (D0.i).** Alice's obligation: rate · 10,000. Unchanged. The 10,000 bytes remain in I-space at their permanent addresses. Alice's delete changed D's POOM, not dom(Σ.ispace).

**Ownership (D5).** owner(aₖ) = 1.0.2 for all k. Unchanged. The addresses still encode Alice's account prefix.

**Royalty routing (D5a).** royalty_recipient(aₖ) = 1.0.2 for all k. Unchanged.

**Cash register (D0.iii).** Σ'.register(D) = Σ.register(D). No delivery occurred during the delete.

**Bob's document E.** Bob's POOM is unaffected (D4.iii, cross-document isolation). E still maps V-positions to {a₁, ..., a₅₀₀₀}. When a reader accesses E, those 5,000 bytes are delivered from Alice's I-space. D's cash register increments by 5,000. Alice receives Σ.nib · 5,000 in royalty. Alice's deleted content generates income through Bob's transclusion.

**Carol's link L.** L's endsets reference {a₉₀₀₀, ..., a₁₀₀₀₀} in I-space. These addresses are permanent. L remains valid. If a reader follows L and the system delivers those bytes (e.g., via historical backtrack of D), Alice's register increments and she receives royalty.

**Historical backtrack of D.** A reader requests D as it existed before the deletion. The system delivers all 10,000 bytes. Alice receives Σ.nib · 10,000 in royalty for that delivery.

**The economic picture.** Alice bears storage cost for 10,000 bytes continuously. She receives royalty for 5,000 bytes whenever Bob's document is read, for 10,000 bytes whenever her historical version is read, and for 1,000 bytes whenever Carol's link is followed to a historical version. Her delete changed the *probability distribution* of deliveries but not the *rate structure* or *obligation structure*.


## D6: The Monotonic Burden

The scenario above illustrates a broader property that we should state in full generality.

**D6 (Monotonic storage burden).** For any account u, the storage obligation is monotonically non-decreasing:

    Σ.storage(u) ≤ Σ'.storage(u)    for all operations transforming Σ to Σ'

*Derivation.* Σ.storage(u) = rate · #{a : a ∈ dom(Σ.ispace) ∧ owner(a) = u}. Since dom(Σ.ispace) ⊆ dom(Σ'.ispace) (I-space is append-only) and owner is invariant (D5), the count can only increase or stay the same. INSERT adds new addresses (increasing the count). All other operations leave dom(Σ.ispace) unchanged (preserving the count).

The burden never decreases because there is no operation that removes content from I-space. Nelson's append-only architecture makes this inevitable: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically" [LM 2/14]. An append-only store has no mechanism for reducing the total. Every byte ever created by an account accumulates into its storage obligation.

This is the formal expression of what Nelson calls "the price of permanence." The author's commitment to the docuverse is irrevocable. Others will link to their content. Others will quote it. Others will build upon it. The publication contract makes this explicit: "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility" [LM 2/43]. The storage cost is the cost of that commitment.


## D7: The Discovery Obligation

An owner whose content has been deleted from their own V-space but persists in I-space — generating storage costs and possibly royalty income through others' transclusions — needs to know the state of their economic obligations. We now ask: must the system provide this information?

Nelson specifies building blocks. The cash register gives aggregate accounting per document: total deliveries, from which total royalty can be computed. But it does not decompose by span — the owner cannot determine which specific bytes generated which revenue.

FINDDOCSCONTAINING can locate transclusions: "This returns a list of all documents containing any portion of the material included by ⟨vspec set⟩" [LM 4/70]. But the owner must specify *which content* to search for, and if they have deleted it from their current V-space, they must recover the relevant addresses through historical backtrack before they can query.

The path exists but is circuitous. We formalize the obligation:

**D7 (Economic discoverability).** The system must provide sufficient operations for a content owner to determine, for any content they own:

    (i)   whether that content persists in I-space (always yes, by permanence)
    (ii)  which other documents currently transclude it
    (iii) the aggregate delivery count (via the cash register)
    (iv)  the ongoing storage cost

Nelson's principles require this. He describes the system as having "a contractual structure which makes it possible for people to use it confidently" [LM 4/4]. An owner who cannot discover what economic activity is tied to content they own cannot participate confidently in the system.

The system *possesses* all information needed for (i)–(iv): I-space tracks content existence; the span index tracks transclusion relationships; the cash register tracks deliveries; the storage model computes cost from I-space occupancy. The question is whether the system is obligated to expose these in a composable way. We observe that the building blocks — historical backtrack, FINDDOCSCONTAINING, the cash register — suffice in principle but do not compose into a single query. A dedicated operation — "enumerate all persisting economic obligations for content owned by account u" — is not specified, but is implied by the contractual participation guarantee.

We note a subtlety: FINDDOCSCONTAINING is approximate. It returns a superset of documents that currently contain the queried addresses, because the span index is append-only and retains stale entries. Therefore the owner's query for "who is currently transcluding my content" may overcount. The owner must filter results by resolving each candidate document's POOM against the queried addresses — an exact but more expensive operation. The system guarantees no false negatives (every current transclusion is reported) but may produce false positives (past transclusions that no longer hold).


## The Permanence-Sustainability Tension

We have now formalized the invariants. What remains is to characterize precisely where the specification leaves a gap. The tension is between two properties that Nelson states independently:

**Permanence.** Content in I-space is permanent. No operation removes it. The append-only architecture makes destruction structurally impossible.

**Self-sustainability.** "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily" [LM 4/5]. Storage must be paid for. The question is *by whom*.

For content whose owner is actively paying, there is no tension. The owner pays storage rental; delivery royalties offset some or all of that cost; the net economic position may be positive (popular content) or negative (unpopular content), but the obligations are clear.

The tension emerges for content whose owner has stopped paying. D6 says the storage obligation is monotonically non-decreasing. D5b says the storage obligor is permanently the original owner. But what if the owner defaults?

The content cannot be destroyed (permanence). The obligation cannot be transferred (D5b — ownership is structural). The obligation cannot be reduced (D6 — the burden is monotone). Yet someone must pay for physical storage (self-sustainability).

Nelson identifies several mechanisms that delay but do not resolve this collision:

1. **Royalty offset.** Content that others transclude continues to generate delivery royalties. These may offset storage costs. But for unpopular deleted content — content no one reads and no one transcludes — there is no offset.

2. **The Author's Fund.** "When bytes are taken from an unpublished document (one in the public domain), this surcharge is added to the Author's Fund, an escrow account whose purpose is the charitable funding of worthy causes within the network" [LM 5/12]. Nelson did not extend this to cover storage costs for defaulted content from owned documents, but the mechanism exists in principle.

3. **Declining storage costs.** Nelson designed the system anticipating that storage costs would fall exponentially over time. Content that is expensive to store today may cost essentially nothing to store in a decade. The tension is self-limiting if storage costs approach zero.

4. **Vendor transition.** "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16]. Content migrates; it does not vanish.

We formalize the gap without claiming to resolve it:

**D8 (The storage lapse problem).** For content at address a where owner(a)'s economic status has lapsed:

    a ∈ dom(Σ.ispace)                               — content exists (permanence)
    ∧ storage_obligor(a) = owner(a)                  — owner owes the cost (D5b)
    ∧ owner(a) is not paying                         — owner has defaulted
    ∧ storage_cost(a) > 0                            — physical storage requires funding
    ⟹  ???

The system has an obligation (permanence) and a constraint (self-sustainability) that are jointly unsatisfiable when no party pays. Nelson does not specify which yields. What we *can* state is what must NOT happen: the content must not be destroyed (the append-only architecture forbids it), the ownership must not be severed (the address encoding forbids it), and the economic structure must not be altered (D0, D5 forbid it). The content may become inaccessible — withheld from delivery — but this is a delivery-layer decision, not a storage-layer event. The content remains in I-space, waiting to be re-lit.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.owner | owner : IAddr → AcctId — account identity derived from I-address prefix | introduced |
| Σ.storage | storage : AcctId → Cost — ongoing per-byte storage rental, proportional to I-space occupancy | introduced |
| Σ.nib | nib : Cost — universal per-byte delivery royalty rate, set network-wide | introduced |
| Σ.register | register : DocId → N — per-document cash register counting byte deliveries | introduced |
| D0 | DELETE does not create, destroy, or modify any economic obligation (storage, nib, register, ownership all invariant) | introduced |
| D1 | Royalty accrues if and only if a delivery event occurs — no standing obligation, purely transactional | introduced |
| D2 | Royalty rate is universal: every byte delivered at the same nib, no per-document or per-author rates | introduced |
| D3 | Compound-document royalties split proportionally by byte count, determined automatically from the POOM | introduced |
| D4 | Storage-royalty asymmetry: deletion preserves storage cost, eliminates one delivery pathway, leaves others intact | introduced |
| D5 | Ownership inseverability: no operation changes owner(a) for allocated a | introduced |
| D5a | Royalty routing is permanent: royalty_recipient(a) = owner(a) in every reachable state | introduced |
| D5b | Storage obligation is permanent: storage_obligor(a) = owner(a) in every reachable state | introduced |
| D5c | No orphaning: every allocated I-address has an owner; content cannot become unowned | introduced |
| D6 | Monotonic storage burden: Σ.storage(u) ≤ Σ'.storage(u) — the obligation never decreases | introduced |
| D7 | Economic discoverability: the system must allow owners to discover persisting obligations for content they own | introduced |
| D8 | The storage lapse problem: when the owner defaults, permanence and self-sustainability are jointly unsatisfiable | introduced |


## Open Questions

Must the system guarantee that storage costs for content deleted from V-space can never exceed the royalty income that content generates through transclusion and historical backtrack?

Must the system distinguish between storage costs for content the owner actively uses and content the owner has deleted but the system retains — or is a uniform per-byte rate the only consistent model?

What must the system guarantee about the cash register's granularity — must it decompose deliveries by I-address span, or is aggregate per-document accounting sufficient for an owner to make informed economic decisions?

Must the system provide a single operation for discovering all persisting economic obligations, or may it require the owner to compose multiple queries (historical backtrack, FINDDOCSCONTAINING, cash register)?

What invariants must govern the Author's Fund if it is extended to absorb storage costs for defaulting owners of published content?

Must the system guarantee that content whose storage cost is being borne by a third party (e.g., through a preservation mechanism) retains the original owner's royalty routing — or may the funding party negotiate economic terms?

What minimum economic disclosure must the system provide to third parties (transcluders, linkers) whose content depends on another owner's I-space content that may become inaccessible due to storage default?
