# Consultation Answers — Permanence and Economic Obligations

**Inquiry:** What must the system guarantee about its permanence invariants when economic obligations are not met — are address permanence, content immutability, and publication irrevocability unconditional or conditioned on continued payment?
**Date:** 2026-02-24 18:28
**Questions:** 10 (10 nelson, 0 gregory)

---

## Question 1 [nelson]

> Must an address assigned to content remain permanently valid even if the content's owner ceases all payment to the system?

### Nelson's Answer

# Address Permanence vs. Payment Lapse

This question exposes a genuine tension in Literary Machines between two explicitly stated principles that Nelson never fully reconciles.

## What IS Specified: Addresses Are Permanent

The tumbler addressing system guarantees that addresses, once assigned, are never invalidated or reassigned:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This is a property of the **addressing system itself**, not of storage infrastructure. Tumblers grow by forking — new addresses are created by subdivision, never by reusing old ones. An address that once referred to your content will always refer to your content, structurally. It cannot be given to someone else.

The ghost elements concept reinforces this — even positions with *nothing stored* remain valid addresses:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

An address without stored content is a ghost element. It is still *valid* — links can point to it, searches can reference it. It simply has nothing to return.

## What IS Specified: Storage Must Be Self-Supporting

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage requires ongoing rental payment from the content owner. There is no endowment, no charitable fund dedicated to keeping unpaid content alive. The economics are explicit — the owner pays to keep content accessible, readers pay per-byte-delivered, and royalties offset the owner's costs for popular content.

## What Is NOT Specified: The Intersection

Nelson does **not** specify what happens when an owner stops paying storage rental. The storage-funding design intent document in the knowledge base explicitly identifies this gap:

- What happens to content when storage rental lapses?
- Whether there is a grace period before content becomes inaccessible
- Whether unclaimed royalties or the Author's Fund can preserve orphaned content
- How the permanence guarantee interacts with payment cessation over centuries

## The Distinction: Address Validity vs. Content Accessibility

The answer to your question requires separating two things Nelson treats differently:

**Address validity** — yes, permanent, unconditionally. The tumbler `1.3.27.4` will always mean "that content." It will never be reassigned. It will never become syntactically invalid. This is a mathematical property of the addressing scheme.

**Content accessibility** — not guaranteed without payment. The self-supporting principle means someone must pay for storage. If no one does, the content may become a ghost element — a valid address with nothing behind it.

## Mechanisms That Resist Content Loss

Nelson does provide several structural protections against content disappearing, even if the original owner stops paying:

1. **Published content has social obligation:**
   > "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

2. **Vendor contracts require orderly transition:**
   > "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

3. **Distributed redundancy:** Content is replicated across vendors for backup and performance. The BEBE protocol distributes copies based on demand: "Material is moved between servers for... redundancy and backup purposes." [LM 4/71]

4. **The Author's Fund** provides partial safety net for public domain content, including "subsidies to struggling writers and artists, and other worthy purposes." [LM 5/12] — though this is not explicitly directed at preserving lapsed-payment content.

5. **Others' links create obligations:** Because other users may have linked to published content, and those links are *their* property at *their* addresses, withdrawing content would damage others' property. This is the deepest structural argument against content disappearing.

## My Intent

I designed a system where addresses are permanent and literature is preserved. The self-supporting requirement was a practical necessity — someone must pay for the disk. But the deeper principle is that published content enters the permanent record of human civilization:

> "This attrition of the heritage can in principle be stopped... Only digital archives give us long-term hope for preserving our heritage." [LM 3/25]

The honest answer is that I specified two principles that exist in tension, and I did not fully resolve the tension. The address remains valid — always. Whether the content behind it remains accessible when no one pays is a question I left to implementation. But the spirit of the system is clear: published content should survive. The mechanisms of distributed storage, vendor obligations, backup replication, and the moral weight of others' links all push toward preservation. The self-supporting principle constrains *how* preservation is funded, not *whether* it should occur.

The address is permanent. The content should be permanent. The economics must sustain both. I specified the first two clearly and left the third incompletely resolved.

---

## Question 2 [nelson]

> Can stored content ever be deleted or modified by the system as a consequence of unpaid economic obligations, or is immutability unconditional once content is accepted?

### Nelson's Answer

# Can Unpaid Obligations Cause Content Removal?

This question strikes at a genuine, unresolved tension in Literary Machines between two explicitly stated principles that Nelson never reconciles.

## The Two Principles in Conflict

### Principle 1: Permanence Is Fundamental

Nelson's language about content permanence is strong and repeated:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "This attrition of the heritage can in principle be stopped... Only digital archives give us long-term hope for preserving our heritage." [LM 3/25]

The I-space model is append-only by design:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Even "deletion" does not destroy content — it removes V-space mappings while I-space bytes persist:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

### Principle 2: All Services Must Be Self-Supporting

Nelson is equally explicit that storage requires ongoing payment:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage is modeled as rental, not purchase:

> "Except now there is no 'printing and warehousing,' but a certain required minimum disk rental. Thus a 'publisher' is someone who pays for the rapid accessibility of materials and benefits from their use along with the author." [LM 2/61]

The projected cost structure includes ongoing annual fees per megabyte per server [LM 5/11]. This is not a one-time cost but a continuing obligation.

## What Nelson Does NOT Specify

The specification contains a gap precisely where these two principles collide. Nelson never addresses:

- What happens to content when storage rental lapses
- Whether there is a grace period before content becomes inaccessible
- Whether the Author's Fund can preserve orphaned content
- Whether permanence is conditional on payment or unconditional once content is accepted
- How the economics work over centuries as content accumulates but readership may not

