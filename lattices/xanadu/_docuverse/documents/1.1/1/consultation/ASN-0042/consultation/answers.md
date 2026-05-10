# Consultation Answers — Tumbler Ownership

**Inquiry:** What does it mean to own a tumbler position? How is ownership established, delegated, and structurally determined?
**Date:** 2026-03-15 19:00
**Questions:** 19 (10 nelson, 9 gregory)

---

## Question 1 [nelson]

> Does owning a position in the address space mean exclusive authority over that region, or can multiple users share ownership of the same position?

### Nelson's Answer

## Ownership Is Exclusive Authority

Owning a position in tumbler-space means **exclusive, hierarchical authority** over that region. Nelson's model has no concept of shared ownership at the same address. The architecture enforces this at every level.

### The Hierarchical Delegation Model

Ownership flows downward through the tree by delegation ("baptism"):

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." (4/17)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

Each level delegates exclusively to the next. A server owner assigns accounts; an account owner assigns documents; a document owner assigns versions. At every stage, **one entity controls** the allocation beneath it:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." (4/29)

### Modification Rights Are Sole

Only the owner may alter content at a position:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." (2/29)

This is absolute. Nelson provides no mechanism for granting write access to another user. The editing operations (INSERT, DELETE, REARRANGE, COPY-into) all require ownership of the target document.

### What Ownership Does NOT Control

Ownership is exclusive over the position but **not** over what references it. Publication creates an irrevocable openness to incoming links:

> "Each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." (2/43)

And link ownership is determined by the link's home document, not by what it points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

So Alice exclusively owns her document. Bob exclusively owns his links *about* her document. Neither can touch the other's property.

### Collaboration Through Forking, Not Sharing

When someone wants to modify content they don't own, the system's answer is not "share access" but "fork your own version":

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." (2/45)

The CREATENEWVERSION operation creates a new document (at your address, under your ownership) that transcludes from the original. You now own your version exclusively; the original owner still owns theirs exclusively. There is no shared editing.

### Private Document Access ≠ Shared Ownership

Nelson does mention that private documents can be accessed by "the owner and his or her associates" [2/42]. But this is **read access**, not ownership or modification rights. The designees can see the content; they cannot change it.

### Transfer, Not Sharing

Ownership can transfer — Nelson mentions "someone who has bought the document rights" [2/29] — but this transfers sole authority to a new single owner. There is no mechanism described for joint ownership.

### Summary

| Capability | Owner | Others |
|-----------|-------|--------|
| Modify content | Yes (exclusive) | No — fork instead |
| Allocate sub-positions | Yes (exclusive) | No |
| Withdraw document | Yes (with due process) | No |
| Read (if published) | Yes | Yes |
| Link to (if published) | Yes | Yes |
| Read (if private) | Yes | Designees only |

The address space is a tree of exclusive ownership. Every position has exactly one owner. Collaboration happens through the interplay of independently owned documents — transclusion, linking, versioning — not through shared control of any single position.

---

## Question 2 [nelson]

> Is ownership inherently hierarchical — does owning a position automatically confer ownership of all positions subordinate to it in the address structure?

### Nelson's Answer

## Ownership and Hierarchy in Tumbler Space

The short answer: **allocation authority is hierarchical, but ownership of content is not transitive**. Owning a position gives you the right to *create* subordinate positions, but not to *own* what is created under delegated sub-positions.

### What Nelson Specifies

Nelson establishes two distinct concepts that the question conflates:

**1. Baptism authority (hierarchical)**

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

This is clearly hierarchical. If you own position X, you can create X.1, X.2, X.3 beneath it. No one else can.

**2. Content ownership (follows creation, not hierarchy)**

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Ownership follows *who created*, not *where in the tree*. The owner is the creator, not the parent position's owner.

### The Delegation Boundary

Nelson draws this distinction explicitly at the account level:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

This reveals the pattern:
- The **server operator** allocates account positions (baptizes user numbers)
- But once assigned, the **account holder** has "full control over its subdivision forevermore"
- The server operator cannot reach down into the user's domain

The word "forevermore" is significant — delegation is permanent and irrevocable. The parent cannot reclaim allocation authority once delegated.

### The Four-Field Structure Encodes This

The tumbler address `Node.0.User.0.Document.0.Element` has three zero-delimited boundaries, each representing a delegation point:

| Level | Allocated By | Owned By |
|-------|-------------|----------|
| Node | Parent node operator | Node operator |
| Account | Node operator | Account holder |
| Document | Account holder | Account holder (creator) |
| Element | System (append-only) | Document owner |

Each zero-delimiter marks where authority transfers from one party to another. The server operator baptizes accounts but does not own the documents created under those accounts.

### What About the Server's Relationship to User Content?

The enforcement model makes this explicit through the Storage Vendor contract:

> "Storage Vendor agrees to engage in best efforts for the preservation and privacy of all customer material, and not to breach the confidence of any customer, examining customers' stored materials only as required for the orderly maintenance of the system." [LM 5/14-5/15]

The vendor has *custodial obligations*, not ownership rights. The vendor holds the content but may not examine it except for maintenance. This is the opposite of hierarchical ownership — the higher-level entity (vendor) is *constrained* by the lower-level entity's (user's) rights.

### Versions: The Telling Case

When a user creates a new version of someone else's document:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The new version lives under the *creating user's* account, not under the original document's position. The address indicates ancestry but ownership follows creation. This confirms that the hierarchy tracks *provenance* (where something came from), not *authority* (who controls it).

### Summary

| Question | Answer |
|----------|--------|
| Does owning X let you create X.1, X.2...? | **Yes** — baptism authority is hierarchical |
| Does owning X mean you own X.1? | **Only if you created X.1 yourself** |
| Can the server operator modify user documents? | **No** — contractually prohibited |
| Can delegation be revoked? | **No** — "full control... forevermore" |
| Does the hierarchy encode ownership? | **No** — it encodes provenance and delegation |

The tumbler hierarchy is a *delegation tree*, not an *ownership tree*. Each level delegates creation authority to the next, but delegation is permanent and the delegatee owns what they create. The address tells you the *lineage* of how something came to exist, not who currently controls it.

---

## Question 3 [nelson]

> Is ownership structurally encoded in the address itself, so that inspecting an address reveals its owner, or is ownership a separate association the system maintains?

### Nelson's Answer

## Ownership Is Structurally Encoded in the Address

Yes — ownership is encoded directly in the tumbler address. The User field is one of the four major fields of every tumbler:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

Inspecting any address reveals the account that created it. The User field **is** the owner identifier — not a pointer to a separate ownership record.

## The Baptism Principle

Ownership flows from the address hierarchy itself through "baptism":

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Once you have User account `1.3`, everything under `1.0.3.0.*` is yours. You fork documents beneath your account number. Those documents fork versions. The tree of ownership is the tree of addresses.

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

## Links Follow the Same Rule

For links, ownership is determined by the link's home document — which is itself addressed under the creator's account:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

You can link to anyone's content, but the link lives at **your** address. Inspecting the link's home address reveals who created it.

## No Separate Ownership Metadata

Nelson does not describe a separate ownership table or metadata association. The system doesn't even store explicit "account objects":

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." [LM 4/23]

Accounts are "ghost elements" — positions on the tumbler line with no stored object. Ownership is inherent in the address structure, not in a record that could be queried, modified, or corrupted independently.

## One Caveat: Transfer of Rights

Nelson mentions that a document owner may be "the rightful copyright holder, or someone who has bought the document rights" [LM 2/29]. This implies that legal ownership can transfer (as with any property). But the address remains permanent — the User field always reflects the **originating account**, not necessarily the current legal owner. How ownership transfer would be reflected in the system (a metalink? a contractual record?) is not specified.

NEED_RAW: [2/29-2/30] — to check whether Nelson says anything more about ownership transfer mechanics beyond the brief mention of "bought the document rights."

## Summary

Ownership is **structural, not associative**. The tumbler address encodes provenance permanently. There is no separate "owner" field to update, no metadata to strip, no table to corrupt. The address **is** the proof of origin.

---

## Question 4 [nelson]

> What is the relationship between a user's identity and the positions they own — must each user correspond to a unique, non-overlapping region of the address space?

### Nelson's Answer

## Identity and Address Space Ownership

**Yes — each account corresponds to a unique, non-overlapping region of the address space.** This is not an additional constraint imposed by policy but a structural consequence of the tree-based tumbler addressing.

### The Tree Makes It Automatic

The tumbler hierarchy is a tree:

```
Node.0.User.0.Document.0.Element
```

Each account occupies a subtree. Because subtrees of a tree are disjoint by construction, no two accounts can overlap. The "tumbler line" (the depth-first ordering of the tree) maps each account's subtree to a contiguous, non-overlapping range:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

Ownership flows strictly downward through the tree. The node operator assigns you an account address; everything beneath that address is yours:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

### Account vs. Person: A Critical Distinction

The non-overlapping property holds between **accounts**, not between **persons**. Nelson speaks of numbers owned by "individuals or companies" [LM 4/17]. This means:

- **One person, multiple accounts**: A person can hold accounts on different nodes, each a separate non-overlapping region. Nothing in the specification prevents this.
- **One account, multiple persons**: A company or organization is a single account owner but represents many people. Sub-accounts can be delegated: "accounts can spin off accounts" [LM 4/19].
- **Sub-delegation**: An account holder can subdivide their space and delegate sub-accounts to others. The sub-accounts remain within the parent's subtree — still non-overlapping with accounts outside it.

### Ownership vs. Reference

The non-overlapping constraint applies to **where content lives** (I-space addresses), not to **what content references**. Links and transclusions freely cross ownership boundaries:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

When you transclude content from another user's document, that content stays at its original I-address (in the other user's subtree). Your document's V-space references it; your I-space does not absorb it. The address tells you who created it:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### Why This Matters

The identity-address binding serves three purposes:

1. **Ownership is structural, not metadata.** The User field of any I-address IS the owner. You cannot forge ownership because you cannot create content at someone else's address — you can only create content under your own account's subtree.

2. **Attribution is unforgeable within the system.** Origin traceability follows from the address structure: every byte's I-address encodes which account created it.

3. **Decentralized coordination.** No central authority allocates addresses globally. Each owner subdivides their own space independently: "all numeration in the docuverse is compressed into a single mechanism" [LM 4/19]. The tree structure guarantees non-collision without coordination.

### Summary

Each account maps to a unique subtree — and therefore a unique, non-overlapping region — of tumbler space. This is inherent in the tree structure, not a rule that must be enforced. A person may own multiple accounts (multiple disjoint regions), and an account may represent multiple people, but the account-to-region mapping is always one-to-one and non-overlapping. Content lives exclusively in its creator's region; references (links, transclusions) cross regions freely.

---

## Question 5 [nelson]

> Can ownership of a position be permanently transferred from one user to another, or is the original assignment irrevocable?

### Nelson's Answer

## Ownership Transfer in Xanadu

Nelson's text reveals a **deliberate separation** between the permanent address (which encodes origin) and the ownership of rights (which he implies can transfer). But he specifies no mechanism for the transfer itself.

### Evidence That Transfer Is Contemplated

The clearest statement is from 2/29:

> "Every document has an owner, the person who created and stored it **(or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights**... Only the owner has a right to withdraw a document or change it." [LM 2/29]

The parenthetical is significant. Nelson explicitly names two cases where the owner is NOT the person who typed the words:

1. A publishing company that "arranged" creation
2. Someone who "bought the document rights"

Both imply ownership can originate with or transfer to a different party than the creator.

### But the Address Is Irrevocable

The tumbler address permanently encodes the originating account:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The I-space address structure is `Node.0.User.0.Document.0.Element` [LM 4/26]. The User field is baked into the permanent address. If user 3 creates a document at `1.0.3.0.5`, that address cannot become `1.0.7.0.5` after a sale to user 7. The address tells you where content was *born*, not who currently holds the rights.

This means the **address encodes provenance, not current ownership**. The system must track current ownership separately from the address — presumably in what Nelson calls "the user's system area, along with passwords and accounting information" [LM 5/13].

### What Is NOT Specified

Nelson provides no mechanism for:

- How ownership transfer is recorded in the system
- Whether the original account holder retains any residual rights
- How royalty routing changes after transfer (the "cash register" lives at the document, but who collects?)
- Whether transfer of a document also transfers the right to fork sub-addresses under it
- Whether an entire account (the User field and everything below it) can be transferred

### The Tension

There is an unresolved tension between two principles:

| Principle | Implication |
|-----------|-------------|
| **Permanent addresses** | The User field in the tumbler forever says "created by account X" |
| **Transferable ownership** | "Someone who has bought the document rights" is the owner |
| **Origin traceability** | "You can at once ascertain the home document of any specific word or character" [LM 2/40] |

