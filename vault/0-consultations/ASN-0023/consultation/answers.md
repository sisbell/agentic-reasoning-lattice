# Consultation Answers — Deletion Economics

**Inquiry:** What must the system guarantee about economic obligations — storage costs, royalty flows, ownership accounting — when content is deleted from V-space but persists in I-space?
**Date:** 2026-02-26 20:24
**Questions:** 10 (10 nelson, 0 gregory)

---

## Question 1 [nelson]

> When an author removes content from a document but the system retains it permanently, must the author continue to bear the storage cost for the retained copy?

### Nelson's Answer

## Storage Cost for Retained "Deleted" Content

This is a genuine gap in my specification. I addressed the pieces but never explicitly connected them for this case. Let me walk through what I *did* say and where the logic leads.

### What I Specified

**Delete is not destruction.** Content removed from a document's V-space arrangement remains permanently in I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

**Storage is ongoing rental, per-byte, paid by the owner:**

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

The projected costs (in 1990 dollars): $20/meg one-time, $1/meg annual maintenance per server [LM 5/11].

**The append-only model:**

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### What I Did NOT Specify

I never addressed the intersection: **who pays for bytes that the owner has removed from their current arrangement but the system retains for structural integrity?**

The storage rental model described in Chapter 5 speaks of storage costs per-byte-stored. The deletion model in Chapter 4 says deleted bytes remain in I-space. But I never wrote the sentence connecting these two facts.

### What the Logic of My System Implies

The honest answer is that the author must bear the cost, and here is why:

1. **Storage rental is about physical storage (I-space), not arrangement (V-space).** You pay for what is stored under your control. Deleted bytes are still stored under your control — they are native bytes of your document at your I-address.

2. **The system has no mechanism for "orphaning" I-space content.** There is no operation that severs ownership. The I-address permanently encodes the home document:

   > "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

3. **Self-sustainability demands it.** If authors could escape storage costs by "deleting" from V-space while the system retains the bytes, who pays? Not the reader (they pay delivery charges). Not other authors. Not the Storage Vendor (they must be self-sustaining too). The only party with an ownership relationship to those bytes is the original author.

### The Compensating Factor

This is not as punitive as it sounds, because the royalty mechanism provides income for retained content:

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 5/12]

If other documents transclude your "deleted" content, you still receive royalties when those bytes are delivered. The bytes you deleted from your own view may be very much alive in the docuverse — quoted, linked to, transcluded — and each delivery generates income for you. Your storage cost for retaining them is offset by their continued use.

Historical backtrack also requires these bytes. When someone requests a previous version of your document, your deleted content is delivered and you receive royalty for it.

### What I Should Have Addressed But Didn't

Several questions follow that I left unresolved:

- **Can an author distinguish "bytes I want to keep in I-space" from "bytes the system insists on retaining"?** No — there is no such distinction in my model. All I-space content is permanent.

- **What if storage costs exceed royalty income indefinitely?** This is analogous to a publisher warehousing unsold books. Eventually the economics force a choice. But in my system, you cannot "pulp" I-space content — it is permanent. So the cost continues.

- **Could the Author's Fund absorb orphaned storage costs?** I specified the Author's Fund for public domain content:

  > "When bytes are taken from an unpublished document (one in the public domain), this surcharge is added to the Author's Fund, an escrow account whose purpose is the charitable funding of worthy causes within the network." [LM 5/12]

  But I never extended this to cover storage costs for retained deleted content from owned documents.

- **What happens when the owner stops paying entirely?** I explicitly noted this as unspecified in the storage funding model. The content cannot be destroyed (permanence guarantee), but whether it becomes inaccessible — and what that means for other documents that transclude it — is a serious architectural question I did not resolve.

### The Deeper Tension

This question exposes a real tension in my design between two principles:

1. **Permanence**: Nothing is ever destroyed. Every version remains.
2. **Self-sustainability**: Every service pays for itself. No subsidies.

If content must be permanent but storage must be paid for, then *someone* must always pay for *everything ever written*, forever. For popular content, royalties cover this naturally. For obscure content that no one reads, the author bears an eternal obligation for bytes they may no longer want.