## What CAN Be Inferred

### Published vs. Private Content

The permanence language is strongest for **published** content. Publication creates a social contract — others will have linked to it, and their links (which are their property, at their addresses) depend on continued accessibility:

> "Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it." [LM 2/43]

Private content has weaker permanence claims. Nelson even describes "privashing" — making content universally accessible but retaining the right to withdraw it — which implies private documents can be withdrawn by the owner. Non-payment by an owner might be analogous to voluntary withdrawal.

### Vendor Failure Is Addressed; User Non-Payment Is Not

The vendor contract explicitly requires orderly transition on cancellation:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

This handles the case where a vendor fails — content migrates. But it does not address the case where a **user** stops paying their vendor. The vendor's obligation is to the franchise and to other vendors' customers, not necessarily to a non-paying user's content.

### Address Permanence vs. Content Accessibility

A critical distinction may resolve the tension partially. Nelson guarantees that **addresses are permanent** — a tumbler, once assigned, is never reassigned to different content. But this is not identical to guaranteeing that content at that address is always **served**. An address could remain valid (reserved, never reused) while the content behind it becomes inaccessible due to non-payment.

This would be analogous to a library catalog number that permanently identifies a book, even if the book is in deep storage rather than on the shelf.

### The Royalty Feedback Loop

For published content, there is a potential self-sustaining mechanism: popular content generates royalties that could offset storage costs. But this only works for content that is actually read. Rarely-accessed published content would need its owner to continue paying storage rental — and Nelson acknowledges no backstop if they stop.

## My Assessment of Nelson's Intent

Reading the full architecture, I believe Nelson **intended** immutability to be unconditional for published content — that the system's design should make it economically viable to preserve everything, not that preservation is contingent on payment. The self-sustainability requirement is about designing the economic model so that it CAN sustain perpetual storage, not about creating a kill switch for unpaid content.

Several factors support this reading:

1. The archiving vision explicitly imagines content surviving "wars, natural disasters, political upheaval" — survival that would be meaningless if content could be lost to a billing dispute.

2. The franchise model distributes content across multiple vendors with backup copies, making single-point economic failure recoverable.

3. The strongest permanence language applies to published content, which is also the content most likely to generate self-sustaining royalties.

4. Nelson frames the system as "the printing press of the future" — and books don't disappear from libraries when publishers go bankrupt.

However, this is my interpretation of intent, not a specification Nelson wrote. **He never explicitly states that immutability is unconditional, nor does he state that it is conditional on payment.** The gap is real.

## The Honest Answer

**Nelson's specification does not resolve this question.** Immutability of I-space content is presented as architecturally fundamental (append-only, never overwritten). Self-sustainability of storage is presented as economically essential. What happens at their intersection — when someone stops paying for content that the architecture says should be permanent — is left unspecified.

For a modern implementation, this is a design decision that must be made explicitly, consistent with Nelson's principles. The most faithful interpretation, in my view, is that published content's permanence should be unconditional (the economic model must be designed to sustain it), while private content's permanence may be conditional on the owner's continued participation.

NEED_RAW: [5/6-5/12] — The user contract terms in early Chapter 5 may contain specific clauses about storage obligations, payment default, and content disposition that the curated sources do not fully extract.

---

## Question 3 [nelson]

> Once a document is published, can the system revoke its published status due to the author's failure to meet ongoing financial obligations?

### Nelson's Answer

# Can Published Status Be Revoked for Non-Payment?

Nelson never answers this question directly. What he creates instead is an **unresolved tension** between two explicitly stated principles that point in opposite directions.

## Principle 1: Published Content Must Stay Published

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is structural, not sentimental. Other users will have created links to the published document — links that *they* own, at *their* addresses:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it" [LM 2/43]

Withdrawing a published document would break other people's property. Their links, their transclusions, their compound documents — all depend on the continued existence of the target.

## Principle 2: All Services Must Be Self-Supporting

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage requires ongoing payment by the owner. Nelson envisions a publisher as "someone who pays for the rapid accessibility of materials" [LM 2/61]. The projected costs include ongoing annual maintenance per server per megabyte [LM 5/11]. There is no endowment, no charitable fund for keeping published content alive when the owner stops paying.

## The Collision

If Alice publishes a document, Bob and Carol link to it and build compound documents that transclude it, and then Alice stops paying her storage rental — what happens?

Nelson's principles give contradictory guidance:

- **Permanence says:** The document must remain accessible. Bob's and Carol's links depend on it. Withdrawal requires "lengthy due process."
- **Self-sustainability says:** No one is subsidizing Alice's storage. If she won't pay, the money must come from somewhere, and cross-subsidy "could only work temporarily."

## What Nelson Does NOT Specify

The curated analysis of storage funding identifies this gap explicitly. Nelson does not address:

- What happens to content when storage rental lapses
- Whether there is a grace period before content becomes inaccessible
- Whether the Author's Fund can preserve orphaned content
- How the permanence guarantee interacts with payment failure
- Whether the system can or should distinguish between voluntary withdrawal (forbidden without due process) and financial abandonment

## What Can Be Inferred

The Author's Fund exists but is narrowly scoped:

> "When bytes are taken from an unpublished document (one in the public domain), this surcharge is added to the Author's Fund, an escrow account whose purpose is the charitable funding of worthy causes within the network." [LM 5/12]

This fund handles public domain content, not orphaned published documents. Nelson does not specify it as a safety net for this scenario.

The vendor failure case IS addressed — vendors must arrange "orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16] — but author payment failure is a different problem. The vendor is contractually bound; the author who simply stops paying has no analogous obligation beyond the publication contract itself.