Origin traceability survives transfer — it traces to the *document*, not the *owner*. The I-address always tells you which document created the bytes. But if ownership transfers, the User field in that document's address no longer identifies the current owner. The address becomes a historical record ("created under this account") rather than a current authority record ("owned by this account").

### My Assessment as Designer

The address assignment is irrevocable — that is structural and absolute. But **ownership of the rights to a document** (modification, withdrawal, royalty collection) is transferable. I said as much when I mentioned "someone who has bought the document rights."

The address is like a birth certificate — it records where something originated. Ownership is like a deed — it records who currently holds the rights. These are different things, and the system needs both. I did not specify the deed mechanism in detail, which is a gap in the specification.

NEED_RAW: [2/29-2/31, 5/19-5/21] — The full text of the ownership section and the publication agreement may contain additional detail about transfer mechanics or constraints that the curated extracts abbreviate.

---

## Question 6 [nelson]

> Can an owner delegate partial authority over a subregion to another user while retaining ownership of the larger region?

### Nelson's Answer

Let me check some key pages to verify what Nelson says about ownership delegation at different levels of the hierarchy.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-184.png</file_path>
</parameters>
</tool_call>
<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-187.png</file_path>
</parameters>
</tool_call>
<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-109.png</file_path>
</parameters>
</tool_call>

---

## Answer: Delegation in the Tumbler Hierarchy

Nelson's design supports delegation **at the address-space level** (nodes, accounts, sub-accounts) but does **not** support partial authority **within a document**. Ownership of a document is absolute and indivisible.

### What IS Specified: Address-Space Delegation via Forking

The tumbler hierarchy is fundamentally a delegation mechanism. An owner of a number can "bestow" sub-numbers on others:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

And specifically for accounts:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

This means an account owner **can** create sub-accounts and grant them to other users. Those sub-users then own their sub-accounts fully and create documents within them. The parent account holder delegated the *address space*, and the child owns everything created within it.

### What IS Specified: Document Ownership Is Absolute

At the document level, there is no partial authority:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Nelson's access model is binary: you own the document (full control) or you don't (read-only for published, no access for private unless you're a designee). The session model analysis confirms:

- No access control lists — only owner/designees/everyone
- No read vs. write modes — you own it (modify freely) or you don't (create a version)
- Modification requires ownership — only the owner may insert, delete, rearrange, or copy-into

There is no mechanism described for "User A may edit bytes 500-1000 of this document but not bytes 1-499."

### What IS Specified: The "Designee" Concept

For **private** documents, the owner can designate others who may **read** (not write):

> "A private document may be read and linked-to only by the owner and his or her associates." [LM 2/42]

This is read delegation, not write delegation.

### The Intended Workaround: Versioning by Inclusion

Nelson's answer to "I want to modify someone else's work" is not delegation — it's **forking**:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

If you cannot modify the original, you create your own version that transcludes the parts you keep and adds your modifications. The original remains untouched. This is explicit in the session model: "Writing always succeeds — if you cannot modify the original, you create a version."

### Summary

| Level | Can You Delegate? | Mechanism |
|-------|-------------------|-----------|
| **Node → Account** | Yes | Node owner bestows account addresses |
| **Account → Sub-account** | Yes | Account owner subdivides and bestows |
| **Document (whole)** | No partial delegation | Owner has absolute control |
| **Document (subregion)** | Not specified | No mechanism exists |
| **Read access (private docs)** | Yes | Owner designates associates |

Nelson designed a system where ownership is **per-document and absolute**, and the remedy for non-owners is **versioning, not delegation**. The forking mechanism handles collaborative evolution at the document boundary: you don't edit my document, you create your own that references mine.

### What Nelson Does NOT Address

Nelson does not discuss:
- Collaborative editing of a single document by multiple users
- Granting write access to specific document regions
- Shared or committee ownership
- Transfer of document ownership

These gaps are consistent with his vision of documents as individually authored works in a literary tradition, not collaboratively edited artifacts. The "ongoing braid" metaphor [LM 2/14] describes a single author's evolving work, not a shared workspace.

NEED_RAW: [2/30-2/31] — The curated sources quote 2/29 and 2/31 but pages 2/30-2/31 may contain additional detail about ownership transfer or delegation that the extracts don't capture.

---

## Question 7 [nelson]

> If delegation is possible, what structural constraints govern how an owner may partition their region among delegates?

### Nelson's Answer

## Structural Constraints on Tumbler Delegation

Nelson specifies a small but precise set of constraints on how owners partition their address regions. The constraints are architectural — they fall out of the tumbler design rather than being imposed as policy.

### 1. Downward Only (Tree Containment)

Delegation is strictly hierarchical. You can only create addresses *under* addresses you own:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

You cannot create sibling addresses, ancestor addresses, or addresses in someone else's subtree. Your entire delegatable region is the subtree rooted at your own address.

### 2. Sequential Creation

New sub-addresses are created as successive integers:

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

This implies allocation proceeds in order — you baptize 2.1, then 2.2, then 2.3. The numbering is a creation-order sequence, not an arbitrary assignment.

### 3. Field-Semantic Level Constraints

The four major fields (Node, User, Document, Element) define what kind of entity each forking level creates:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

The word "respectively" is doing significant work. A node owner forks to create sub-nodes or accounts. An account owner forks to create documents. A document owner forks to create versions. The semantic level constrains what forking *means* at each position.

The cross-level delegation chain:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

### 4. Permanence (No Reallocation)

Once created, an address cannot be reassigned, reused, or reorganized:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This means delegation is irrevocable. If you assign sub-region 3.5 to a delegate, you cannot reclaim it, renumber it, or give it to someone else. The tree only grows; it never reshapes.

### 5. Contiguity on the Tumbler Line

Each owner's region forms a contiguous range on the tumbler line. This is a mathematical consequence of the depth-first tree-to-line mapping, not an explicit rule:

> "In a sense the tumbler line is like the real line... But the tumbler line is a different kind of abstraction from the real line. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

Because every subtree maps to a contiguous span, an owner's delegatable region can be expressed as a single span. This is what makes span-based searching and addressing efficient.

### 6. Owner's Full Discretion Within Their Region

Within these structural constraints, the owner has complete freedom:

> "Subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

And once assigned an account, the user's autonomy is permanent:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

### 7. Recursive Delegation

Delegation is inherently recursive. A delegate who receives a sub-region becomes the owner of that region and can further subdivide it without permission from the parent:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

### What Nelson Does NOT Constrain

- **No capacity limits** per region — each digit has "no upper limit" [LM 4/19]
- **No depth limits** — forking can continue indefinitely
- **No categorization requirement** — "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]
- **No semantic constraint on version numbering** — "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

### Summary

The constraints form a compact set: **downward, sequential, permanent, semantically-typed by field, contiguous, and fully autonomous within the allocated region**. This is the minimum needed to ensure global consistency (no address collisions, no coordination required) while preserving local autonomy (owners freely subdivide their regions).

NEED_RAW: [4/20-4/21] — The curated sources cover the main quotes from these pages, but they may contain additional detail about whether sequential allocation is a hard constraint or merely the typical pattern, and whether any exceptions to the "respective" field-semantic delegation are discussed.

---

## Question 8 [nelson]

> Must the system guarantee that every valid position in the address space has a determinable owner at all times, with no orphaned or unowned regions?

### Nelson's Answer

## Yes — Ownership Is Structural, Encoded in the Address Itself

The tumbler address system makes ownership determinable by inspection. Every address has the form `Node.0.User.0.Document.0.Element`, and the **User field IS the owner**:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The forking mechanism guarantees a complete chain of ownership delegation:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Every position in tumbler-space exists on a tree where each node was "baptized" by a parent who owned the level above. The User field of any address tells you the owner. This is not metadata that can be stripped — it is the address itself.

## Ghost Elements Are Owned Too

Even positions where nothing is stored have determinable owners:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

A ghost element at `1.3.0.7.0.42.0.1` has a determinable owner (User 7 on Node 1.3) even though nothing is stored there. The ownership tree covers the entire address space, occupied or not.

## But Nelson Does Not Address Practical Orphanage

While ownership is always **determinable**, Nelson does not guarantee that the owner is always **reachable or active**. Several scenarios create what we might call practical orphanage:

**1. Anonymous publication.** Nelson explicitly allows "John Doe publication" — anonymous, walk-in users [LM 2/60]. The address still has a User field, but the identity behind it is unknown. Nelson never specifies who exercises ownership rights when John Doe vanishes.

**2. Owner death or disappearance.** Nelson says "Only the owner has a right to withdraw a document or change it" [LM 2/29], but never addresses succession when the owner ceases to exist. The address still encodes ownership; the owner is simply gone.

**3. Storage payment lapse.** Nelson requires "ALL SERVICES MUST BE SELF-SUPPORTING" [LM 4/5] and envisions ongoing storage rental. He does not specify what happens to content — or to ownership — when payment stops.

**4. Vendor failure.** The contract requires "orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16] upon cancellation, but does not address whether ownership transfers or merely persists in its original (possibly unreachable) form.

## The Root Problem

The entire tree descends from server 1:

> "The server address always begins with the digit 1, since all other servers are descended from it." [LM 4/28]

Nelson does not specify who owns the root. Implicitly it is Project Xanadu (the franchisor), but this is never stated explicitly. The ownership chain terminates at a point that is organizationally defined, not structurally specified.

## Summary

**The system guarantees that every position has a determinable owner — yes.** The tumbler address encodes ownership structurally. There are no positions in the address space where you cannot determine who the owner is by reading the address.

**The system does not guarantee that every owner is reachable, alive, or solvent — and Nelson acknowledges this gap only obliquely.** He builds for the optimistic case (honorable participants in a libertarian system) and leaves the pathological cases — death, abandonment, anonymity, insolvency — to what he calls "the printing press of the future" analogy, where such issues are handled socially and legally rather than technically.

The design principle is: **ownership is a fact of the address, not a fact of the world.** The address always tells you who owns it. Whether that person still exists to exercise ownership is a problem Nelson leaves to the contractual and social layers, not the technical architecture.

---

## Question 9 [nelson]

> Must ownership boundaries align with the natural structural boundaries of the address hierarchy, or can ownership be assigned at arbitrary granularity?

### Nelson's Answer

## Ownership Must Align with Structural Boundaries

Nelson's design is explicit: **ownership follows the tree hierarchy of the tumbler address space.** There is no mechanism for assigning ownership at arbitrary granularity independent of structural boundaries.

### The Ownership-Hierarchy Principle

The tumbler system operates on what Nelson calls "owned numbers":

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This creates a strict cascading delegation:

1. **Node owner** → controls account allocation beneath it
2. **Account owner** → controls document allocation beneath it  
3. **Document owner** → controls versions, content, and links beneath it

Each level owns everything structurally subordinate to it.

### The Document Is the Unit of Ownership

Nelson is unambiguous that the **document** is the fundamental ownership unit:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)... Only the owner has a right to withdraw a document or change it." [LM 2/29]

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist." [LM 2/29]

You cannot own byte 500 of someone else's document. You cannot own a span within a document independently of owning the document. The document boundary IS the ownership boundary.

### Sub-Document Ownership Through Transclusion, Not Through Arbitrary Assignment

When multiple authors contribute to a compound document, ownership is preserved through I-space origin, not through sub-document ownership grants:

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "Each compound document is like the other documents: it has an owner and receives royalties." [LM 2/33]

The compound document's owner owns the *arrangement* (V-space). The *content* at each byte traces back to its I-space origin — the document where it was natively created. That native document has its own owner. Royalties split accordingly:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

This is not arbitrary sub-document ownership assignment. It is structural: the I-address encodes the home document, the home document has an owner, and that owner receives royalties for their bytes wherever they appear.

### Links Follow the Same Rule

Link ownership is also structurally determined:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

You own links in your document. You do not own links in other people's documents, even if those links point at your content. Ownership is determined by the link's position in the address hierarchy, not by what it references.

### Achieving Fine-Grained Ownership: Create More Documents

If you need finer ownership granularity, the answer is to create more structural units. Nelson provides two mechanisms:

**Sub-accounts:** The User field is "continually subdividable for sub-accounts" [LM 4/29]. You can delegate sub-account ownership, creating new structural boundaries within your account.

**More documents:** Since "everything in the system is part of a document" and documents can be composed through transclusion, you achieve fine-grained ownership by factoring content into separate documents owned by separate parties, then assembling them through windows.

The account holder retains control over subdivision:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

### Summary

Ownership boundaries **must** align with the address hierarchy. Nelson provides no mechanism for cross-cutting ownership that violates structural boundaries. The system achieves flexible ownership not by allowing arbitrary assignment, but by making it trivially easy to create new structural units (documents, sub-accounts) and compose them through transclusion. The document is the atom of ownership; composition through windowing is the molecule.

---

## Question 10 [nelson]

