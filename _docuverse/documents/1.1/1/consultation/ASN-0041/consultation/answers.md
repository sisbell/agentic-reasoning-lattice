# Consultation Answers — Tumbler Ownership

**Inquiry:** What does it mean to own a tumbler position? How is ownership established, delegated, and what does it confer?
**Date:** 2026-03-15 15:34
**Questions:** 15 (10 nelson, 5 gregory)

---

## Question 1 [nelson]

> What rights does owning a position in the address space confer upon the owner?

### Nelson's Answer

## Rights of Address-Space Ownership

Owning a position in tumbler-space confers a specific bundle of rights. Let me be precise about each.

### 1. The Right to Baptize

The most fundamental right is **subdivision** — the right to create new addresses beneath your own.

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

If you own account 1.2, you and only you can create documents 1.2.1, 1.2.2, 1.2.3 beneath it. If you own document 1.2.5, you can create versions beneath it. This right is **perpetual and exclusive**:

> "Once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

No one else can baptize addresses in your subtree. No central authority allocates them for you. You own your branch of the tree, period.

### 2. The Right to Modify

Owning a document means you alone can change its contents:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This covers INSERT, DELETE, REARRANGE, APPEND — all operations that alter the document's V-space arrangement. No one else may perform these operations on your document.

### 3. The Right to Create Links at Your Address

Links created in your document belong to you. Ownership is determined by the link's home address, not by what it points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

This is subtle but important. Your annotations, comments, citations — any links you create — live at YOUR address. The person whose content you link to cannot delete your links. Your links are your property.

### 4. The Right to Withdraw (with constraints)

For **private** documents, withdrawal is straightforward — your document, your choice.

For **published** documents, this right is deliberately constrained:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

Publication is a social contract. You chose to make it permanent. Others have linked to it — their links, at their addresses, depend on your content's continued existence.

### 5. The Right to Receive Royalties

Ownership of published content entitles you to automatic compensation:

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

Your "cash register" increments every time your bytes are delivered to anyone, anywhere in the docuverse.

### 6. The Right to Control Access (Private Documents)

> "A document may be private or published. A private document may be read and linked-to only by the owner and his or her associates." [LM 2/42]

You decide who your "designees" are.

---

## What Ownership Does NOT Confer

Equally important — rights you explicitly **do not** have:

**No control over in-links.** Once you publish, anyone may link to your work. You relinquished that right:

> "Each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

**No control over quotation.** Anyone may window (transclude) your published content:

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

**No control over derivative works.** Others may create versions that include your content:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

**No control over your node address.** You don't choose which server you're assigned to:

> "Typically, the user will have no control over the node address he, she or it is assigned." [LM 4/29]

---

## Summary

Ownership of an address-space position is a **bundle of creative and economic rights**: you can subdivide infinitely, modify freely, link from your address, receive royalties, and control private access. But publication creates a **reciprocal obligation** — your content stays available, others may link and quote freely, and you accept automatic royalty as your sole compensation. The tradeoff is deliberate: you give up control over use, but you never give up compensation for use.

---

## Question 2 [nelson]

> Does ownership of a position automatically extend to all positions subordinate to it in the hierarchy?

### Nelson's Answer

## Yes for allocation authority. No for content ownership.

Nelson describes two distinct concepts that the question conflates:

### 1. Baptism Rights (Allocation Authority) — Yes, extends downward

The owner of a position controls the creation of sub-positions beneath it:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

A server operator creates accounts. An account holder creates documents. A document owner creates versions. This authority flows strictly downward through the hierarchy.

### 2. Content Ownership — No, does not extend upward

Once a subordinate position is assigned, its occupant owns it:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

The node operator does not own the user's documents. The Storage Vendor contract makes this explicit — vendors are custodians, not owners:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system." [LM 5/14-5/15]

### 3. Addressability — Extends, but is not ownership

A search or link targeting a higher position reaches everything beneath it:

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

This is a property of the address space, not an ownership claim. You can find all documents under an account because the tumbler tree structure makes them addressable as a contiguous span — but finding content is not the same as owning it.

### The Delegation Model

The pattern is delegation, not inheritance:

| Level | Controls allocation of... | Owns content of... |
|-------|--------------------------|---------------------|
| Node operator | Accounts under the node | The node itself only |
| Account holder | Documents under the account | Their documents |
| Document owner | Versions under the document | Their document |

Each level grants authority to the level below, then relinquishes control over what's created there. This parallels how DNS delegation works: ICANN controls TLDs, but once `example.com` is assigned, its registrant controls all subdomains.

### One gap

Nelson does not explicitly address what happens if a node operator *revokes* an account, or whether revocation is even possible. The Storage Vendor contract requires "orderly transition of all customer-stored materials to other Xanadu locations" upon cancellation [LM 5/16], suggesting the vendor cannot simply delete a user's content — but the authority relationship between node operator and account holder at the tumbler level is not fully specified.

NEED_RAW: 4/17-4/20 (for any additional detail on ownership delegation vs. inheritance that the curated summaries may have condensed)

---

## Question 3 [nelson]

> Can an owner delegate partial rights over a portion of their address space to another party without transferring ownership itself?

### Nelson's Answer

## Delegation of Partial Rights in Xanadu

Nelson describes two mechanisms that touch on this question, but neither constitutes a fully specified partial-rights delegation model. The answer is: **partially, through subdivision and bestowment — but not through granular permission delegation over existing space.**

### What Nelson DOES Specify

**1. Baptism: Subdivision and Bestowment**

The primary mechanism is forking — the owner creates sub-addresses and bestows them on others:

> "Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

This is ownership **creation and transfer**, not delegation of partial rights. When you bestow sub-address 1.3.7 on someone, they now **own** 1.3.7 and everything under it. You retain ownership of 1.3 but not of 1.3.7. The phrase "on whatever basis the owners choose" hints at flexibility in the terms of bestowment, but Nelson does not elaborate on what those terms might be.

**2. Designees: Access to Private Documents**

Nelson mentions that private documents can be shared with "associates" or "designees":

> "A private document may be read and linked-to only by the owner and his or her associates." [LM 2/42]

This implies some ability to grant read access without transferring ownership. But the mechanism is unspecified — there are no access control lists, no per-user permission grants, no role definitions.

### What Nelson Does NOT Specify

- **Granular permission delegation** — There is no mechanism for "you may modify bytes 100-200 of my document but not the rest"
- **Read-only vs. modify access** — The model is binary: you own it (full control) or you don't (no modification rights)
- **Revocable delegation** — No mechanism for granting and later revoking partial rights
- **Access control lists** — Only three access levels exist: owner, designees (unspecified mechanism), everyone

### The Ownership Model Is Absolute

Nelson's ownership principle is stark:

> "Every document has an owner... Only the owner has a right to withdraw a document or change it." [LM 2/29]

There is no concept of "co-editors," "collaborators with write access," or "administrators with partial control." If you want someone to modify content, the Xanadu pattern is: they create their **own version** (via `CREATENEWVERSION`) or their own **derivative document** (via transclusion with modifications). They never modify your document — they fork from it.

### The Architectural Consequence

This absoluteness is deliberate. It aligns with Nelson's principle that **writing always succeeds** — if you cannot modify someone else's document, you create a version. Denial is a fork, not an error. The system never needs partial permissions because the response to "you can't edit this" is always "then make your own."

The forking mechanism effectively replaces permission delegation: instead of granting someone partial rights over your space, you subdivide your space and grant them full ownership of the subdivision. The hierarchy of the tumbler address preserves the provenance (1.3.7 is visibly "under" 1.3), but the ownership is complete.

### Summary