## My Intent

I designed the publication contract as a **solemn commitment** — signing "something very like a credit-card triplicate slip." Publication is not casual. The analogy to paper publishing is deliberate: when you print a book, copies exist in libraries and cannot be recalled. The economic burden of keeping books in libraries falls on the libraries, not the author.

The honest answer is that I did not fully resolve the economics of perpetual availability. The principle is clear — published content stays published — but the funding mechanism for enforcing that principle when the owner defaults was left to implementation. The system was designed with the assumption that royalties flowing back to popular content would offset storage costs for most publishers, and that the publication commitment itself (a contractual act, not a button press) would deter those not prepared to maintain their obligations.

But to answer the question directly: **the system should not revoke published status.** The permanence guarantee exists to protect the links and transclusions of *other users*, not to reward the publisher. If someone must bear the cost of maintaining orphaned content, that is an infrastructure problem to be solved at the franchise level — not by breaking the promises the system made to everyone who built upon that content.

NEED_RAW: [5/6-5/10, 5/19-5/21] — These pages may contain additional contract terms about publication obligations, payment default procedures, or withdrawal mechanics that the curated sources do not fully cover.

---

## Question 4 [nelson]

> If content becomes inaccessible due to non-payment, must the system distinguish between content that still exists but is withheld and content that has been destroyed?

### Nelson's Answer

# Must the System Distinguish Withheld from Destroyed?

**Yes, the architecture demands this distinction**, though Nelson never directly addresses the non-payment scenario. The answer emerges from the collision of several structural principles.

## The Tension

Two guarantees are in conflict:

**Permanence:** "Any address of any document in an ever-growing network may be specified by a permanent tumbler address" [LM 4/19]. Content in I-space is append-only and permanent.

**Self-sustainability:** "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining" [LM 4/5].

Nelson specifies that storage requires ongoing rental fees. He does NOT specify what happens when payment lapses. The storage-funding design intent file confirms this gap: Nelson does not address "What happens to content when storage rental lapses," "Whether there is a grace period," or "Minimum storage period requirements."

## Why the Distinction Is Architecturally Required

### 1. Other users' links depend on the content

Published content cannot be withdrawn precisely because others have linked to it:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

If Alice links to Bob's published document and Bob stops paying storage rental, treating that content as *destroyed* would violate Alice's link guarantee. Her links — which are her property, at her address — would be broken not by any action of hers or Bob's, but by an administrative lapse. The system must know that the content *exists* so that it can potentially be restored, migrated, or served from a backup.

### 2. I-space is permanent by definition

The I-space model is append-only. Content at an I-address never changes and, by the architecture's own logic, never vanishes:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Destroying content would invalidate the I-space guarantee. Withholding it preserves the guarantee while acknowledging an operational constraint. These are fundamentally different states.

### 3. The system already has a "not currently addressable" state

Nelson explicitly describes content that exists but cannot be accessed through normal means:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This is content that *exists in I-space* but is removed from the current V-space view. Non-payment inaccessibility would be an analogous state: the bytes exist, the I-address is valid, but delivery is suspended for an administrative reason. The architecture already distinguishes "present but not currently served" from "absent."

### 4. The network already handles unavailability as normal

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

The BEBE protocol handles this through forwarding, backup copies, and subrepresentation. "Not currently available" is a routine system state, distinct from "does not exist." A payment lapse that makes content temporarily unreachable is operationally identical to a server being down — the content exists somewhere, it just can't be delivered right now.

### 5. Ghost elements establish the inverse distinction

Ghost elements are addresses where nothing is stored:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

The docuverse already distinguishes between "address exists but nothing stored" (ghost) and "address exists and content is stored." If content were destroyed due to non-payment, it would revert to a ghost element — but one that *previously had content*, that other documents transclude, and that other users' links reference. This is a categorically different situation from an address that was always empty.

### 6. The vendor contract mandates transition, not destruction

The Storage Vendor contract requires:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

Content migrates; it does not vanish. Even when the business relationship ends, the contractual structure preserves the content's existence. This implies the system is designed so that content outlasts any particular payment relationship.

## What Nelson Does NOT Tell Us

Nelson leaves several critical questions unresolved:

- **Who pays to maintain withheld content?** If the owner stops paying, the storage cost doesn't vanish. Someone bears it — the vendor, the Author's Fund, the network collectively. Nelson's "self-supporting" principle says this can't be subsidized indefinitely, but he provides no mechanism.

- **How long before withholding becomes destruction?** There may be a practical point where maintaining inaccessible content becomes economically unsustainable. Nelson doesn't address this.

- **Can the Author's Fund preserve orphaned content?** The Author's Fund is described as supporting "the charitable funding of worthy causes within the network" including "subsidies to struggling writers and artists" [LM 5/12]. Whether it could absorb storage costs for content whose owner has disappeared is unspecified.

- **Does the archival vision ("deep rock and deep space") override the economic model?** Nelson's most ambitious statements about permanence — "a digital system of the kind described in this book can provide security for the human heritage of literature, art and science" [LM 3/25] — suggest content should survive *any* administrative disruption. But the economic model provides no funding mechanism for this.

## My Intent

The system **must** distinguish between content that exists but is withheld and content that has been destroyed. These are different states with different implications for links, transclusions, version history, and the permanence guarantee.

Treating non-payment as destruction would cascade through the docuverse: breaking other users' links, invalidating transclusions, corrupting version histories, and violating the fundamental promise that "a thing once published stay published." The correct behavior is to mark the content as inaccessible — analogous to the "not currently addressable" state of deleted bytes — while preserving the I-space content for potential restoration.