> What happens to owned positions when the owning user permanently leaves the system — does the design require a succession or inheritance guarantee for those positions?

### Nelson's Answer

## Succession and Inheritance of Owned Positions

**Nelson does not specify any succession, inheritance, or transfer-of-ownership mechanism in Literary Machines.** This is a genuine gap in the specification, and it creates several unresolved tensions with other stated guarantees.

### What IS Specified About Ownership

Ownership is structural and permanent:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Ownership of the address subtree is total:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

That "forevermore" is telling — it assumes continuous ownership, not transfer.

### The Tensions

Three explicit guarantees collide when an owner permanently departs:

**1. Permanence vs. Payment.** Published content must stay published:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

But storage requires ongoing payment from the owner:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

If the owner dies or vanishes, who pays storage rental? Nelson does not say.

**2. Link dependence vs. owner absence.** Others' links create a permanence obligation on the target:

> "Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

But this presumes an author who *could* withdraw — an active agent constrained by the system. When the owner is gone, there is no agent to constrain, and no agent to maintain the content.

**3. Address permanence vs. content accessibility.** Tumbler addresses are permanent, but ghost elements show that addresses can exist without stored content:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them." [LM 4/23]

So the address survives forever, but the content behind it could become inaccessible if storage lapses — and Nelson never specifies a grace period or fallback.

### Partial Mitigations Nelson Does Provide

**Institutional ownership.** Nelson explicitly allows companies to own documents: "the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)" [LM 2/29]. Institutional owners outlive individuals, partially addressing succession through organizational continuity.

**The Author's Fund.** For public domain content (unowned documents), royalty surcharges accumulate in an escrow account for "the charitable funding of worthy causes within the network... subsidies to struggling writers and artists, and other worthy purposes" [LM 5/12]. But this covers *unowned* content, not *abandoned owned* content — these are distinct categories in Nelson's model.

**Vendor transition obligations.** When a *Storage Vendor* fails, the contract requires: "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16]. This handles infrastructure failure but not owner departure.

**Distributed backup.** The BEBE protocol ensures content is replicated across servers: "Material is moved between servers... for redundancy and backup purposes" [LM 4/71]. So copies may persist at other nodes even if the home node loses the owner's account. But Nelson does not address the legal status of these copies when the owner vanishes.

### What Is NOT Specified

Nelson does not address:

- Transfer of document ownership (sale, gift, bequest)
- Transfer of account ownership
- What happens to the subtree when an account owner dies
- Whether accumulated royalties can be inherited
- Whether orphaned published content reverts to public domain
- Whether the Author's Fund or any other mechanism takes custody
- Any "estate" or "executor" concept for digital holdings
- Timeout or lapse mechanisms for abandoned accounts

### Assessment

The omission is consistent with Nelson's general approach — he designs the *conceptual* and *contractual* structures, leaving operational details to implementation. He acknowledges this pattern explicitly:

> "There is no thinking out all these eventualities. But the system we propose is a libertarian system: restrict it, and all will lose." [LM 2/59]

The most likely interpretations:

1. **Nelson assumed institutional ownership would dominate** — publishers, companies, and organizations persist across generations, making individual succession a rare edge case.

2. **Conventional legal inheritance applies by default** — since ownership is contractual (the publication contract is "something very like a credit-card triplicate slip"), standard property law governs transfer on death. The document rights are property rights; they pass through estates like any other intellectual property.

3. **The gap is intentional** — Nelson specifies the invariants (addresses permanent, published content stays published) and leaves the mechanism for maintaining those invariants across owner changes to the franchise and its legal counsel.

The design does **not** require a succession guarantee at the architectural level. Tumbler addresses are permanent regardless of ownership state. Ghost elements prove that addressability survives even when nothing is stored. But the *accessibility* guarantee for published content — the social contract that "a thing once published stay published" — does implicitly require *some* succession mechanism, even if Nelson leaves its form unspecified.

NEED_RAW: [5/1-5/10, 2/29-2/31] — These pages in the business overview and ownership sections might contain additional detail on ownership transfer not captured in the curated extractions.

---

## Question 11 [gregory]

> In the tumbler hierarchy `Node.0.User.0.Doc.0.Element`, is ownership a pure structural predicate — i.e., can the system determine "user U owns tumbler T" solely by comparing tumbler prefixes, without consulting any separate ownership table?

### Gregory's Answer

## KB Synthesis

Yes — ownership is a pure structural predicate. The KB gives enough evidence to conclude this firmly.

## The structural ownership mechanism

From [SS-TUMBLER-CONTAINMENT], the containment primitive is:

```
tumblertruncate(&A, tumblerlength(&B), &truncated);
tumblereq(&truncated, &B);  // TRUE if A is under B
```

This is pure tumbler arithmetic. No table lookup, no side channel.

From [ST-VERSION-OWNERSHIP] / [SS-VERSION-ADDRESS] Finding 0068, the actual ownership check for VERSION is:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

where `wheretoputit` is the current session's account tumbler (stored in per-session state per [SS-SESSION-STATE]).

`tumbleraccounteq` compares the account-component of two tumblers — structural. `isthisusersdocument` checks whether the document falls under the session's account — also structural, given:

- The address hierarchy encodes the owner directly: `1.1.0.2` (account) → `1.1.0.2.0.1` (first doc under that account). [SS-ADDRESS-SPACE] Finding 0021
- Allocation itself is verified by containment check: after `findpreviousisagr`, the result is validated against the parent via prefix truncation. [PRE-ADDRESS-ALLOC]
- No ownership table exists anywhere in the KB — [SS-BERT] is an access-control table for *open sessions*, not an ownership registry

## What makes this work

Because documents are allocated under the owning account's tumbler prefix by construction ([ST-ADDRESS-ALLOC], [SS-ADDRESS-ALLOC]), ownership is encoded at allocation time and readable forever after by prefix comparison. The address space is the ownership table.

## The one caveat the KB leaves open

The internals of `isthisusersdocument` are not fully spelled out — the KB names it but doesn't expand it. However, given:
- No ownership table appears anywhere in the 78-finding KB
- All allocation, validation, and access control uses tumbler comparison or tree search
- The function name aligns with a simple prefix check against session account state

the structural interpretation is strongly supported. If `isthisusersdocument` did anything beyond tumbler prefix comparison, that would be a significant architectural departure that would appear in the KB.

**Answer:** Ownership is a pure structural predicate. `user U owns tumbler T` iff `tumbler_contains(U.account, T)`, implemented via `tumbleraccounteq` and related prefix operations — no separate ownership table exists or is consulted. [SS-TUMBLER-CONTAINMENT], [ST-VERSION-OWNERSHIP], [PRE-ADDRESS-ALLOC], [SS-SESSION-STATE]

---

## Code Exploration

I now have everything needed for a complete answer.

---

## Answer: Ownership Is a Pure Structural Predicate

**Yes.** In udanax-green, "user U owns document T" is determined entirely by comparing tumbler digits — no separate ownership table, registry, or persistent user-to-document mapping is consulted. The check reduces to a single function call on two tumblers.

---

### The Call Chain

**Entry point** — `bert.c:81`:

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
}
```

When a document is not already open by any connection with write access, the system falls through to `isthisusersdocument(tp)`.

---

### `isthisusersdocument` — Three Implementations, One Body

All three backend entry-point files implement the function identically:

**`be.c:171-176`** (single-user backend):
```c
int isthisusersdocument(tumbler *tp)
{
  bool result = tumbleraccounteq(tp, &taskptrx->account);
  return result;
}
```

**`socketbe.c:197-201`** (multi-user socket backend):
```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

**`xumain.c:198-201`** (X-window backend):
```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp,&taskptrx->account);
}
```

Every path leads to `tumbleraccounteq`. No table lookup, no file I/O, no external call.

---

### `tumbleraccounteq` — The Structural Predicate

`tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  INT i, j_b;
  if (aptr->sign != bptr->sign) { return(FALSE); }

  for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
      if (++j_b == 2) {
        return(TRUE);  /* Account terminated, document is under this account */
      }
      /* First zero: document may continue to sub-address, skip mismatch check */
    } else {
      /* Account has non-zero: document must match exactly */
      if (aptr->mantissa[i] != bptr->mantissa[i]) {
        return(FALSE);
      }
    }
  }
  return (TRUE);
}
```

The comment at `tumble.c:53-59` is explicit about the semantics: the account tumbler is treated as a prefix pattern. Its non-zero digits must match the document tumbler exactly at the same positions; a pair of consecutive zeros terminates the account's address space, and whatever follows in the document tumbler doesn't matter. This is exactly the "prefix ownership" implied by the hierarchy `Node.0.User.0.Doc.0.Element`.

---

### `berttable` Is Not an Ownership Table

`bert.c:29`:
```c
static conscell *berttable[NUMBEROFBERTTABLE];
```

This is searched first in `checkforopen` (`bert.c:63-78`), but it is **not** an ownership registry. It is a session-scoped, in-memory hash table that tracks which documents are currently **open** by which connections and in what mode (READ/WRITE). Its contents are created by `addtoopen`, destroyed by `removefromopen` and `exitbert`, and never persisted to disk. It supports locking and copy-on-write versioning, not ownership.

---

### The Account Tumbler Is Self-Asserted

The account tumbler (the "U" side of the comparison) is obtained by reading from the network:

**`get1.c:190-203`** (`getxaccount`):
```c
gettumbler(taskptr, accountptr)
&& validaccount(taskptr, accountptr);
taskptr->account = *accountptr;
return(TRUE);
```

**`get2.c:157-160`** (`validaccount` — the only validation hook):
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return(TRUE);
}
```

`validaccount` returns `TRUE` unconditionally in both implementations (`get2.c:157` and `get2fe.c:338`). No cross-check against any table or registry. The client asserts its own account tumbler and the backend accepts it.

In the single-user `be.c` backend, the account is not even negotiated — it defaults to a hardcoded tumbler (`be.c:37`):
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```
...and is copied directly into the task at `be.c:88`.

---

### Also Used in `docreatenewversion`

The same structural test appears in `do1.c:270`:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    /* This does the right thing for new version of someone else's document */
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

The comment labels this an "ownership test" explicitly. It is resolved purely by tumbler comparison, selecting how the new version's address is allocated in the granfilade.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Is ownership a pure structural predicate? | **Yes** | `isthisusersdocument` calls only `tumbleraccounteq` — no table |
| What is the predicate? | Prefix match: account's non-zero digits must match document at same positions; two zeros terminate account prefix | `tumble.c:38-70` |
| Is there any persistent ownership table? | **No** | `validaccount` returns `TRUE` unconditionally; `berttable` is session-local open-tracking only |
| How is the user's account tumbler established? | Client-asserted, read from wire by `gettumbler`, accepted without verification | `get1.c:190`, `get2.c:157`, `get2fe.c:338` |
| Is the `berttable` an ownership table? | **No** — it tracks open documents for locking/versioning | `bert.c:29`, `addtoopen`, `removefromopen` |

**The system determines "user U owns tumbler T" solely by asking: does the account tumbler U.account, treated as a prefix pattern, match T?** That is the complete ownership check. The tumbler hierarchy is the ownership hierarchy, and the predicate is computable by digit comparison alone.

---

## Question 12 [gregory]

> How is a user's tumbler range initially established on a node — does the node allocate a `Node.0.User` prefix via the same `findisatoinsertnonmolecule` max+1 mechanism used for documents, or is there a separate user-provisioning path?

### Gregory's Answer

## KB Synthesis

The KB does not contain findings that document the user-provisioning path directly. Here is what can be inferred, and where the gap is.

## What the KB documents

The `findisatoinsertnonmolecule` mechanism is described for two cases [SS-ADDRESS-SPACE, Finding 0021]:

| supertype | subtype | depth | Meaning |
|-----------|---------|-------|---------|
| NODE | NODE | 1 | Node under node |
| ACCOUNT | DOCUMENT | 2 | Document under account |
| DOCUMENT | DOCUMENT | 1 | Version under document |

The depth formula is `depth = (supertype == subtype) ? 1 : 2`. The mechanism itself is stateless query-and-increment: compute upper bound from parent address, find the highest existing child via `findpreviousisagr`, increment by 1 [SS-ADDRESS-ALLOC, Finding 0021].

The `makehint` table in the KB shows no `NODE | ACCOUNT` entry — the case that would govern allocating a user's account address (`1.1.0.2`) under a node (`1.1`).

## What can be inferred (not confirmed)

By structural analogy, a `NODE | ACCOUNT` allocation would use depth=2 (different types), which crosses one `.0.` boundary — consistent with the address form `Node.0.User` (e.g., `1.1.0.2`). This would use the same `findisatoinsertnonmolecule` machinery with a hint of type `(NODE, ACCOUNT)`.