| Mechanism | What It Does | Is It Partial Delegation? |
|-----------|-------------|--------------------------|
| Baptism/Forking | Create sub-address, bestow on another | No — ownership transfer, not delegation |
| Designees | Grant access to private docs | Partially — mentioned but unspecified |
| Versioning | Others create their own versions | No — independent ownership, not delegation |

Nelson's design favors **ownership clarity over permission complexity**. Rather than a rich permission model, the system provides absolute ownership plus the ability to subdivide and bestow. The philosophical stance is that literature works through independent ownership and interconnection (via links and transclusion), not through shared control over the same space.

NEED_RAW: [2/29-2/31, 4/17-4/20] — to verify whether Nelson says anything more about the terms of bestowment or the mechanism for designating "associates" that the curated sources may not fully capture.

---

## Question 4 [nelson]

> Is ownership of a position permanent once granted, or can the system revoke it under any circumstances?

### Nelson's Answer

## Ownership Is Permanent — With Obligations

Nelson is explicit: once you are assigned a position in tumbler-space, your control over it is **permanent and irrevocable**.

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore."
> — [LM 4/29]

The word "forevermore" is deliberate. Combined with the permanence guarantee on addresses themselves:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address."
> — [LM 4/19]

The system never reassigns or reclaims tumbler positions. The owner "baptizes" sub-addresses freely, and those sub-addresses belong to their designees permanently in turn.

## What Ownership Does NOT Grant

Permanence of ownership does not mean unlimited freedom. Nelson imposes **obligations that flow FROM ownership**:

**Published documents create binding constraints on the owner:**

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process."
> — [LM 2/43]

You own the document. You cannot easily withdraw it. Publication constrains the owner — it does not transfer ownership to anyone else.

**Link freedom constrains the owner's control over incoming connections:**

> "Each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract."
> — [LM 2/43]

Again, this limits what ownership means in practice, but does not revoke it.

## Edge Cases Where Content Can Be Removed

Nelson describes two scenarios where content is removed, but neither revokes ownership of the position:

**1. Peremptory challenge (anonymous content only):**

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge."
> — [LM 2/60]

This removes the *content*, not the address or its ownership. The John Doe is absent, so the challenge succeeds by default.

**2. "Lengthy due process" (accountable publishers):**

For identified publishers, peremptory challenge "no longer holds water" — removal requires "negotiation or court order." This is legal process external to the system, not a system mechanism for revoking ownership.

## Storage Vendor Failure

When a vendor goes down, ownership is preserved through migration:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations."
> — [LM 5/16]

The owner's content and position transfer intact. The system is designed so that infrastructure failure never becomes ownership revocation.

## The Unspecified Gap: Storage Payment Lapse

Nelson requires that "ALL SERVICES MUST BE SELF-SUPPORTING" [LM 4/5] and storage requires ongoing rental. He does **not** specify what happens if an owner stops paying. The address itself cannot be reassigned (permanence guarantee), but accessibility may lapse. This is a gap in the specification — ownership of the position is permanent, but whether the content remains *accessible* without ongoing payment is unresolved.

## Summary

| Scenario | Ownership Revoked? | Content Affected? |
|----------|-------------------|-------------------|
| Normal operation | No | No |
| Publication | No (constrained) | Cannot withdraw easily |
| Peremptory challenge | No | Removed (anonymous only) |
| Court order | No | Possibly removed |
| Vendor failure | No (migrated) | Transitions to new vendor |
| Payment lapse | No (address permanent) | Accessibility unspecified |

**The system has no mechanism for revoking ownership of a tumbler position.** Ownership is structural — encoded in the address itself — and permanent by design. What the system does constrain is what owners may *do* with their positions once publication creates obligations to others.

---

## Question 5 [nelson]

> Must the system record and preserve the provenance of every ownership grant — who granted what to whom?

### Nelson's Answer

## Ownership Grant Provenance: What Nelson Specifies

**Short answer: No. Nelson does not require the system to record the provenance of ownership grants as auditable events. Ownership is structural (encoded in the address), not journaled.**

---

### What IS Specified: Structural Provenance

The tumbler address itself permanently encodes the delegation chain:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Document `1.2.3.4` structurally tells you: server `1`, account `1.2`, document `1.2.3`, version `1.2.3.4`. The hierarchy of *who could have created what* is readable from the address. This is permanent and immutable — addresses are never reassigned.

Similarly, origin traceability for content is structural:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

But this traces content to its *home document*, not the chain of human decisions that authorized the account or allocated the address.

### What Is NOT Specified: Grant Events

Nelson does not describe:

1. **Audit logs for baptism** — When account `1.2` "baptizes" sub-account `1.2.5`, there is no specified record of that act (who requested it, when, under what authority).

2. **Timestamps on address creation** — Time is explicitly excluded from the tumbler: "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]. What "kept track of separately" means for ownership grants is unspecified.

3. **Ownership transfer records** — Nelson acknowledges ownership can change ("The rightful copyright holder, or someone who has bought the document rights" [LM 2/29]) but specifies no protocol for recording transfers.

4. **Grant authorization chains** — The system knows `1.2` owns everything under `1.2.*`, but it does not record *why* `1.2` was assigned to a particular user, or by whom.

### The Enforcement Model Is Contractual, Not Technical

Nelson's trust model operates through franchise contracts, not system-recorded audit trails:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material." [LM 5/14-5/15]

The "tripod of legal relationships" (Project Xanadu ↔ Storage Vendor ↔ User) handles authorization through contracts signed on "something very like a credit-card triplicate slip" — paper, not system state.

The session model extraction confirms this gap:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The word "assigned" implies an act that happens, but no mechanism records it within the system.

### What The System Does Track

The closest thing to grant provenance Nelson specifies is the **cash register** mechanism:

> "Each published document has a cash register. This is a system-maintained counter... It is in the user's system area, along with passwords and accounting information." [LM 5/13]

The "user's system area" contains passwords and accounting — suggesting some per-account state exists. But Nelson never specifies that ownership delegation events are recorded there.

### Summary

| Aspect | Specified? | Mechanism |
|--------|-----------|-----------|
| Who owns what now | Yes | Structural — encoded in tumbler address |
| Content origin | Yes | Structural — I-address encodes home document |
| Who granted an account | No | Contractual (paper), not system-recorded |
| When a grant occurred | No | "Time is kept track of separately" — unspecified for grants |
| Ownership transfer history | No | Acknowledged as possible, no protocol specified |
| Authorization chain | No | Implicit in address hierarchy, not journaled |

The tumbler hierarchy lets you *infer* that server `1` must have authorized account `1.2`, and account `1.2` must have created document `1.2.3` — but the system does not record these acts as events with timestamps, actors, and justifications. Provenance of the ownership *structure* is implicit in the addresses; provenance of ownership *decisions* is outside the system's scope as Nelson defines it.

NEED_RAW: [4/29, 2/29-2/31, 5/6-5/8] — these pages may contain additional detail on account creation, ownership mechanics, and the user's system area that could clarify whether any grant-recording obligation is implied.

---

## Question 6 [nelson]

> Can ownership be transferred from one party to another, and if so, does the original owner retain any residual rights?

### Nelson's Answer

## Ownership Transfer in Xanadu

### Transfer Is Acknowledged but Mechanically Unspecified

Nelson acknowledges that ownership can change hands. His definition of "owner" on page 2/29 is notably broad:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This definition admits at least three paths to ownership:
1. **Creation** — you made it
2. **Arrangement** — you commissioned it (e.g., a publishing company)
3. **Purchase** — you "bought the document rights"