I did not resolve this tension. The system as I described it implicitly places the burden on the author, because that is where ownership — and therefore financial responsibility — resides. Whether this is just, or whether a more sophisticated model (graduated rates for cold storage, Author's Fund absorption after abandonment, community preservation mechanisms) would better serve the vision, is a question I left for implementors.

The principle stands: the storage cost is real, someone must pay it, and ownership determines who. The author's "delete" changes their view, not their obligation.

---

## Question 2 [nelson]

> If content is no longer visible in any document but persists in permanent storage, must royalty obligations to the original creator continue or may they be suspended?

### Nelson's Answer

## Royalty Obligations for Content Removed from V-Space

The answer is clear from Nelson's architecture: **royalty obligations are not suspended, because they are not standing obligations in the first place.** The royalty mechanism is triggered by *delivery*, not by *existence*. And content removed from all current V-space arrangements can still be delivered.

### The Trigger: Delivery, Not Storage

Nelson's royalty is per-byte-delivered, not per-byte-stored:

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." [LM 5/13]

There is no standing royalty obligation that accrues while content sits idle. If no one requests the content, no royalty is generated. The question of "suspension" is a category error — there is nothing to suspend when the mechanism is purely transactional.

### Content Removed from V-Space Is Not Invisible

The premise that content could become "no longer visible in any document" misunderstands what DELETE means in Xanadu. Nelson is explicit:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Content removed from the current V-space arrangement remains accessible through two channels:

1. **Historical backtrack.** Every previous version persists. "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

2. **Transclusions in other documents.** If any other document ever transcluded (windowed) that content, their V-space mapping still references the same I-space bytes: "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

In both cases, when a user requests delivery — whether through historical backtrack or through reading a document that transcludes the content — the bytes are transmitted, and the per-byte royalty applies automatically.

### The Economic Logic

Nelson's model has two separate payment streams, and they operate independently:

**Storage rental** (paid by the owner, ongoing):
> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

The owner continues paying storage rental for I-space content regardless of whether anyone reads it. This is the cost of permanence.

**Byte delivery royalty** (paid by the reader, per-access):
> "Royalty is fixed per byte delivered. The unit of royalty is the nib." [LM 5/13]

This only flows when content is actually transmitted. No delivery, no royalty. Delivery through any channel — current version, historical version, transclusion — triggers the same mechanism.

### The Asymmetry

This creates a deliberate asymmetry:

- **Unpopular content costs the owner.** Storage rental accrues without offsetting royalty revenue. The owner bears the cost of persistence.
- **Popular content pays for itself.** Delivery royalties offset storage costs and generate profit.
- **Deleted-but-accessible content** sits in between: the owner pays storage, and receives royalty only when someone actually accesses a historical version or follows a transclusion.

Nelson acknowledges this economic reality through the Author's Fund mechanism for public domain content, but does not provide any "royalty suspension" for low-traffic content.

### Summary

| Scenario | Royalty? | Why |
|----------|---------|-----|
| Content in current V-space, actively read | **Yes** | Bytes delivered → nib charged |
| Content deleted from V-space, accessed via historical backtrack | **Yes** | Bytes still delivered → nib charged |
| Content deleted from V-space, transcluded by another document, that document read | **Yes** | Bytes delivered from I-space → nib charged to original |
| Content in I-space, no one requests it | **No royalty generated** | No delivery occurs; but obligation is not "suspended" — it simply has no trigger |

The royalty obligation *cannot* be suspended because it is not a standing debt. It is a per-transaction charge. As long as content can be delivered — and in Xanadu, content in I-space can *always* be delivered through historical backtrack — the mechanism remains active. The question is not whether the obligation exists, but whether anyone triggers it.

---

## Question 3 [nelson]

> Must the system maintain an unbroken ownership record for content that has been removed from all documents but still exists in the permanent layer?

### Nelson's Answer

## Ownership of Unreferenced I-Space Content

The short answer: **yes, but the question assumes a separation that doesn't exist in my architecture.** There is no "ownership record" separate from the content's address. The I-address IS the ownership record.

### The Address Is the Provenance

Every byte in I-space has a permanent tumbler address of the form:

```
Node.0.User.0.Document.0.Element
```

The User field identifies who created it. The Document field identifies which document it was born in. This is not metadata attached to the content — it is the address itself. You cannot fetch the content without knowing its origin, because the origin is how you address it.

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

There is no separate ownership database that could become "broken." The provenance chain is structural and immutable.

### Content Removed from All Documents

When content is deleted from its document's V-space and is not transcluded by any other document, it enters what I called the "deleted bytes" state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Note the phrasing: "not currently addressable" — meaning not reachable through any current V-space arrangement. But the bytes remain in I-space. They are "awaiting historical backtrack functions." They have not ceased to exist.

Furthermore:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Even in the limiting case where no other document includes them, the I-space content persists. The append-only storage model guarantees this:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Why the Ownership Chain Cannot Break

Three properties make an "unbroken ownership record" automatic rather than something that must be separately maintained:

1. **I-addresses are permanent.** Content at address `1.0.3.0.27.0.1.5` will always be at that address. The "3" will always mean account 3. The "27" will always mean document 27.

2. **I-space is append-only.** Content is never removed from I-space. There is no garbage collection, no expiration, no reclamation of unreferenced content.

3. **Addresses are never reassigned.** A tumbler address that once pointed to content will never point to different content. "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

The ownership record is not maintained *alongside* the content — it is *constitutive* of the content's identity. The content cannot exist without its address, and its address cannot exist without encoding its origin.

### The Unresolved Tension: Who Pays?

There is, however, a genuine tension that I did not fully resolve. My funding model requires ongoing storage rental:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

If content has been removed from all V-space arrangements, it generates no byte-delivery royalties (no one is reading it). Yet it still occupies I-space and must be stored. Who pays?

The document's owner presumably continues paying storage rental for the document as a whole, which includes its I-space contents — both currently visible and "deleted." But I did not explicitly address the case where the owner stops paying, or what happens to orphaned I-space content whose owner has vanished.

The permanence guarantee and the self-sustainability requirement are in tension here. I stated both as requirements but did not reconcile them for this edge case.

### Summary

The system does not need to *maintain* an ownership record for unreferenced content because it cannot *lose* one. The ownership is the address. The address is permanent. The content is permanent. No mechanism exists by which the ownership chain could break.

What I left unspecified is what happens economically when no one is paying for storage of content that exists only in I-space with no V-space references — content that is, in a sense, dark matter in the docuverse. It exists, it has an owner encoded in its address, but no one may be sustaining it financially.

NEED_RAW: [4/5, 4/9, 4/79, 5/11-5/13] — to verify whether Nelson says anything further about the lifecycle of unreferenced I-space content or the economic obligations of document owners for "deleted" content specifically.

---

## Question 4 [nelson]

> When a document edit removes quoted content, does the transclusion royalty obligation end at the moment of removal or persist as long as the content remains permanently stored?

### Nelson's Answer

# Royalty Obligation After Transclusion Removal

The answer falls cleanly out of the architecture: **royalty is triggered by delivery, not by storage.** The obligation ends for the current version at the moment of removal, but persists for all historical versions that still contain the transclusion.

## The Mechanism: Per-Byte-Delivered

The royalty fires on transmission, not on existence:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

The cash register increments on delivery:

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." [LM 5/13]

No delivery means no royalty. Storage alone generates no royalty obligation.

## What "Removal" Actually Does

Removing a transclusion is a V-space edit. It changes the document's current arrangement but destroys nothing:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

After removal:
- The **current version's V-space** no longer maps to the quoted content
- Readers of the current version **receive no bytes** from the quoted source
- Therefore **no royalty accrues** from current-version readings

## But Historical Versions Persist

Every previous version of the document still exists and still contains the transclusion. Nelson is explicit that all versions are permanently accessible:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

When someone accesses an **old version** that still contains the transclusion, the quoted bytes are delivered, and royalty fires normally. The original author gets paid for that delivery just as they would for any other.

## The Two Revenue Streams (Separated)

Nelson's funding model distinguishes storage cost from delivery royalty:

| Stream | Trigger | Who Pays | Relevant Here? |
|--------|---------|----------|----------------|
| **Storage rental** | Ongoing, per-byte stored | Document owner | No — this is paid by the owner of the *quoting* document for their own storage |
| **Byte delivery charge** | Per-byte delivered to reader | Reader | Yes — stops when bytes stop being delivered |
| **Royalty surcharge** | Per-byte delivered to reader | Reader → Author | Yes — stops when bytes stop being delivered |

Storage rental is the owner's cost for keeping their document accessible. It has nothing to do with the quoted author's royalty. The quoted author's income comes entirely from delivery:

> "When the network charges incurred by that document have been offset, the remainder becomes the author's profit." [LM 5/12]

## Summary

The question frames a false binary. Royalty is event-driven, not state-driven:

- **Current version**: No delivery → no royalty. Obligation ends at removal.
- **Historical versions**: Still deliver the bytes → royalty still fires. Obligation persists as long as anyone reads old versions.
- **I-space persistence**: Irrelevant to royalty. Content existing in permanent storage generates no income by itself. Only delivery triggers payment.

This is architecturally consistent. Nelson designed royalty as "proportional use of byte delivery" [LM 2/43] — a usage-based model, not a storage-based model. The permanent I-space storage of content is a preservation guarantee, not an economic obligation. The economic relationship lives entirely in the delivery event.

---

## Question 5 [nelson]

> Must the system distinguish between "content a user chose to delete" and "content the system must retain for permanence" when calculating who owes storage costs?

### Nelson's Answer

# Storage Costs for "Deleted" Content

## The Short Answer

Nelson does not explicitly address this distinction. His architecture implies that the question is **structurally moot** — because "deleted" content and "retained" content are the same thing in I-space. There is no separate category to distinguish.

## Why the Distinction Dissolves

Nelson's DELETE operates exclusively on V-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The I-space content is unchanged by deletion. The bytes still live at their permanent I-address, still under the document's storage. From the storage system's perspective, nothing happened — a V-space mapping was removed, but no bytes were created, moved, or destroyed.

## What Nelson Says About Storage Costs

Storage rental is per-byte, ongoing, paid by the owner:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

The pricing is based on bytes **stored**, not bytes **currently visible in V-space**:

> "One-time charge (including redundant storage at one other server): $20/meg... Annual maintenance, per server: $1/meg" [LM 5/11]

Since deleted bytes remain in I-space storage, they remain stored bytes. Nelson's cost model counts them the same as any other byte.

## The Economic Tension

This creates an asymmetry Nelson does not resolve. Consider:

1. Alice creates 10,000 bytes in her document
2. Bob transcludes 5,000 of those bytes into his document
3. Alice "deletes" all 10,000 bytes from her V-space
4. The 10,000 bytes still exist in I-space under Alice's document
5. Bob's document still shows the 5,000 transcluded bytes
6. Alice is still paying storage rental for all 10,000 bytes

Alice cannot destroy the I-space content because:
- Bob's transclusion depends on it
- Previous versions of Alice's document reference it
- Links may point to it
- The append-only model forbids removal

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

## The Partial Offset

Nelson's royalty model provides a partial answer. When Bob's document delivers Alice's transcluded bytes to readers, Alice receives royalties:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

So "deleted" content that others still use generates revenue for the original owner, offsetting the storage cost. Content that nobody reads or transcludes generates no revenue — but the owner still pays storage.

## What Nelson Does NOT Specify

Several questions remain open:

1. **Whether "deleted" bytes count toward the owner's storage rental** — implied yes (they're still stored), but never stated explicitly
2. **Whether storage costs can be transferred** — if Alice's content exists solely because Bob transcludes it, can Bob be charged?
3. **Whether there is a category of "system-retained" content** with different economics — never mentioned
4. **Whether storage rental lapses lead to inaccessibility** — never addressed
5. **Whether the Author's Fund can absorb orphaned storage costs** — the Fund is specified for "public domain" content [LM 5/12], not for content whose owner stops paying