However, user provisioning may involve a separate administrative path entirely — not a runtime `findisatoinsertnonmolecule` call triggered by the FEBE protocol, but a bootstrapping or configuration step. The KB contains no findings that observe account creation in action, and no finding covers `init.c` or startup provisioning logic beyond `createenf` for the empty enfilade.

## The honest answer

**The KB cannot answer this question.** The mechanism for establishing `Node.0.User` ranges is outside the scope of findings 0001–0078. To answer definitively, you would need to examine `init.c`, the bootstrap document setup, and any administrative FEBE opcodes that are absent from the current finding set.

---

## Code Exploration

---

## Answer: How User Tumbler Ranges Are Established

**The short answer: there is no server-side user provisioning path.** The backend does not allocate user account tumblers via `findisatoinsertnonmolecule` or any other allocation mechanism. The client asserts its own account tumbler, and the backend stores it unconditionally.

---

### The Provisioning Path (or lack thereof)

#### Step 1 — Process startup: account is zeroed

At startup, `xumain.c:49` calls:

```c
getaccount(&task, &task.account);
```

`getaccount()` in `task.c:28-41` is:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr)
{
  bool validaccount();
  tumblerclear (accountptr);
  return (TRUE);
  /* gettumbler / validaccount was commented out */
}
```

The active code is just `tumblerclear(accountptr)` — the account starts as a zero tumbler. The original interactive-prompt code (`gettumbler` / `validaccount`) is commented out [`task.c:37-40`].

---

#### Step 2 — Client sends XACCOUNT: backend accepts unconditionally

The actual account is set when the client sends an `XACCOUNT` FEBE request. The handler in `fns.c:364-373`:

```c
void xaccount(typetask *taskptr)
{
  bool getxaccount();
  if (getxaccount(taskptr, &(player[user].account))) {
      putxaccount(taskptr);
  } else {
      putrequestfailed(taskptr);
  }
}
```

`getxaccount()` in `get1fe.c:213-226`:

```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
  bool validaccount();
  logstuff = TRUE;
  if (interfaceinput)
      fprintf(interfaceinput, "%d~", XACCOUNT);

  gettumbler(taskptr, accountptr)          // read client-supplied tumbler
  && validaccount(taskptr, accountptr);    // return value DISCARDED
  player[user].account = *accountptr;      // store it unconditionally
  taskptr->account = *accountptr;
  return(TRUE);                            // always succeeds
}
```

Key observations:
- `gettumbler` reads whatever tumbler the client sends over the wire.
- The `&&` expression with `validaccount()` is **a statement whose return value is discarded** — the result is not captured in any variable.
- `player[user].account = *accountptr` is assigned regardless.
- The function returns `TRUE` unconditionally.

`validaccount()` in `get2fe.c:338-341` is itself a complete stub:

```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return (TRUE);
}
```

No validation occurs.

---

#### What `createnode_or_account` actually does

The FEBE handler `createnode_or_account` (`fns.c:375-386`) calls `docreatenode_or_account` (`do1.c:243-258`):

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
  typeisa isa;
  typehint hint;
  tumblercopy(isaptr, &isa);
  makehint(NODE, NODE, 0, &isa, &hint);   // NODE under NODE
  result = createorglingranf(taskptr, granf, &hint, &isa);
  if (result) tumblercopy(&isa, isaptr);
  return result;
}
```

This does invoke `findisatoinsertnonmolecule` — but only for allocating a **NODE under a NODE**. The depth parameter for `NODE→NODE` is `1` (same supertype/subtype, `granf2.c:209`), so the child address is `hint.0.1`, `hint.0.2`, etc.

Critically: there is no `makehint(NODE, ACCOUNT, ...)` anywhere in the codebase. There is no path that allocates an ACCOUNT address via the max+1 mechanism. The "or_account" in the function name appears to be vestigial — the implementation only creates NODEs.

---

### How `findisatoinsertnonmolecule` *is* used (for comparison)

For documents, `docreatenewdocument` (`do1.c:234-241`) uses:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

`depth = 2` (ACCOUNT ≠ DOCUMENT), so the first document under account `1.1.0.1` becomes `1.1.0.1.0.1`, the second `1.1.0.1.0.2`, etc. This is the allocation mechanism the question references — but it **only runs after the account tumbler is already established by the client**.

---

### Summary

| Mechanism | What it allocates | Who drives it |
|---|---|---|
| `findisatoinsertnonmolecule` (depth=2) | DOCUMENT under ACCOUNT | Backend, from client's pre-asserted account |
| `findisatoinsertnonmolecule` (depth=1) | NODE under NODE | Backend, from client-supplied parent hint |
| `XACCOUNT` request path | Account tumbler | **Client asserts its own identity** |
| `validaccount()` | Nothing — stub returning TRUE | No-op |

**The user's account tumbler is entirely client-provided.** The node (server) does not allocate a `Node.0.User` prefix via any mechanism. There is no user-provisioning path — whoever the client claims to be (via `XACCOUNT`), the server believes them. The `findisatoinsertnonmolecule` max+1 mechanism only runs *within* the context of an already-asserted account to allocate documents and structural nodes beneath it.

---

## Question 13 [gregory]

> `makehint` (do2.c:78-84) branches version allocation based on whether the caller "owns" the source document — what exact comparison does it perform to determine ownership, and at which level of the tumbler hierarchy does it match (node, user, or document prefix)?

### Gregory's Answer

## KB Synthesis

The KB has this directly, across two findings.

**The comparison (`do1.c:272-280`):**

```
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

Both conditions must be true for the "owned" path to fire. [SS-VERSION-ADDRESS, Finding 0068]

**What each check does:**

`tumbleraccounteq(isaptr, wheretoputit)` compares at the **account (user) level** — the prefix up to the first `.0.` boundary. For a document at `1.1.0.1.0.1`, the account field is `1.1.0.1`. It asks: does the source document's account prefix match `wheretoputit` (the current session's account)? [ST-VERSION-OWNERSHIP]

`isthisusersdocument(isaptr)` then verifies the document is actually registered under the current session's user, not merely address-compatible. The two checks together close the gap between "structurally under my account" and "actually mine."

**The hierarchy level:**

Account level — one `.0.` boundary deep. From the address table [SS-ADDRESS-SPACE, Finding 0021]:

| Address | Level |
|---------|-------|
| `1.1.0.1` | account |
| `1.1.0.1.0.1` | document under that account |
| `1.1.0.1.0.1.1` | version (child of document) |

The comparison truncates to the account prefix (depth-2 field), not the document prefix. This is why cross-user versioning falls through to the `ACCOUNT` path in `makehint`: if User B (account `1.1.0.2`) tries to version User A's document `1.1.0.1.0.1`, `tumbleraccounteq` sees `1.1.0.1 ≠ 1.1.0.2` and the owned-path condition fails. The version is then allocated under User B's account (`1.1.0.2.0.1`) via `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` with depth=2 — same as a fresh document creation. [SS-VERSION-ADDRESS, Finding 0068; ST-VERSION-OWNERSHIP]

---

## Code Exploration

---

## Answer

`makehint` at `do2.c:78-84` is itself a **pure setter** — it performs no comparison. The ownership branch happens in its caller, `docreatenewversion`, immediately before the two `makehint` calls.

---

### The branch site — `do1.c:268-276`

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

Two conditions must both be true for the "owned" path:

1. **`tumbleraccounteq(isaptr, wheretoputit)`** — source document and destination share the same account prefix
2. **`isthisusersdocument(isaptr)`** — source document belongs to the current user's account

---

### `isthisusersdocument` — `socketbe.c:197-201`

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

It delegates entirely to `tumbleraccounteq`, comparing the document tumbler `tp` against the current user's account tumbler `player[user].account`. (There's a bug note in the comment — the original code used `n_players` instead of `user`, which was wrong.) Identical implementations also appear in `be.c:171-176` and `xumain.c:198-201` for different build targets.

---

### The actual comparison — `tumble.c:38-70`

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    if (aptr->sign != bptr->sign) {
        return(FALSE);
    }
    /* Compare until account (bptr) terminates with two zeros.
       Document (aptr) may continue beyond the account's address space. */
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
            /* First zero in account - skip mismatch check */
        } else {
            /* Account has non-zero - document must match exactly */
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The algorithm:
- Iterates mantissa slots left to right
- For each **non-zero** slot in the account tumbler (`bptr`): the document tumbler (`aptr`) must match exactly — **or return FALSE**
- A zero in the account tumbler means "end of this component" — it is skipped without requiring a match
- When **two consecutive zeros** appear in the account tumbler, the account address has terminated → return TRUE (the document lives beneath this account prefix, regardless of what follows)

---

### What hierarchy level does it match?

The match operates at the **ACCOUNT prefix level** — specifically the account component of the tumbler, which ends at the double-zero terminator. The document tumbler can have arbitrary content beyond that boundary (VERSION, DOCUMENT, sub-address components). Only the account portion must agree.

The first call in the condition — `tumbleraccounteq(isaptr, wheretoputit)` — checks that both the source document and the caller-supplied destination share the same account prefix (i.e., same "owner account"). The second call inside `isthisusersdocument` checks that prefix against `player[user].account`, the currently-authenticated user's own account tumbler.

---

### What each branch does

| Condition | `makehint` call | Effect |
|---|---|---|
| Both true: same account, user owns it | `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` | Allocate new version within the existing document's address space — a true versioning operation |
| Either false: different account, or user doesn't own source | `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` | Allocate a fresh document under the account — mirrors `docreatenewdocument` [`do1.c:239`] |

The asymmetry in the hint type (`DOCUMENT,DOCUMENT` vs `ACCOUNT,DOCUMENT`) controls how `createorglingranf` routes the address allocation — either threading into an existing document's granfilade node or creating a new root entry under the account.

---

## Question 14 [gregory]

> Can a user delegate a sub-range of their tumbler space to another entity — for example, granting `1.1.0.2.0.100` through `1.1.0.2.0.200` to a collaborator — or is address-space authority strictly one level deep (node delegates to user, user delegates to documents, no further)?

### Gregory's Answer

## KB Synthesis

The KB does not describe any sub-range delegation mechanism. Based on what is documented, address space authority is strictly structural and follows the tumbler hierarchy — there is no way to carve out a sub-range and grant another entity allocation rights within it.

**What the hierarchy actually is:**

[SS-ADDRESS-SPACE] (Finding 0021) documents the `makehint` depth table:

| supertype | subtype | depth | Meaning |
|-----------|---------|-------|---------|
| NODE | NODE | 1 | Node under node |
| ACCOUNT | DOCUMENT | 2 | Document under account |
| DOCUMENT | DOCUMENT | 1 | Version under document |

Documents are allocated directly under accounts — there is no intermediate "sub-account" or "delegated range" level in the hierarchy.

**How ownership is determined:**

VERSION allocation (Finding 0068) uses `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` — a binary account-level prefix comparison. You either own the account prefix or you don't. There is no predicate of the form "this entity is authorized over the range `account.0.100` through `account.0.200`."

**What BERT provides instead:**

[SS-BERT] (Finding 0014) provides document-level access control (READBERT / WRITEBERT) over individual documents, not over address ranges. This lets a connection *operate on* existing documents in another account's space, but does not grant the ability to *allocate* new addresses within it.

**Conclusion:**

The KB describes no delegation mechanism. Address space authority follows the structural hierarchy: a session's account context (set per-session, per [SS-SESSION-STATE]) determines where new documents are allocated, and the allocation algorithm ([SS-ADDRESS-ALLOC]) always places new addresses under the current session's account. Granting a collaborator the ability to allocate within `1.1.0.2.0.100–200` would require giving them the account `1.1.0.2` context — there is no finer-grained mechanism documented. Whether such a mechanism *could* be built on top of the tumbler containment predicate [SS-TUMBLER-CONTAINMENT] is a design question, not an implementation fact answerable from this KB.

---

## Code Exploration

I now have everything needed to answer the question. Let me compile the full code-grounded analysis.

---

## Can a User Delegate a Sub-Range of Tumbler Space?

**Short answer: No. The ownership model is structurally capped at one level below the account, and `tumbleraccounteq` — the sole ownership test — cannot represent a sub-range delegation. The `validaccount` function is also an unimplemented stub that returns `TRUE` unconditionally, meaning there is no server-side verification of account identity at all.**

---

### 1. The Account Tumbler IS the Authority Token

Each connected session has a single account tumbler stored in the `PLAYER` struct (`players.h:20`):

```c
typedef struct _player {
    ...
    tumbler account;    /* xanadu host and account tumbler */
} PLAYER;
```

This tumbler is set during the `XACCOUNT` handshake (`get1fe.c:213-226`):

```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
    ...
    gettumbler(taskptr, accountptr) && validaccount(taskptr, accountptr);
    player[user].account = *accountptr;
    taskptr->account = *accountptr;
    return(TRUE);
}
```

Critically, `validaccount` in both `get2.c:157-160` and `get2fe.c:338-341` is a stub:

```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return (TRUE);
}
```

**There is no server-side authentication of account identity.** Any client can claim any account tumbler.

---

### 2. The Ownership Test: `tumbleraccounteq`

`isthisusersdocument` in `socketbe.c:197-201` (and `be.c:171-176`) performs the sole ownership check:

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account) !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

`tumbleraccounteq` in `tumble.c:38-70` compares a document tumbler (aptr) against the session account tumbler (bptr):

```c
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        /* Account has a zero - check if it's the terminator (second zero) */
        if (++j_b == 2) {
            return(TRUE);  /* Account terminated, document is under this account */
        }
        /* First zero in account - document can have any value here */
    } else {
        /* Account has non-zero - document must match exactly */
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);
        }
    }
}
return (TRUE);
```

The algorithm terminates the comparison as soon as it encounters **two zeros in the account tumbler's mantissa**. For account `1.1.0.2` with mantissa `[1, 1, 0, 2, 0, 0, ...]`:

| index | account mantissa | action |
|-------|-----------------|--------|
| 0 | 1 | doc[0] must == 1 |
| 1 | 1 | doc[1] must == 1 |
| 2 | 0 | first zero → j_b=1, skip |
| 3 | 2 | doc[3] must == 2 |
| **4** | **0** | **second zero → j_b=2 → return TRUE** |

The comparison terminates at the second zero — positions 5 and beyond in the document are never examined.

---

### 3. Why Sub-Range Delegation Fails Structurally

The question is whether a sub-range account like `1.1.0.2.0.100` (mantissa `[1, 1, 0, 2, 0, 100, 0, ...]`) could be used to restrict a collaborator to only the range `1.1.0.2.0.100.*`.

Tracing `tumbleraccounteq` with account `1.1.0.2.0.100`:

| index | account mantissa | action |
|-------|-----------------|--------|
| 0 | 1 | doc[0] must == 1 |
| 1 | 1 | doc[1] must == 1 |
| 2 | 0 | first zero → j_b=1, skip |
| 3 | 2 | doc[3] must == 2 |
| **4** | **0** | **second zero → j_b=2 → return TRUE immediately** |
| 5 | 100 | **(never reached)** |

**The digit `100` at position 5 is never checked.** Account `1.1.0.2.0.100` is ownership-equivalent to account `1.1.0.2` — both claim exactly the same set of documents. A collaborator given account `1.1.0.2.0.100` would own all documents under `1.1.0.2`, not just the sub-range.

---

### 4. Document Address Allocation Uses Account as Hint

`docreatenewdocument` (`do1.c:234-241`) places new documents relative to the current session's account:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

In `findisatoinsertnonmolecule` (`granf2.c:203-242`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// ACCOUNT(2) != DOCUMENT(3), so depth = 2
...
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
// First doc under 1.1.0.2 → mantissa[3+2] = mantissa[5] = 1
// Result: 1.1.0.2.0.1
```