The phrase "someone who has bought the document rights" explicitly presumes transfer is possible. But Nelson specifies **no in-system mechanism** for executing a transfer — no TRANSFEROWNERSHIP command in the FEBE protocol, no contract provision for reassignment, no tumbler-level operation.

### The Structural Tension

Transfer creates an architectural tension that Nelson does not resolve. The I-space address permanently encodes the originating account:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

If Alice creates a document, its I-address is `Node.0.Alice.0.Doc.0.Element`. If Bob buys the rights, the address still says "Alice." The permanence guarantee forbids changing it:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

So after transfer, the system would need to distinguish between **structural origin** (encoded in the address — always Alice) and **current ownership** (now Bob). Nelson does not describe how this distinction is tracked. The curated sources contain no discussion of an ownership registry, transfer ledger, or reassignment metadata.

### Residual Rights: Not Explicitly Addressed

Nelson says nothing about whether the original owner retains any rights after transfer. The curated sources are silent on:

- Moral rights (attribution after transfer)
- Reversion rights (reclaiming ownership under certain conditions)
- Revenue sharing between original creator and new owner
- Whether the original creator retains any control over modifications

However, there is one **structural residual** that cannot be eliminated: origin traceability.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

Because the I-address permanently encodes the creating account, the system will always show that Alice's account originated the content — even if Bob now owns it. This is not a "right" in the legal sense, but it is a permanent structural fact that no transfer can erase. Whether Nelson intended this as a form of inalienable attribution or simply as an artifact of the addressing scheme is not stated.

### The Publishing Complication

For published documents, transfer is further constrained by permanence obligations:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

A new owner inherits this obligation. The publication contract binds the document, not the person — anyone who owns a published document must keep it published because others' links depend on it.

### Summary

| Question | Answer |
|----------|--------|
| Can ownership be transferred? | Yes — Nelson explicitly mentions "someone who has bought the document rights" |
| Is there a transfer mechanism? | No — no FEBE command, no contract provision, no protocol |
| Does the original owner retain rights? | Not specified |
| Does structural attribution persist? | Yes — I-addresses permanently encode the originating account |
| Does the new owner inherit obligations? | Implied — published documents must stay published regardless of owner |

NEED_RAW: [2/29-2/31, 5/6-5/10] — These pages may contain additional detail on ownership mechanics and the business framework for rights transfer that the curated sources summarize only partially.

---

## Question 7 [nelson]

> Does the design distinguish between owning a position and merely having permission to act within it?

### Nelson's Answer

## Ownership vs. Permission in the Xanadu Design

Short answer: **Yes, but minimally.** Nelson draws a sharp line between ownership (structural, encoded in addresses) and access (binary: designee or everyone). But he does not develop a granular permission model. The distinction exists at two levels: the tumbler hierarchy (who owns positions) and document access (who can see content).

---

### Ownership Is Structural

Ownership in Xanadu is encoded directly in the tumbler address. The User field of an I-address IS the owner:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

Ownership confers absolute control:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

The word **bestowed** is key. When a node operator assigns an account number, or an account holder creates a document, the recipient OWNS that sub-position. This appears to be an irrevocable transfer:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

"Forevermore" is strong language. Once you own a position, you own everything you create beneath it.

---

### Permission Is Binary and Minimal

Nelson's access model has exactly three tiers:

| Level | Can read | Can modify | Can link to |
|-------|----------|------------|-------------|
| **Owner** | Yes | Yes | Yes |
| **Designee** | Yes (private docs) | No | Yes (private docs) |
| **Everyone** | Yes (published docs) | No | Yes (published docs) |

> "A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

There is no concept of:
- Delegated write access
- Revocable sub-ownership
- Role-based permissions
- Per-user access control lists
- Shared editing authority

The "designee" or "associate" mechanism is mentioned but never specified technically. Nelson acknowledges this gap — private documents were not even implemented in XU.87.1:

> "Private documents. (Currently all documents are visible to all users.)" [LM 4/79]

---

### The Crucial Asymmetry: Denial Is a Fork

The deepest design consequence of this model is what happens when you lack ownership. In conventional systems, "permission denied" is an error. In Xanadu, it's a creative act:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