How long that state can persist before economic reality forces a harder decision is something I left to the implementors. But the architecture is clear: the distinction must exist, because other users' rights depend on it.

---

## Question 5 [nelson]

> What must the system guarantee about links that reference content whose owner has stopped paying — must those links remain valid and resolvable?

### Nelson's Answer

# Links to Content Whose Owner Stops Paying

This question exposes a genuine tension in the specification. Nelson establishes two principles that pull in opposite directions, and he does not resolve the conflict explicitly.

## The Two Competing Principles

**Principle 1: Published content must persist.**

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

Publication creates a social contract. Others will link to your work, and those links — which are *their* property, at *their* addresses — depend on your content remaining accessible.

**Principle 2: All services must be self-supporting.**

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Someone must always pay for storage. Nelson explicitly frames storage as ongoing rental, not a one-time deposit.

## What the Link Guarantees DO Cover

Three things remain true regardless of payment status:

**1. The link itself survives.** Links live at the *creator's* address, not the target's. If Alice links to Bob's content and Bob stops paying, Alice's link still exists at Alice's address, under Alice's control. The link is Alice's property.

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

**2. The tumbler address remains valid.** Addresses are permanent by design — they are never reassigned or recycled.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

**3. The I-space content is never destroyed.** DELETE in Xanadu removes content from V-space arrangement only. Nothing is ever erased from I-space.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## What Nelson Does NOT Resolve

The curated source on storage funding states this explicitly:

> Nelson does NOT specify:
> - What happens to content when storage rental lapses
> - Whether there is a grace period before content becomes inaccessible
> - Whether the Author's Fund can be used to preserve orphaned content

The question of **resolvability** — whether following a link actually returns content — depends on whether the target content is *accessible*, and that requires someone to pay.

## The Strongest Argument: Links Create Permanence Obligations

Nelson's most relevant argument comes from his discussion of why published documents cannot be withdrawn:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

The logic is clear: **links justify permanence**. Others' links to your published work are their property, and your work's continued accessibility is what makes their links meaningful. Simply ceasing to pay should not override this social obligation — that would be equivalent to unilateral withdrawal, which Nelson prohibits.

## Available Safety Nets

Nelson provides several mechanisms that could absorb orphaned content, though he doesn't explicitly connect them to this scenario:

**The Author's Fund:**
> "When bytes are taken from an unpublished document (one in the public domain), this surcharge is added to the Author's Fund, an escrow account whose purpose is the charitable funding of worthy causes within the network." [LM 5/12]

**Vendor transition obligations:**
> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

**Distributed redundancy:**
> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

Content is replicated across vendors. Backup copies exist elsewhere. The network routes around failures.

## My Assessment

As the designer, my intent is unambiguous on the principle even if I left the mechanism underspecified:

**Published content that has been linked to MUST remain accessible.** The entire architecture rests on the guarantee that links work, that addresses resolve, and that published literature persists. If an owner's failure to pay could silently break thousands of other users' links, the system's fundamental promise — permanent, interconnected literature — collapses.

The economic mechanism for handling lapsed payments is an implementation problem. The principle is not. Possible resolutions include:

- Royalties accumulating against the content could offset storage costs (popular content pays for itself)
- The Author's Fund could absorb orphaned published content
- Storage costs decrease over time with technology; archival tiers become cheap
- The franchise system could treat orphaned published content as a shared network obligation

What I would **not** accept is a design where cessation of payment silently makes content dark and breaks every link pointing to it. That would violate:

> "It is in the common interest that a thing once published stay published, as in the world of paper." [LM 2/43]