If the session account were set to `1.1.0.2.0.100`, documents would be created at `1.1.0.2.0.100.0.1`, `1.1.0.2.0.100.0.2`, etc. — these ARE in the sub-space. But the ownership check would still permit that account to open/modify any document under `1.1.0.2`, not just those sub-addresses. The sub-space confinement for creation is not matched by sub-space confinement for access.

---

### 5. The `CREATENODE_OR_ACCOUNT` Mechanism Does Not Add Delegation

`docreatenode_or_account` (`do1.c:243-258`) uses `makehint(NODE, NODE, ...)`, which allocates sub-nodes with depth=1 (since supertype == subtype). This creates new entries in the granfilade one level deeper than the hint, but it does not establish any delegation relationship. The ownership check is still `tumbleraccounteq`, which cannot represent sub-range authority.

`docreatenewversion` (`do1.c:260-298`) explicitly calls `isthisusersdocument` for its branching logic (`do1.c:270`), but again only at the account level.

---

### 6. The Hardcoded Default Account

`socketbe.c:35` and `be.c:37` define:

```c
// socketbe.c
tumbler defaultaccount = {0,0,0,0,  1,1,0,14,0};  // 1.1.0.14
// be.c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

These are used as fallback accounts. The fact that both implementations use flat three-level accounts (`1.1.0.N`) confirms the design intent: the hierarchy is Node → Account → Documents, with no intended sub-account level.

---

## Summary

The authority model in udanax-green is **strictly one level deep** at the user layer:

```
Node (1.1)
  └── Account (1.1.0.N)         ← one XACCOUNT per session, self-reported, unverified
        └── Documents (1.1.0.N.0.M)  ← owned iff tumbleraccounteq matches
```

**There is no sub-range delegation** because:

1. **`tumbleraccounteq` terminates at the second zero** in the account mantissa — any digits beyond that in a "sub-account" are never examined (`tumble.c:54-68`).
2. A hypothetical sub-range account like `1.1.0.2.0.100` would claim ownership of ALL documents under `1.1.0.2`, not just the sub-range `1.1.0.2.0.100.*`.
3. **`validaccount` is a stub** returning `TRUE` unconditionally (`get2fe.c:338-341`, `get2.c:157-160`), so there is no server-side enforcement of which account a client is entitled to claim.
4. The protocol's `XACCOUNT` request (`get1fe.c:213-226`) simply stores whatever tumbler the client sends; there is no challenge/response or cryptographic binding.

To support sub-range delegation, the codebase would require at minimum: a new ownership predicate that can check sub-range containment (not just the two-zero termination logic), plus server-side verification that the account presented is one the client is authorized to use.

---

## Question 15 [gregory]

> When a user creates a version of a document they do NOT own, the version is allocated under the versioning user's account — does this mean the versioning user now owns that version's entire sub-tree, including the right to create sub-versions and allocate further addresses beneath it?

### Gregory's Answer

## KB Synthesis

Yes — a user who versions an unowned document owns the resulting version and gains full authority over its sub-tree.

## Mechanism

From [SS-VERSION-ADDRESS] (Finding 0068), when the ownership check fails:

```c
makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)
```

This sets `depth=2`, placing the version as a direct child of the creating user's **account** rather than a child of the source document. The result is structurally identical to a fresh document creation under that user's account.

Example from the KB:
- User A's doc: `1.1.0.1.0.1`
- User B (account `1.1.0.2`) versions it → version at `1.1.0.2.0.1`

The address `1.1.0.2.0.1` is a descendant of `1.1.0.2` — User B's account.

## Ownership of the New Version

The ownership check in `docreatenewversion` is:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

When User B subsequently operates on `1.1.0.2.0.1`:
- `tumbleraccounteq` compares the document's account prefix with the current user's account → **match** (both `1.1.0.2`)
- `isthisusersdocument` checks document ownership → **true** (it was allocated under User B's account)

So the owned-document path applies, and sub-versions are allocated as children of the version: `1.1.0.2.0.1.1`, `1.1.0.2.0.1.2`, etc. [SS-ADDRESS-ALLOC, Finding 0068]

## Address Containment = Authority Boundary

From [INV-ACCOUNT-ISOLATION] and [SS-TUMBLER-CONTAINMENT]: account ownership is defined purely by address prefix containment — `contains(account, doc_address)` via tumbler truncation/comparison. Since `1.1.0.2.0.1` and all addresses beneath it are descendants of `1.1.0.2`, they fall entirely within User B's account namespace. The hierarchical address allocation algorithm ([ST-ADDRESS-ALLOC]) will correctly scope all further allocations under `1.1.0.2.0.1` to User B's account, satisfying [INV-ACCOUNT-ISOLATION].

## Practical Implication

The cross-user version severs the address-based lineage chain. User A's version tree is:
```
1.1.0.1.0.1          (User A's doc)
└── 1.1.0.1.0.1.1    (User A's own versions)
```

User B's fork lives separately:
```
1.1.0.2.0.1          (User B's fork of User A's doc)
├── 1.1.0.2.0.1.1    (User B's sub-version)
└── 1.1.0.2.0.1.2    (another sub-version)
```

Content identity is shared (via the text I-address copying in `docopyinternal` [ST-VERSION-CREATE, Finding 0046]), but address lineage is not. `compare_versions` can still detect shared content [SS-COMPARE-VERSIONS], but there is no address-structural relationship linking `1.1.0.2.0.1` to `1.1.0.1.0.1`.

**Summary:** The versioning user owns the cross-user version completely. They can create sub-versions, allocate addresses beneath it, and the entire sub-tree is isolated within their account namespace.

---

## Code Exploration

Now I have everything I need. Let me write the full answer.

---

## Answer: Cross-User Versioning and Sub-Tree Ownership in udanax-green

### The Short Answer

**It depends entirely on which code path created the version.** There are two paths through `docreatenewversion`, and they produce radically different results. The stated premise — that the version lands under the versioning user's account — is **only true in the `doopen` access-control path**, not in the direct FEBE `createnewversion` protocol path. Where the premise does hold, the versioning user gains full recursive sub-tree ownership by the mechanics of tumbler-prefix matching.

---

### Code Path 1: `doopen` (BERTMODECOPY / BERTMODECOPYIF)

**This is the path where the premise holds.**

`bert.c:264–298`:
```c
bool doopen(typetask *taskptr, tumbler *tp, tumbler *newtp, int type, int mode, int connection)
{
   if (mode == BERTMODECOPY) {
       docreatenewversion(taskptr, tp, &taskptr->account, newtp);  // bert.c:274
       addtoopen(newtp, connection, TRUE, type);
       return 1;
   }
   ...
   case BERTMODECOPYIF:
       if (openState == -1) {
           docreatenewversion(taskptr, tp, &taskptr->account, newtp);  // bert.c:290
```

Here, the third argument `wheretoputit` is `&taskptr->account` — **user B's own account tumbler** (e.g., `1.1.0.2`), not the original document's address.

---

### Code Path 2: Direct FEBE `createnewversion`

**This path does NOT place the version under the versioning user's account.**

`fns.c:289–299`:
```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
    if (
       getcreatenewversion (taskptr, &originaldocisa)
    && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))  // fns.c:296
        putcreatenewversion (taskptr, &newdocisa);
```

Both `isaptr` and `wheretoputit` are `&originaldocisa`. The new version is allocated *relative to user A's document address*, not user B's account.

---

### The Branching Logic in `docreatenewversion`

`do1.c:260–298`:
```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    /* ECH 7-13 introduced test for ownership to do right thing for explicit creation
       of new version of someone else's document */
    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
        makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);  // do1.c:271
    } else {
        /* This does the right thing for new version of someone else's document, as it
           duplicates the behavior of docreatenewdocument */
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // do1.c:275
    }
```

The condition at `do1.c:270` gates on two tests:

**`tumbleraccounteq(isaptr, wheretoputit)`** — `tumble.c:38–70`:
> Checks whether `isaptr` falls under the account described by `wheretoputit`, by treating two consecutive zeros in `wheretoputit` as the account-boundary terminator.

**`isthisusersdocument(isaptr)`** — `socketbe.c:197–201`:
```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &(player[user].account));
}
```
> Ownership is purely whether the document's tumbler address has the current user's account as a prefix. **Address IS ownership.**

When user B calls `docreatenewversion` on user A's document:
- Path A (`doopen`): `wheretoputit = &taskptr->account` (user B's account `1.1.0.2`). `tumbleraccounteq(user_A_doc, user_B_account)` = **FALSE** → `else` branch with hint `(ACCOUNT, DOCUMENT, user_B_account)`. New version allocated under user B's account.
- Path B (direct FEBE): `wheretoputit = &originaldocisa = user_A_doc`. `tumbleraccounteq(user_A_doc, user_A_doc)` = **TRUE**, but `isthisusersdocument(user_A_doc)` = **FALSE** → `else` branch with hint `(ACCOUNT, DOCUMENT, user_A_doc)`. New version allocated within user A's document address space.

---

### Address Allocation Mechanics

The hint type determines the depth at which the new address is generated — `granf2.c:209`:
```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

| supertype → subtype | depth | Example |
|--------------------|-------|---------|
| `DOCUMENT, DOCUMENT` | 1 | Self-versioning: `1.1.0.1.0.1` → `1.1.0.1.0.1.1` |
| `ACCOUNT, DOCUMENT` | 2 | New doc under account: `1.1.0.2` → `1.1.0.2.0.1` |

- **Path A** (`doopen`, hint = `ACCOUNT, DOCUMENT, user_B_account`): depth=2, new version = `1.1.0.2.0.1` — under user B's account.
- **Path B** (FEBE, hint = `ACCOUNT, DOCUMENT, user_A_doc`): depth=2, new version = `1.1.0.1.0.1.0.0.1` — inside user A's document's address space.

Finding 0021 and finding 0007 confirm this structure:
> "Original: 1.1.0.1.0.1 / Version: 1.1.0.1.0.1.1" (depth=1 for self-versioning via DOCUMENT,DOCUMENT hint)