## My Intent

The system I designed does not need to distinguish between "deleted" and "retained" content for storage costs because the distinction is an artifact of thinking in terms of destructive file systems. In Xanadu, you are not paying for a file that sits on a disk. You are paying for your contribution to the permanent record of civilization.

When you create content and publish it, you are making a commitment. Others will link to it. Others will quote it. Others will build upon it. The publication contract makes this explicit:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

The storage cost is the cost of that commitment. Whether you currently display the content in your own document's V-space is your editorial choice — it does not change the obligation to the network.

That said, I acknowledge the economics are not fully worked out. The scenario where an owner "deletes" everything from V-space but remains perpetually liable for I-space storage costs — especially for content only others use — is a tension I did not resolve in Literary Machines. The royalty mechanism provides a partial answer (you earn when others use your content), but it does not cover the case where content generates no traffic yet cannot be removed.

NEED_RAW: [4/5, 5/11-5/13] — to verify whether Nelson says anything more specific about per-byte storage accounting that distinguishes active from inactive content.

---

## Question 6 [nelson]

> If a link points to content that has been removed from its source document but still exists permanently, must the system preserve the economic relationship between the linking party and the content owner?

### Nelson's Answer

# Must the System Preserve the Economic Relationship for "Deleted" Content?

**Yes.** This follows necessarily from the intersection of several explicitly stated principles. Let me trace the reasoning.

