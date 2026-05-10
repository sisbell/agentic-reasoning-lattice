## Question 1 [nelson]

> When a new document is created, what properties must the system assign to it at the moment of creation that can never change afterward?

# Properties Assigned at Document Creation That Can Never Change

When the system executes CREATENEWDOCUMENT, it assigns properties that become permanent the instant the document ID is returned. These fall into four categories.

## 1. The Tumbler Address (Document ID)

This is the most fundamental immutable property. The system assigns a tumbler address encoding the document's permanent position in the docuverse tree.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The address has the form `Node.0.User.0.Document.0.Element` [LM 4/26], and the first three fields are fixed at creation. No subsequent operation can change them.

## 2. Ownership

Ownership is not metadata attached to the document — it IS the User field of the tumbler address. Since the address never changes, ownership never changes.

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)." [LM 2/29]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The owner is whoever controls the account under which the document is baptized. This is structural, not a property that can be transferred through some "change owner" operation — no such operation exists in FEBE.

## 3. The I-Space Namespace

All native content created in the document will have I-space addresses that fall under this document's tumbler prefix. The document field determines the permanent home location of every byte the owner will ever store there.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This means the document's identity as an origin point — the fact that I-address `N.0.U.0.D.0.X` traces back to document `N.0.U.0.D` — is permanent and structural. It is how origin traceability works:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

## 4. Ancestry (for Versions)

When a document is created via CREATENEWVERSION rather than CREATENEWDOCUMENT, the ancestry is encoded in the document ID itself:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

The parent-child relationship in the forking tree is permanent. Once `2.4.1` is baptized under `2.4`, that lineage cannot be altered.

## 5. Position in the Forking Tree

More broadly, the document's position in the universal tree of nodes, accounts, and documents is permanent:

> "So the docuverse is all really one big forking document." [LM 4/18]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Once a number is forked, no reorganization ever happens. The document at address `1.3.27.4` is forever the fourth document (or version) under document 27 of account 3 on node 1.

## What Is NOT Immutable

For contrast, the following are mutable:

- **V-space arrangement** — changes with every INSERT, DELETE, REARRANGE
- **Content** — can be added (INSERT, APPEND) or removed from view (DELETEVSPAN)
- **Links** — can be created (MAKELINK) or deleted by owner
- **Publication status** — can transition from private to published (though published cannot easily revert: "its author may not withdraw it except by lengthy due process" [LM 2/43])

## A Note on Time

Time of creation is tracked but is explicitly NOT part of the tumbler:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

Whether the creation timestamp is immutable is not explicitly stated in the sources. It is reasonable to assume it is (what would it mean to change a creation time?), but Nelson does not specify this directly. NEED_RAW: [4/65, 5/6-5/8] for any additional detail on document creation mechanics and system-maintained metadata.

## Summary

At the moment of creation, the system permanently assigns:

| Property | Where Encoded | Why Immutable |
|----------|---------------|---------------|
| Tumbler address | The ID itself | Addresses are permanent by design |
| Ownership | User field of tumbler | No transfer operation exists |
| I-space namespace | Document field of tumbler | All native bytes will live here |
| Ancestry | Document field subdivisions | Forking tree is append-only |
| Tree position | All fields of tumbler | "No reorganization ever happens" |

These are not five independent properties but five facets of one fact: **the tumbler address, once baptized, is eternal**. Everything that the address encodes — owner, origin, lineage, position — is therefore eternal with it.