---

### Sub-Tree Ownership for Path A (the Premise Holds)

Given user B's copy is at `1.1.0.2.0.1` and user B's account is `1.1.0.2`:

**1. Immediate ownership.** `isthisusersdocument(1.1.0.2.0.1)` calls `tumbleraccounteq(1.1.0.2.0.1, 1.1.0.2)`. The algorithm in `tumble.c:54–69` scans mantissa, matches `1`, `1`, `0`, `2`, then hits two zeros → returns TRUE. User B "owns" the version.

**2. Write access without copying.** `checkforopen` at `bert.c:81`:
```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;  // "not open, but can open"
}
```
When user B tries to write to `1.1.0.2.0.1` and it's not open, `isthisusersdocument` returns TRUE → `checkforopen` returns 0 → `doopen` adds a BERT entry without creating another copy. User B writes in place.

**3. Sub-versioning allocates within the sub-tree.** When user B calls `createnewversion` on their own copy (`1.1.0.2.0.1`):
- `isaptr = wheretoputit = 1.1.0.2.0.1`
- `tumbleraccounteq(1.1.0.2.0.1, 1.1.0.2.0.1)` = TRUE
- `isthisusersdocument(1.1.0.2.0.1)` = TRUE (user B owns it)
- → **TRUE branch**: `makehint(DOCUMENT, DOCUMENT, 0, 1.1.0.2.0.1, &hint)` with depth=1
- Sub-version allocated at `1.1.0.2.0.1.1` — still under `1.1.0.2`

**4. Recursive.** Any address nested beneath `1.1.0.2.0.1` — e.g., `1.1.0.2.0.1.1`, `1.1.0.2.0.1.1.1`, etc. — will satisfy `tumbleraccounteq(addr, 1.1.0.2)` because `1.1.0.2` is a prefix of all of them. Ownership extends to arbitrary depth with no additional mechanism required.

---

### What User A Can (and Cannot) Do to User B's Copy

`checkforopen` for user A trying to access `1.1.0.2.0.1`:
- No BERT entry for user A on this document
- `isthisusersdocument(1.1.0.2.0.1)` with user A's account `1.1.0.1` = FALSE
- For `READBERT`: `!foundnonread && type == READBERT` = TRUE → returns 0 → **user A can open for reading**
- For `WRITEBERT`: `!foundnonread && isthisusersdocument(tp)` = FALSE → returns -1 → **user A must create a new version** (which would land under `1.1.0.1`)

**User A can read user B's copy but cannot write to it without forking again.**

---

### The Path B Anomaly (Direct FEBE, Premise Does Not Hold)

In Path B, user B's "version" of user A's document is allocated at `1.1.0.1.0.1.0.0.1` — inside user A's address space:
- `isthisusersdocument(1.1.0.1.0.1.0.0.1)` for user B = FALSE (prefix `1.1.0.1` ≠ user B's `1.1.0.2`)
- `checkforopen` for user B WRITE → returns -1 → user B cannot write to the thing they just created without triggering another copy
- Sub-versioning by user B would again fork → the chain spirals into user A's address space at increasing depth

This is likely a latent bug or an incomplete code path. The comment at `do1.c:273` says it "duplicates the behavior of docreatenewdocument," but `docreatenewdocument` uses `&taskptr->account` [do1.c:239], not `&originaldocisa`. The direct FEBE path passes `wheretoputit = &originaldocisa`, which is semantically different.

---

### Summary

| Condition | New version address | User B owns it? | Can sub-version? |
|-----------|--------------------|--------------------|------------------|
| Via `doopen` BERTMODECOPY/COPYIF (`wheretoputit = &taskptr->account`) | `user_B_account.0.N` | **Yes** — `isthisusersdocument` = TRUE | **Yes** — recursively under user B's account |
| Via direct FEBE `createnewversion` (`wheretoputit = &originaldocisa`) | `user_A_doc.0.0.N` | **No** — inside user A's space | **No** — would fork again into user A's space |

**Where the premise holds (Path A), the answer is an unqualified yes.** Tumbler-prefix IS ownership. Once an address is allocated under user B's account, all further addresses generated from it (sub-versions, content atoms) inherit that prefix. `isthisusersdocument` returns TRUE for all of them. The versioning user owns the entire sub-tree transitively, to arbitrary depth, with no additional mechanism required and no mechanism available for user A to reclaim it.

The ownership model is not a policy rule enforced by an ACL — it is structural. The tumbler address space *is* the ownership space. Whoever holds the account address holds the namespace.

---

## Question 16 [gregory]

> Is there a structural boundary between "this is my address space" and "this is someone else's" that the backend enforces, or is the ownership boundary purely conventional — could user `1.1.0.2` in principle write a POOM entry under `1.1.0.3`'s document range if no check prevents it?

### Gregory's Answer

## KB Synthesis

The boundary is **structurally weak at the access level and entirely absent at the mutation level**. Here's the breakdown:

## Address Allocation: Structurally Enforced

When *creating* new documents or links, the allocation algorithm in `findisatoinsertnonmolecule` bounds its search to the parent's address range and applies a containment check via `tumblertruncate`/`tumblereq`. Without a passing containment check, the allocator falls back to the correct first-child address. [PRE-ADDRESS-ALLOC], [SS-TUMBLER-CONTAINMENT]

This is real structural enforcement — a session acting as account `1.1.0.2` cannot accidentally (or even intentionally through normal operations) *allocate* a new document address under `1.1.0.3`. Bug 0013 demonstrated exactly this: the pre-fix allocator crossed account boundaries, and the fix added the containment check. [ST-ADDRESS-ALLOC]

## Writing to Existing Documents: Advisory Only

For *accessing and mutating* existing documents, the BERT table is the intended enforcement mechanism. `checkforopen` does distinguish "owned" vs. "unowned" documents and returns -1 (denied) for write requests on unowned documents. [PRE-OPEN-DOC, SS-BERT]

However, this enforcement is architecturally broken in two ways:

**1. Response-before-check:** For INSERT, DELETEVSPAN, REARRANGE, and COPY, the backend sends the success response (`putXXX`) *before* executing the operation (`doXXX`). The BERT check inside `findorgl(..., WRITEBERT)` runs after the front end has already received success. A failing check causes the operation to be silently skipped — but the caller believes it succeeded. [EC-RESPONSE-BEFORE-CHECK]

**2. Protocol trust, not enforcement:** The BERT table is a coordination tool for compliant front ends. A non-compliant front end that acquires a WRITEBERT token without following the protocol, or that submits mutations without a token, cannot be structurally stopped. [INT-BERT-FEBE]

> "The back end trusts the front end to: (1) acquire BERT tokens before mutations, (2) respect write exclusivity, (3) release tokens when done."

## The POOM Specifically

`insertpm` is called from `docopy` only *after* `findorgl` returns true. If `findorgl` returns false (BERT check fails), `doinsert` returns and nothing is written. But this is the honest path. Nothing in the POOM machinery itself checks address-space ownership — it receives a document orgl pointer and writes into it. [SS-POOM-MUTABILITY]

Similarly, `acceptablevsa()` — which was presumably intended to validate V-positions against document structure — unconditionally returns TRUE. There is no subspace check, no account check, nothing. [PRE-INSERT, PRE-SUBSPACE-CONVENTION]

## Summary

| Layer | Enforcement |
|-------|------------|
| Address *allocation* | Structurally enforced via containment check |
| Document *access* (BERT) | Intended but advisory — response-before-check bug breaks it |
| POOM *mutation* | No ownership check at all; relies entirely on front-end compliance |

So yes: user `1.1.0.2` could in principle write a POOM entry under `1.1.0.3`'s document if they bypass BERT token acquisition — the backend would silently accept it (or rather, silently do nothing via the `findorgl` check failing and the response already sent). The system's security model requires trusting the front end. [INT-BERT-FEBE, INV-WRITE-EXCLUSIVITY]

---

## Code Exploration

Now I have the complete picture. Here is the full analysis.

---

## Ownership Boundary Analysis: Structural Enforcement vs. Convention

**Short answer:** There is a real, code-enforced ownership boundary, but it is a *software fence* — not a cryptographic or hardware boundary. It can be bypassed by code paths that pass `NOBERTREQUIRED`, and it is absent entirely in the single-user (xumain) build mode.

---

### 1. How Ownership Is Encoded in the Tumbler Address

The tumbler is a hierarchical address. A user's *account tumbler* (e.g., `1.1.0.2`) is the prefix for all documents they own. The key function is `tumbleraccounteq` in `tumble.c:38`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    // bptr is the account, aptr is the document being tested
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) return(TRUE);  // two zeros = account terminated, doc is under it
            // first zero: doc can have any value here, skip mismatch check
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) return(FALSE);  // must match exactly
        }
    }
    return(TRUE);
}
```

This is a prefix match: the account address terminates with two zeros; any document whose mantissa matches the account's non-zero positions is considered to *belong* to that account. A document with address starting `1.1.0.3` will fail this match against account `1.1.0.2`.

---

### 2. `isthisusersdocument` — The Ownership Predicate

There are three implementations depending on build mode, all equivalent. From `socketbe.c:197`:

```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &(player[user].account));
}
```

And `be.c:171`:

```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

The `player[user].account` tumbler is set at session initialization time. The check is: does the document's address fall under the current user's account prefix?

---

### 3. The BERT Table: The Gatekeeper for Write Access

The BERT (open document registry) is the primary access control mechanism. `checkforopen` in `bert.c:52` is the gate:

```c
int checkforopen(tumbler *tp, int type, int connection)
{
    // ... search the BERT table ...
    
    if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
        return 0;   // not open yet, but can be opened
    } else {
        return -1;  // blocked: someone else has it for write, or not your document
    }
}
```

**[bert.c:81]**: If a document is not in the BERT table, write access (`WRITEBERT`) is only possible if `isthisusersdocument(tp)` is true. Read access is allowed to anyone whose document is not already open for write by another. An attempt to write to a document with address `1.1.0.3` by user `1.1.0.2` falls through to `isthisusersdocument` → `tumbleraccounteq` → **FALSE** → `checkforopen` returns -1.

---

### 4. `findorgl` — Where the Gate Is Applied

Every write operation goes through `findorgl` in `granf1.c:17`, which calls `checkforopen` before touching any data:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {
            return FALSE;   // block the operation
        }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

**[granf1.c:22]**: The guard fires for any `type != NOBERTREQUIRED`. Core operations that use `WRITEBERT`:
- `dorearrange` → `findorgl(..., WRITEBERT)` [do1.c:40]
- `docopy` → `findorgl(..., WRITEBERT)` [do1.c:55]
- `dodeletevspan` → `findorgl(..., WRITEBERT)` [do1.c:164]

---

### 5. New Document Allocation Enforces Ownership By Construction

`docreatenewdocument` [do1.c:234]:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

The hint's `hintisa` is set to the *requesting user's own account*. The enfilade address allocator (`findisatoinsertgr` → `findisatoinsertnonmolecule`) finds the next available slot *within that account's sub-space*. Users have no mechanism to pass someone else's account address as the hint — the `taskptr->account` is taken from the server-managed `player[user]` struct, not from the client.