If you cannot modify a document (because you don't own it), you create a version that you DO own. Your version transcludes the original and adds your changes. The system never produces a permanent "access denied" — only a redirect to your own position in the address space.

---

### The Vendor Exception: Acting Without Owning

The clearest example of "permission to act within a position without owning it" is the Storage Vendor. The Vendor operates the physical node — stores bytes, forwards requests, maintains the system — but does NOT own the content within it:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system." [LM 5/14-5/15]

The Vendor has access (for operational purposes) but not ownership. This is a contractual distinction, not a technical one — enforced by franchise agreement rather than access control machinery.

---

### What Nelson Does NOT Distinguish

Several ownership/permission questions are left unresolved:

1. **Can a node owner revoke an account?** "Forevermore" suggests not, but Nelson doesn't address disputes.

2. **Can ownership be shared?** No mechanism is described. Documents have one owner.

3. **Can the designee mechanism be fine-grained?** Nelson mentions "associates" without specifying how designation works — per-document? per-account? revocable?

4. **What about sub-accounts?** The tumbler hierarchy allows accounts to be "continually subdividable" [LM 4/29], but it's unclear whether sub-account holders are owners or delegates of the parent account.

5. **What about publishing companies?** Nelson notes a document can be owned by "someone who arranged it to be created and stored, such as a publishing company" [LM 2/29]. This suggests proxy ownership, but the mechanism for establishing or transferring it is unspecified.

---

### Summary

Nelson's design distinguishes ownership from permission, but the distinction is deliberately simple:

- **Ownership** is absolute, structural, permanent, and encoded in addresses. It confers full control.
- **Permission** is binary (designee or public), confers read-only access, and is socially rather than technically enforced.
- **There is no middle ground** — no "write permission without ownership," no "delegated authority," no ACLs.
- **The Vendor relationship** is the one case where someone acts within a position they don't own, governed by contract rather than address structure.

The design philosophy is clear: keep the authorization model as simple as possible, and handle everything else through the forking mechanism. If you can't modify it, make your own version. Ownership is structural; permission is social.

---

## Question 8 [nelson]

> What obligations does ownership impose on the owner — are there responsibilities the system enforces, not just rights it grants?

### Nelson's Answer

## Obligations of Ownership in Xanadu

Nelson's design imposes significant obligations on document owners — obligations that increase dramatically upon publication. The system is not just about granting rights; it's about creating a web of mutual commitments that make the docuverse work.

---

### 1. Publication Creates Irrevocable Commitments

The most striking obligation: **publishing is nearly irreversible.** Once you publish, you surrender several forms of control.

**You cannot withdraw:**

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The enforcement model specifies withdrawal requires **one year's notice and a fee** [LM 5/20 area]. This is not a right the system grants grudgingly — it is an obligation the system imposes: you MUST keep your published content available because others have built upon it.

**You must permit all linking:**

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

You cannot block, hide, or interfere with incoming links. Your published document is open territory for annotation, criticism, commentary — by anyone.

**You must permit all quotation:**

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

You cannot prevent others from windowing your content into their documents. Your sole remedy is economic: you get paid per byte delivered.

**You accept automatic royalty as your sole compensation** — no negotiation, no premium pricing, no withholding. The rate is fixed system-wide by Project Xanadu.

---

### 2. Economic Obligations

**Ongoing storage rental:**

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Owners must pay ongoing per-byte storage rental. This is not a one-time publication fee — it is a continuing obligation. If you stop paying, there is no guarantee your content remains accessible. The system does not provide free permanent hosting; permanence of the *address* (once assigned, never reused) is distinct from permanence of *accessibility* (requires ongoing payment).

Nelson frames this explicitly:

> "a 'publisher' is someone who pays for the rapid accessibility of materials and benefits from their use along with the author." [LM 2/61]

---

### 3. Obligations Imposed by Participation

Every user — owner or not — signs the contract. Nelson envisions this as "something very like a credit-card triplicate slip." The obligations include:

**Not to store pirated content:**
The user agrees not to store others' copyrighted material without authorization.

**Not to resell without forwarding royalties:**
If you redistribute content, royalties must flow to the original creators through the standard mechanism.

**Responsibility for accuracy:**

> "User acknowledges that responsibility for the accuracy of material on the network rests with those users furnishing and publishing it; that liability for the consequences of inaccurate material rests with those users who furnish or publish it and represent it to be correct and usable." [LM 5/17-5/18]

This is a meaningful obligation: you bear legal liability for what you publish.

**Responsibility for your own privacy:**

> "Considering such risks, if User still desires to store private material, User agrees to exercise diligence in the encryption of all materials User considers private; but User acknowledges that no such methods have been proven safe or reliable." [LM 5/17]

The system provides no encryption. If you want privacy, that's YOUR obligation.

---

### 4. What the System Architecturally Enforces vs. What Is Contractual

This distinction matters. Some obligations are enforced by the architecture itself; others rely on the franchise and contract structure.

| Obligation | Enforcement Mechanism |
|---|---|
| Content permanence in I-space | **Architectural** — append-only storage; deletion is V-space only |
| Only owner can modify | **Architectural** — tumbler ownership encoded in address |
| Royalty accounting | **Architectural** — cash register increments on every byte delivered |
| Cannot withdraw easily | **Contractual** — one year notice + fee required |
| Must permit linking | **Contractual** — publication contract; architecturally, links are independent objects the target owner cannot touch |
| Must permit quotation | **Contractual** — Internal Copyright Convention |
| Must not store pirated content | **Contractual only** — system cannot verify provenance |
| Must not resell without royalty | **Contractual only** — system cannot control terminal behavior |

Nelson is candid about the limits:

> "There is no way whatever to ascertain or control what happens at the users' terminals. Therefore perforce all use whatever is legitimate, and anyone who plans to be vulnerable to 'misuse,' whatever he or she thinks that may be, had better keep his or her stuff off the system." [LM 2/47]

---

### 5. The Deepest Obligation: Reciprocity

The Internal Copyright Convention is fundamentally a system of **mutual obligation**:

> "if you publish a thing through the network, you have to agree to the same rules as everybody else — which are intended to create a fair balance of incentives." [LM 2/41-2/45 area]

You give up control in exchange for the same freedom to link to and quote from everyone else. You accept automatic royalty in exchange for the same automatic payment when others use your work. The obligation is symmetrical: what you must permit others to do with your work, you gain the right to do with theirs.

Nelson frames this as a contractual foundation, not just a technical feature:

> "Because the conceptual structure expects participants to behave in certain ways, these are embraced in the contract offered to users. These provisions are necessary for the orderly and confident use of published material by many people." [LM 4/4]

---

### Summary

Ownership in Xanadu is not sovereignty — it is **stewardship within a contractual commons.** The owner has absolute control over modification (only you can change your document), but publication imposes binding obligations: you must keep content available, permit linking, permit quotation, accept standardized compensation, pay for storage, and bear responsibility for accuracy. The system enforces some of these architecturally (append-only storage, tumbler-based ownership, automatic royalty accounting) and others contractually (the Internal Copyright Convention, the franchise model). The design deliberately trades owner control for network-wide interconnectability — that tradeoff IS the social contract of the docuverse.

---

## Question 9 [nelson]

> If an owner delegates a sub-range of their space, can the delegate further sub-delegate portions of that range to others?

### Nelson's Answer

## Yes — Sub-Delegation Is Inherent in the Design

The forking mechanism is **recursive by definition**. Whoever owns a number controls all sub-numbers beneath it, and whoever receives a sub-number becomes its owner with the same power.

### The Core Principle

> "The owner of a given item controls the allocation of the numbers under it."
> — [LM 4/20]

This is the complete rule. There is no qualifier like "only the original owner" or "only one level deep." Ownership of a number confers full authority over its subdivision.

### How It Works

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers."
> — [LM 4/17]

So if Server 1 bestows Account 1.3 on Alice, Alice owns 1.3 and can create documents 1.3.1, 1.3.2, etc. She can also sub-delegate: bestow sub-account 1.3.5 on Bob. Bob then owns 1.3.5 and can create 1.3.5.1, 1.3.5.2 — or further delegate 1.3.5.7 to Carol. Carol can then fork beneath 1.3.5.7 indefinitely.

Nelson makes the recursive nature explicit:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism."
> — [LM 4/19]

The "and so on" is not hand-waving — it's the point. The mechanism repeats at every level:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants."
> — [LM 4/19]

### Permanence of Delegated Authority

Once assigned, control is permanent:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore."
> — [LM 4/29]

"Forevermore" — not "until the parent revokes it." The delegation is a one-way act. You baptize a sub-number and the new owner takes permanent control of that subtree.

### The Architectural Consequence

> "So the docuverse is all really one big forking document."
> — [LM 4/18]

The entire docuverse is a single recursively-forking tree. Every node in the tree has the same property: its owner can subdivide it, and each subdivision's new owner can subdivide further. There is no distinguished "root level" with special powers — the mechanism is uniform at every depth.

### Summary

Sub-delegation is not merely permitted — it is the **only** delegation mechanism. There is no way to grant someone a number while restricting their ability to fork beneath it. Ownership of a tumbler address means control of its entire subtree, including the right to delegate sub-ranges to others who gain the same recursive authority.

---

## Question 10 [nelson]

> Must the system guarantee that no two parties can independently hold ownership of the same position?

### Nelson's Answer

Yes — exclusive ownership of each position is a structural invariant of the tumbler addressing system, though Nelson states it as a design property rather than as a separately enumerated guarantee.

## The Structural Argument

The tumbler system is a **tree** with strict ownership at every node. Three properties together enforce exclusivity:

**1. Owned numbers with singular ownership.**

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

Nelson consistently uses the singular: "**the** owner of a given item controls the allocation of the numbers under it" [LM 4/20]. Not "an owner" or "owners" — **the** owner.

**2. Baptism as the sole creation mechanism.**

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

New positions are created only by forking from a parent. The parent's owner is the sole authority who can baptize sub-numbers. Two independent parties cannot baptize the same address because doing so would require both to own the parent — which contradicts singular ownership at that level.

**3. The address encodes ownership.**

The I-space tumbler `Node.0.User.0.Document.0.Element` structurally encodes which account owns which document. The User field **is** the owner:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The account holder has "full control" over subdivision — not shared control with anyone else.

## Why This Must Be Exclusive

Several of Nelson's guarantees depend on exclusive ownership being inviolable:

- **Modification rights**: "Only the owner has a right to withdraw a document or change it" [LM 2/29]. If two parties owned the same position, conflicting modifications would be irreconcilable.

- **Royalty accounting**: "Each published document has a cash register... the remainder becomes the author's profit" [LM 5/12]. The royalty flows to **the** owner. Dual ownership would make royalty disposition ambiguous.

- **Link ownership**: "Its home document indicates who owns it, and not what it points to" [LM 4/12]. Link ownership is determined by address; ambiguous ownership of positions would make link ownership ambiguous.

- **Origin traceability**: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. This guarantee requires unambiguous ownership at every I-address.

## Ownership Transfer vs. Dual Ownership

Nelson does allow ownership transfer — "the rightful copyright holder, or someone who has bought the document rights" [LM 2/29] — but this is succession, not co-ownership. At any point in time, each position has exactly one owner. The transfer replaces one owner with another; it does not create a second concurrent owner.

## What Nelson Does NOT Address

Nelson does not specify the mechanism that prevents collisions at the network level — that is, how two servers are prevented from independently assigning the same tumbler address to different parties. The tree structure makes this conceptually impossible (each server controls its own sub-tree), but the interserver coordination details are left to BEBE, which Nelson states is "still undergoing definition" [LM 4/70].

The franchise model provides a social backstop: Storage Vendors must "use software furnished by Project Xanadu without modification" [LM 5/14], so the allocation algorithm is centrally controlled even though allocation authority is distributed.

## Summary

Exclusive ownership of each position is not listed among Nelson's explicit "fundamental guarantees" but is a structural invariant of the tumbler tree that every explicit guarantee depends on. The tree-based baptism mechanism makes dual independent ownership of the same position architecturally impossible: you can only create sub-addresses beneath addresses you already exclusively own.

---

## Question 11 [gregory]

> Is ownership of a tumbler position determined structurally from the tumbler hierarchy (e.g., `1.1.0.2` is owned by whoever owns the `1.1.0.2` account prefix), or is there a separate ownership table or data structure that records who owns what?

### Gregory's Answer

## KB Synthesis

Ownership is determined **structurally from the tumbler hierarchy** — there is no separate ownership table.

The evidence is explicit in [ST-VERSION-OWNERSHIP] (Finding 0068):

> The ownership check uses `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)`. **Ownership is determined by account prefix matching, not by an explicit permissions table.**

`tumbleraccounteq` compares the account component of two tumbler addresses — i.e., it checks whether the document's address prefix matches the current session's account address. The session's current account (set via the `account()` operation, isolated per-session per [FC-SESSION-ACCOUNT-ISOLATION]) establishes the ownership context for each operation.

Supporting structure from [SS-TUMBLER-CONTAINMENT]:

> Containment of address A under prefix B is checked by truncating A to the length of B and comparing for equality.

So `isthisusersdocument(isa)` amounts to: truncate the document's ISA to account-depth, compare against the current session's account address. If they match, the session owns it.

The BERT table ([SS-BERT]) is a related but distinct mechanism — it records `(connection, document) → access_level` during an open session, tracking read/write access control. BERT is session-scoped access control, not persistent ownership. The address hierarchy is ownership; BERT is current-access-state.

**Summary:** Ownership is a structural property — a document is owned by whoever's account address is a prefix of the document's address. The address hierarchy encodes ownership directly; no ownership registry exists.

---

## Code Exploration

I now have everything needed to answer the question fully.

---

## Ownership Is Purely Structural — Tumbler Prefix Matching

There is no separate ownership table. Ownership of a tumbler position is determined entirely by **structural prefix matching** between the document's tumbler and the current user's account tumbler.

---

### The Core Function: `tumbleraccounteq`

`tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  /* Compare until account (bptr) terminates with two zeros.
     Document (aptr) may continue beyond the account's address space. */
  for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
      if (++j_b == 2) {
        return(TRUE);  /* Account terminated, document is under this account */
      }
    } else {
      if (aptr->mantissa[i] != bptr->mantissa[i]) {
        return(FALSE);
      }
    }
  }
  return (TRUE);
}
```

**Algorithm**: Walk the account tumbler (the shorter one, `bptr`). For each non-zero digit, the document must match exactly. When the account's mantissa terminates with two consecutive zeros, the document is considered "under" that account prefix — regardless of what it has in those positions. A document like `1.1.0.2.3` is owned by account `1.1.0.2` because the two trailing zeros of the account signal the boundary.

---

### `isthisusersdocument` — Three Implementations, Same Logic

The ownership check is invoked as `isthisusersdocument(tp)` and all three backend variants delegate directly to `tumbleraccounteq`:

- `xumain.c:200`: `return tumbleraccounteq(tp, &taskptrx->account);`
- `socketbe.c:200`: `return tumbleraccounteq(tp, &(player[user].account));`
- `be.c:173`: `return tumbleraccounteq(tp, &taskptrx->account);`

No table lookup, no index, no registry. Pure arithmetic comparison.

---

### Where the Account Tumbler Comes From

The current user's account tumbler is **self-declared** by the client over the FEBE protocol:

`get1fe.c:213-225`:
```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
    gettumbler(taskptr, accountptr)
    && validaccount(taskptr, accountptr);
    player[user].account = *accountptr;
    taskptr->account = *accountptr;
    return(TRUE);
}
```

The client sends an `XACCOUNT` message with its account tumbler. The server stores it in `player[user].account` (defined as `tumbler account` in `players.h:20`) and copies it into the active `task` struct at `bed.c:123`:

```c
task.account = player[user].account;
```

### `validaccount` Always Returns TRUE

`get2.c:157-160` and `get2fe.c:338-341`:
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return(TRUE);
}
```

There is **no server-side validation** of the claimed account. The server accepts whatever tumbler the client sends as its account identity.

---

### The Bert Table Is NOT an Ownership Table

`bert.c:29`:
```c
static conscell *berttable[NUMBEROFBERTTABLE];
```

The `berttable` hash table (1327 buckets) tracks **open documents** (active read/write locks per connection), not ownership. Each `bertentry` records `{connection, documentid, type, count}`. It answers "is this document open by this connection?" — not "does this connection own this address space?"

---

### The Ownership Decision Path in `checkforopen`

`bert.c:81`:
```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
}
```

When no bert entry exists for a document and no other connection has it open for write, the fallback is `isthisusersdocument(tp)` — which is pure tumbler prefix matching against `task.account`. That's the entire ownership model.

---

### Summary

Ownership is **entirely structural**: a document tumbler is owned by whoever's account tumbler is a prefix of it, as computed by `tumbleraccounteq`. There is no ownership registry, no ownership table, no server-side mapping. The account tumbler is self-reported by the client via the `XACCOUNT` FEBE message, and `validaccount` accepts it unconditionally. The granfilade (`granf`) tracks document addresses, and the bert open-table tracks session locks — but neither serves as an ownership ledger. Ownership falls directly out of the tumbler's numeric structure.

---

## Question 12 [gregory]

> In `makehint`, what exact predicate determines whether the current session "owns" the source document — is it a tumbler prefix match between the session's account address and the document's I-address, or something else?

### Gregory's Answer

## KB Synthesis

The ownership predicate is a conjunction of two checks, not a single predicate:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

**`tumbleraccounteq(isaptr, wheretoputit)`** — yes, this is an account-level prefix match. `isaptr` is the source document's I-address; `wheretoputit` is the session's current account address. The function extracts and compares the account component of the document address against the session account. So it checks: does this document's address fall under the current session's account? [SS-VERSION-ADDRESS, Finding 0068]

**`isthisusersdocument(isaptr)`** — a secondary predicate confirming the document belongs to the current user. The KB doesn't detail its implementation, but it's applied conjunctively with the prefix match.

Both must be true for the "owned" path (`makehint(DOCUMENT, DOCUMENT, ...)` → version under source document). If either fails, the "unowned" path is taken (`makehint(ACCOUNT, DOCUMENT, ...)` → version under session's account). [ST-VERSION-OWNERSHIP]

The KB characterizes this as "account prefix matching, not an explicit permissions table" — the tumbler address hierarchy encodes ownership structurally. An explicit ACL table plays no role. [SS-TUMBLER-CONTAINMENT, ST-VERSION-OWNERSHIP]

One caveat: the KB notes `wheretoputit` in the code without fully specifying how the session's account address is materialized into that variable. It's reasonable to infer it's the session's currently-set account (from `SETACCOUNT`), but the KB doesn't confirm this at code level for the `wheretoputit` argument specifically.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Answer: The ownership predicate in `makehint`

### Short answer

`makehint` itself contains **no ownership test**. It is a pure structure initializer. The ownership predicate lives in the *callers* — specifically in `docreatenewversion` [`do1.c:270`] — and it is a **tumbler prefix match**, implemented by `tumbleraccounteq`. But the match is not a simple prefix: it is a match up to the point where the account tumbler's mantissa terminates (two consecutive zero slots), while the document's mantissa may continue freely beyond that boundary.

---

### `makehint` itself — `do2.c:78–84`

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

`makehint` does exactly four things: writes three type integers into a `typehint` struct, then copies the ISA tumbler into `hintptr->hintisa` via `movetumbler`. There is no conditional, no comparison, no ownership check anywhere in the function body.

---

### Where the ownership decision actually lives — `do1.c:268–276`

The only caller that performs an ownership test before choosing which `makehint` call to make is `docreatenewversion`:

```c
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