## 1. "Deletion" Does Not Destroy Content

DELETE in Xanadu removes content from V-space only. The I-space content is permanent:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes still exist at their permanent I-address. They are "not currently addressable" in the current V-space arrangement — but they have not left the system.

## 2. Links Survive Because They Point to I-Space

Links attach to bytes, not to V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Since the "deleted" bytes still exist in I-space, links pointing to them remain valid. The link doesn't know or care that the content was removed from the current V-space arrangement.

## 3. Royalty Triggers on Byte Delivery, Not V-Space Presence

The royalty mechanism is explicit — it fires on *transmission*, not on current arrangement:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

And the accounting mechanism:

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." [LM 5/13]

The trigger is "bytes delivered," not "bytes currently in the V-stream." When someone follows a surviving link and the system transmits those bytes from I-space, the cash register increments.

## 4. Origin Determines Who Gets Paid

The I-address structurally encodes ownership:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The bytes' I-address still encodes the original document. The system knows whose cash register to increment because the address itself says so. This cannot be altered by V-space operations.

## 5. Publication Creates an Irrevocable Obligation

The author cannot escape this relationship by "deleting" published content:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it." [LM 2/43]

The former version *must remain* precisely because others have linked to it. And if it remains and is delivered, royalties flow.

## The Complete Chain