For `docreatenewversion` [do1.c:260], the ownership check is explicit:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);   // version within same doc space
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // fork into requester's space
}
```

**[do1.c:270–275]**: A new version of *someone else's* document is automatically placed in the requester's *own* account space, not in the original owner's space. This is semantically correct and structurally enforced by where the allocator is told to look.

---

### 6. The Bypass: `NOBERTREQUIRED`

Several internal call paths explicitly opt out of ownership checking:

- `dofinddocscontaining` → `specset2ispanset(..., NOBERTREQUIRED)` [do1.c:21]
- `docopy` → `specset2ispanset(..., NOBERTREQUIRED)` [do1.c:54] (the source document)
- `docreatelink` → `findorgl(..., NOBERTREQUIRED)` [do1.c:213]
- `doretrievedocvspanfoo` → `findorgl(..., NOBERTREQUIRED)` [do1.c:307]
- `docopyinternal` → all calls use `NOBERTREQUIRED` [do1.c:74-80]

These are meant for *internal server operations* where the server itself is acting on behalf of an operation it already authorized. But they represent gaps: if a code path reaches one of these with an attacker-controlled document ISA, no ownership check fires.

---

### 7. The `isxumain` Bypass

**[granf1.c:31–36]**: The `findorgl` check is skipped entirely in single-user (xumain) mode:

```c
if (!isxumain) {
    return FALSE;
}
```

In xumain mode, *all* operations proceed regardless of BERT state or ownership. There is no ownership enforcement in this build mode.

---

### Verdict: Structural, But Not Hardened

| Property | Enforced? | Mechanism |
|---|---|---|
| Address space defined by tumbler prefix | Yes | `tumbleraccounteq` in `tumble.c:38` |
| Write to another user's open document | Blocked | BERT `foundnonread` check, `bert.c:74` |
| Write to another user's unopened document | Blocked | `isthisusersdocument` in `bert.c:81` |
| New doc allocated outside your space | Blocked | `makehint` uses `taskptr->account`, `do1.c:239` |
| New version of foreign doc allocated in their space | Blocked | `tumbleraccounteq` branch in `do1.c:270` |
| Internal operations with `NOBERTREQUIRED` | **Not checked** | Design gap, `granf1.c:22`, multiple sites |
| Single-user (xumain) mode | **Not checked** | `isxumain` bypass, `granf1.c:31` |

**User `1.1.0.2` cannot, through the normal FEBE protocol, write a POOM entry into `1.1.0.3`'s document space.** The chain `findorgl` → `checkforopen` → `isthisusersdocument` → `tumbleraccounteq` would return FALSE at every write operation, blocking it cleanly.

However, the boundary is a *software convention enforced by a gate in `findorgl`*, not an architectural invariant in the enfilade data structures themselves. The enfilade tree has no concept of ownership — it is purely positional. Nothing in `insertpm`, `insertnd`, or the enfilade core would reject an insertion at a foreign address if `findorgl` were bypassed (via `NOBERTREQUIRED` or `isxumain`). The fence lives only at the access-control layer, not in the storage model.

---

## Question 17 [gregory]

> The type namespace lives at `1.0.2.x` — who owns this range? Is it a system-level or node-level allocation that sits outside any user's tumbler prefix, and how is write authority to the type namespace determined?

### Gregory's Answer

## KB Synthesis

The KB has partial but incomplete information on this.

## What the KB says

**The type namespace is in the bootstrap document.** [SS-LINK-ENDPOINT / Finding 0024] establishes that link types are VSpec references into a "type registry in the bootstrap document (doc 1)," with known entries at:

| Type | Address |
|------|---------|
| JUMP | `1.0.2.2` |
| QUOTE | `1.0.2.3` |
| FOOTNOTE | `1.0.2.6` |
| MARGIN | `1.0.2.6.2` |

The hierarchical nesting (`1.0.2.6.2` contained in `1.0.2.6`) uses the same tumbler containment predicate as the document address space — making type subtyping a consequence of address prefix-matching, not a separate mechanism [SS-TUMBLER-CONTAINMENT].

**Address structure.** Per the `.0.` field-divider convention [SS-TUMBLER / Finding 0001], `1.0.2.x` parses as node `1`, separator `0`, entity `2`, sub-addressing at `x`. This places the bootstrap document under node `1` at position `2` — distinct from user account space (which follows the `Node.0.User.0.Doc` pattern).

**Write authority in general.** [SS-BERT / Finding 0014] establishes that any document mutation requires WRITEBERT for that document. [PRE-OPEN-DOC] and [INV-WRITE-EXCLUSIVITY] formalize this: at most one connection holds WRITE access at a time. This applies to the bootstrap document the same as any other.

## What the KB cannot answer

The KB does not contain findings about:

- **Who created the bootstrap document** or under which account it was allocated — the KB has no exploration findings targeting system initialization beyond `createenf()` startup [SS-ENFILADE-TREE / Finding 0058]
- **Whether `1.0.2.x` is node-level (system) or user-level allocation** — the address structure suggests it sits under node `1` rather than under a user account prefix, but this is inference from address anatomy, not from a finding
- **Governance of type namespace extension** — no finding documents whether ordinary sessions can acquire WRITEBERT on the bootstrap document, or whether type registration is restricted to a privileged process

The KB is silent on bootstrap document lifecycle. You'd need an additional discovery session targeting `initenffile()`, the bootstrap document creation code, and the BERT permissions on document `1.0.2` to answer the ownership and write-authority questions definitively.

---

## Code Exploration

I now have everything needed for a complete answer.

---

## The `1.0.2.x` Type Namespace: Full Analysis

### What it is

`1.0.2.x` is **not a global tumbler prefix**. It is a set of **local V-addresses within document `1.1.0.1.0.1`** (the bootstrap document — the first document under the default account). The C backend has zero hardcoded references to `1.0.2` anywhere in the source.

The definition lives entirely in `febe/client.py:597-612`:

```python
# Link type addresses - types are in document 1's link subspace (0.2)
# Full address format: 1.1.0.1.0.1.0.2.X where X is the type number
# Local address within doc: version.0.link_subspace.type = 1.0.2.X
LINK_TYPES_DOC = Address(1, 1, 0, 1, 0, 1)  # Bootstrap doc
JUMP_TYPE      = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 2),     Offset(0, 1))])
QUOTE_TYPE     = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 3),     Offset(0, 1))])
FOOTNOTE_TYPE  = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6),     Offset(0, 1))])
MARGIN_TYPE    = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6, 2),  Offset(0, 1))])
```

---

### Address decoding

**Text subspace** in a document runs at V-positions `>= 1.0`, established by `do1.c:394-395`:

```c
tumblerclear(&text_subspace_start);
tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start);  // = 1
```

**Link subspace** starts at V-position `2`, established by `orglinks.c:36-37`:

```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);  // = 2
```

So V-positions `1 ≤ V < 2` are text subspace; `V ≥ 2` are link subspace. V-address `1.0.2.X` has first digit `1`, so it falls inside the **text subspace** (not link subspace, despite the comment). These addresses sit in a conventional gap: real text starts at `1.0.1` (from `findvsatoappend` → `orglinks.c:42-43`), while these type-identifier addresses sit at `1.0.2.X` sub-positions that are never populated by normal content.

The comment in `client.py:603` cross-references `2.X` positions as "version.0.link_subspace.type = 1.0.2.X" — meaning `1.0.` is a version-level prefix prepended to the raw link-subspace slot `2.X`. This is a naming convention, not a mechanical derivation from the POOM structure.

---

### Who owns this range

Ownership flows from document ownership. The range has no independent owner in the global tumbler tree — it is entirely contained within document `1.1.0.1.0.1`, which is under account `1.1.0.1`:

```c
// be.c:37
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

At startup `be.c:88` copies `defaultaccount` into `task.account`. Document creation uses `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` (`do1.c:239`), so the first document gets allocated under `1.1.0.1` → ISA `1.1.0.1.0.1`.

There is no node at `1.0` in the standard addressing hierarchy. The `1.0` prefix in `1.0.2.x` is artificial — it is not the address of any node, account, or document in the global tumbler tree.

---

### System-level or node-level?

**Neither.** This is a **client-level convention**, and purely so:

- No C source file contains `1.0.2` as a constant or address range.
- `init.c` (the backend initialization) sets up request handlers but creates no bootstrap document and no type registry.
- `rcfile.c` reads runtime config but does nothing with type addresses.
- The C backend never enforces or inspects the type address range. Any VSpec is accepted as the third endset of a `createlink` call.

The convention is analogous to how `1.X.0.Y.0.Z` is interpreted as node.account.document in the global space: a useful semantic model layered onto raw tumbler ordering, but the backend only cares about tumblers as ordered identifiers, not the naming convention they encode.

---

### Write authority

Write authority to the `1.0.2.x` range = write authority to document `1.1.0.1.0.1`. The backend's two-step check:

1. **BERT check** — `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)` in `do1.c:40, 55` requires an active WRITEBERT entry for the document. `bert.c:63-119` uses a hash table keyed on the document's tumbler.

2. **Account ownership** — `isthisusersdocument` (`be.c:171-176`) calls `tumbleraccounteq(tp, &taskptrx->account)`. However, Finding 0050 ("bert-not-enforced-at-backend") shows BERT enforcement is partial.

In practice, because no initialization code bootstraps the type registry document, the `1.0.2.x` addresses contain no content. When a type VSpec like `VSpec(LINK_TYPES_DOC, [Span(1.0.2.2, Offset(0,1))])` is used as a link's third endset, `docreatelink` calls `specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)` (`do1.c:216`). That function converts V-spans to I-spans via POOM lookup — if no content has been inserted at `1.0.2.2`, the result is empty. Then `insertendsetsinspanf` only stores a type entry when `threesporglset` is non-null (`do2.c:122`):

```c
if (threesporglset) {
    insertspanf(taskptr, spanf, linkisaptr, threesporglset, LINKTHREESPAN);
}
```

So type endsets are silently dropped. This is the root cause of the retrieval failure described in Finding 0024.

---

### Why the type-subtype hierarchy works at all

The hierarchical containment of MARGIN under FOOTNOTE (`1.0.2.6.2` under `1.0.2.6`) is structurally valid because tumbler ordering is lexicographic. Any tumbler query against an interval that contains `1.0.2.6` would also contain `1.0.2.6.2` if the width is large enough, enabling "find all footnote-family links" by a range query. This is the intended semantic — tumbler sub-addressing naturally encodes type inheritance. But realizing it requires actual content at the type addresses and a query that explicitly searches a range rather than exact V-span.

---

### Summary

| Claim | Finding |
|-------|---------|
| `1.0.2.x` is a global tumbler prefix | **False** — it's local to doc `1.1.0.1.0.1` |
| Defined in backend C code | **False** — defined only in `febe/client.py:605-608` |
| System-level allocation | **False** — client convention, no backend enforcement |
| Node-level allocation | **False** — no node at `1.0`; doc is under account `1.1.0.1` |
| Write authority via BERT | **True** — `bert.c` governs writes to doc `1.1.0.1.0.1` |
| Types work for link retrieval | **False** — bootstrap doc has no content at `1.0.2.x`, so `specset2sporglset` returns empty and the endset is never stored (`do2.c:122`) |

---

## Question 18 [gregory]

> In a multi-node topology, does ownership of a tumbler prefix on node `1.1` imply anything about that user's authority on node `1.2`, or is ownership strictly local to the node prefix — meaning the same human would have separate ownership roots on each node?

### Gregory's Answer

## KB Synthesis

The KB doesn't explicitly document multi-node ownership policy, but the structural mechanics make the answer clear: **ownership is strictly local to the node prefix**.

Here's the reasoning from the KB:

**Ownership is purely prefix-based.** [SS-TUMBLER-CONTAINMENT] defines the containment predicate as: truncate address A to the length of prefix B, compare for equality. `1.1.0.1.0.x` is under `1.1.0.1`. `1.2.0.1.0.x` is NOT under `1.1.0.1` — those address spaces are disjoint siblings under the docuverse root.

**The ownership check uses account prefix matching.** [SS-ADDRESS-SPACE] Finding 0068 shows that the ownership test is `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)`. `tumbleraccounteq` compares the account-level components of two tumbler addresses. A user with session account `1.1.0.1` fails this test against any address rooted at `1.2.x`.