The branch taken determines the `supertype` passed to `makehint`:

- **Own document** → `supertype = DOCUMENT, subtype = DOCUMENT` (version within the same document)  
- **Someone else's document** → `supertype = ACCOUNT, subtype = DOCUMENT` (new document under the session's own account)

The guard is a **conjunction of two predicates**:

1. `tumbleraccounteq(isaptr, wheretoputit)` — the source document and the target address are in the same account  
2. `isthisusersdocument(isaptr)` — the source document belongs to the current session's account

---

### The actual predicate: `tumbleraccounteq` — `tumble.c:38–70`

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    INT i, j_b;
    if (aptr->sign != bptr->sign) {
        return(FALSE);
    }
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);   /* account terminated → doc is under this account */
            }
            /* first zero: skip mismatch check, doc may continue freely */
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The algorithm:

1. Signs must match.
2. Walk both mantissa arrays in lockstep. The **account** tumbler (`bptr`) is treated as the pattern.
3. When `bptr->mantissa[i] != 0`: the document's mantissa must match exactly at that position — any mismatch returns `FALSE`.
4. When `bptr->mantissa[i] == 0`: this marks a "hole" in the account address. A **second** consecutive zero is the terminator — at that point we return `TRUE` regardless of what the document's mantissa holds beyond.
5. The first zero is not a terminator; the document is allowed to have any value there.