Putting it together:

1. Alice publishes content → bytes get permanent I-addresses encoding Alice's document
2. Bob creates a link pointing to those bytes (via I-space) → Bob owns the link
3. Alice "deletes" the content from her current version → V-space mapping removed; I-space bytes untouched
4. A reader follows Bob's link → system fetches bytes from their I-space home location (Alice's document)
5. Bytes are delivered → Alice's cash register increments → royalty flows to Alice

Every step is individually specified by Nelson. The economic relationship is preserved because:
- The bytes still exist (non-destruction)
- The link still works (survivability)
- Delivery still triggers payment (per-byte royalty)
- The address still identifies the owner (origin traceability)

## What Nelson Does Not Explicitly Address

Nelson never poses this exact scenario — "what happens to royalties when V-space-deleted content is accessed via a surviving link." But the answer is fully determined by his stated principles. There is no mechanism by which the economic relationship *could* be severed without violating at least one fundamental guarantee:

- Destroying I-space content would violate permanence
- Breaking the link would violate survivability
- Skipping the royalty would violate per-byte payment
- Losing the owner would violate origin traceability

The economic relationship persists because every component it depends on is independently guaranteed to persist.

---

## Question 7 [nelson]

> Must the system guarantee that no economic obligation can be created or destroyed by the mere act of removing content from a visible document?

### Nelson's Answer

# Economic Neutrality of Content Removal

## Short Answer

Yes — but Nelson does not state this as an explicit guarantee. It is an **architectural invariant** that follows necessarily from three independent design decisions, each of which he specifies clearly.

## The Three Pillars

### 1. DELETE Is a V-Space Operation Only

DELETE removes content from a document's current arrangement (V-space) but does not touch permanent storage (I-space).

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content still exists at its permanent I-address. Previous versions still contain it. Other documents that transclude it still show it.

### 2. Economic Obligations Are Tied to I-Space Delivery, Not V-Space Visibility

The royalty mechanism triggers on **byte transmission**, not on whether those bytes appear in any particular document's current V-stream:

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." [LM 5/13]

The cash register counts deliveries from I-space. It is indifferent to whether the document's current V-stream includes or excludes those bytes.

### 3. Storage Costs Are Tied to I-Space Occupancy

Storage rental is per-byte in permanent storage, paid by the owner regardless of V-space arrangement:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Since DELETE does not remove bytes from I-space, storage obligations are unchanged by deletion.

## The Proof

Trace through any deletion scenario:

**Alice publishes document D containing content C. Bob transcludes C into document E.**

1. Alice deletes C from D's current V-stream.
2. C remains at its permanent I-address under D.
3. C remains visible in D's previous versions.
4. C remains visible in Bob's document E (transclusion resolves to I-space).
5. When any reader accesses C — through E, through D's history, through any other transclusion — D's cash register increments.
6. Alice's royalty entitlement per byte delivered is unchanged.
7. Alice's storage obligation for C's I-space occupancy is unchanged.
8. Bob's royalty entitlement for his arrangement is unchanged.

No economic obligation was created. No economic obligation was destroyed. The deletion changed the **likelihood** of certain deliveries (fewer readers may encounter C if D is the primary access path), but the **obligation structure** — who pays whom, at what rate, upon what trigger — is identical before and after.

