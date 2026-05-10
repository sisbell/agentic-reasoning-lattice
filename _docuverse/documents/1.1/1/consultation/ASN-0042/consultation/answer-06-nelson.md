## Question 6 [nelson]

> Can an owner delegate partial authority over a subregion to another user while retaining ownership of the larger region?

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