So the predicate is **not** a simple byte-by-byte prefix match. It is: _the document's tumbler shares all non-zero mantissa components with the account tumbler, up to the account's double-zero terminator_. This allows the tumbler encoding of hierarchical account address spaces where zeros are structural separators, not just padding.

---

### `isthisusersdocument` — the session binding

`isthisusersdocument` in the socket server (`socketbe.c:197–201`) is:

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

And in the standalone/batch backends (`be.c:171–175`, `xumain.c:198–200`):

```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &taskptrx->account);
}
```

Both delegate entirely to `tumbleraccounteq`. The `player[user].account` comment annotates a historical bug fix — a previous version used `n_players` (the count) instead of `user` (the current session index), which would have compared against the wrong account.

---

### Summary

The predicate determining whether the session "owns" the source document is:

> **`tumbleraccounteq(document_isa, session_account)`** — returns true iff the document's I-address tumbler begins with the same non-zero mantissa components as the session's account tumbler, continuing until the account tumbler's double-zero terminator is reached. The document may extend further; only the non-zero prefix of the account is required to match exactly.

It is not a plain prefix match on raw bytes. It is an account-aware prefix match that treats each zero in the account mantissa as a structural boundary marker, and requires a **second zero** to confirm termination before declaring the document belongs to the account.

---

## Question 13 [gregory]

> Does ownership of a node-level tumbler (e.g., `1.1`) automatically confer ownership of all descendant tumblers beneath it (accounts `1.1.0.x`, documents `1.1.0.x.0.y`), or is each level independently assigned?

### Gregory's Answer

## KB Synthesis

The KB does not fully answer this question, but provides partial evidence.

## What the KB says

**Ownership is checked at the account level, not node level.**

[SS-VERSION-ADDRESS] (Finding 0068) describes the ownership predicate as:
```
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```
where `wheretoputit` is the session's current account address. This comparison is account-scoped — it checks whether the document's account prefix matches the session's active account. There is no mention of node-level (`1.1`) ownership as a separate concept.

**Address hierarchy is structural, not access-control.**

[SS-TUMBLER-CONTAINMENT] and [SS-ADDRESS-SPACE] describe containment (prefix matching via `tumblertruncate` + `tumblereq`) as the mechanism for address hierarchy — e.g., `1.1.0.2.0.1` is *under* `1.1.0.2`. This is used for allocation bounds, not for access grants.

**Account isolation is enforced per-account, not per-node.**

[INV-ACCOUNT-ISOLATION] states documents allocated under one account must have addresses that are proper descendants of that account's address. The unit of isolation is the account (e.g., `1.1.0.2`), not the node (`1.1`).

**Access control is tracked per-document, per-connection.**

[SS-BERT] (Finding 0014) records access at the `(connection, document)` granularity — not at the node or account level.

## What the KB cannot answer

The `isthisusersdocument` function is cited in [ST-VERSION-OWNERSHIP] but not defined in the KB. Whether this function checks node-level containment (i.e., whether owning `1.1` confers ownership of `1.1.0.2.0.1`) cannot be determined from available findings.

**The KB does not describe node-level tumbler ownership as a concept.** The node address (`1.1`) appears only as the top of the hierarchy; the KB's access control entries all operate at account and document levels. Whether `1.1` ownership is independently assigned or derived from higher-level authority is not answerable from this KB.

---

## Code Exploration

I now have everything needed to answer the question definitively. Here is the full analysis:

---

## Tumbler Ownership and Descendant Inheritance in udanax-green

### Short Answer

**Yes**, ownership of a node-level tumbler (e.g., `1.1`) automatically confers ownership of all descendant tumblers beneath it. Each level is **not** independently assigned — ownership is purely hierarchical, determined entirely by a prefix-matching algorithm encoded in `tumbleraccounteq`.

---

### The Ownership Check Chain

Every ownership decision in the backend traces through two functions:

**1. `isthisusersdocument` — the ownership predicate**

Three implementations exist (for different runtime modes), all semantically identical:

- `socketbe.c:197-201`: `return tumbleraccounteq(tp, &(player[user].account));`
- `be.c:171-176`: `return tumbleraccounteq(tp, &taskptrx->account);`
- `xumain.c:198-201`: `return tumbleraccounteq(tp, &taskptrx->account);`

The user's identity is encoded in a single tumbler — the "account tumbler" stored in `player[user].account` (set by `xaccount` via `getxaccount` in `get1fe.c:213-226`). This is an arbitrary tumbler provided by the client; `validaccount` (`get2fe.c:338-341`) always returns `TRUE` — there is no validation.

**2. `tumbleraccounteq` — the core algorithm**

`tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    // bptr = account tumbler (the "owner")
    // aptr = document tumbler being tested
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  // two zeros = end of account space → document is owned
            }
            // first zero: skip (account boundary separator)
        } else {
            // non-zero: document must match exactly
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The algorithm is a **prefix matcher with a double-zero terminator**. The account tumbler's mantissa is scanned; when **two consecutive zeros** are encountered, the function returns `TRUE` unconditionally — meaning all remaining digits of the document tumbler are irrelevant. The document is owned.

---

### How the Tumbler Hierarchy Encodes Levels

From `xanadu.h:140-143`:
```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