**The same holds when no transclusion exists.** If Alice deletes C and no one has transcluded it, the content remains in I-space. Previous versions remain accessible. The royalty rate per byte delivered is unchanged. Storage costs are unchanged. The only thing that changes is the practical probability of delivery — a revenue effect, not an obligation effect.

## Why This Must Be a Guarantee

Nelson does not state this invariant explicitly, but it is **required** by guarantees he does state:

1. **Non-destruction guarantee**: "Without damaging the originals" [LM 2/45]. If deletion could destroy economic obligations, it would damage the originals' economic structure — a form of damage to the original.

2. **Attribution guarantee**: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. Attribution is the basis for royalty routing. If attribution survived but economic obligations didn't, the system would be internally contradictory.

3. **Link freedom guarantee**: "Each user is free to link to anything" [LM 2/43]. Others' links depend on the continued economic accessibility of content. If deletion could destroy the economic obligation to serve that content, it would undermine the link freedom guarantee.

4. **Permanence guarantee**: "Any address of any document in an ever-growing network may be specified by a permanent tumbler address" [LM 4/19]. A permanent address that resolves to content whose economic obligations have been destroyed is an address to economically inaccessible content — a hollow permanence.

## The Architectural Elegance

The guarantee costs nothing to implement because it falls out of the I-space/V-space separation. Nelson did not need to add a special rule saying "DELETE must not affect economics." By designing DELETE as a pure V-space operation and designing economics as an I-space phenomenon, economic neutrality of deletion is **structurally inevitable**.

This is characteristic of Nelson's design philosophy: the right architectural separation eliminates entire categories of problems without requiring explicit rules to handle them.

## What Nelson Does NOT Address

The guarantee holds for **content removal from a visible document** (DELETE). It does not extend to:

- **Document withdrawal** — Nelson acknowledges this is possible "by lengthy due process" [LM 2/43] and it would affect future deliveries. But even withdrawal doesn't destroy existing obligations; it prevents new ones from accruing.
- **Storage lapse** — If an owner stops paying storage rental, content accessibility may be affected. Nelson does not specify what happens. This is a gap in the specification, not a contradiction of the invariant.
- **Link deletion** — An owner can delete their own links, which could reduce discovery paths to content and thus reduce deliveries. But the obligation per delivery remains unchanged.

---

## Question 8 [nelson]

> When multiple versions of a document exist and content appears in earlier versions but not the current one, must the system account for storage costs across all versions or only the version that introduced the content?

### Nelson's Answer

# Storage Costs Across Versions

## Short Answer

The system must account for storage costs across **all versions**, not just the current one. This follows necessarily from the append-only architecture. "Deleted" content remains in I-space permanently — the owner pays for every native byte regardless of its visibility in the current arrangement.

## Why This Is Structural, Not a Policy Choice

Three principles lock this in:

**1. I-Space is append-only.** Content is never removed from storage.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**2. "Deletion" removes from V-space only.** The bytes remain in I-space.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

**3. Native bytes are stored under the document's control.**

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

Bytes that were created in your document remain native to your document forever. Their I-space address encodes your document as their origin. They don't migrate to some other owner's storage just because you removed them from your current V-space arrangement.

## The Billing Consequence

Storage rental is ongoing, per-byte, paid by the owner:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

The pricing model charges per megabyte stored:

> "STORAGE... One-time charge (including redundant storage at one other server): $20/meg... Annual maintenance, per server: $1/meg" [LM 5/11]

Since the system **cannot** remove bytes from I-space, and the pricing is per megabyte **stored**, the owner necessarily pays for all bytes that are native to their document — including those present only in earlier versions. There is no mechanism by which "deleting" content from the current version would reduce the storage footprint, because the bytes are still physically present in the append-only store.

## The Offsetting Revenue

