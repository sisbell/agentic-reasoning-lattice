## Question 10 [nelson]

> If a link connects passages owned by two different users and one user's document undergoes extensive revision, what guarantee does the other user have that their end of the link remains intact and reachable?

# Link Integrity Across Ownership Boundaries Under Revision

The other user has a **layered set of guarantees** — architectural, structural, and contractual — that their end of the link remains intact and reachable even under extensive revision of the connected document.

## 1. Links Attach to Bytes, Not Positions

The foundational guarantee is architectural. Xanadu links are not pointers to positions in a document; they are "straps between bytes" identified by their permanent Istream addresses:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Editing operations — insertions, deletions, rearrangements — change the **Vstream** (the document's current arrangement). They do not alter the **Istream** (the permanent content store). Since links point to I-addresses, not V-addresses, editing literally cannot touch what links point to.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-addresses shift around. The I-addresses — and therefore the link endpoints — are immovable.

## 2. "Deletion" Does Not Destroy Content

Even if the revising user deletes the passage that one end of the link connects to, the bytes are not destroyed. DELETE in Xanadu removes content from the Vstream (current view) only:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes still exist in Istream. The link still resolves to them. The content is recoverable through historical backtrack or through previous versions that still contain it.

## 3. The Survivability Condition

The explicit survivability guarantee from Nelson:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

This is the critical condition. A link breaks only when **all** bytes at one endset have been removed from every version and every transclusion. Given Istream's append-only nature, this effectively cannot happen — the bytes are permanent.

Nelson extends this to alternative versions:

> "This also works for alternative versions in which part of each end has survived." [LM 4/42]

## 4. Published Documents Cannot Be Withdrawn

The contractual layer reinforces the structural guarantee. Once published, a document stays published precisely **because** others have linked to it:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The revising user may publish a new version, but the old version must remain:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

## 5. Links Reach Through to New Versions

If the revising user publishes a superseding version, the other user's link doesn't just cling to the old version — it can follow correspondence into the new one:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Because versions share Istream content, the system can compute which parts of the new version correspond to the linked passage in the old. The reader following the link can be directed to the same content in the current version, if it still exists there.

## 6. Link Ownership Is Independent

The other user's link is **their property**, stored at their address. The revising user has no power over it:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

The revising user owns their document; the linking user owns their link. Neither can touch the other's property.

## Summary of Guarantees

| Threat | Protection |
|--------|------------|
| Content rearranged | Links point to I-addresses, unaffected by V-address changes |
| Content "deleted" | Bytes remain in Istream; link still resolves |
| Document revised with new version | Old version stays on network; link reaches through to new version |
| Document withdrawn | Not permitted for published documents (contractual) |
| Other user tries to remove the link | Cannot — link is owned by its creator, not the target's owner |

The guarantee is comprehensive: as long as the Xanadu system operates according to its design, the other user's link endpoint remains intact and reachable. The system was designed so that the web of interconnections — the structure of literature — cannot be destroyed by any individual participant's editing activity.