Zeros act as level separators in the mantissa array. The address space structure is:

| Level    | Example address | Mantissa layout         |
|----------|-----------------|-------------------------|
| Node     | `1.1`           | `[1, 1, 0, 0, ...]`     |
| Account  | `1.1.0.1`       | `[1, 1, 0, 1, 0, 0, ...]` |
| Document | `1.1.0.1.0.1`   | `[1, 1, 0, 1, 0, 1, 0, 0, ...]` |

---

### Node `1.1` Owns Everything Beneath It

Trace `tumbleraccounteq` with:
- `bptr` = node `1.1` → mantissa `[1, 1, 0, 0, ...]`
- `aptr` = document `1.1.0.1.0.3` → mantissa `[1, 1, 0, 1, 0, 3, ...]`

```
i=0: bptr[0]=1, aptr[0]=1 → match (j_b=0)
i=1: bptr[1]=1, aptr[1]=1 → match (j_b=0)
i=2: bptr[2]=0 → j_b=1 (first zero, skip)
i=3: bptr[3]=0 → j_b=2 → return TRUE  ← triggered immediately
```

The double-zero in the node tumbler fires at positions 2–3 before any account or document digits are examined. **Every tumbler that begins with `1.1` is owned**, regardless of what follows.

---

### Account `1.1.0.1` Owns Only Its Documents

Trace with:
- `bptr` = account `1.1.0.1` → mantissa `[1, 1, 0, 1, 0, 0, ...]`
- `aptr` = document `1.1.0.1.0.3` → mantissa `[1, 1, 0, 1, 0, 3, ...]`

```
i=0: bptr[0]=1, aptr[0]=1 → match
i=1: bptr[1]=1, aptr[1]=1 → match
i=2: bptr[2]=0 → j_b=1 (skip)
i=3: bptr[3]=1, aptr[3]=1 → match (j_b still 1)
i=4: bptr[4]=0 → j_b=2 → return TRUE
```

And with sibling account `1.1.0.2`'s document:
- `bptr` = `1.1.0.1` → `[1, 1, 0, 1, ...]`
- `aptr` = `1.1.0.2.0.1` → `[1, 1, 0, 2, ...]`

```
i=3: bptr[3]=1, aptr[3]=2 → MISMATCH → return FALSE
```

Account `1.1.0.1` does NOT own documents under `1.1.0.2`.

---

### Where This Check Is Applied

`bert.c:81` — the fallback in `checkforopen` (the document-open access gate):

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;  // allowed to open
}
```

If no bert entry exists for the document (it's not already locked by another connection) and either the request is READ-only or the document is owned, the open is permitted.

`do1.c:270` — `docreatenewversion` uses the same check to decide the address hint strategy:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Own document → allocate under it. Someone else's → allocate under your own account.

---

### No Independent Level Assignment

There is no mechanism to grant or restrict ownership at individual levels below the account tumbler. The account tumbler in `player[user].account` is set once per session via `xaccount` (`fns.c:368`, `get1fe.c:223-224`), and all subsequent ownership checks are derived purely from `tumbleraccounteq` prefix matching against that single stored value.

**Summary:** Ownership cascades downward through the double-zero terminator rule. A node tumbler `1.1` contains two consecutive zeros in positions 2–3 of its mantissa; `tumbleraccounteq` hits them immediately and returns TRUE for any descendant. An account tumbler `1.1.0.x` contains its terminating zeros one level deeper; it owns documents under it but not those under sibling accounts. Each level is **not** independently assigned — the entire hierarchy is implicit in the prefix structure of a single tumbler.

---

## Question 14 [gregory]

> Is there a delegation mechanism where an owner of a tumbler range can grant another account the right to allocate new children within that range — for example, a node operator granting a new user the right to create documents under their allocated account prefix?

### Gregory's Answer

## KB Synthesis

The KB contains no evidence of a delegation mechanism of this kind. Here is what the KB does say about address allocation and access control, and what it leaves silent:

## What address allocation actually checks

[SS-ADDRESS-ALLOC] describes `findisatoinsertnonmolecule` as a pure stateless query-and-increment over the granfilade tree. The allocator's only inputs are:

1. The `hintisa` (parent address) passed by the caller
2. The current maximum address found under that parent in the granfilade

There is no permission predicate of the form "may caller C allocate under prefix P?" The allocator is agnostic to who is asking.

## The only ownership check in the allocation path

[SS-VERSION-ADDRESS, Finding 0068] documents the sole instance where something resembling ownership enters allocation: `CREATENEWVERSION` checks `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` to decide *where* to allocate (under the source document vs. under the creating session's own account). This is a routing decision — it determines which parent address to pass to the allocator — not a gatekeeping decision about whether allocation is permitted at all.

## BERT controls document mutation, not address-space allocation

[SS-BERT, PRE-OPEN-DOC] establishes that BERT tokens govern read/write access to existing documents. BERT has no concept of "right to allocate children under prefix P." Opening a document for WRITE means you can modify its content — it says nothing about whether you can create new documents under its address.

## Account isolation is enforced by allocation, not by permission checks

[INV-ACCOUNT-ISOLATION] notes that documents must be proper descendants of their account's address, and that Bug 0013 showed this was violated by the original allocation algorithm when containment checking was missing. The fix added a prefix-match check to keep allocations within the correct parent range. This is a correctness guard on the allocator itself, not a delegation permission system.

## Conclusion

The KB describes no delegation mechanism. There is no data structure, no operation, and no protocol element that would let account A authorize account B to allocate new addresses within A's tumbler range. The system's session model ([SS-SESSION-STATE]) ties each session to a single current account, and all allocations happen within that account's namespace. Granting another account allocation rights within your prefix would require support that simply does not appear anywhere in the KB.

If such a mechanism existed, it would need to be threaded through `findisatoinsertnonmolecule` as an additional check, or handled at the session/account-setup level before the allocator is invoked. Neither is described.

---

## Code Exploration

## Answer: No Delegation Mechanism in udanax-green

**Short answer: No.** There is no delegation mechanism. The system uses strict account-based namespace partitioning with no support for one owner granting another rights to allocate within their tumbler range.

---

### How Ownership Actually Works

Ownership is determined by prefix matching via `tumbleraccounteq()` in `backend/tumble.c:38-70`. An account is a tumbler terminated by **two consecutive zeros** in the mantissa. Any document tumbler whose leading non-zero digits match the account prefix is "owned" by that account:

```c
// backend/tumble.c:58-67
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        if (++j_b == 2) {
            return(TRUE);  /* Account terminated, document is under this account */
        }
    } else {
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);
        }
    }
}
```

The check happens at the `checkforopen()` gate in `backend/bert.c:52-87` via `isthisusersdocument()`, which compares the requested document's tumbler against `player[user].account`.

---

### Access Control Model

`findorgl()` in `backend/granf1.c:22` calls `checkforopen()` before fetching any document. The only paths to success are:

1. The document is open in the BERT table for this connection (`bert->connection == user`)
2. No write-lock exists elsewhere **and** the operation is a read or `isthisusersdocument()` returns true

```c
// backend/bert.c:81
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
}
```

There is no third path — no "granted by owner" check.

---

### New Document Allocation

`docreatenewdocument()` at `backend/do1.c:234-241` always passes `taskptr->account` as the hint for the granfilade allocator:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return createorglingranf(taskptr, granf, &hint, isaptr);
```

`docreatenewversion()` at `backend/do1.c:260-299` makes this even explicit — if you're versioning someone else's document, the new version is forced into **your own** namespace:

