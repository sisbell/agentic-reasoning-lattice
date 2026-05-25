## Question 10 [theory]

> What must the system guarantee about the permanence of the lineage record itself — can the connection between original and edited link ever be severed or revised?

# The Permanence of Lineage in Xanadu

The system guarantees that **the historical record itself cannot be expunged**, but I must distinguish two kinds of lineage to answer precisely.

## Document Version Ancestry: Structurally Permanent

When a new version is created from an existing document, the ancestry is encoded **in the address itself**. From the CREATENEWVERSION operation:

> "The new document's id will indicate its ancestry." (4/66)

And further:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (4/29)

Because tumbler addresses are permanent — "any address, once assigned, remains valid forever" (4/19) — the lineage encoded in those addresses is permanent too. This kind of lineage cannot be severed or revised. The ancestor address IS embedded in the descendant's address.

## Link-Asserted Lineage: Suppressible but Never Expunged

If by "edited link" you mean a successor link related to an original via a user-created metalink (such as a supersession link or counterpart link), then the lineage record itself is a link — owned by whoever made it. That owner has administrative rights:

> "Only the owner has a right to withdraw a document or change it." (2/29)

But — and this is the crucial guarantee — deletion in Xanadu is **non-destructive**. Even deleted links remain in the historical record:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

This is the same regime as deleted bytes: removed from the current Vstream view, but permanent in Istream, recoverable through historical backtrack, and potentially still alive in other documents that referenced or versioned them.

## The Core Invariant

The principle underlying both cases is append-only storage:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes [flow] into the storage system, filed, as it were, chronologically." (2/14)

And the explicit non-destruction guarantee:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals." (2/45)

## What an Owner CAN Do

- Delete their own link (making it "not currently addressable")
- Create a new link that contradicts or supplants an earlier lineage assertion
- Publish a superseding document via a supersession link

## What an Owner CANNOT Do

- Erase the deleted link from Istream
- Prevent historical backtrack from reconstructing the prior state
- Affect lineage assertions made by *other* owners about the same content (anyone can make a supersession or counterpart link — see [supersession-authority.md])
- Sever the address-encoded ancestry of a versioned document

## The Boundary

The lineage record is as permanent as any other content in the docuverse. It can be **administratively suppressed** (removed from current visibility) by the owner of the link expressing it, but it cannot be **destroyed** — it persists in the historical record and may persist in transclusions or version snapshots taken before the deletion. As I put it about deleted bytes: they remain "in all other documents where they have been included" (4/11).

So: the connection can be revised (by adding new contradicting links) and suppressed (by deletion), but never severed from the permanent record.

NEED_RAW: I have not explicitly verified whether Literary Machines specifies a structural version-ancestry mechanism for individual links analogous to document versioning. The curated sources establish that links have permanent creation-order addresses (4/31) but do not describe a "link version" forking mechanism. If such a mechanism is specified anywhere it would likely be in 4/30-4/40 or 4/41-4/60, which would warrant raw verification for a complete answer.
