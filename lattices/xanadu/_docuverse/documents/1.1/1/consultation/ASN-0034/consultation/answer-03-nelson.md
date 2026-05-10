## Question 3 [nelson]

> What distinct levels does an address contain, and what does each level uniquely identify — a user, a document, a position within content?

# Tumbler Address Levels

A Xanadu tumbler address contains **four major fields**, separated by three zero-digit dividers:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

---

## Level 1: Node (Server)

Identifies the **physical server or station** in the network. Always begins with digit `1`, since all servers descend from the root.

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

Servers can fork sub-servers: `1.2` is a descendant of `1`. This forms the network topology.

## Level 2: User (Account)

Identifies the **owner/account** on that server. The user field is continually subdividable for sub-accounts.

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

Ownership flows from this field — the User portion of an I-address permanently records who created the content.

## Level 3: Document (including Versions)

Identifies the **logical document**. This field can be further subdivided to indicate versions and sub-documents:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

So `1.0.3.0.7` is document 7 under account 3 on server 1. If that document has version 2, it becomes `1.0.3.0.7.2` — the version extends the document field, not a separate major field.

## Level 4: Element (Contents)

Identifies **individual bytes or links** within a document version. This field has two subspaces:

**Bytes** (content positions):
> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

**Links** (stored connections):
> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

The `0.1` prefix designates bytes; `0.2` designates links. Links are numbered sequentially by creation order and are not rearrangeable.

---

## The Hierarchy as Ownership Delegation

Each level delegates to the next through "baptism" — the owner of a number can create sub-numbers beneath it:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "So the docuverse is all really one big forking document." [LM 4/18]

---

## Summary Table

| Level | Field | Identifies | Example | Who assigns it |
|-------|-------|-----------|---------|----------------|
| 1 | Node | Server/station | `1.2` | Parent server |
| 2 | User | Owner/account | `1.2.0.5` | Server operator |
| 3 | Document | Document + version | `1.2.0.5.0.3.1` | Account owner |
| 4 | Element | Byte or link position | `1.2.0.5.0.3.1.0.1.47` (byte 47) | System (append-only) |

The three zeros act as punctuation separating the four semantic tiers. Each field is independently extensible without limit, and the entire scheme imposes no structure on content — it is purely a mapping mechanism:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17–4/18]