```c
// backend/do1.c:268-275
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    /* new version of someone else's document goes under YOUR account */
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

---

### No ACL Structures

The BERT entry in `backend/bert.c:13-24` contains only:

```c
typedef struct {
    int connection;      /* which user has it open */
    tumbler documentid;  /* which document */
    char created, modified;
    int type;            /* READBERT or WRITEBERT */
    int count;
} bertentry;
```

No grantor, no permission flags, no delegation chain. The BERT is a **session lock table**, not an ACL.

---

### Account Assignment

Accounts are set via `xaccount` in `backend/fns.c:364-373`, which calls `getxaccount()` in `backend/get1.c:190-204`. The account tumbler comes directly from the client request with **no validation** that the user is authorized to claim that account — it's a protocol-level assumption. There is no "create user under my prefix" operation anywhere in the FEBE protocol.

---

### Conclusion

The access control model in udanax-green is a simple **namespace partition** scheme:

- Each user has an `account` tumbler (a fixed prefix)
- All documents under that prefix are owned by that user
- No user can allocate in another user's prefix
- There is no way for a user to grant a sub-range to another party
- There are no ACLs, capability tokens, or delegation records anywhere in the codebase

A "node operator granting a new user the right to create documents under their allocated account prefix" would require new protocol operations, a new data structure for delegation records, and changes to the `checkforopen()` / `isthisusersdocument()` ownership chain — none of which exist.

---

## Question 15 [gregory]

> Does the system distinguish between "owns this specific tumbler" and "has allocation rights under this tumbler prefix"? For example, can an account own document `1.1.0.2.0.5` without having the right to create `1.1.0.2.0.6`?

### Gregory's Answer

## KB Synthesis

The KB does not support such a distinction. The system conflates "owns this document" with "holds allocation rights under this account prefix" — they are the same predicate applied at different granularities.

**Account = allocation namespace.** New documents are allocated by `findisatoinsertnonmolecule` with the session's current account as the parent hint [SS-ADDRESS-ALLOC Finding 0021]. The algorithm finds the highest existing child under the account and increments it: if `1.1.0.2.0.5` exists, the next call allocates `1.1.0.2.0.6`. The right to do so flows entirely from the session's current account context, not from any per-document ownership claim.

**Ownership check is prefix-based, not registry-based.** `isthisusersdocument(isaptr)` is used to decide version-allocation strategy — "is the source document mine?" [SS-VERSION-ADDRESS Finding 0068]. This is implemented as `tumbleraccounteq(isaptr, wheretoputit)`: a tumbler-prefix comparison between the document's address and the session's account address. Any document whose address is contained under your account prefix passes this check. There is no separate per-document ownership registry.

**Consequence for your example.** If your session account is `1.1.0.2`, you pass `isthisusersdocument` for *any* document under `1.1.0.2`, and the allocation algorithm will allocate `1.1.0.2.0.6` the next time you create a document. There is no mechanism to hold `1.1.0.2.0.5` without implicitly holding allocation rights to all siblings under `1.1.0.2.0.*`.

**What BERT adds.** BERT [SS-BERT Finding 0014] provides per-document READ/WRITE access control, but this governs *mutation access* to existing documents, not the right to *create new siblings* under an account. A WRITEBERT token on `1.1.0.2.0.5` does not affect whether you can allocate `1.1.0.2.0.6`.

**KB gap.** The KB is silent on whether the bootstrap configuration or any higher-level protocol restricts account membership itself (i.e., preventing a session from calling `account(1.1.0.2)` if it doesn't "own" that account). The allocation and ownership machinery assumes the caller already has legitimate account access; it doesn't model how that access was granted.

---

## Code Exploration

I now have all I need to answer comprehensively.

---

## Answer: Ownership vs. Allocation Rights in udanax-green

**No. The system does not distinguish between "owns this specific tumbler" and "has allocation rights under this tumbler prefix." They are the same thing, implemented by a single predicate.**

---

### The Sole Ownership Predicate: `isthisusersdocument`

All three runtime implementations of `isthisusersdocument` reduce to one call:

- `be.c:173`: `return tumbleraccounteq(tp, &taskptrx->account);`
- `socketbe.c:200`: `return tumbleraccounteq(tp, &(player[user].account));`
- `xumain.c:199`: `return tumbleraccounteq(tp, &taskptrx->account);`

There is no separate "allocation rights" check. The same function gates both **access to existing documents** and **placement of new ones**.

---

### What `tumbleraccounteq` Actually Tests

`tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    // bptr = account tumbler (the "prefix")
    // aptr = document tumbler (the one being tested)
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  // Account terminated, document is under this account
            }
            // First zero: document may continue to sub-address. Skip check.
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

**This is a prefix match, not an exact match.** The account tumbler terminates when two consecutive zeros appear. Any document whose mantissa matches the account's non-zero digits up to that terminator is considered "owned" by that account. The document's mantissa may continue arbitrarily beyond that point.

So if your account tumbler represents `1.1.0.2`, then *both* `1.1.0.2.0.5` and `1.1.0.2.0.6` return TRUE — they are both "your documents" under identical logic.

---

### How Ownership Gates Access

`bert.c:52-87`, `checkforopen`:

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;  // document can be opened
} else {
    return -1;  // must create new version
}
```

The open-state table (`bert.c:37-50`) shows that for an unregistered document, `isthisusersdocument` is the deciding factor. If TRUE, you may open it. If FALSE and it's a write, you get `-1` (must create new version).

There is no additional "may create siblings" check at any level.

---

### How New Document Allocation Works

`do1.c:234-241`, `docreatenewdocument`:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

The hint's `hintisa` is `taskptr->account` — the current user's account tumbler. `granf2.c:203-241`, `findisatoinsertnonmolecule`, then searches for the **highest existing document under that prefix** and increments it:

```c
// If something already exists under hint prefix:
tumblertruncate(&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```

So `1.1.0.2.0.1`, `1.1.0.2.0.2`, ..., `1.1.0.2.0.5`, `1.1.0.2.0.6` are all sequentially allocated under the same account `1.1.0.2`. The counter is implicit in the enfilade — whatever already exists at that level, the next allocation increments past it.

---

### The `docreatenewversion` Branch

`do1.c:270-278`:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);  // version under same doc prefix
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // new doc under account
}
```

Both conditions use `tumbleraccounteq` / `isthisusersdocument` — the same prefix test — to decide whether the new version falls under the existing document's sub-address space or under the account's top-level document space. No finer-grained authorization concept is consulted.

---

### Direct Answer to the Example

> Can an account own document `1.1.0.2.0.5` without having the right to create `1.1.0.2.0.6`?

**No.** Here is why:

If your account tumbler is `1.1.0.2`, then `tumbleraccounteq` returns TRUE for any document starting with `1.1.0.2`. You "own" all of `1.1.0.2.0.5` and `1.1.0.2.0.6` simultaneously. New document allocation calls `docreatenewdocument`, which pins the hint to `&taskptr->account` — so it always creates the next document in your entire account space, including at `.0.6`.

The only way to own `1.1.0.2.0.5` but *not* `1.1.0.2.0.6` would be if your account tumbler were `1.1.0.2.0.5` itself. In that case, `tumbleraccounteq(1.1.0.2.0.6, 1.1.0.2.0.5)` would return FALSE at the `5` vs `6` comparison. But then you also couldn't create `1.1.0.2.0.6` via `docreatenewdocument` — because the new document hint is your account prefix `1.1.0.2.0.5`, and new allocations go under *it* (e.g., `1.1.0.2.0.5.0.1`), not at the same level as it.

**The system has no concept of "leaf ownership without sibling allocation rights."** Ownership *is* a prefix, and a prefix defines both which existing objects you can open and where new objects are allocated. The two are inseparable.