This cost is partially offset by royalties. When someone accesses an older version of your document (which they can always do — "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]), the byte delivery generates royalty:

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

So "deleted" content that people still access via historical backtrack generates revenue for the owner. The economic incentive aligns: you pay to store your full history, but you earn when anyone reads any part of it.

## What Nelson Does NOT Specify

Nelson does not explicitly address these related questions:

- Whether billing distinguishes "currently visible" bytes from "historical" bytes at different rates
- Whether a document that grows through many edits (accumulating I-space bytes) hits a practical economic limit where the owner stops paying
- What happens to the content when storage rental lapses — the curated sources note this as a gap: "Nelson does NOT specify what happens to content when storage rental lapses"
- Whether there is any garbage-collection mechanism for truly orphaned bytes (the architecture strongly implies there is not)

NEED_RAW: [4/5, 5/11-5/13] — these pages contain the detailed economics. The curated sources capture the key quotes but the original pages may contain additional detail about how storage costs are calculated relative to document size over time.

## Summary

| What | Who Pays | Why |
|------|----------|-----|
| Current V-space content | Document owner | Native bytes under owner's control |
| "Deleted" content (earlier versions only) | Document owner | Still native, still in I-space, still stored |
| Transcluded content from others | Original author's document | Bytes are native to origin, not to transcluding document |

The system charges for physical storage, and physical storage is append-only. Every byte you ever created remains stored. You pay for all of them. This is the price of permanence.

---

## Question 9 [nelson]

> Must the system provide the content owner a way to discover all persisting economic obligations tied to content that is no longer visible in any document?

### Nelson's Answer

## Yes — but the mechanism is only partially specified

Nelson's architecture creates clear conditions under which economic obligations persist for content removed from V-space, and his principles imply the owner must be able to discover them. But the specified FEBE operations leave a gap in the discovery path.

### Economic obligations survive V-space deletion

Three guarantees combine to create persistent obligations:

**1. I-space permanence.** DELETE removes content from V-space only; I-space is untouched.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

**2. Transclusion creates independent V-space references.** When Bob uses COPY to transclude Alice's content, Bob's document creates its own V-space mapping to Alice's I-space content. Alice's subsequent deletion of that content from her V-space has no effect on Bob's mapping.

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

**3. Royalty accrues per byte delivered, automatically.** When Bob's document delivers Alice's content to a reader, Alice receives royalty — determined automatically by I-space origin.

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

So: Alice creates content. Bob transcludes it. Alice deletes it from her own document. Bob's document still delivers Alice's bytes. Royalties still flow to Alice. The economic obligation persists indefinitely.

### What discovery mechanisms exist

Nelson specifies building blocks that partially address the problem:

**The cash register** provides aggregate accounting per document:

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document. The cash register has no size limit. It is in the user's system area, along with passwords and accounting information." [LM 5/13]

But the cash register is per-document and aggregate. It does not break down which spans generated which deliveries, nor does it distinguish between content visible in the current version versus content only accessible through transclusion or historical backtrack.

**FINDDOCSCONTAINING** can locate transclusions:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This is the right operation — it finds all documents containing your content. But it requires the owner to specify *which content* to search for, via a vspec set. If the content has been deleted from the owner's current V-space, the owner must first recover the relevant addresses.

**Historical backtrack** provides recovery of deleted addresses:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

The owner can retrieve a previous version where the content was still in V-space, obtain the relevant V-space addresses, and then use FINDDOCSCONTAINING to locate all transclusions.

### The gap

The building blocks exist, but no single operation answers the question: "What economic obligations persist for content I own but have removed from my current arrangement?" The owner must:

1. Know (or suspect) that deleted content may still be transcluded
2. Use historical backtrack to recover old V-space addresses
3. Use FINDDOCSCONTAINING to search for transclusions
4. Correlate results with the cash register to understand economic impact

Nelson does not specify:
- An operation to enumerate all I-space content owned by an account
- An operation to list all active transclusions of an owner's content
- Whether the cash register provides per-span breakdowns
- A notification mechanism when owned content is transcluded

### What Nelson's principles require

The ownership guarantee is absolute:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

And the royalty guarantee is automatic:

> "This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

If the system automatically tracks what the owner is owed (it must, to pay royalties), and if ownership is structural (encoded in the I-address), then the system *possesses* the information needed to report on persisting economic obligations. The question is whether it is *obligated* to expose that information to the owner.

I believe it must, for two reasons:

**First**, the contractual foundation requires informed participation. Nelson describes the system as having "a contractual structure which makes it possible for people to use it confidently" [LM 4/4]. An owner who cannot discover what economic activity is tied to content they own cannot participate confidently in the system.

**Second**, the self-supporting services principle [LM 4/5] implies that content owners must be able to make informed decisions about storage costs versus royalty income. If Alice is paying ongoing storage rental for content that is generating substantial royalties through others' transclusions, she needs to know that — otherwise she might stop paying storage, thinking her content is unused.

### Conclusion

Nelson's architecture creates conditions where economic obligations demonstrably persist after V-space deletion. His principles of ownership, automatic compensation, and confident participation imply the system must expose this information to owners. The specified FEBE operations provide partial discovery (FINDDOCSCONTAINING + historical backtrack + cash register), but no single operation directly answers "what are my persisting economic obligations for content I've removed from my current arrangement?" This is a gap in the specification that an implementation must fill to satisfy Nelson's stated guarantees.

NEED_RAW: 5/11-5/13 (to verify whether the cash register specification includes any per-span breakdown or whether it is purely aggregate)

---

## Question 10 [nelson]

> If permanently stored content is later reintroduced into a new document, must the system guarantee that the economic terms match the original obligations, or may new terms be established?

### Nelson's Answer

# Economic Terms on Reintroduced Content

## Short Answer

The system does not permit new terms. Nelson's royalty model is **universal, fixed-rate, and follows the bytes** — not the document arrangement. When permanently stored content appears in any new document, the same per-byte royalty flows to the original owner at the standard rate set by Project Xanadu. There is no mechanism for renegotiation.

## Why the Question Dissolves

In Nelson's architecture, content is never "reintroduced" because it never leaves. I-space content is permanent and always present:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When someone creates a new document that includes existing content, the COPY operation creates a V-space reference to the **same I-space bytes**. The content is fetched from its home location each time it is delivered. There is no separate "copy" with separate terms — there is one set of bytes, permanently at one address, with one owner.

## The Fixed-Rate Mechanism

Nelson's royalty rate is not negotiable per document or per use. It is set centrally:

> "Royalty amount (Nib) will be fixed by Project Xanadu, and may be modified from time to time." [LM 5/20]

> "Royalty is fixed per byte delivered. The unit of royalty is the nib." [LM 5/13]

The ASCAP analogy makes this explicit:

> "When you put a quarter in the jukebox you are paying royalties to songwriter, singer, musicians and agents. This method (worked out by ASCAP, the American Society of Composers and Performers), permits an immense amount of commercial traffic by handling the matter of royalty automatically on a fixed-fee basis." [LM 5/13]

Individual songwriters do not negotiate per-play fees with each jukebox. The rate is standardized. The same applies in Xanadu: individual publishers do not set their own per-byte rates, and cannot establish different terms when their content appears in different contexts.

## What Happens in Compound Documents

When a compound document is read and it contains content from multiple owners, the royalty splits proportionally — but at the **same per-byte rate**:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

This means:
- Alice publishes 1000 bytes. Nib rate applies per byte.
- Bob creates a compound document: 500 bytes of Alice's content + 500 bytes of his own.
- When a reader accesses Bob's document, Alice gets Nib × 500 for her bytes, Bob gets Nib × 500 for his bytes.
- The rate is identical. The only variable is **proportion** — who wrote what.

## The Cash Register Follows the Document

Each published document has a cash register that counts deliveries:

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." [LM 5/13]

The cash register is at the **original document**, not at each place the content appears. When Alice's bytes are delivered through Bob's compound document, Alice's cash register increments. The same counter, the same rate, regardless of the delivery context.

## What "Modified from Time to Time" Means

The Nib rate can change — but it changes **universally**, not per document:

> "Royalty amount (Nib) will be fixed by Project Xanadu, and may be modified from time to time." [LM 5/20]

If the Nib changes from $0.000001 to $0.000002 per byte, this applies to **all** content deliveries across the entire docuverse. There is no mechanism for content published in 1990 to carry different rates than content published in 2020. The rate is a network-wide parameter, not a per-document attribute.

## Why This Design Is Necessary

Nelson's model **requires** uniform rates to achieve its core goal: quotation without permission friction.

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

If authors could set their own rates, this guarantee would collapse. An author could set a prohibitively high rate as a de facto refusal of quotation. The system would degenerate back into permission-based copyright, which is precisely what Nelson designed Xanadu to bypass.

The Internal Copyright Convention works because it offers a **non-negotiable tradeoff**: you give up control over how your work is used, but you never give up compensation. Both sides of this bargain require fixed, universal terms.

## Summary

| Question | Answer |
|----------|--------|
| Can the original owner set new terms? | No — rates are set by Project Xanadu, not publishers |
| Can the new document author set terms? | No — same Nib rate applies universally |
| Does delivery context affect the rate? | No — same rate regardless of which document delivers the bytes |
| Can rates change over time? | Yes — but universally, not per-document |
| Who gets paid? | The original I-space owner, always, at the standard Nib |

The economic terms are a property of the **network**, not of the content or the document. Content carries its owner's identity (structural, via I-address) but not its own price (universal, via Nib). This is what makes frictionless quotation possible.