**Address allocation is namespace-bounded.** [SS-ADDRESS-ALLOC] Finding 0021 documents that `findisatoinsertnonmolecule` computes `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent — and searches only within that range. Document creation under account `1.1.0.1` is bounded to `[1.1.0.1, 1.1.0.2)`. Nothing in `1.2` is reachable.

**Version creation reinforces this.** [SS-VERSION-ADDRESS] Finding 0068: when a user versions a document they don't own, the version is allocated under `children(user.account)`, not under the document. This confirms the session account establishes the user's home namespace, and that namespace is their specific account address, not a broader node-level authority.

**Conclusion:** The same human would need independent account addresses on each node — `1.1.0.k` for node `1.1`, `1.2.0.k` for node `1.2`. There is no cross-node authority inheritance in the implementation. Ownership is per-account-prefix, and node prefixes (`1.1` vs `1.2`) are sibling subtrees with no containment relationship.

The KB does not document any higher-level policy mechanism (e.g., a node operator granting cross-node authority), so that question is unanswerable from the KB alone.

---

## Code Exploration

I now have everything needed for a precise answer. Here it is.

---

## Answer: Ownership is Strictly Local — No Cross-Node Authority Propagation

The code contains zero mechanism for cross-node authority. Ownership of a tumbler prefix on node `1.1` implies nothing about authority on node `1.2`. Here is the full chain of evidence.

---

### 1. The Tumbler Structure: A Flat Mantissa With No Node Layer

`common.h:59-65` defines the tumbler:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT ;
    short exp;
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

A tumbler is a 16-digit rational number. Conventional xanadu address notation like `1.1.0.1.0.1` maps directly onto `mantissa[0]=1, mantissa[1]=1, mantissa[2]=0, mantissa[3]=1, ...`. The digits at positions 0–1 (the "node" prefix `1.1`) are just leading digits in the mantissa — no special field, no special treatment. There is no struct member for "node" separate from the rest. The representation is uniform.

---

### 2. User Identity: One Account Tumbler Per Player

`players.h:13-21`:

```c
typedef struct _player {
    char    *name;
    INT      userid;
    INT      wantsout;
    INT      socket;
    FILE    *inp;
    FILE    *outp;
    tumbler  account;    /* xanadu host and account tumbler */
} PLAYER;
```

Every connected user has exactly one `account` tumbler. There is no per-node account table, no list of accounts, and no node-keyed map. A user is their account.

---

### 3. The Ownership Test: Pure Prefix Match on the Mantissa

The sole ownership predicate is `tumbleraccounteq()` in `tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    if (aptr->sign != bptr->sign) return(FALSE);

    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) return(TRUE);   // account terminated; document is under it
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) return(FALSE);
        }
    }
    return (TRUE);
}
```

The function asks: does document tumbler `aptr` begin with account prefix `bptr`? It scans digit by digit, stopping when `bptr` reaches its double-zero terminator. It has no knowledge of "node boundaries." It does not treat position 0 or 1 as special. A user whose account is `1.1.0.1.0.0` owns anything whose mantissa starts with `1,1,0,1` before the terminating zeros — and that test is applied uniformly whether the leading digits are `1.1` or `1.2` or anything else.

---

### 4. `isthisusersdocument()` — Three Implementations, Same Logic

In `socketbe.c:197-201` (multi-user daemon):

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

In `be.c:171-176` (single-process backend) and `xumain.c:198-201` (xumain variant):

```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &taskptrx->account);
}
```

All three compare the document against the **current session's single account tumbler**. No node lookup, no multi-node check, no delegation table.

---

### 5. How `checkforopen()` Uses Ownership — The Permission Gate

`bert.c:52-87` is the only place access is gated before a write operation:

```c
int checkforopen(tumbler *tp, int type, int connection)
{
    // ...scan bert table for existing open by this connection...

    if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
        return 0;   // open allowed
    } else {
        return -1;  // must create a new version under your own account
    }
}
```

The permission logic is: you may write to a document if either (a) you are opening it for read, or (b) `isthisusersdocument()` returns true — i.e., your single account tumbler is a prefix of the document's address. There is no "same node" bonus, no "node admin" override, no cross-node delegation path.

---

### 6. What Happens When You Try to Write Another User's Document

`do1.c:268-276`:

```c
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);   // same document address
} else {
    /* This does the right thing for new version of someone else's document */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // new doc under your account
}
```

If you do not own the target document, the system creates a **new document under your account** (`wheretoputit` is `taskptr->account`). It never escalates to ask whether you might own a parent node. The account mismatch path leads directly to `ACCOUNT`-scoped creation — a copy under your own space.

---

### 7. Node Creation Is Address Allocation, Not Authority Delegation

`do1.c:243-258`:

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
    tumblercopy(isaptr, &isa);
    makehint (NODE, NODE, 0, &isa, &hint);
    result = createorglingranf (taskptr, granf, &hint, &isa);
    // ...
}
```

`CREATENODE_OR_ACCOUNT` is a granfilade address allocation call — it registers a new numeric prefix in the enfilade so subsequent inserts know where to place content. It does **not** grant the creating user authority over that prefix. Authority still derives from whether your `account` tumbler is a prefix of the target document — not from who created the node address.

`granf2.c:224-227` makes this concrete with a bug fix comment:

```
BUG FIX #2: Also check if lowerbound is actually under hintisa. If the
found item is from a different account (e.g., 1.1.0.1.0.1 when creating
under 1.1.0.2), treat it as if nothing was found. Otherwise documents
get created under the wrong account.
```

Accounts `1.1.0.1` and `1.1.0.2` — both living under the `1.1` node — are treated as entirely distinct namespaces. The code treats any "bleed" across them as a bug to be eliminated.

---

### 8. No Multi-Node Networking Layer

`rcfile.c:19-32` shows the only network configuration the backend reads:

```c
#define HOSTMETANAME  "host"
// ...
char hostname[256] = "localhost";
```

`bed.c` runs a single `select()` loop over local socket file descriptors. There is no code for routing requests to remote nodes, no code for querying another node's ownership table, and no internode trust model.

---

## Conclusion

**Ownership in udanax-green is strictly local to the account tumbler prefix, not the node prefix.**

The ownership check is a single-function call — `tumbleraccounteq(document, user_account)` — which tests whether the user's account tumbler is a numeric prefix of the document's address. The node digits (e.g., `1.1` vs `1.2`) are not distinguished from any other digits in this comparison. There is no concept of "node administrator," no cross-node authority, and no federation of identity between nodes.

The same human would need **separate account tumblers** on each node — e.g., `1.1.0.1.0.0` on node `1.1` and `1.2.0.1.0.0` on node `1.2` — and those accounts have completely independent authority scopes. Ownership of everything under `1.1.0.1` says nothing about `1.2` because the permission check at `bert.c:81` is a pure prefix match against a single `account` field in the current session, with no cross-node lookup path in the code at all.

---

## Question 19 [gregory]

> Does the `.0.` separator play any role in ownership computation, or is it purely a human-readable convention — specifically, does any code path use the position of zero digits to determine where one ownership level ends and another begins?

### Gregory's Answer

## KB Synthesis

The `.0.` separator is functional — it IS the hierarchy encoding — but no code path scans for zero positions to determine ownership. The mechanism is arithmetic, not pattern-matching.

**How containment actually works** [SS-TUMBLER-CONTAINMENT]:

```c
tumblertruncate(&A, tumblerlength(&B), &truncated);
tumblereq(&truncated, &B);  // TRUE if A is under B
```

`tumblerlength()` returns `nstories(t) - t.exp`, where `nstories` counts the last *non-zero* significant digit. This means trailing zeros don't count toward length — so `1.1.0.2` has length 4 (stops at the `2`), not 6. Containment is pure digit-count prefix matching: truncate the candidate to parent's length, compare.

**How zeros get there** [SS-ADDRESS-ALLOC, SS-ADDRESS-SPACE]:

`makehint` encodes a `depth` value (1 for same-type hierarchy, 2 for cross-type). `tumblerincrement(hintisa, depth-1, 1)` places the increment `1` at position `depth-1` digits from the right of the significant portion. When allocating a document (depth=2) under account `1.1.0.2`:
- Increment at position 1 from right → places a `1` two digits past the account, with a zero in between
- Produces `1.1.0.2.0.1` — the `.0.` is synthesized by the arithmetic, not written explicitly

**The key distinction**:

The zeros are structurally essential — the total order puts `1.1.0.2 < 1.1.0.2.0.1` because `nstories` of the shorter address is 4, and truncating the longer to length 4 yields exact equality. But the code never asks "where is the next zero?" It asks "what is the digit count?" The `.0.` boundaries emerge from how `tumblerincrement` with the right `rightshift` distributes digits across the mantissa.

**Confirming evidence** from [PRE-ADDRESS-ALLOC]: Bug 0013 was a containment failure — after `findpreviousisagr` found `1.1.0.1.0.1`, allocation incorrectly used it as a base for account `1.1.0.2`. The fix added a post-check: truncate the found address to parent length and verify equality. No zero-scanning — pure prefix length arithmetic.

**Summary**: The `.0.` separators are not a human-readable convention — they are the actual stored hierarchy encoding. But they are produced and checked via length arithmetic (`tumblerlength`, `tumblerincrement` with `rightshift`, `tumblertruncate`), not by locating zero-digit positions in the mantissa.

---

## Code Exploration

Now I have all the facts needed from the actual source. Let me write the definitive answer.

---

## Does `.0.` Play a Functional Role in Ownership Computation?

**Yes — the `.0.` separator is mechanically significant in `tumbleraccounteq`, and its zero positions directly determine ownership boundaries. It is not purely decorative.**

---

### The Core: `tumbleraccounteq` — `tumble.c:38–70`

This is the single function that implements "is document `a` under account `b`?" It does not compare tumblers digit-by-digit. Instead, it counts zero-valued digits in the account tumbler:

```c
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        if (++j_b == 2) {
            return(TRUE);   // account boundary reached → document is under account
        }
        // first zero: skip mismatch check for this position
    } else {
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);  // non-zero digit must match exactly
        }
    }
}
```

The algorithm has two distinct behaviors triggered by zero digits:

1. **First zero** (`j_b == 1`): the match check is skipped. The document can have *any* value at this position.
2. **Second zero** (`j_b == 2`): the function returns `TRUE` immediately — the account's owned space has been fully traversed, and the document falls within it.

---

### How This Interacts with the `1.1.0.1` Account Structure

The default account is defined at `be.c:37`:

```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

Its mantissa array is `[1, 1, 0, 1, 0, 0, ...]`. Walking `tumbleraccounteq` with this account:

| Index | `bptr->mantissa[i]` | Action | `j_b` |
|-------|---------------------|--------|--------|
| 0 | 1 | non-zero → require match on `aptr[0]` | 0 |
| 1 | 1 | non-zero → require match on `aptr[1]` | 0 |
| 2 | **0** | **first zero → skip match check (wildcard)** | **1** |
| 3 | 1 | non-zero → require match on `aptr[3]` | 1 |
| 4 | **0** | **second zero → return TRUE** | **2** |

The structural `.0.` at mantissa index 2 is zero #1. The first trailing zero at index 4 is zero #2 — the terminator. Without the structural `.0.`, an account like `1.1.1` would require *two* consecutive trailing zeros before returning TRUE, placing the ownership boundary two positions further along and changing which document addresses match.

The `.0.` separator also has a wildcard effect: when the account has `0` at index 2, the document's value at index 2 is *not checked*. This is what allows a document `1.1.X.1.0.1` to technically match account `1.1.0.1` for any `X`. In standard usage all documents have `0` at that structural position, so this wildcard is invisible — but the mechanism is real.

---

### The Call Chain: Ownership All the Way Up

**`isthisusersdocument`** — `be.c:171–175` / `socketbe.c:197–201`:

```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

All ownership queries reduce to `tumbleraccounteq`.

**`checkforopen`** — `bert.c:81`:

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;  // open permitted without an explicit bert entry
} else {
    return -1;
}
```

Whether a connection may open a document without holding a bert lock depends entirely on whether `tumbleraccounteq` returns true for that document against the user's account tumbler. The zero positions in the account tumbler gate every access check.

**`do1.c:270`** uses the function directly for version creation routing:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

If the document address is under the user's account (per zero-counting), the hint is anchored to the document itself; otherwise to the account. The `.0.` structure is what distinguishes these two cases.

---

### `.0.` Is Also Generated as a Structural Boundary

`findisatoinsertnonmolecule` — `granf2.c:203–241` — explicitly inserts `.0.` separators when creating the first document under an account. With `depth = 2` (when `supertype != subtype`, i.e., crossing a hierarchy level), `tumblerincrement` shifts the new address two "stories" to the right of the hint:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// ...
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
}
```

The comment at `granf2.c:151` spells this out literally:

```
the account address itself (1.1.0.1 instead of 1.1.0.1.0.1).
```

The `.0.` between `1.1.0.1` (account) and the trailing `1` (first document) is deliberately placed by `tumblerincrement` with `rightshift=2`. The zero digit at the boundary position is not an accident of padding — it is inserted as the separator between hierarchy levels.

---

### The `istextcrum`/`islinkcrum` Distinction — `orglinks.c:246–261`

Zero positions also gate content-type classification:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if (crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr)
{
    if (crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

`mantissa[1] == 0` identifies text content (a "1.0" address family); `mantissa[1] != 0` identifies link content (a "1.n" address family). These checks are what the comment in `islinkcrum` describes as "1.n tumbler where n != 0." Zero at mantissa index 1 is the dividing line between text ownership space and link space — a direct structural role.

---

### Summary

| Function | File:Line | How zero digits are used |
|----------|-----------|--------------------------|
| `tumbleraccounteq` | `tumble.c:38–70` | Counts zeros in account tumbler; first zero = wildcard; second zero = ownership boundary reached |
| `isthisusersdocument` | `be.c:171–175` | Delegates to `tumbleraccounteq` |
| `checkforopen` | `bert.c:81` | Gates document access on `isthisusersdocument` |
| `do1.c:270` | `do1.c:270` | Routes version creation based on `tumbleraccounteq` result |
| `findisatoinsertnonmolecule` | `granf2.c:235–237` | Inserts `.0.` separator when crossing hierarchy levels with `depth=2` |
| `istextcrum` / `islinkcrum` | `orglinks.c:246–261` | `mantissa[1] == 0` determines text vs. link ownership subspace |

**The `.0.` separator is not purely human-readable convention.** In `tumbleraccounteq`, the zero digit at the structural separator position advances the zero counter, which governs when ownership is declared. The trailing zero of the account's mantissa array fires the boundary return only because the structural `.0.` has already advanced `j_b` to 1. Zero positions also gate text-vs-link classification (`orglinks.c`) and hierarchy-level transitions during address generation (`granf2.c`). All three are real code paths, not cosmetic notation.