For **private** (unpublished) content, the calculus is different. Only the owner and designees can access it. No one else has linked to it (or if they have, only with the owner's permission). If the owner stops paying, there is no third-party obligation being violated. The content may reasonably become inaccessible — though the I-space bytes and the tumbler address should still be preserved for potential future recovery.

## Summary

| Aspect | Published Content | Private Content |
|--------|------------------|-----------------|
| Link remains valid? | **Yes** — link is creator's property | **Yes** — same |
| Address remains valid? | **Yes** — tumblers are permanent | **Yes** — same |
| Content accessible? | **Must be** — social obligation via links | **Not guaranteed** — no third-party reliance |
| Who pays? | **Unspecified** — genuine gap | Owner, or no one |
| I-space content preserved? | **Yes** — non-destruction guarantee | **Yes** — same |

The specification guarantees the *principle* (links to published content must remain resolvable) but leaves the *funding mechanism* for orphaned content to implementation. This is a gap I acknowledge, but the principle is clear: the system exists to preserve interconnected literature, and allowing payment lapses to silently sever the web of links would defeat its entire purpose.

---

## Question 6 [nelson]

> If one author's content is shared into another author's document through transclusion, does non-payment by the original author affect the integrity of the second author's document?

### Nelson's Answer

# Transclusion Dependency and Non-Payment

This question exposes a genuine tension in Nelson's design between two principles that pull in opposite directions: **permanence of published content** and **self-sustaining economics**.

## The Architectural Dependency Is Real

Transclusion creates a structural dependency. Author B's document does not contain a copy of Author A's content—it contains references to Author A's I-space addresses that must be resolved at retrieval time:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When a reader opens Author B's document, the system fetches Author A's content from its home location. If that home location becomes inaccessible, Author B's document is structurally incomplete—it has gaps where the transcluded content should appear.

So yes: **non-payment by Author A could, in principle, affect Author B's document.** The transclusion model means Author B's document is only as complete as the availability of everything it references.

## Nelson's Mitigating Mechanisms

Nelson was aware that distributed systems fail, and designed several layers of protection:

### 1. Publication Is a Permanent Commitment

Publication creates a contractual obligation against withdrawal:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Non-payment is not a permitted withdrawal mechanism. It is a breach of the publication contract.

### 2. BEBE Replication and Backup

The inter-server protocol distributes content across multiple locations:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

Popular transcluded content would be cached at multiple servers. The system is designed to route around failures:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

### 3. Vendor Preservation Obligations

Storage Vendors are contractually bound to preserve content and handle transitions:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material." [LM 5/14-5/15]

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

The vendor cannot simply delete content when an author stops paying. The content is part of the published record; the vendor's obligation to the network persists.

## The Unresolved Tension

Despite these protections, Nelson does not fully resolve the funding question. The storage-funding design intent notes explicitly:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

And from my analysis of the storage-funding model, Nelson does **not** specify:

- What happens to content when storage rental lapses
- Whether there is a grace period before content becomes inaccessible
- Whether the Author's Fund can be used to preserve orphaned content
- How the permanence guarantee survives an owner who disappears

The curated storage-funding analysis states this directly: "Permanence of the address (once assigned, never reused) is distinct from permanence of accessibility (requires ongoing payment)."

## What I Intended

Here is my honest assessment as the designer:

**The publication contract is the answer.** When Author A publishes, they enter into a binding agreement. That agreement says published content stays published. Non-payment is a contractual failure, not a design pathway for withdrawal. The system's response should be:

1. The **Storage Vendor** absorbs the cost temporarily (they signed a preservation contract)
2. The **BEBE replication** ensures copies exist at other nodes
3. The content migrates to another vendor or enters some form of trusteeship
4. The **Author's Fund** could potentially cover orphaned content preservation

The deeper principle is this: **the docuverse is a public commitment, not a rental agreement.** When you publish, you are not renting shelf space that disappears when you stop paying. You are placing your work into the permanent record of human expression. The economic mechanisms must serve this permanence, not undermine it.

I acknowledge that I did not fully work out the economics of orphaned content. The tension between "all services must be self-supporting" and "published content must persist" is real, and I left it unresolved. But the *intent* is clear: **Author B's document should never break because Author A failed to pay a bill.** The system's contractual, replication, and vendor-obligation mechanisms exist precisely to prevent this scenario.

The fact that I did not specify every detail of the orphan-content economic model does not change the design guarantee. It means the implementation must solve a problem I identified but did not fully resolve.

NEED_RAW: [5/14-5/16, 5/19-5/21] — to verify whether the publication contract includes any explicit provision about content becoming dark due to non-payment, or whether the vendor-to-publisher contract addresses this scenario directly.

---

## Question 7 [nelson]

> Must the identity association between a creator and their content survive the creator's failure to meet economic obligations?

### Nelson's Answer

# Must Identity Association Survive Economic Failure?

**Yes — structurally and unconditionally.** The identity association between creator and content is encoded in the address itself, not in any contractual or economic layer. It cannot lapse, be revoked, or be severed by non-payment.

But **content accessibility** is a separate question, and there Nelson leaves a gap.

---

## The Structural Argument

The I-space address encodes identity as part of its permanent form:

```
Node.0.User.0.Document.0.Element
```

The **User field** IS the creator's identity. It is not metadata attached to content — it is the address by which content is fetched.

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This identity is permanent by the fundamental guarantee of tumbler addressing:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The address does not expire. It does not depend on payment. It does not depend on the creator being alive, solvent, or in good standing. The identity association is a mathematical fact of the addressing scheme, not a contractual privilege.

---

## Identity Survives Even in Ghost State

Nelson explicitly designs for entities that exist in address space but have no content stored:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

If a creator's content becomes inaccessible — for whatever reason, including economic failure — the **addresses still exist**. The User field still identifies the creator. Links to that content still carry the creator's identity in their endsets. Ghost elements are "virtually present" — the identity association persists even when nothing is stored.

---

## Identity Survives Through Transclusion

When others transclude a creator's content, the I-address travels with it:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Every transclusion carries the original creator's I-address. If Alice's content is transcluded into Bob's document, Carol's document, and a thousand others — every one of those transclusions encodes Alice's User address. Even if Alice's original content goes dark, the identity association survives in every document that references it.

---

## But Accessibility Is Economically Contingent

Nelson is explicit that storage requires ongoing payment:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage is rental, not purchase:

> "Except now there is no 'printing and warehousing,' but a certain required minimum disk rental. Thus a 'publisher' is someone who pays for the rapid accessibility of materials and benefits from their use along with the author." [LM 2/61]

Nelson **does not specify** what happens when rental lapses. The `storage-funding` design intent document lists this explicitly among unresolved questions:

- What happens to content when storage rental lapses
- Whether there is a grace period before content becomes inaccessible
- Whether the Author's Fund can be used to preserve orphaned content
- How inflation affects these economics over centuries

---

## The Append-Only Constraint

There is a deep tension here. The permascroll is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

And deleted content enters a recoverable state, not destruction:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

If content is never truly destroyed in I-space, and the address is permanent, then the identity association is doubly permanent — both the address and the content it points to survive. The question is only whether the content remains **deliverable**.

---

## The Vendor Transition Obligation

Nelson does address one failure scenario — vendor shutdown:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

This suggests content should migrate, not vanish. But this is the vendor's obligation, not the creator's. If the **creator** fails to pay (rather than the vendor shutting down), Nelson is silent.

---

## Summary

| Question | Answer |
|----------|--------|
| Does the I-address encode the creator? | **Yes** — permanently, structurally |
| Can economic failure sever this encoding? | **No** — the address is mathematical, not contractual |
| Does the creator's identity survive in transclusions? | **Yes** — every reference carries the I-address |
| Does the creator's identity survive as a ghost element? | **Yes** — ghost elements are "virtually present" |
| Can the content become inaccessible? | **Possibly** — Nelson doesn't specify what happens on non-payment |
| Is the content destroyed on non-payment? | **Unclear** — append-only storage says no; "self-supporting" says maybe |

The identity association is an invariant of the addressing system. It survives anything — including the creator's death, bankruptcy, or abandonment. What Nelson leaves unresolved is whether the **content at that address** remains deliverable when no one pays for its storage.

The distinction matters: you will always be able to say "this content was created by User X" (identity survives). You may not always be able to say "here is the content" (accessibility may lapse). Nelson designed an architecture where attribution is as permanent as mathematics. He left the economics of perpetual accessibility as an open problem.

NEED_RAW: [4/5, 5/11-5/13, 5/16-5/18] — to verify whether there is any language about content disposition specifically on creator non-payment, as opposed to vendor shutdown.

---

## Question 8 [nelson]

> Must the version history of a document remain intact and retrievable even when the document's owner has abandoned all financial commitment to the system?

### Nelson's Answer

# Version History and Abandoned Financial Commitment

This question exposes a genuine and unresolved tension in Literary Machines between two principles Nelson states with equal force.

## The Permanence Principle

Nelson repeatedly and emphatically promises that version history is permanent and always retrievable:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The storage model is explicitly append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Even "deleted" content remains in I-space, awaiting historical backtrack:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And permanence of addressing is a foundational guarantee:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

For published documents specifically, the obligation is even stronger:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

## The Self-Sustainability Principle

With equal force, Nelson insists that storage must pay for itself:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage requires ongoing rental paid by the owner. Nelson envisions publication as analogous to paying for warehouse space:

> "Except now there is no 'printing and warehousing,' but a certain required minimum disk rental. Thus a 'publisher' is someone who pays for the rapid accessibility of materials and benefits from their use along with the author." [LM 2/61]

## The Unresolved Gap

Nelson does **not** specify what happens when these two principles collide. The storage-funding analysis in the curated sources identifies this explicitly:

> "Nelson does NOT specify: What happens to content when storage rental lapses; Whether there is a grace period before content becomes inaccessible; Minimum storage period requirements; Whether the Author's Fund can be used to preserve orphaned content."

This is not a minor oversight. Version history depends on I-space content being retrievable — the "ongoing braid" can only be reconstructed if the bytes that compose each version remain accessible. If the owner abandons financial commitment and no one pays for storage, the I-space content becomes unreachable, and with it every version of the document.

## What Can Be Inferred

Several factors complicate a simple "yes" or "no":

**For published documents**, others will have linked to them. Those links are owned by other users and depend on the content's continued existence. Nelson says withdrawal requires "lengthy due process" precisely because of this dependency. An owner abandoning payment is not the same as an owner requesting withdrawal — the obligation to others persists regardless of the owner's intent.

**The Author's Fund** provides a partial mechanism. Surcharges on public domain byte delivery accumulate into an escrow account for "charitable funding of worthy causes within the network" including "subsidies to struggling writers and artists, and other worthy purposes" [LM 5/12]. Whether this extends to preserving orphaned content is unspecified.

**Byte delivery revenue** from readers partially offsets storage costs for popular published content. If enough people read the work, delivery charges could sustain its storage even without the owner's contribution.

**For private, unpublished documents**, the case is weaker. No one else has linked to them (or shouldn't have). No delivery revenue offsets costs. The self-sustainability principle applies most cleanly here.

## My Answer

Nelson's design intent is that version history should be permanent — this is not a nice-to-have feature but the fundamental nature of what a document IS in Xanadu. The "ongoing braid" model, the append-only storage, the "DELETED BYTES... awaiting historical backtrack functions" — all of these treat version history as structurally inseparable from the document itself.

But I did not resolve the economics of perpetual storage for abandoned content. I stated that archival storage must be "economically self-sustaining" and that the system should preserve the human heritage, and I left the reconciliation to implementation.

The honest answer: **for published documents, the design intent is yes** — version history should survive owner abandonment, because others depend on it, and the archiving principle demands it. But **I did not specify who pays**, and my insistence that all services be self-supporting means someone must. This is a gap in the specification, not a resolved design decision.

For private, unpublished documents with no external links, the case for preservation is weaker under my own principles. No one else depends on the content. The self-sustainability principle would suggest such content may eventually become inaccessible.

The deeper issue is that I conceived of permanence as a moral imperative and self-sustainability as an economic necessity, and I treated both as non-negotiable without fully working out what happens when they conflict. An implementation must choose — and the choice will define what kind of system Xanadu actually becomes.

NEED_RAW: [4/5, 5/11-5/13] — to verify whether Nelson says anything more specific about storage lapse scenarios or minimum retention periods in the economic sections.

---

## Question 9 [nelson]

> Does the system owe any permanence obligation to third parties — readers, linkers, transcluders — that is independent of the original author's payment status?

### Nelson's Answer

# Third-Party Permanence Obligations in Xanadu

## Yes — Nelson Explicitly Creates Third-Party Obligations

The system owes a permanence obligation to third parties that exists *because of* their reliance on the content, not because of the author's payment status. Nelson states this clearly and repeatedly.

### The Core Obligation

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process."
> — [LM 2/43]

The logic is explicit: the obligation to remain published derives from **others' dependence**, not from the author's wishes or payment. The author "may not withdraw" — this is a constraint *on* the author, *for* third parties.

### Links as the Mechanism of Obligation

Nelson specifies the precise mechanism by which third-party obligations arise — linking:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version."
> — [LM 2/43]

The word "vital" is important. The former version "must remain" not because the author wants it to, but because other users' links depend on it. Those links are the *property* of their creators:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to."
> — [LM 4/12]

If Alice links to Bob's published document, that link is Alice's property at Alice's address. Bob's withdrawal would destroy Alice's property — her link would point to nothing. The publication contract requires Bob to accept this:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract."
> — [LM 2/43]

### Transclusion Deepens the Obligation

The obligation extends beyond linking to transclusion. When someone builds a compound document that windows Bob's content:

> "Document A can include Document B, even though Document B is owned by someone else."
> — [LM 2/35]

> "Each compound document is like the other documents: it has an owner and receives royalties."
> — [LM 2/33]

If Bob's content disappears, compound documents built by third parties are damaged — they would contain broken windows. The compound document owner has a legitimate expectation that the windowed content remains available, since the publication contract guarantees it.

### The Contractual Foundation

Nelson frames this as a contractual, not merely moral, obligation:

> "Because the conceptual structure expects participants to behave in certain ways, these are embraced in the contract offered to users. These provisions are necessary for the orderly and confident use of published material by many people."
> — [LM 4/4]

Publication involves signing a contract "very like a credit-card triplicate slip" that includes the provision: "I agree that anyone may link and window to my document." This is a binding commitment to third parties — not a policy preference but a legal agreement.

---

## The Unresolved Tension: Who Pays When the Author Can't?

While the *obligation* to third parties is clear, the *funding mechanism* is not fully resolved. Nelson creates a direct contradiction:

**Principle 1 — Permanence obligation:**
Published content "must remain on the network" because third parties depend on it.

**Principle 2 — Self-supporting storage:**
> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining."
> — [LM 4/5]

If the author dies, goes bankrupt, or simply stops paying storage rental, the third-party obligation says the content must remain. But the self-supporting principle says no one subsidizes storage. Nelson does not specify what happens in this case.

### What Nelson Does Specify

1. **Withdrawal requires lengthy process and fee:**
   The publishing contract allows withdrawal only "with one year's notice and fee" [LM 5/20]. This is deliberate withdrawal, not payment lapse.

2. **Vendor failure has an orderly transition:**
   > "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations."
   > — [LM 5/16]

   This handles vendor failure but not author payment failure.

3. **The Author's Fund exists but is not scoped for this:**
   > "When bytes are taken from an unpublished document (one in the public domain), this surcharge is added to the Author's Fund, an escrow account whose purpose is the charitable funding of worthy causes within the network."
   > — [LM 5/12]

   The Author's Fund is explicitly for public domain and charitable purposes, not for maintaining orphaned published content. Though "other worthy purposes" could arguably stretch to cover it.

4. **Ongoing royalties may offset storage costs:**
   If the content is still being read, per-byte royalties accrue. These could potentially cover storage rental. But for rarely-read content, royalties may not cover costs.

### What Nelson Does NOT Specify

As noted in the curated storage-funding source:

- What happens to content when storage rental lapses
- Whether there is a grace period before content becomes inaccessible
- Minimum storage period requirements
- Whether the Author's Fund can preserve orphaned content
- How inflation affects these economics over centuries

---

## My Design Intent

The third-party obligation is **philosophically primary**. The self-supporting storage principle is an **economic constraint**. When I wrote that published content "must remain on the network," I meant it. I also meant that the system cannot run on charity.

The resolution I envisioned — though I did not fully specify the mechanics — rests on several factors:

1. **The act of publication creates a durable obligation.** This is why I made publication a "solemn event" with a signed contract. You are not casually posting; you are entering a permanent commitment.

2. **Storage costs decrease over time.** I designed the system anticipating that digital storage would become cheaper — radically so. The long-term cost of maintaining a published document approaches zero even if the author's payments stop.

3. **Popular content sustains itself through royalties.** The per-byte delivery charge means actively-read content generates revenue.

4. **The franchise absorbs orphaned content.** The Storage Vendor's contractual obligation to honor requests from any Xanadu server, combined with the orderly transition requirement, means published content has institutional custody beyond any individual author. The vendor cannot simply delete published content when an author lapses — other vendors' users have links into it.

5. **The archival vision is civilizational, not commercial:**
   > "Only digital archives give us long-term hope for preserving our heritage—not just writings, but text, paintings (stored as detailed photographs), sculpture, architecture, whatever."
   > — [LM 3/25]

   > "The system this book proposes is a generalized and self-networking structure that can eventually be put in deep rock and deep space—Iron Mountain or the asteroid belt."
   > — [LM 3/25]

   A system designed for "deep rock and deep space" does not delete published content because a monthly payment was missed.

---

## Summary

| Question | Answer |
|----------|--------|
| Does the system owe permanence to third parties? | **Yes** — explicitly and contractually |
| Is this independent of the author's payment? | **Yes** — the obligation arises from third-party dependence, not author intent |
| Is the funding mechanism fully specified? | **No** — this is a gap in the specification |
| What is the philosophical priority? | Permanence obligation is primary; economic sustainability is a constraint to be solved, not a limit on the obligation |

The obligation to third parties is a **design invariant**. The question of who pays when the author cannot is an **implementation problem** that must be solved without violating the invariant.

---

## Question 10 [nelson]

> If content carries royalty or micropayment relationships with other parties, must those economic structures be preserved even when the content's owner defaults on storage or hosting obligations?

### Nelson's Answer

# Economic Structures and Storage Default

This question strikes at a genuine tension in Nelson's design — one he acknowledges implicitly but does not fully resolve. Let me trace what he specifies, what he leaves open, and what the architecture implies.

## What Nelson Explicitly Specifies

### Royalties Are Structural and Automatic

The economic relationship between content and its creator is embedded in the I-space address itself. Every byte's permanent address encodes its home document and therefore its owner:

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The cash register is per-document: "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." [LM 5/13]

Because royalty flows are computed from I-addresses — which are permanent and encode origin — the *structure* of who-gets-paid is inherent in the address system itself. It cannot be "stripped" any more than attribution can be stripped. The economic relationship IS the address relationship.

### Published Content Must Stay Published

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

This is stated as a contractual obligation of publication, not merely a preference. The reason is explicitly economic — others have created links and transclusions that depend on the content:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it." [LM 2/43]

### Storage Requires Ongoing Payment

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage is rental, not purchase. Someone must keep paying.

### Vendor Failure Has a Protocol

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

And backup copies are distributed:

> "Material is moved between servers for a number of purposes: ... for redundancy and backup purposes." [LM 4/71]

## The Unresolved Tension

Here is the problem your question identifies: Nelson specifies **three things that cannot all hold simultaneously** when an owner defaults:

1. **Published content must stay published** (permanence guarantee)
2. **Storage must be self-supporting** (no subsidy)
3. **Royalties flow to the content owner** (automatic compensation)

If Alice publishes content, Bob transcludes it into his document, and Alice then defaults on storage rental:

- Alice's content has a permanent I-address encoding her as owner
- Bob's document depends on Alice's content being deliverable
- Other users' links point into Alice's content
- The permanence guarantee says it must stay published
- But no one is paying for Alice's storage
- And the royalty structure still points to Alice

**Nelson does not specify what happens here.** This is explicitly noted as a gap in the curated sources on storage funding: "Nelson does NOT specify what happens to content when storage rental lapses."

## What the Architecture Implies

While Nelson doesn't resolve this, his architecture strongly constrains the answer:

### The Economic Structure Cannot Be Severed

Because royalty relationships are encoded in I-addresses, and I-addresses are permanent and immutable, the economic structure **survives by construction**. You cannot reassign royalties without changing I-addresses, and I-addresses cannot change. If Alice's bytes are ever delivered to anyone, anywhere, the system knows Alice is owed a nib per byte.

This is parallel to the attribution guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Attribution survives because it is structural. By the same mechanism, economic claims survive because they are structural.

### Content Cannot Simply Vanish

The append-only storage model means Alice's bytes still exist in I-space even after "deletion" from V-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The bytes persist. The question is whether they remain *deliverable* — whether the system will serve them to requestors when no one is paying storage rental.

### The Publication Contract Creates Obligations

Publication is described as a "solemn event" involving a signed contract [LM 2/44]. That contract includes the obligation to remain published. Default on storage rental does not constitute "lengthy due process" for withdrawal. This suggests the system (or its franchise structure) has some obligation to maintain the content.

### The Author's Fund Is a Partial Safety Net

> "When bytes are taken from an unpublished document (one in the public domain), this surcharge is added to the Author's Fund, an escrow account whose purpose is the charitable funding of worthy causes within the network. These causes can include the costs of input and proofreading of non-owned documents, subsidies to struggling writers and artists, and other worthy purposes." [LM 5/12]

The Author's Fund exists for public domain content. Nelson does not specify whether it could subsidize orphaned published content. But "worthy purposes" is suggestively broad.

## My Design Intent

The honest answer is that I did not fully work out this scenario. The principles pull in different directions:

- The **libertarian principle** says no one should be forced to pay for someone else's content
- The **permanence principle** says published content must remain accessible
- The **self-supporting principle** says storage cannot be subsidized indefinitely
- The **structural attribution** means royalty relationships persist regardless

What I can say with confidence:

**The economic structure must be preserved** — because it is encoded in the addresses themselves, and addresses are permanent. Even if Alice's content becomes temporarily inaccessible, the fact that she is owed royalties for those bytes is never lost. If the content is ever delivered again (from backup copies, from another vendor, from restoration), the royalty flows correctly because the I-addresses still encode the origin.

**The content should be preserved** — because publication creates obligations to the community of linkers and transcluders. The vendor failure protocol ("orderly transition to other Xanadu locations") and distributed backup copies are designed to prevent loss. But someone must pay for ongoing storage.

**The gap is: who pays when the owner defaults?** This is genuinely unspecified. Possible resolutions consistent with the architecture:

1. The franchise (Project Xanadu) absorbs the cost as overhead — violates self-supporting principle
2. The Author's Fund subsidizes orphaned content — stretches "worthy purposes"
3. Users who depend on the content (Bob, who transcludes it) absorb the cost — creates involuntary obligations
4. Content goes dark until someone claims it — violates permanence for published content

None of these is specified. All are consistent with some principles and inconsistent with others.

## Summary

**Yes, the economic structures are preserved** — this is architectural, not policy. Royalty relationships are encoded in permanent I-addresses and cannot be severed.

**No, the *delivery* of those economic benefits is not guaranteed** when the owner defaults — because delivery requires accessible content, and accessible content requires paid storage.

**The system is designed to prevent this scenario** through distributed backup, vendor transition obligations, and the permanence of publication. But the gap between "content must stay published" and "storage must be self-supporting" is real and unresolved in Literary Machines.

NEED_RAW: [5/14-5/16, 5/19-5/21] — The vendor contract provisions around cancellation and transition may contain more specific language about obligations when a publisher's account lapses. The curated sources cover the main points but the exact contract language on default scenarios would be worth verifying.
